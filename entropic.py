#!/usr/bin/env python3
"""entropic — password entropy analyzer."""

import argparse
import getpass
import math
import string
import sys

CHARSETS = [
    ("lowercase", set(string.ascii_lowercase), 26),
    ("uppercase", set(string.ascii_uppercase), 26),
    ("digits", set(string.digits), 10),
    ("symbols", set(string.punctuation), len(string.punctuation)),
]

GUESSES_PER_SECOND = 1e10

RATINGS = [
    (28, "very weak", "\033[91m"),
    (36, "weak", "\033[93m"),
    (60, "fair", "\033[93m"),
    (80, "strong", "\033[92m"),
    (float("inf"), "very strong", "\033[92m"),
]
RESET = "\033[0m"


def pool_size(password: str) -> tuple[int, list[str]]:
    chars = set(password)
    size = 0
    used = []
    for name, charset, count in CHARSETS:
        if chars & charset:
            size += count
            used.append(name)
    other = chars - set().union(*(c for _, c, _ in CHARSETS))
    if other:
        size += len(other)
        used.append(f"other ({len(other)})")
    return size, used


def shannon_entropy(password: str) -> float:
    if not password:
        return 0.0
    freq = {c: password.count(c) / len(password) for c in set(password)}
    return -sum(p * math.log2(p) for p in freq.values())


def brute_force_bits(password: str) -> float:
    size, _ = pool_size(password)
    if size == 0:
        return 0.0
    return len(password) * math.log2(size)


def humanize_seconds(seconds: float) -> str:
    if seconds < 1:
        return "instant"
    units = [
        ("years", 365 * 24 * 3600),
        ("days", 24 * 3600),
        ("hours", 3600),
        ("minutes", 60),
        ("seconds", 1),
    ]
    for name, size in units:
        if seconds >= size:
            value = seconds / size
            if value >= 1e9:
                return f"{value:.2e} {name}"
            return f"{value:,.1f} {name}"
    return f"{seconds:.2f} seconds"


def rate(bits: float) -> tuple[str, str]:
    for threshold, label, color in RATINGS:
        if bits < threshold:
            return label, color
    return RATINGS[-1][1], RATINGS[-1][2]


def analyze(password: str, use_color: bool = True) -> str:
    if not password:
        return "empty password"

    size, used = pool_size(password)
    bits = brute_force_bits(password)
    shannon = shannon_entropy(password) * len(password)
    crack_seconds = (2 ** bits) / GUESSES_PER_SECOND / 2
    label, color = rate(bits)

    if not use_color:
        color = ""
        reset = ""
    else:
        reset = RESET

    lines = [
        f"length:         {len(password)} chars",
        f"character pool: {size} ({', '.join(used) or 'none'})",
        f"brute-force:    {bits:.1f} bits",
        f"shannon:        {shannon:.1f} bits (given this string)",
        f"crack time:     {humanize_seconds(crack_seconds)} at 10B guesses/sec",
        f"rating:         {color}{label}{reset}",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Analyze password entropy and estimate crack time.",
    )
    parser.add_argument("password", nargs="?", help="password to analyze (omit for prompt)")
    parser.add_argument("--no-color", action="store_true", help="disable ANSI color")
    parser.add_argument("--stdin", action="store_true", help="read password from stdin")
    args = parser.parse_args()

    if args.stdin:
        password = sys.stdin.readline().rstrip("\n")
    elif args.password is not None:
        password = args.password
    else:
        password = getpass.getpass("password: ")

    use_color = not args.no_color and sys.stdout.isatty()
    print(analyze(password, use_color=use_color))
    return 0


if __name__ == "__main__":
    sys.exit(main())

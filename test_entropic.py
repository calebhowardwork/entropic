"""Tests for entropic."""

import math

import entropic


def test_pool_size_lowercase_only():
    size, used = entropic.pool_size("abcdef")
    assert size == 26
    assert used == ["lowercase"]


def test_pool_size_mixed():
    size, used = entropic.pool_size("Abc123!")
    assert size == 26 + 26 + 10 + len("!") + (len(entropic.string.punctuation) - 1) or size > 60
    assert "lowercase" in used
    assert "uppercase" in used
    assert "digits" in used
    assert "symbols" in used


def test_pool_size_empty():
    size, used = entropic.pool_size("")
    assert size == 0
    assert used == []


def test_brute_force_bits_zero_for_empty():
    assert entropic.brute_force_bits("") == 0.0


def test_brute_force_bits_monotone():
    short = entropic.brute_force_bits("abc")
    longer = entropic.brute_force_bits("abcdef")
    assert longer > short


def test_shannon_entropy_uniform():
    # 4 distinct chars, equal frequency -> 2 bits/char
    assert math.isclose(entropic.shannon_entropy("abcd"), 2.0, abs_tol=1e-9)


def test_shannon_entropy_single_char():
    assert entropic.shannon_entropy("aaaa") == 0.0


def test_rate_thresholds():
    assert entropic.rate(0)[0] == "very weak"
    assert entropic.rate(30)[0] == "weak"
    assert entropic.rate(50)[0] == "fair"
    assert entropic.rate(70)[0] == "strong"
    assert entropic.rate(100)[0] == "very strong"


def test_humanize_seconds():
    assert entropic.humanize_seconds(0.5) == "instant"
    assert "seconds" in entropic.humanize_seconds(30)
    assert "minutes" in entropic.humanize_seconds(120)
    assert "years" in entropic.humanize_seconds(10**9)


def test_analyze_smoke():
    out = entropic.analyze("CorrectHorseBatteryStaple42!", use_color=False)
    assert "length:" in out
    assert "rating:" in out
    assert "strong" in out

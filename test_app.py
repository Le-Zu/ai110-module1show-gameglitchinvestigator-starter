import pytest
from unittest.mock import MagicMock
import sys

# Mock streamlit before importing app so the st.* calls at module level don't crash
sys.modules["streamlit"] = MagicMock()

from app import parse_guess, check_guess, update_score, get_range_for_difficulty


# --- get_range_for_difficulty ---

def test_range_easy():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_range_normal():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_range_hard():
    assert get_range_for_difficulty("Hard") == (1, 50)

def test_range_unknown_defaults_to_normal():
    assert get_range_for_difficulty("Unknown") == (1, 100)


# --- parse_guess ---

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42
    assert err is None

def test_parse_guess_valid_float_truncates():
    ok, value, err = parse_guess("7.9")
    assert ok == True
    assert value == 7

def test_parse_guess_none():
    ok, value, err = parse_guess(None)
    assert ok == False
    assert value is None
    assert err == "Enter a guess."

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("")
    assert ok == False
    assert err == "Enter a guess."

def test_parse_guess_letters():
    ok, value, err = parse_guess("abc")
    assert ok == False
    assert err == "That is not a number."

def test_parse_guess_negative():
    ok, value, err = parse_guess("-5")
    assert ok == True
    assert value == -5


# --- check_guess ---

def test_check_guess_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_too_high():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"

def test_check_guess_too_low():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"


# --- update_score ---

def test_update_score_win_early():
    # attempt 1: 100 - 10*(1+1) = 80
    score = update_score(0, "Win", 1)
    assert score == 80

def test_update_score_win_minimum_points():
    # attempt 10: 100 - 10*(10+1) = -10, clamped to 10
    score = update_score(0, "Win", 10)
    assert score == 10

def test_update_score_too_high_deducts():
    score = update_score(100, "Too High", 1)
    assert score == 95

def test_update_score_too_low_deducts():
    score = update_score(100, "Too Low", 1)
    assert score == 95

def test_update_score_unknown_outcome_unchanged():
    score = update_score(100, "SomeOtherOutcome", 1)
    assert score == 100

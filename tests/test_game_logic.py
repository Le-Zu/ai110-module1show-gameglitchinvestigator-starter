from logic_utils import get_range_for_difficulty, parse_guess, check_guess, update_score


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
# Bug fixed: check_guess returns a tuple (outcome, message), not a bare string.
# The original tests/test_game_logic.py compared result == "Win" directly against
# the tuple, so they always failed silently.

def test_check_guess_correct():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_check_guess_too_high():
    # Bug fixed: guess > secret must return "Too High" (FIXME comment in source
    # incorrectly suggested the operator was wrong; the operator was correct).
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"

def test_check_guess_too_low():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"

def test_check_guess_returns_tuple():
    # Regression: check_guess must return (outcome, message), not a bare string.
    result = check_guess(50, 50)
    assert isinstance(result, tuple) and len(result) == 2


# --- update_score ---
# Bug fixed: formula was 100 - 10 * (attempt_number + 1), which under-rewarded
# every win by 20 points. Correct formula is 100 - 10 * (attempt_number - 1),
# where attempt_number is 1-indexed (1 = first guess).

def test_update_score_win_attempt_1():
    # First guess correct: 100 - 10*(1-1) = 100
    score = update_score(0, "Win", 1)
    assert score == 100

def test_update_score_win_attempt_2():
    # Second guess correct: 100 - 10*(2-1) = 90
    score = update_score(0, "Win", 2)
    assert score == 90

def test_update_score_win_attempt_8():
    # Eighth guess correct: 100 - 10*(8-1) = 30
    score = update_score(0, "Win", 8)
    assert score == 30

def test_update_score_win_minimum_clamped():
    # Late win: 100 - 10*(11-1) = 0, clamped to minimum 10
    score = update_score(0, "Win", 11)
    assert score == 10

def test_update_score_accumulates_on_win():
    # Score is added to existing current_score, not replaced.
    score = update_score(50, "Win", 1)
    assert score == 150

def test_update_score_too_high_no_deduction():
    # Bug fixed: wrong guesses previously deducted 5 points each.
    score = update_score(100, "Too High", 1)
    assert score == 100

def test_update_score_too_low_no_deduction():
    score = update_score(100, "Too Low", 1)
    assert score == 100

def test_update_score_unknown_outcome_unchanged():
    score = update_score(100, "SomeOtherOutcome", 1)
    assert score == 100

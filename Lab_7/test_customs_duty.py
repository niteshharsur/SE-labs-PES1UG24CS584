import math

import pytest
from hypothesis import given, settings, strategies as st

from customs_duty import duty_amount, hs_chapter, parse_declaration


unexpected_inputs = st.one_of(
    st.text(), st.none(), st.integers(), st.floats(), st.booleans(),
    st.binary(), st.lists(st.integers(), max_size=4),
    st.dictionaries(st.text(max_size=8), st.integers(), max_size=4),
)


@settings(max_examples=250, derandomize=True, report_multiple_bugs=False)
@given(unexpected_inputs)
def test_parse_declaration_no_crash(text):
    result = parse_declaration(text)
    if result is not None:
        category, value = result
        assert category and category == category.strip().lower()
        assert math.isfinite(value) and value >= 0


@settings(max_examples=250, derandomize=True, report_multiple_bugs=False)
@given(unexpected_inputs)
def test_duty_amount_no_crash(text):
    result = duty_amount(text)
    if result is not None:
        assert math.isfinite(result) and result >= 0


@settings(max_examples=250, derandomize=True, report_multiple_bugs=False)
@given(unexpected_inputs)
def test_hs_chapter_no_crash(code):
    result = hs_chapter(code)
    if result is not None:
        assert isinstance(result, int) and 1 <= result <= 99


@given(st.sampled_from(["Electronics", "Books", "Home Goods"]),
       st.integers(min_value=0, max_value=10**9))
def test_valid_declaration(category, value):
    assert parse_declaration(f" {category} : {value} ") == (category.lower(), value)


@given(st.integers(min_value=0, max_value=10**9),
       st.integers(min_value=0, max_value=1000))
def test_valid_duty(value, rate):
    assert duty_amount(f" {value} @ {rate} ") == pytest.approx(value * rate / 100)


@given(st.integers(min_value=1, max_value=99),
       st.integers(min_value=0, max_value=9999))
def test_valid_hs_chapter(chapter, suffix):
    suffix = f"{suffix:04d}"
    assert hs_chapter(f"{chapter:02d}{suffix[:2]}.{suffix[2:]}") == chapter
    assert hs_chapter(f"{chapter:02d}{suffix}") == chapter


@pytest.mark.parametrize(("function", "data"), [
    (parse_declaration, ":10"),
    (parse_declaration, "books:-1"),
    (parse_declaration, "books:nan"),
    (parse_declaration, "books:inf"),
    (parse_declaration, "books:1:2"),
    (duty_amount, "10@-5"),
    (duty_amount, "-10@5"),
    (duty_amount, "10@nan"),
    (duty_amount, "inf@10"),
    (duty_amount, "1e308@1e308"),
    (duty_amount, "1@@2"),
    (hs_chapter, "00"),
    (hs_chapter, "8"),
    (hs_chapter, "85xyz"),
    (hs_chapter, "8517."),
    (hs_chapter, "１２"),
])
def test_reject_invalid_input(function, data):
    assert function(data) is None


def test_duty_with_representable_result_after_intermediate_overflow():
    assert duty_amount("1e308@20") == pytest.approx(2e307)

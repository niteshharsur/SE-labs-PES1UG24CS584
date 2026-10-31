"""Lab 6 line coverage tests. Nitesh Harsur | PES1UG24CS584."""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


@pytest.mark.parametrize("category,origin,expected", [
    ("electronics", "FTA", 0.10), ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05), ("clothing", "US", 0.12),
    ("books", "US", 0), ("toys", "US", 0.15),
])
def test_duty_rates(category, origin, expected):
    assert duty_rate(category, origin) == pytest.approx(expected)


def test_prohibited_rate():
    with pytest.raises(ValueError, match="^prohibited item$"):
        duty_rate("weapons", "US")


def test_negative_value():
    with pytest.raises(ValueError, match="^negative value$"):
        total_duty("electronics", -1, "US", False)


@pytest.mark.parametrize("category,value,origin,gift,expected", [
    ("electronics", 5000, "US", True, 0),
    ("electronics", 6000, "US", True, 200),
    ("electronics", 1000, "US", False, 0),
    ("electronics", 2000, "US", False, 400),
    ("clothing", 5100, "FTA", True, 50),
    ("books", 6000, "US", False, 0),
])
def test_total_duty(category, value, origin, gift, expected):
    assert total_duty(category, value, origin, gift) == pytest.approx(expected)


@pytest.mark.parametrize("value,category,documents,expected", [
    (500, "weapons", True, "refuse"),
    (100001, "electronics", True, "inspect"),
    (20001, "electronics", False, "inspect"),
    (20001, "electronics", True, "green"),
    (1000, "books", False, "green"),
])
def test_clearance(value, category, documents, expected):
    assert clearance_channel(value, category, documents) == expected

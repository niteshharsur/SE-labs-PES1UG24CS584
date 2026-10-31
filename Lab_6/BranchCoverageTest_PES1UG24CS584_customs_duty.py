"""Lab 6 branch and boundary tests. Nitesh Harsur | PES1UG24CS584."""
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


@pytest.mark.parametrize("category,origin,expected", [
    ("electronics", "FTA", 0.10), ("electronics", "US", 0.20),
    ("clothing", "FTA", 0.05), ("clothing", "US", 0.12),
    ("books", "FTA", 0), ("books", "US", 0),
    ("toys", "FTA", 0.15), ("toys", "US", 0.15),
])
def test_rate_decisions(category, origin, expected):
    assert duty_rate(category, origin) == pytest.approx(expected)


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
def test_prohibited_rate(category):
    with pytest.raises(ValueError, match="^prohibited item$"):
        duty_rate(category, "FTA")


@pytest.mark.parametrize("gift", [True, False])
def test_negative_value_rejected_before_exemptions(gift):
    with pytest.raises(ValueError, match="^negative value$"):
        total_duty("electronics", -1, "US", gift)


@pytest.mark.parametrize("category,value,origin,gift,expected", [
    ("electronics", 0, "US", False, 0),
    ("electronics", 999, "US", False, 0),
    ("electronics", 1000, "US", False, 0),
    ("electronics", 1001, "US", False, 200.2),
    ("electronics", 0, "US", True, 0),
    ("electronics", 4999, "US", True, 0),
    ("electronics", 5000, "US", True, 0),
    ("electronics", 5001, "US", True, 50),
    ("electronics", 5249, "US", True, 50),
    ("electronics", 5250, "US", True, 50),
    ("electronics", 5251, "US", True, 50.2),
    ("electronics", 6000, "FTA", True, 100),
    ("clothing", 6000, "FTA", True, 50),
    ("clothing", 6000, "US", True, 120),
    ("books", 5001, "US", True, 0),
    ("books", 1001, "US", False, 0),
    ("toys", 2000, "US", False, 300),
])
def test_total_duty_boundaries(category, value, origin, gift, expected):
    assert total_duty(category, value, origin, gift) == pytest.approx(expected)


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
@pytest.mark.parametrize("value,gift", [(1001, False), (5001, True)])
def test_taxable_prohibited_item_raises(category, value, gift):
    with pytest.raises(ValueError, match="^prohibited item$"):
        total_duty(category, value, "US", gift)


@pytest.mark.parametrize("category", ["weapons", "narcotics"])
@pytest.mark.parametrize("documents", [False, True])
def test_prohibited_clearance_takes_priority(category, documents):
    assert clearance_channel(100001, category, documents) == "refuse"


@pytest.mark.parametrize("value,documents,expected", [
    (0, False, "green"),
    (19999, False, "green"),
    (20000, False, "green"),
    (20000, True, "green"),
    (20001, False, "inspect"),
    (20001, True, "green"),
    (99999, False, "inspect"),
    (99999, True, "green"),
    (100000, False, "inspect"),
    (100000, True, "green"),
    (100001, False, "inspect"),
    (100001, True, "inspect"),
])
def test_clearance_thresholds(value, documents, expected):
    assert clearance_channel(value, "electronics", documents) == expected

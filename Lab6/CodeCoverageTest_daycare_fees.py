import pytest
from daycare_fees import extra_hours_fee, enrolment_allowed, pickup_status


# ---------- extra_hours_fee ----------
def test_within_included_hours():
    assert extra_hours_fee("toddler", 20, False) == 0

def test_unknown_age_group():
    with pytest.raises(ValueError, match="unknown age group"):
        extra_hours_fee("teen", 10, False)

def test_negative_hours():
    with pytest.raises(ValueError, match="invalid hours"):
        extra_hours_fee("infant", -1, False)

def test_infant_extra_standard_rate():
    # included 20, extra 10, rate 14
    assert extra_hours_fee("infant", 30, False) == 140

def test_infant_extra_high_rate():
    # included 20, extra 30 (>20), rate 14+5+3 = 22
    assert extra_hours_fee("infant", 50, False) == 660

def test_toddler_with_sibling_standard_rate():
    # included 25+5=30, extra 10, rate 9
    assert extra_hours_fee("toddler", 40, True) == 90

def test_toddler_high_rate():
    # included 25, extra 35 (>20), rate 9+5 = 14
    assert extra_hours_fee("toddler", 60, False) == 490


# ---------- enrolment_allowed ----------
def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_immunisation_pending_old_enough():
    assert enrolment_allowed(12, 0, True) is True

def test_enrolment_too_young():
    assert enrolment_allowed(5, 3, False) is False


# ---------- pickup_status ----------
def test_pickup_on_time():
    assert pickup_status(15, False, False) == "on_time"

def test_pickup_late():
    assert pickup_status(5, False, False) == "late"

def test_pickup_overdue():
    assert pickup_status(-10, True, True) == "overdue"

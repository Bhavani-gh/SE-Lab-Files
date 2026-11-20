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

def test_zero_hours_is_valid():
    # hours == 0 -> not negative, falls through, extra <= 0
    assert extra_hours_fee("preschool", 0, False) == 0

def test_exactly_included_hours_boundary():
    # extra == 0 -> still free
    assert extra_hours_fee("infant", 20, False) == 0

def test_infant_sibling_gets_no_bonus_hours():
    # has_sibling True but infant -> included stays 20, extra 5, rate 14
    assert extra_hours_fee("infant", 25, True) == 70

def test_toddler_sibling_bonus_applied():
    # included 30, 30 hours -> free
    assert extra_hours_fee("toddler", 30, True) == 0

def test_toddler_sibling_standard_rate():
    assert extra_hours_fee("toddler", 40, True) == 90

def test_preschool_no_sibling_standard_rate():
    # included 30, extra 5, rate 9
    assert extra_hours_fee("preschool", 35, False) == 45

def test_infant_extra_standard_rate():
    assert extra_hours_fee("infant", 30, False) == 140

def test_infant_extra_exactly_20_not_high_rate():
    # extra == 20 -> boundary of "extra > 20" is False
    assert extra_hours_fee("infant", 40, False) == 280

def test_infant_extra_high_rate():
    # extra 21 -> rate 14+5+3 = 22
    assert extra_hours_fee("infant", 41, False) == 462

def test_toddler_extra_exactly_20_not_high_rate():
    assert extra_hours_fee("toddler", 45, False) == 180

def test_toddler_high_rate():
    # extra 21 -> rate 9+5 = 14
    assert extra_hours_fee("toddler", 46, False) == 294


# ---------- enrolment_allowed ----------
def test_enrolment_allowed():
    assert enrolment_allowed(24, 2, False) is True

def test_enrolment_immunisation_pending_old_enough():
    assert enrolment_allowed(12, 0, True) is True

def test_enrolment_immunisation_pending_too_young():
    assert enrolment_allowed(11, 5, True) is False

def test_enrolment_too_young_no_pending():
    assert enrolment_allowed(5, 3, False) is False

def test_enrolment_age_boundary_six_months():
    assert enrolment_allowed(6, 1, False) is True

def test_enrolment_no_vacancies():
    assert enrolment_allowed(24, 0, False) is False


# ---------- pickup_status ----------
def test_pickup_on_time_regular():
    assert pickup_status(10, False, False) == "on_time"

def test_pickup_late_regular():
    assert pickup_status(9, False, False) == "late"

def test_pickup_late_lower_boundary_regular():
    assert pickup_status(-5, False, False) == "late"

def test_pickup_overdue_regular():
    assert pickup_status(-6, False, False) == "overdue"

def test_pickup_on_time_aftercare():
    assert pickup_status(20, True, False) == "on_time"

def test_pickup_late_aftercare():
    assert pickup_status(5, True, False) == "late"

def test_pickup_overdue_aftercare():
    assert pickup_status(4, True, False) == "overdue"

def test_pickup_friday_raises_cutoff():
    # regular cutoff 10 -> friday 20
    assert pickup_status(15, False, True) == "late"

def test_pickup_friday_aftercare_on_time():
    # cutoff 30
    assert pickup_status(30, True, True) == "on_time"

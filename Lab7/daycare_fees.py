from math import isfinite


def parse_enrolment(text):
    if not isinstance(text, str):
        return None

    try:
        age_group, hours_text = text.split(":")
        hours = float(hours_text)
    except ValueError:
        return None

    age_group = age_group.strip()
    if not age_group or not isfinite(hours) or hours < 0:
        return None

    return age_group.title(), hours


def hours_average(hours_csv):
    if not isinstance(hours_csv, str):
        return None

    try:
        values = [int(value) for value in hours_csv.split(",")]
    except ValueError:
        return None

    if any(value < 0 for value in values):
        return None

    return sum(values) // len(values)


def payable_fee(text):
    if not isinstance(text, str):
        return None

    try:
        fee_text, discount_text = text.split("|")
        fee = float(fee_text)
        discount = float(discount_text)
    except ValueError:
        return None

    if not isfinite(fee) or not isfinite(discount) or fee < 0 or discount < 0:
        return None

    total = fee * 1.18 - discount
    if not isfinite(total):
        return None

    return max(total, 0)


def main():
    print("==== Running parse_enrolment ====")
    result = parse_enrolment(input("Enter age group:hours (e.g. toddler:25): "))
    if result is None:
        print("Invalid enrolment. Enter an age group and nonnegative hours.")
    else:
        print("Age Group and Hours:", result)

    print("\n==== Running hours_average ====")
    result = hours_average(input("Enter weekly hours as CSV (e.g. 20,25,30): "))
    if result is None:
        print("Invalid weekly hours. Enter comma-separated nonnegative integers.")
    else:
        print("Average Hours:", result)

    print("\n==== Running payable_fee ====")
    result = payable_fee(input("Enter fee|discount (e.g. 3000|250): "))
    if result is None:
        print("Invalid fee or discount. Enter two nonnegative amounts.")
    else:
        print("Payable Fee:", result)


if __name__ == "__main__":
    main()
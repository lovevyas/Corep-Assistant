def validate(fields):
    errors = []
    values = {}

    # Collect numeric values safely
    for f in fields:
        if f["value"] != "MISSING":
            values[f["field_id"]] = float(f["value"])

    cet1 = values.get("010")
    at1 = values.get("020")
    tier2 = values.get("040")  # optional, only if present
    total = values.get("030")

    # Basic sanity check
    if cet1 is not None and cet1 < 0:
        errors.append("CET1 cannot be negative")
    if at1 is not None and at1 < 0:
        errors.append("AT1 capital cannot be negative")

    if tier2 is not None and tier2 < 0:
        errors.append("Tier 2 capital cannot be negative")


    # Validate Total Own Funds only if it exists
    if total is not None:
        expected = 0

        if cet1 is not None:
            expected += cet1
        if at1 is not None:
            expected += at1
        if tier2 is not None:
            expected += tier2

        if total != expected:
            errors.append("Total Own Funds mismatch")

    return errors

def build_audit_log(fields):
    return [
        {
            "field": f["field_id"],
            "justification": f["justification"]
        }
        for f in fields
    ]

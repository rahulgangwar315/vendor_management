# Copyright (c) 2026, rahul.gangwar@csm.tech
# For license information, please see license.txt

import frappe


def execute(filters=None):
    filters = filters or {}

    conditions = ""
    values = {}

    # Filter: Risk Level
    if filters.get("risk_level"):
        conditions += " AND risk_level = %(risk_level)s"
        values["risk_level"] = filters["risk_level"]

    # Filter: Status
    if filters.get("status"):
        conditions += " AND workflow_state = %(status)s"
        values["status"] = filters["status"]

    # Filter: From Date
    if filters.get("from_date"):
        conditions += " AND creation >= %(from_date)s"
        values["from_date"] = filters["from_date"]

    # Filter: To Date
    if filters.get("to_date"):
        conditions += " AND creation <= %(to_date)s"
        values["to_date"] = filters["to_date"]

    # Query
    data = frappe.db.sql(f"""
    SELECT
        name AS vendor,
        risk_level,
        workflow_state AS status,
        modified_by AS approved_by
    FROM `tabVendor`
    WHERE 1=1 {conditions}
    ORDER BY creation DESC
""", values, as_dict=True)

    # Columns
    columns = [
        {
            "label": "Vendor",
            "fieldname": "vendor",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": "Risk Level",
            "fieldname": "risk_level",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Status",
            "fieldname": "status",
            "fieldtype": "Data",
            "width": 120
        },
        {
            "label": "Approved By",
            "fieldname": "approved_by",
            "fieldtype": "Link",
            "options": "User",
            "width": 180
        }
    ]

    return columns, data
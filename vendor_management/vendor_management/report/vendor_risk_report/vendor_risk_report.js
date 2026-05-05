// Copyright (c) 2026, rahul.gangwar@csm.tech and contributors
// For license information, please see license.txt

frappe.query_reports["Vendor Risk Report"] = {
    filters: [

        {
            fieldname: "risk_level",
            label: "Risk Level",
            fieldtype: "Select",
            options: ["", "Low", "Medium", "High"]
        },

        {
            fieldname: "status",
            label: "Status",
            fieldtype: "Select",
            options: ["", "Draft", "Pending Approval", "Approved", "Rejected"]
        },

        {
            fieldname: "from_date",
            label: "From Date",
            fieldtype: "Date"
        },

        {
            fieldname: "to_date",
            label: "To Date",
            fieldtype: "Date"
        }

    ]
};
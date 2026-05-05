# Copyright (c) 2026, rahul.gangwar@csm.tech and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname
from frappe.utils import today, now


class Vendor(Document):

    def autoname(self):
        self.vendor_code = make_autoname("VN-.YYYY.-.####")
        self.name = self.vendor_code

    def validate(self):
        self.validate_primary_contact()
        self.prevent_duplicate_email()
        self.validate_risk_role()

    # Primary Contact Validation
    def validate_primary_contact(self):
        primary = [d for d in self.vendor_contacts if d.is_primary]

        if not primary:
            frappe.throw("At least one primary contact is required")

        if len(primary) > 1:
            frappe.throw("Only one primary contact is allowed")

    # Duplicate Email Check
    def prevent_duplicate_email(self):
        if self.email:
            existing = frappe.db.exists(
                "Vendor",
                {"email": self.email, "name": ["!=", self.name]}
            )
            if existing:
                frappe.throw("Vendor with this email already exists")

    # Only Compliance can set Risk Level
    def validate_risk_role(self):
        if self.risk_level and "Compliance Officer" not in frappe.get_roles():
            frappe.throw("Only Compliance Officer can set Risk Level")

    #  Only Finance can approve High Risk Vendors
    def before_submit(self):
        if self.risk_level == "High" and "Finance Approver" not in frappe.get_roles():
            frappe.throw("Only Finance can approve High-risk vendors")

    
    def on_update(self):

    # Auto-set onboarding date
        if self.status == "Approved" and not self.onboarding_date:
            self.onboarding_date = today()

        # Log rejection (fetch latest DB value)
        if self.status == "Rejected" or getattr(self, "workflow_state", None) == "Rejected":
            
            latest_reason = frappe.db.get_value(
                "Vendor", self.name, "rejection_reason"
            )

            frappe.get_doc({
                "doctype": "Vendor Rejection Log",
                "vendor": self.name,
                "reason": latest_reason or "No reason provided",
                "rejected_by": frappe.session.user,
                "rejected_on": now()
            }).insert(ignore_permissions=True)
// Copyright (c) 2026, rahul.gangwar@csm.tech and contributors
// For license information, please see license.txt



frappe.ui.form.on("Vendor", {

    email(frm) {
        if (frm.doc.email) {
            let domain = frm.doc.email.split("@")[1];

            if (domain && (domain.includes("gmail") || domain.includes("yahoo"))) {
                frm.set_df_property("risk_level", "reqd", 1);
            } else {
                frm.set_df_property("risk_level", "reqd", 0);
            }
        }
    },

    validate(frm) {
        let primary = (frm.doc.vendor_contacts || []).filter(d => d.is_primary);

        if (!primary.length) {
            frappe.throw("At least one primary contact is required");
        }
    }

});
import frappe
import requests


def push_vendor_if_approved(doc, method):
    # Trigger only when status changes to Approved
    if doc.status == "Approved" and doc.has_value_changed("status"):
        frappe.enqueue(
            "vendor_management.api.push_vendor_to_api",
            vendor=doc.name
        )


def push_vendor_to_api(vendor):
    doc = frappe.get_doc("Vendor", vendor)

    try:
        response = requests.post(
            "https://mock-api.com/vendor",
            json={
                "vendor_name": doc.vendor_name,
                "email": doc.email,
                "risk_level": doc.risk_level
            }
        )

        # Proper success/failure handling
        if response.status_code == 200:
            frappe.log_error(
                title="Vendor Sync Success",
                message=response.text
            )
        else:
            frappe.log_error(
                title="Vendor Sync Failed",
                message=response.text
            )
            raise Exception("API call failed with status code " + str(response.status_code))

    except Exception as e:
        frappe.log_error(
            title="Vendor Sync Failed",
            message=str(e)
        )
        raise
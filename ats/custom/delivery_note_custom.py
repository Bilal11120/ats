import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_sales_invoice(delivery_note):
    doc = get_mapped_doc(
        "Delivery Note",
        delivery_note,
        {
            "Delivery Note": {
                "doctype": "Sales Invoice",
                "field_map": {
                    "customer": "customer",
                    "name": "delivery_note"   # optional reference
                }
            },
            "Delivery Note Item": {
                "doctype": "Sales Invoice Item",
                "field_map": {
                    "item_code": "item_code",
                    "item_name": "item_name",
                    "qty": "qty",
                    "uom": "uom",
                    "rate": "rate",
                    "amount": "amount"
                }
            }
        }
    )

    return doc

import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def create_delivery_note(sales_order):
    doc = get_mapped_doc(
        "Sales Order",
        sales_order,
        {
            "Sales Order": {
                "doctype": "Delivery Note",
                "field_map": {
                    "customer": "customer",
                    "name": "against_sales_order"
                }
            },
            "Sales Order Item": {
                "doctype": "Delivery Note Item",
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

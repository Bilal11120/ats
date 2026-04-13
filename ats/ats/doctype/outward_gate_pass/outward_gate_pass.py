# Copyright (c) 2025, Ats and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class OutwardGatePass(Document):

    def validate(self):
        
        if self.sales_order:

            exists = frappe.db.exists(
                "Outward Gate Pass",
                {
                    "sales_order": self.sales_order,
                   
                    "name": ["!=", self.name]
                }
            )

            if exists:
                frappe.throw("❌ OGP already exists against this Sales Order")


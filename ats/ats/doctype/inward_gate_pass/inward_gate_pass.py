# Copyright (c) 2025, Ats and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class InwardGatePass(Document):

    def validate(self):

        if self.purchase_order:

            exists = frappe.db.exists(
                "Inward Gate Pass",
                {
                    "purchase_order": self.purchase_order,
                    "name": ["!=", self.name]
                }
            )

            if exists:
                frappe.throw("❌ OGP already exists against this Purchase Order")
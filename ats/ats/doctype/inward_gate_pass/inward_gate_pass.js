// Copyright (c) 2025, Ats and contributors
// For license information, please see license.txt
frappe.ui.form.on('Inward Gate Pass', {
    purchase_order: function(frm) {
        if (frm.doc.purchase_order) {

            frm.clear_table('items');

            frappe.call({
                method: 'frappe.client.get',
                args: {
                    doctype: 'Purchase Order',
                    name: frm.doc.purchase_order
                },
                callback: function(r) {
                    if (r.message) {
                        let po = r.message;

                        (po.items || []).forEach(function(d) {
                            let row = frm.add_child('items');

                            row.item_code = d.item_code;
                            row.qty = d.qty;
                            row.uom = d.uom;
                        });

                        frm.refresh_field('items');
                        calculate_total_qty(frm); // ✅ yahan call
                    }
                }
            });
        }
    }
});

// 🔹 Child table events
frappe.ui.form.on('Inward Gate Pass Item', {
    qty: function(frm) {
        calculate_total_qty(frm);
    },
    items_remove: function(frm) {
        calculate_total_qty(frm);
    }
});

// 🔹 Function
function calculate_total_qty(frm) {
    let total = 0;

    (frm.doc.items || []).forEach(function(d) {
        total += flt(d.qty);
    });

    frm.set_value('total_qty', total);
}


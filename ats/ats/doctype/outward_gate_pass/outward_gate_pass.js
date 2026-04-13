// Copyright (c) 2025, Ats and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Outward Gate Pass", {
// 	refresh(frm) {

// 	},
// });

frappe.ui.form.on('Outward Gate Pass', {

    sales_order: function(frm) {
        
        if (!frm.doc.sales_order) return;

        frm.clear_table('items');

        frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Sales Order',
                name: frm.doc.sales_order
            },
            callback: function(r) {
                if (r.message) {

                    let so = r.message;
                    frm.set_value("good_dispatched_type", "Finished Goods")   
                    // 🔵 Supplier / Customer logic (Sales Order se)
                    frm.set_value("customer", so.customer);

                    // 🔵 Load items from Sales Order
                    (so.items || []).forEach(function(d) {
                        let row = frm.add_child('items');

                        row.item_code = d.item_code;
                        row.qty = d.qty;
                        row.uom = d.uom;
                        row.rate = d.rate;
                        row.amount = d.amount;
                    });

                    frm.refresh_field('items');
                    calculate_total_qty(frm);
                }
            }
        });
    }
});


// 🔹 Child Table Events
frappe.ui.form.on('Outward Gate Pass Item', {

    qty: function(frm) {
        calculate_total_qty(frm);
    },

    items_remove: function(frm) {
        calculate_total_qty(frm);
    }
});


// 🔹 Total Calculation
function calculate_total_qty(frm) {
    let total = 0;

    (frm.doc.items || []).forEach(function(d) {
        total += flt(d.qty);
    });

    frm.set_value('total_qty', total);
}
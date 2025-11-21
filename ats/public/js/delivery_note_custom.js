frappe.ui.form.on('Delivery Note', {
    refresh: function(frm) {

        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(
                __("Sales Invoice"),
                () => frm.events.map_to_sales_invoice(frm),
                __("Create")
            );
        }
    },

    map_to_sales_invoice: function(frm) {

        frappe.call({
            method: "ats.custom.delivery_note_custom.create_sales_invoice",
            args: {
                delivery_note: frm.doc.name
            },
            freeze: true,
            freeze_message: __("Creating Sales Invoice..."),
            callback: function(r) {
                if (r.message) {
                    const si_doc = frappe.model.sync(r.message)[0];
                    frappe.set_route("Form", "Sales Invoice", si_doc.name);
                }
            }
        });

    },
});

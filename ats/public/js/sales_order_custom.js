frappe.ui.form.on('Sales Order', {
    onload(frm) {
        
        // Ensure company field always visible
        frm.set_df_property('company', 'hidden', 0);

        // Optional: also make it read-only false if needed
        frm.set_df_property('company', 'read_only', 0);
    }
});


frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {

        if (frm.doc.docstatus === 1) {
            frm.add_custom_button(
                __("Delivery Note"),
                () => frm.events.map_to_delivery_note(frm),
                __("Create")
            );
        }
    },

    map_to_delivery_note: function(frm) {

        frappe.call({
            method: "ats.custom.sales_order_custom.create_delivery_note",
            args: {
                sales_order: frm.doc.name
            },
            freeze: true,
            freeze_message: __("Creating Delivery Note..."),
            callback: function(r) {
                if (r.message) {
                    const dn_doc = frappe.model.sync(r.message)[0];
                    frappe.set_route("Form", "Delivery Note", dn_doc.name);
                }
            }
        });

    },
});


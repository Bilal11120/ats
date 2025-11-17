frappe.ui.form.on('Sales Order', {
    onload(frm) {
        
        // Ensure company field always visible
        frm.set_df_property('company', 'hidden', 0);

        // Optional: also make it read-only false if needed
        frm.set_df_property('company', 'read_only', 0);
    }
});

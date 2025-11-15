frappe.ui.form.on('Quotation', {
    onload_post_render(frm) {
        frm.set_df_property('company', 'hidden', 0);
        frm.set_df_property('company', 'read_only', 0);
    },
    refresh(frm) {
        frm.set_df_property('company', 'hidden', 0);
        frm.set_df_property('company', 'read_only', 0);
    }
});

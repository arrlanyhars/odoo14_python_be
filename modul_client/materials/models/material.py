from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Material(models.Model):
    _name = 'materials.model'
    _description = 'Material Model'
    _inherit = ['mail.thread']

    material_code = fields.Char(string='Material Code', required=True)
    material_name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection(
        [('fabric', 'Fabric'), ('jeans', 'Jeans'), ('cotton', 'Cotton')],
        string='Material Type',
        required=True
    )
    material_buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Related Supplier', required=True)
    is_saved = fields.Boolean(string="Is Saved", default=False)
    to_be_deleted = fields.Boolean(string='To Be Deleted', default=False)

    @api.constrains('material_buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.material_buy_price < 100:
                raise ValidationError("Material Buy Price must be at least 100.")

    def action_save(self):
        for record in self:
            if not record.material_code or not record.material_name:
                raise ValidationError("Material code and name are required to save.")
            self._check_buy_price()
            record.is_saved = True
            self._send_notification_to_supplier()
        return True

    def _send_notification_to_supplier(self):
        for record in self:
            if record.supplier_id:
                message = f"Material '{record.material_name}' has been successfully saved with code {record.material_code}."
                record.supplier_id.message_post(body=message)


    def request_delete(self):
        for record in self:
            if record.is_saved:
                raise ValidationError("Cannot delete material that has already been saved.")
            record.to_be_deleted = True
            record.message_post(body="Material has been marked for deletion.")

    
    def action_confirm_delete(self):
        for record in self:
            record.to_be_deleted = True
            record.message_post(body="Material has been marked for deletion. You can now delete it.")


    def unlink(self):
        for record in self:
            # if record.to_be_deleted:
            return super(Material, self).unlink()
            # else:
                # raise ValidationError("Please confirm the deletion before proceeding.")
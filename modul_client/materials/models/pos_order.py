from odoo import models, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model
    def create(self, values):
        order = super(PosOrder, self).create(values)
        if order.partner_id.email:
            template = self.env.ref('custom_pos.mail_template_receipt')
            self.env['mail.template'].browse(template.id).send_mail(order.id, force_send=True)
        return order

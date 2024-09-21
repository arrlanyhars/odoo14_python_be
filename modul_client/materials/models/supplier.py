from odoo import models, fields

class Supplier(models.Model):
    _name = 'supplier.model'
    _description = 'Supplier Model'
    _inherit = 'res.partner'
    _inherit = ['mail.thread']
    
    is_supplier = fields.Boolean(string='Is a Supplier', default=False)

from odoo import http, fields, api, _
from odoo.http import request
from odoo.addons.base_rest.controllers import main
from odoo.exceptions import ValidationError

class MaterialController(http.Controller):

    @http.route('/materials', type='json', auth='public', methods=['GET'], csrf=False)
    def list_materials(self, **kwargs):
        material_type = kwargs.get('material_type', False)
        domain = []
        if material_type:
            domain.append(('material_type', '=', material_type))

        materials = request.env['material.model'].sudo().search(domain)
        material_list = []
        for material in materials:
            material_list.append({
                'code': material.material_code,
                'name': material.material_name,
                'type': material.material_type,
                'buy_price': material.material_buy_price,
                'supplier': material.supplier_id.name if material.supplier_id else "Unknown"
            })
        return {'status': 200, 'data': material_list}

    @http.route('/materials/<int:material_id>', type='json', auth='public', methods=['GET'], csrf=False)
    def get_material(self, material_id):
        material = request.env['material.model'].sudo().browse(material_id)
        if not material.exists():
            return {'status': 404, 'message': 'Material not found'}

        material_data = {
            'code': material.material_code,
            'name': material.material_name,
            'type': material.material_type,
            'buy_price': material.material_buy_price,
            'supplier': material.supplier_id.name if material.supplier_id else "Unknown"
        }
        return {'status': 200, 'data': material_data}

    @http.route('/materials/update/<int:material_id>', type='json', auth='public', methods=['POST'], csrf=False)
    def update_material(self, material_id, **kwargs):
        material = request.env['material.model'].sudo().browse(material_id)
        if not material.exists():
            return {'status': 404, 'message': 'Material not found'}

        material_code = kwargs.get('material_code')
        material_name = kwargs.get('material_name')
        material_type = kwargs.get('material_type')
        material_buy_price = kwargs.get('material_buy_price')
        supplier_id = kwargs.get('supplier_id')

        if material_code:
            material.material_code = material_code
        if material_name:
            material.material_name = material_name
        if material_type:
            material.material_type = material_type
        if material_buy_price:
            if material_buy_price < 100:
                return {'status': 400, 'message': 'Material buy price must be at least 100.'}
            material.material_buy_price = material_buy_price
        if supplier_id:
            material.supplier_id = supplier_id

        return {'status': 200, 'message': 'Material updated successfully'}

    @http.route('/materials/delete/<int:material_id>', type='json', auth='public', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        material = request.env['material.model'].sudo().browse(material_id)
        if not material.exists():
            return {'status': 404, 'message': 'Material not found'}

        try:
            material.unlink()
            return {'status': 200, 'message': 'Material deleted successfully'}
        except ValidationError as e:
            return {'status': 400, 'message': str(e)}

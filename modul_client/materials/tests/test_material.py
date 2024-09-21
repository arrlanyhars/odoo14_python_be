from odoo.tests import HttpCase
from odoo import exceptions

class TestMaterialController(HttpCase):
    
    def setUp(self):
        super(TestMaterialController, self).setUp()
        self.supplier = self.env['res.partner'].create({
            'name': 'Test Supplier',
            'is_company': True,
        })
        self.material = self.env['material.model'].create({
            'material_code': 'M001',
            'material_name': 'Test Material',
            'material_type': 'fabric',
            'material_buy_price': 150,
            'supplier_id': self.supplier.id
        })

    def test_list_materials(self):
        response = self.url_open('/materials')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(len(result['data']) > 0)

    def test_get_material(self):
        response = self.url_open(f'/materials/{self.material.id}')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['data']['code'], 'M001')
        self.assertEqual(result['data']['name'], 'Test Material')

    def test_update_material(self):
        response = self.url_open(
            f'/materials/update/{self.material.id}', 
            data={
                'material_name': 'Updated Material',
                'material_buy_price': 200,
            }, 
            method='POST'
        )
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'Material updated successfully')
        self.material.refresh()
        self.assertEqual(self.material.material_name, 'Updated Material')
        self.assertEqual(self.material.material_buy_price, 200)

    def test_delete_material(self):
        response = self.url_open(f'/materials/delete/{self.material.id}', method='DELETE')
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result['message'], 'Material deleted successfully')
        with self.assertRaises(exceptions.MissingError):
            self.material.refresh()

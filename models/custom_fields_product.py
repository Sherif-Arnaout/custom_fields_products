from odoo import models, fields, api
from random import choice
from string import digits
from odoo.exceptions import ValidationError


# Inherit Product Template
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Function to generate custom barcode
    def generate_custom_barcode(self):
        for product in self:
            if not product.categ_id and not product.detailed_type:
                raise ValidationError("Product name is required to generate barcode.")

            barcode_prefix = 'P00' + "".join(choice(digits) for i in range(5))
            detailed_type = product.detailed_type
            categ_id = product.categ_id

            if detailed_type == "product":
                detailed_type_code = 'ST'
            elif detailed_type == "consu":
                detailed_type_code = 'CO'
            elif detailed_type == "service":
                detailed_type_code = 'SE'
            else:
                detailed_type_code = ''

            if categ_id:
                categ_id_code = categ_id.name[:2].upper()
            else:
                categ_id_code = ''

            product.barcode = f"{detailed_type_code}-{categ_id_code}/{barcode_prefix}"

    # Action call to generate custom barcode
    def action_generate_random_barcode(self):
        self.generate_custom_barcode()

    # Action call to print custom barcode
    def print_custom_barcode(self):
        return self.env.ref('custom_fields_products.report_action_custom_barcode_print').read()[0]


# Inherit Stock Move
class CustomFieldsStock(models.Model):
    _inherit = 'stock.move'

    barcode = fields.Char(string="Barcode")

    # Function triggered on barcode scan
    @api.onchange('barcode')
    def _onchange_barcode_scan(self):
        product_rec = self.env['product.product']
        if self.barcode:
            product = product_rec.search([('barcode', '=', self.barcode)])
            self.product_id = product.id


# Inherit Stock Picking
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    barcode = fields.Char(string='Barcode')

    # Function triggered on barcode scan
    @api.onchange('barcode')
    def product_barcode(self):
        product_item = self.env['product.product']
        product_id = product_item.search([('barcode', '=', self.barcode)])
        product_found = False
        if self.barcode and not product_id:
            raise ValidationError("Product not found.")

        if self.barcode and self.move_ids_without_package:
            for line in self.move_ids_without_package:
                if line.product_id.barcode == self.barcode:
                    line.quantity_done += 1
                    product_found = True
        if self.barcode and not product_found:
            if product_id:
                raise Warning("Barcode already scanned.")

    # Function to write barcode and increment quantity
    def write(self, vals):
        res = super(StockPicking, self).write(vals)
        if vals.get('barcode') and self.move_ids_without_package:
            for line in self.move_ids_without_package:
                if line.product_id.barcode == vals['barcode']:
                    line.quantity_done += 1
                    self.barcode = None
        return res

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    Technical_order_id = fields.Many2one('technical.order')






class SaleOrderline(models.Model):
    _inherit = 'sale.order.line'

    teccnical_order_line_id = fields.Many2one('order.lines')

    @api.constrains('product_uom_qty')
    def quantitty_constrains(self):
        for rec in self:
            if rec.product_uom_qty > rec.teccnical_order_line_id.Quantity:
                raise ValidationError(
                    _("  the quantities soline shouldn't exceed the ones requested in the TO."))
    # @api.onchange('product_uom_qty')
    # def onchange_of_product_uom_qty(self):
    #     for rec in self:
    #       if  rec.product_id == rec.teccnical_order_line_id.product_id :
    #           rec.teccnical_order_line_id.remening = rec.teccnical_order_line_id.Quantity - rec.product_uom_qty


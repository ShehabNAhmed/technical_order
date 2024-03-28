from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TechnicalOrder(models.Model):
    _name = 'technical.order'
    _description = 'technical order'
    _inherit = ['mail.thread', 'mail.activity.mixin', ]
    _rec_name = 'Request_name'

    Request_name = fields.Char(string="Name", required=True)
    ref = fields.Char(readonly=True)
    Requested_by = fields.Many2one('res.users', string="Requested_by", default=lambda self: self.env.user)
    customer_id = fields.Many2one('res.partner', domain="[('is_tech_offer', '=', True)]", required=True)
    Start_Date = fields.Date(string='Start Date', default=fields.Date.context_today)
    End_date = fields.Date(string="End Date")
    Rejection_Reason = fields.Text(string="Rejection Reason", readonly=True)
    orderlines_ids = fields.One2many('order.lines', 'purchase_id', string='orderlines')
    Total_Price = fields.Float(string='total price', compute='compute_total_price')
    state = fields.Selection(
        [('draft', 'draft'), ('to be approved', 'to be approved'), ('reject', 'reject'), ('approve', 'approve'),
         ('cancel', 'Cancelled')],
        string='state', default='draft', required=True)
    sale_order_id = fields.Many2one('sale.order')

    hide_btn_create = fields.Boolean(compute='_compute_hide_btn_create', default=False)

    @api.depends("orderlines_ids.product_id", )
    def _compute_hide_btn_create(self):
        for rec in self:
            for line in rec.orderlines_ids:
                sale_line = self.env['sale.order.line'].search(
                    [('product_id', '=', line.product_id.id),
                     ('teccnical_order_line_id', '=', line.id)])
                # print(sale_line)
                sale_qty = sum(sale_line.mapped('product_uom_qty'))
                # qty_to =line.Quantity - sale_qty
                if sale_qty >= line.Quantity:
                    rec.hide_btn_create = True
                else:
                    rec.hide_btn_create = False

    def create_sale_order(self):
        sale_list = []
        for sale in self.orderlines_ids:
            sale_line = self.env['sale.order.line'].search(
                [('product_id', '=', sale.product_id.id),
                 ('teccnical_order_line_id', '=', sale.id)])
            sale_qty = sum(sale_line.mapped('product_uom_qty'))
            qty_to = sale.Quantity - sale_qty
            sale_list.append(
                (0, 0, {
                    'product_id': sale.product_id.id,
                    'product_uom_qty':qty_to ,
                    'price_unit': sale.Cost_Price,
                    'name': sale.Description,
                    'teccnical_order_line_id': sale.id,

                })
            )

        self.env['sale.order'].create({
            'partner_id': self.customer_id.id,
            'state': 'draft',
            'order_line': sale_list,
            'Technical_order_id': self.id

        })

    @api.depends('orderlines_ids.Total')
    def compute_total_price(self):
        for rec in self:
            rec.Total_Price = sum(rec.orderlines_ids.mapped('Total'))

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('technical.order')
        return super(TechnicalOrder, self).create(vals)

    def action_in_to_be_approved(self):
        for r in self:
            r.state = 'to be approved'

    def action_draft(self):
        for r in self:
            r.state = 'draft'

    def action_approve(self):
        print("shehaanb")
        technical_order = self.env.ref('technical_orde.Technical_Order_Manager_group')
        partner_ids = [user.partner_id.id for user in technical_order.users]
        if partner_ids:
            print("shehaanefreeeeeeeeeeeeeeeb")
            self.message_post(body=("Technical Order" + " " + self.Request_name + " " + "has been approved"),
                              partner_ids=partner_ids)
        for r in self:
            r.state = 'approve'

    def action_cancel(self):
        for r in self:
            r.state = 'cancel'

    def action_reject(self):
        for r in self:
            r.state = 'reject'

    def action_back_to_draft(self):
        for r in self:
            r.state = 'draft'

    count_to = fields.Integer(compute='_compute_count')

    def _compute_count(self):
        for rec in self:
            count = self.env['sale.order'].search_count([('Technical_order_id', '=', self.id)])
            self.count_to = count

    def action_open_related_sale(self):
        print("shehab")

    def smart_button_so(self):
        action = self.env['ir.actions.act_window']._for_xml_id("sale.action_quotations_with_onboarding")
        action['domain'] = [('Technical_order_id', '=', self.id), ]
        action['context'] = {'create': False}
        return action


class Orderline(models.Model):
    _name = "order.lines"
    _description = "order line"

    product_id = fields.Many2one('product.product')
    Description = fields.Char(related='product_id.name')
    Quantity = fields.Integer(string='Quantity', default=5)
    Cost_Price = fields.Float(readonly=True, related='product_id.list_price')
    Total = fields.Float(readonly=True, compute='compute_total')
    remainung_quantity = fields.Float(compute='_compute_remaining_qty')
    purchase_id = fields.Many2one('technical.order', string="technical_id")
    sale_order_line_id =fields.Many2one('sale.order.line')
    #
    # @api.depends('Quantity','sale_order_line_id.product_uom_qty')
    # def _compute_remaining_qty(self):
    #     for rec in self:
    #
    #         sale_line = self.env['sale.order.line'].search(
    #             [('product_id', '=', rec.product_id.id), ('teccnical_order_line_id', '=', rec.id)])
    #         qty_so = sum(sale_line.mapped('product_uom_qty'))
    #         rec.remainung_quantity = rec.Quantity - qty_so


    @api.depends('Quantity', 'Cost_Price')
    def compute_total(self):
        for r in self:
            r.Total = r.Cost_Price * r.Quantity

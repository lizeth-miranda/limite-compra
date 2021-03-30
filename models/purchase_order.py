# -*- coding: utf-8 -*-
# instruccion para hacer importaciones desde odoo
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class Limit(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection(selection_add=[(('lock', 'Bloqueado'))])

    copyamount = fields.Monetary(
        compute='funcopyamount',
        store=True,
    )

    @api.depends('amount_total')
    def funcopyamount(self):
        for record in self:
            record.copyamount = record.amount_total

    # Función que revisa el limite de compra, cambia los estados
    @api.constrains('product_id')
    def button_confirm(self):
        res = super(Limit, self).button_confirm()
        for record in self:
            if record.copyamount >= 10000.0:
                self.write({'state': 'lock'})
                record.copyamount = record.copyamount-record.copyamount

                # raise ValidationError(
                #     _("La compra excede a los $10,000 pesos, favor de pedir autorización a dirección"))
        return res

    def action_lock(self):
        self.write({'state': 'draft'})

    # función que busca presupuestos bloqueados y los desbloquea despues de un tiempo
    def check_lock(self):
        purchase_orders = self.env['purchase.order'].search([])
        for order in purchase_orders:
            if order.state == 'lock':
                order.write({'state': 'draft'})

    # suma = fields.Float(
    #     compute='_suma',
    #     store=True,
    # )
    # analytic = fields.Char(
    #     related="order_line.account_analytic_id.display_name",
    #     store=True,
    # )

    # sumar_horas = fields.Datetime(
    #     string="suma",
    #     compute='sumarhoras',
    # )

    # ahora = fields.Datetime(string="Ahora", default=fields.Datetime.now)
    # default=fields.Datetime.now,
    # store=True,

    # @api.depends('origin')
    # def _suma(self):
    #     for attendance in self:
    #         attendance.suma = sum(self.env['purchase.order'].search([
    #             ('analytic', '=', attendance.analytic),
    #         ]).mapped('amount_total'))

    # @api.model ** esta función le suma dias,horas, minutos, etc a un campo Datetime**
    # def sumarhoras(self):
    #     if self.date_approve:
    #         self.sumar_horas = self.date_approve + timedelta(minutes=40)
    #         return fields.Date.context_today(self, timestamp=self.sumar_horas)
    #     else:
    #         self.sumar_horas = False

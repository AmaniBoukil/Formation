# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# création de table

class HospitalAppointement(models.Model):
    _name = "hospital.appointement" # In terminal name became hospital_patient
    _description = "Hospital Appointement"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit mail.thread to hospital.patient model
    # _rec_name = 'patient_id'

    patient_id = fields.Many2one(comodel_name="hospital.patient", string="Patient", ondelete="restrict")
    appointement_time = fields.Datetime(string="Appointement Time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    gender = fields.Selection(default="female", related="patient_id.gender", readonly=False)
    ref = fields.Char(string="Reference", help="Reference of the patient from patient record")

    prescription = fields.Html(string="Prescription")

    ######
    namename = fields.Char(string="namename")
    ######

    priority = fields.Selection([
        ('0', 'Very Low'),
        ('1', 'Low'),
        ('2', 'Normal'),
        ('3', 'High')], string='Priority')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')], default="draft", string='Status', required=True)

    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=1)
    pharmacy_lines_ids = fields.One2many("appointement.pharmacy.lines", 'appointement_id', string="Pharmacy Lines")

    hide_sales_price = fields.Boolean("Hide Sales Price")

    @api.onchange("patient_id")
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("Button Clicked !!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Click successful',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref("om_hospital.action_cancel_appointment").read()[0]
        print(action)
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # def action_cancel(self):
    #     for rec in self:
    #         rec.state = 'cancel'

    ######
    @api.model
    def create(self, vals):
        print("create method is triggered.....", vals)
        vals['namename'] = self.env['ir.sequence'].next_by_code('hospital.appointement')
        return super(HospitalAppointement, self).create(vals)

    def write(self, vals):
        print("write method is triggered.....", vals)
        if not self.namename and not vals.get('namename'):
            vals['namename'] = self.env['ir.sequence'].next_by_code('hospital.appointement')
        return super(HospitalAppointement, self).write(vals)

    def name_get(self):
        company = self.env.user.company_id.id
        print("Company : ", company)

        for record in self:
            print("ID appointment unique : ", record.id, "[%s] %s" % (record.ref, record.namename))
        return [(record.id, "[%s] %s" % (record.ref, record.namename))for record in self]
    ######

    #override unlink method
    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can only delete appointment with 'Draft' status"))
        return super(HospitalAppointement, self).unlink()


class AppointementPharmacyLines(models.Model):
    _name = "appointement.pharmacy.lines"
    _description = "Appointement Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string="Price", related="product_id.list_price")
    qty = fields.Integer(string="Quantity", default=1)
    appointement_id = fields.Many2one("hospital.appointement", string="Appointement")










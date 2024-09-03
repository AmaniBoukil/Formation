# -*- coding: utf-8 -*-
import datetime
from odoo import api, fields, models,_
from odoo.exceptions import ValidationError

# création de table

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields):
        res = super(CancelAppointmentWizard, self).default_get(fields)
        #res['reason'] = "Cancellation"
        print("Default get executed ....", fields, "......", res)
        res['date_cancel'] = datetime.date.today()
        #print(res)
        if self.env.context.get('active_id'):
            print('Active ID is : ', self.env.context['active_id'])
            res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one('hospital.appointement', string="Appointment")
    # domain=['|', ('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))]

    reason = fields.Text(string="Reason")
    date_cancel = fields.Date(string="Cancellation date")

    def action_cancel(self):

        if self.appointment_id.booking_date == fields.Date.today():
            print(fields.Date.today())
            print(datetime.date.today())
            raise ValidationError(_("Sorry, cancellation is not allowed on the same day of booking !"))
        self.appointment_id.state = 'cancel'
        return

    # def action_cancel(self):
    #     print("cancel.appointment.wizard / self.env.context : ", self.env.context)
    #     for appointement in self.env['hospital.appointement'].browse(self.env.context['active_ids']):
    #         print("appointement : ", appointement)
    #         appointement.state = 'cancel'
    #     return

    # for rec in self:
    #     rec.state = 'cancel'



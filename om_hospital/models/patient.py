# -*- coding: utf-8 -*-
from datetime import date
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# création de table

class HospitalPatient(models.Model):
    _name = "hospital.patient" # In terminal name became hospital_patient
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # inherit mail.thread to hospital.patient model

    name = fields.Char(tracking=1)
    ref = fields.Char(string="Reference")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", tracking=1)
    active = fields.Boolean(string="Active", default=True) # visibilité
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string="Age", tracking=1, compute="_compute_age", store=True)

    appointement_id = fields.Many2one(comodel_name="hospital.appointement", string="Appointement")

    image = fields.Image(string="Image")

    tag_ids = fields.Many2many('patient.tag', string="Tags", store=True)

    #appointment_count = fields.Integer("Appointment Count")
    appointment_count = fields.Integer(string="Appointment Count", compute="_compute_appointment_count", store=True)

    appointment_ids = fields.One2many('hospital.appointement', 'patient_id', string='Appontments')

    parent = fields.Char(string="Parent")
    marital_status = fields.Selection([('maried', 'Maried'), ('single', 'Single')],
                                      string="Marital Status", tracking=True)
    partner_name = fields.Char(string="Partner Name")


    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointement'].search_count([("patient_id", "=", rec.id)])

    # constrainte sur date of birth
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("The entered date is not acceptable !"))

    #override create method
    @api.model
    def create(self, vals):
        print("create funct inherited ....", vals)

        #simple creation
        # if vals.get('ref') == False:
        #     print(vals.get('ref'))
        #     vals['ref'] = "OMTEST"
        #     print(vals.get('ref'))

        #génération automatique des séquences
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        # print("Amani experiences" , self.env.ref('om_hospital.seq_hospital_patient'))
        return super(HospitalPatient, self).create(vals)

    # override write method
    def write(self, vals):
        print("write method is triggered.....", vals)
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)


    #computed method : calculate age from date of birth
    @api.depends('date_of_birth')
    def _compute_age(self):
        #print("self.....", self)
        #print(type(self))
        today = date.today()
        print("Today Date", today)
        for rec in self:
            if rec.date_of_birth:
                print(rec)
                print(str(rec.name)+" Date Of Birth : ", rec.date_of_birth, rec.date_of_birth.year)
                rec.age = today.year - rec.date_of_birth.year
                print("age =", rec.age)
            else:
                rec.age = 1

    # rec_name
    def name_get(self):
        return [(record.id, "[%s] %s" % (record.ref, record.name))for record in self]
        # patient_list=[]
        # print(self)
        # for record in self:
        #     print(record)
        #     name = record.ref +' '+ record.name
        #     patient_list.append((record.id, name))
        # return patient_list

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You cannot delete a patient with appointment !"))


    def action_test(self):
        print("Clicked")
        return

    def print_custom_report(self):
        return self.env.ref("om_hospital.report_custom_patients_details_action").report_action(self)

# -*- coding: utf-8 -*-
from odoo import models, fields, api
from ast import literal_eval

class HospitalSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    cancel_days = fields.Integer(string='Cancel Days', config_parameter='om_hospital.cancel_day')
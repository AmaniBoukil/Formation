# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.model
    def default_plan(self):
        plan = self.env.ref('ct_fleet.analytic_plan_vehicle', raise_if_not_found=False)
        return plan.id if plan else False

    analytic_plan_vehicle = fields.Many2one("account.analytic.plan",
                                            string='Default Analytic Plan',
                                            config_parameter='ct_fleet.analytic_plan_vehicle',
                                            default=default_plan,
                                            readonly=False)

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param('ct_fleet.analytic_plan_vehicle',
                                                         self.analytic_plan_vehicle.id or False)
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        dflt_plan = self.env['ir.config_parameter'].sudo().get_param('ct_fleet.analytic_plan_vehicle')
        res.update(analytic_plan_vehicle=int(dflt_plan) if dflt_plan else False)
        return res


    # @api.model
    # def default_get(self, fields_default):
    #     defaults = super().default_get(fields_default)
    #
    #     print(self.env['ir.config_parameter'].get_param('ct_fleet.default_analytic_plan'))
    #     # print(defaults['default_analytic_plan'])
    #
    #     return defaults

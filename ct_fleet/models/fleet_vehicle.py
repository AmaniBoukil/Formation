from odoo import models, fields, api, exceptions, _
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', store=True)

    @api.constrains('analytic_account_id')
    def _check_analytic_account_id(self):
        for vehicle in self:
            if vehicle.analytic_account_id:
                count = self.env['account.analytic.account'].search_count([('name', '=', vehicle.analytic_account_id.name)])
                print(count)
                if count > 1:
                    raise ValidationError(_("A vehicle can only be linked to one unique analytic account."))
        return


    def create_analytic_account(self):
        dflt_plan_id = int(self.env['ir.config_parameter'].sudo().get_param('ct_fleet.analytic_plan_vehicle'))

        for vehicle in self:
            if not vehicle.analytic_account_id:
                analytic_account = self.env['account.analytic.account'].create({
                    'name': vehicle.display_name,
                    'plan_id': dflt_plan_id,
                })
                vehicle.analytic_account_id = analytic_account.id
        return

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    def open_wizard(self):
        action = self.env.ref("ct_fleet.action_generate_analytic_entries").read()[0]
        return action

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


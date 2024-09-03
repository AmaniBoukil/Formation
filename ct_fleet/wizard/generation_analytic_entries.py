from odoo import api, fields, models, _, exceptions
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class GenerationAnalyticEntriesWizard(models.TransientModel):
    _name = "generation.analytic.entries.wizard"
    _description = "Generation Analytic Entries Wizard"

    message = fields.Text(
        default="Veuillez annuler cette opération, si vous avez déjà lié ces dépenses à une ligne de facture d'achat, "
                "sinon vous risquez d'avoir une duplication des écritures analytiques.")

    def action_generation(self):

        actv_ids = self.env.context['active_ids']
        print("Active_ID ...................", actv_ids)
        if not actv_ids:
            raise exceptions.UserError(_("No active fleet vehicle log service found"))

        for actv_id in actv_ids:
            log_service = self.env['fleet.vehicle.log.services'].browse(actv_id)
            if not log_service:
                raise exceptions.UserError(_("No fleet vehicle log service found"))

            if not log_service.description:
                raise exceptions.UserError(_("Veuillez saisir une description avant de continuer."))

            if not log_service.service_type_id:
                raise exceptions.UserError(_("Veuillez sélectionner un type de service avant de continuer."))

            if not log_service.amount:
                raise exceptions.UserError(_("Veuillez entrer un cout avant de continuer."))

            if not log_service.date:
                raise exceptions.UserError(_("Veuillez entrer une date avant de continuer."))

            account = log_service.vehicle_id.analytic_account_id
            print("Account............", account)
            if not account:
                raise exceptions.UserError(_("No analytic account found for this vehicle"))

            plan = log_service.vehicle_id.analytic_account_id.plan_id
            print("Plan..........", plan)
            if not plan:
                raise exceptions.UserError(_("No analytic plan found for this vehicle"))

            product = self.env['product.product'].search([('name', '=', 'Services')], limit=1)
            print("Product...........", product)
            if not product:
                raise exceptions.UserError(_("No service product found"))

            self.env['account.analytic.line'].create({
                'name': f"{log_service.description} /  {log_service.service_type_id.name}",
                'account_id': account.id,
                'plan_id': plan.id,
                'company_id': self.env.company.id,
                'amount': -log_service.amount,
                'unit_amount': 1,
                'product_id': product.id,
                'date': log_service.date,
            })

        return

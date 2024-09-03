from datetime import date
from odoo import api, fields, models

class OdooPlayGround(models.Model):
    _name = "odoo.playground"
    _description = "Odoo PlayGround"

    DEFAULT_EW_VARIABLES =""

    model_id = fields.Many2one('ir.model', string="Model")
    code = fields.Text(string="Code", default=DEFAULT_EW_VARIABLES)
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            #not empty
            if self.model_id:
                print(self) #instance du module / current object
                print(self.env) #odoo api env object
                print(self.model_id) #instance du related module / class
                print(type(self.model_id.model)) #attribut de type str / nom de class

                model = self.env[self.model_id.model] # model = self.env['res.partner']

                print(type(model)) #attribut odoo api / object de class
                print(type(self.code))

                # execution of code champ in result champ
                self.result = str(eval(self.code))

            else:
                model = self
                print(model) #instance du current module
                self.result = str(eval(self.code))

        except Exception as e:
            self.result = str(e)

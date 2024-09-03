from odoo import models, fields, api
from odoo.exceptions import UserError

class VisitorTable(models.Model):
    _name = 'visitor.table'
    _description = 'Visitor'

    name = fields.Char(string='Name')
    image = fields.Binary(string='Image')
    # image2 = fields.Image(string="Image")
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    camera_id = fields.Many2one(comodel_name="camera.table", string="Camera")
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')

    cameras_lines_ids = fields.One2many("cameras.lines", 'camera_line_id', string="CamerasLines")

    # create method : creating lines automatiquement lors creation d'un nouveau visiteur
    @api.model_create_multi
    def create(self, vals_list):
        print("visiteur / create / vals_list : ", vals_list) # vals of current object
        vis = super(VisitorTable, self).create(vals_list) # current object

        # Rechercher les visiteurs existants dans la base de données
        existing_visitors = self.search([('name', '=', vis.name)])

        for existing_visitor in existing_visitors:
            cameras_lines_vals = {
                'camera_line_id': vis.id, # Associe la ligne au nouveau visiteur
                'cam_id': existing_visitor.camera_id.id,  # Utiliser .id pour obtenir l'ID de l'enregistrement de la caméra
                'check_in': existing_visitor.check_in,
                'check_out': existing_visitor.check_out,
            }
            self.env['cameras.lines'].create(cameras_lines_vals)

        print("visiteur / update / vals_list : ", vals_list)
        # print(vals_list[0]["cameras_lines_ids"])

        return vis

    # delete method : restriction
    # def unlink(self):
    #     for visitor in self:
    #         print(visitor)
    #
    #         if visitor.cameras_lines_ids:
    #             raise UserError("You cannot delete a visitor with associated camera lines.")
    #     return super(VisitorTable, self).unlink()

class CamerasLines(models.Model):
    _name = "cameras.lines"
    _description = "Cameras Lines"

    camera_line_id = fields.Many2one('visitor.table', string="Num Of Camera")
    cam_id = fields.Many2one('camera.table')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')


    # @api.model_create_multi
    # def create(self, vals_list):
    #     print("cameras lines / create / vals_list : ", vals_list)
    #     return super(CamerasLines, self).create(vals_list)




########################################################################################################################
# TO-DO :
# Créer un class de visiteurs comme le table 'hr.employees' dans Odoo à coté de model 'table.visitors' d'attendances.
# Hide champ camera_id dans le form view.
# compléter delete method : restriction.
########################################################################################################################
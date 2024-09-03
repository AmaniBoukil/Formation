from odoo import models, fields, api

class CameraTable(models.Model):
    _name = 'camera.table'
    _description = 'Camera'

    name = fields.Char(string='Name')



########################################################################################################################
# TO-DO : Ajouter des fields pour caractériser les caméras.
########################################################################################################################
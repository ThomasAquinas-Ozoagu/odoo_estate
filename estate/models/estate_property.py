# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate housing distribution"

    name = fields.Char(required=True, default='Unkwown Property')

    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    partner_id = fields.Many2one("res.partner", string="Customer", copy=False)
#    partner_email = fields.Char(related="partner_id.email", string="Customer Email", readonly=True)
#    partner_address = fields.Char(related="partner_id.contact_address", string="Customer Address", readonly=True)
#    partner_phone = fields.Char(related="partner_id.phone", string="Customer Phone", readonly=True)
    
    seller_id = fields.Many2one("res.users", string="Agent", index=True, tracking=True, default=lambda self: self.env.user)
#    seller_email = fields.Char(related="seller_id.email", string="Agent Email", readonly=True)
#    seller_phone = fields.Char(related="seller_id.partner_id.phone", string="Agent Phone", readonly=True)
#    seller_login = fields.Char(related="seller_id.login", string="Agent Login", readonly=True)
#    seller_role = fields.Selection(related="seller_id.partner_id.function", string="Agent Role", readonly=True)

    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")    
    
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, 
        default=lambda self: fields.Date.today() + relativedelta(months=3)
        )
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    

    @api.onchange('garden')
    def _onchange_garden(self):
        if not self.garden:
            self.garden_area = 0
            self.garden_orientation = False
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
            return {
                'warning': {
                    'title': ("Garden added"),
                    'message': ("Default values have been set for garden area and orientation."),
                }
            }
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        [
        ('north', 'North'),
        ('south',  'South'),
        ('east', 'East'),
        ('west', 'West')
        ],
    )
    state = fields.Selection(    
    [
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancelled', 'Cancelled')
    ]
    )
    def action_set_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise UserError("A cancelled property cannot be sold.")
            if record.state == 'sold':
                raise UserError("The property is already sold.")
            if record.state == 'offer_accepted':
                record.state = 'sold'
                record.active = False
            else:
                raise UserError("Only properties with an accepted offer can be marked as sold.")
        return True

    def action_set_canceled(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("A sold property cannot be cancelled.")
            if record.state == 'cancelled':
                raise UserError("The property is already cancelled.")
            if record.state in ['new', 'offer_received']:
                record.state = 'cancelled'
                record.active = False
            else:
                raise UserError("Only new properties or those with received offers can be cancelled.")
        return True
    
    
    active = fields.Boolean(default=True)
    total_area = fields.Float(
        string="Total Area (sqm)",
        compute="_compute_total_area",
        store=True,
        help="Total area in square meters (living area + garden area)"
    )

    best_offer = fields.Float(
        string="Best Offer",
        compute="_compute_best_offer",
        store=True,
        help="Best offer made by a potential buyer for this property"
    )

    offer_count = fields.Integer(
        string="Offer Count",
        compute="_compute_offer_count",
        store=True,
    )


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0.0) + (record.garden_area or 0.0)
    
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offer_ids:
                record.best_offer = max(record.offer_ids.mapped('price'))
            else:
                record.best_offer = 0.0

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)




    # NEW RELATIONAL FIELDS ADDED FOR TUTORIAL #
    # ---------------------------------------- #

    # Many2one field: A property has one type.
    # property_type_id = fields.Many2one("estate.property.type", string="Property Type")



    # One2many field: A property can have many offers.
    # The 'inverse_name' must be the name of the Many2one field in the 'estate_property_offer' model.
    # offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Many2many field: A property can have many tags.
    # tag_ids = fields.Many2many("estate.property.tag", string="Tags")


#    @api.model
#    def demo_access_property_type(self, property_id):
#        """Example method to show how to access Many2one data like tutorial"""
#        property_record = self.browse(property_id)
#        if property_record and property_record.property_type_id:
#            return f"Property '{property_record.name}' has type '{property_record.property_type_id.name}'"
#        return "No property type linked."

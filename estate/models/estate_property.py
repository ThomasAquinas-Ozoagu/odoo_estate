# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real estate housing distribution"

    name = fields.Char(required=True, default='Unkwown Property')
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
    active = fields.Boolean(default=True)


    # NEW RELATIONAL FIELDS ADDED FOR TUTORIAL #
    # ---------------------------------------- #

    # Many2one field: A property has one type.
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")

    # One2many field: A property can have many offers.
    # The 'inverse_name' must be the name of the Many2one field in the 'estate_property_offer' model.
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")

    # Many2many field: A property can have many tags.
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")


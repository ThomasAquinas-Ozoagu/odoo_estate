# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers made for properties in our Real estate housing distribution"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    date_deadline = fields.Date(
        string="Offer Deadline",
        compute="_compute_offer_deadline",
        inverse="_inverse_offer_deadline",
        store=True,
        help="Deadline for the current offer"
    )

    validity = fields.Integer(
        string="Offer Validity (days)",
        default=7,
        help="Number of days an offer is valid"
    )

    @api.depends('validity')
    def _compute_offer_deadline(self):
        """
        Computes the offer deadline based on the offer's validity and its creation date.
        The creation date of an offer is stored in the standard 'create_date' field.
        """
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_offer_deadline(self):
        """
        Computes the validity in days based on the offer deadline and creation date.
        """
        for record in self:
            if record.date_deadline and record.create_date:
                # Correcting the type mismatch by getting just the date part of create_date
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    def action_accept_offer(self):
        for record in self:
            # Accept the offer 
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            # Refuse all other offers for the same property
            other_offers = self.search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id)
            ])
            other_offers.write({'status': 'refused'})
        return True
    
    def action_reject_offer(self):
        for record in self:
            record.status = 'refused'
        return True
    

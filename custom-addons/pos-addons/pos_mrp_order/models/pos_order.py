from odoo import models, fields, api


class PosOrder(models.Model):
    """About this module
    
    This module will add a Boolean field to mark that a POS order is manufatured or not
    And the add the Manufaturing Order Id to POS Order Model
    
    Example:
    
        Define the custom field first inside the pos.order model by inheriting it.

            class PosOrderInherit(models.Model):
                _inherit = "pos.order"    
                custom_field = fields.Text(string="Custom Field")
        
        Next, inside the javascript use the load_fields() to load the new field into the pos session.

            odoo.define("custom_module", function (require) {
                "use strict";
                var screens = require("point_of_sale.screens");
                var models = require("point_of_sale.models");    
                models.load_fields("pos.order", ["custom_field"]);    //Add the customisation code
            });
        
        Add the new field to be displayed in pos interface.

            var _super_posmodel = models.PosModel.prototype;
            models.PosModel = models.PosModel.extend({
                initialize: function(session,attributes)
                    {
                        var contact_model = _.find(this.models,function(model)
                        {
                            return model.model === "res.partner";
                        });
                        contact_model.fields.push("my_field");
                        return _super_posmodel.initialize.call(this,session,attributes);
                    },
                });
                
        Others:
            var models = require("point_of_sale.models");
            var _super_posmodel = models.PosModel.prototype;

            models.PosModel = models.PosModel.extend({
                initialize: function (session, attributes) {
                    // New code
                    var partner_model = _.find(this.models, function(model){
                        return model.model === "product.product";
                    });
                    partner_model.fields.push("qty_available");

                    // Inheritance
                    return _super_posmodel.initialize.call(this, session, attributes);
                },
            });
    """
    
    _inherit = "pos.order"

    # made_mrp = fields.Boolean(string="made_mrp", default=False, help="Default value is false ")
    made_mrp = fields.Boolean(string="made_mrp", help="Default value is false ",default=False,)
    mrp_order_id = fields.Many2one(comodel_name="mrp.production", string="MRP Order")

    @api.model
    def _order_fields(self,ui_order):
        # Here we have called the super method for inheriting method
        res = super(PosOrder, self)._order_fields(ui_order)
        # Here we have assigned input field value inside the custom field which we have added in the pos.order
        res["made_mrp"] = ui_order.get("made_mrp")
        return res
    # @api.model
    # def _order_fields(self, ui_order):
    #     res = super(PosOrder, self)._order_fields(ui_order)
    #     res["amount_via_discount"] = ui_order.get("amount_via_discount", 0)
    #     return res
    
    def get_mrp_status(self):
        return self.made_mrp
    
    def update_made_mrp(self):
        if self.made_mrp == False:
            self.made_mrp = True
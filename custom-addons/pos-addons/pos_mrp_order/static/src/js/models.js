odoo.define('pos_mrp_order.models', function(require) {
    'use strict';

    var pos_models = require("point_of_sale.models");
    pos_models.load_fields('pos.order', ['made_mrp']);

    var models = pos_models.PosModel.prototype.models;
    

    /** Add field "to_make_mrp" to Product Model */
    for (var i = 0; i < models.length; i++) {
        var model = models[i];
        if (model.model === "product.product") {
          model.fields.push("to_make_mrp");
        }
      }

    
    /** Add field "to_make_mrp" to Product Model */
    // for (var i = 0; i < models.length; i++) {
    //     var model = models[i];
    //     if (model.model === "product.product") {
    //       model.fields.push("to_make_mrp");
    //     }
    //   }
});
odoo.define("pos_mrp_order.receipt_screen", function (require) {
    "use strict";
    // var pos_model = require("point_of_sale.models");
    // const PosComponent = require('point_of_sale.PosComponent');
    // var pos_screens = require('point_of_sale.screens');
    // const pos_screens = require('point_of_sale.PaymentScreen');
    // var models = pos_model.PosModel.prototype.models;
    var rpc = require("web.rpc");
    // const Registries = require('point_of_sale.Registries');
    // const { useListener } = require('web.custom_hooks');
  
    // for (var i = 0; i < models.length; i++) {
    //   var model = models[i];
    //   if (model.model === "product.product") {
    //     model.fields.push("to_make_mrp");
    //   }
    // }
  
    // const { Gui } = require("point_of_sale.Gui");
    // const PosComponent = require("point_of_sale.PosComponent");
    // const { posbus } = require("point_of_sale.utils");
    // const ProductScreen = require("point_of_sale.ProductScreen");
    // const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");
    const ReceiptScreen = require("point_of_sale.ReceiptScreen");
    const CustomButtonReceiptScreen = (_ReceiptScreen) =>
      class extends _ReceiptScreen {
        constructor() {
          super(...arguments);
        //   var o = this.env.pos.get_order();
        //   o.to_invoice = true;
        }
        async call_to_make_mrp(){
          let order = this.env.pos.get_order();
          let order_line = order.orderlines.models;
          let due = order.get_due();
          if (order.is_paid() && order.get_client()) {
            const { confirmed, payload } = await this.showPopup(
              "DateInputPopup",
              {
                title: "Tạo lịch sản xuất cho đơn hàng",
                body: " Bạn có muốn tạo lịch sản xuất cho đơn hàng này ko?  \
                        <br/> - Nếu có thì chọn ngày sản xuất và bấm 'OK'. \
                        <br/>  - Nếu không thì chọn 'Cancel'. ",
                confirmText: "Tạo lịch SX",
                cancelText: "Không tạo"
  
              }
            );
            console.log("confirmed", confirmed);
            if (confirmed) {
              console.log("payload: ", payload);
              console.log("order:", order);
              console.log("is_made_mrp", order.made_mrp);
  
              if (order.made_mrp) {
                console.log("có make mrp");
                order.update_made_mrp();
              } else {
                console.log("Go ashead: ", order.made_mrp);
              }
              for (var i in order_line) {
                var list_product = [];
                console.log(
                  "order_line[i].product.to_make_mrp",
                  order_line[i].product
                );
                if (order_line[i].product.to_make_mrp) {
                  if (order_line[i].quantity > 0) {
                    var product_dict = {
                      id: order_line[i].product.id,
                      qty: order_line[i].quantity,
                      product_tmpl_id: order_line[i].product.product_tmpl_id,
                      pos_reference: order.name,
                      uom_id: order_line[i].product.uom_id[0],
                      start_date: payload,
                      pos_order_id: order.id
                    };
                    list_product.push(product_dict);
                  }
                }
  
                console.log("list hàng cần sản xuất: ", list_product);
                if (list_product.length) {
                  this.make_mrp(list_product);
                }
              }
            }
          }
        }
  
        async make_mrp(list_product) {
          return rpc
            .query({
              model: "mrp.production",
              method: "create_mrp_from_pos",
              args: [1, list_product],
            })
            .then(function (data) {
              console.log("mrp: ", data);
            });
        }
      };
    Registries.Component.extend(ReceiptScreen, CustomButtonReceiptScreen);
    return CustomButtonReceiptScreen;
  });
  
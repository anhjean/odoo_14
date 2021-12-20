odoo.define("pos_category.CategoryScreen", function (require) {
  "use strict";
  const PosComponent = require("point_of_sale.PosComponent");
  const ProductScreen = require("point_of_sale.ProductScreen");
  const { useListener } = require("web.custom_hooks");
  const Registries = require("point_of_sale.Registries");
  const { Gui } = require("point_of_sale.Gui");
  var framework = require("web.framework");
  var rpc = require("web.rpc");
  //   var _t = core._t;

  class CategoryScreen extends PosComponent {
    back() {
   
        this.trigger("close-temp-screen");
    }
    async draft() {
      // const { confirmed, payload } = await this.showPopup('ConfirmPopup', {
      //     title: this.env._t( "Create Sale Order and discard the current" + " PoS Order?"),
      //     body: this.env._t("This operation will permanently discard the current PoS" +
      //     " Order and create a Sale Order, based on the" +
      //     " current order lines."),
      // });
      var self = this;
      const { confirmed, payload } = await this.showPopup("ConfirmPopup", {
        title: this.env._t("Confirm Popup"),
        body: this.env._t("This click is successfully done."),
      });
      if (confirmed) {
        console.log("payload", payload);
        framework.blockUI();

        console.log('pos',self.env.pos);
        console.log(self.env.pos.get("selectedOrder").export_as_JSON());
        // console.log(' action: ',action)
        rpc
          .query({
            model: "sale.order",
            method: "create_order_from_pos",
            args: [self.env.pos.get("selectedOrder").export_as_JSON(), 'draft'],
          })
          .then(function () {
            console.log("payload", payload);
            self.hook_create_sale_order_success();
          })
          .catch(function (error, event) {
            self.hook_create_sale_order_error(error, event);
          });
      }
    }

    /**
     * Overloadable function to make custom action after Sale order
     * Creation succeeded
     */
    hook_create_sale_order_success() {
      console.log("hook create is runiing");
      framework.unblockUI();
      this.env.pos.get("selectedOrder").destroy();
    }

    /**
     * Overloadable function to make custom action after Sale order
     * Creation failed
     */
    hook_create_sale_order_error(error, event) {
      console.log("hook error is runiing");
      framework.unblockUI();
      event.preventDefault();
      if (error.code === 200) {
        // Business Logic Error, not a connection problem
        this.gui.show_popup("error-traceback", {
          title: error.data.message,
          body: error.data.debug,
        });
      } else {
        // Connexion problem
        this.gui.show_popup("error", {
          title: _t("The order could not be sent"),
          body: _t("Check your internet connection and try again."),
        });
      }
    }
  }
  CategoryScreen.template = "CreateSaleOrderScreenWidget";
  Registries.Component.add(CategoryScreen);
  return CategoryScreen;
});

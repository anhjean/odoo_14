odoo.define("ws_dynamic_add_cart.dynamic_add_cart", function (require) {
  "use strict";
  var ajax = require("web.ajax");
  var wSaleUtils = require("website_sale.utils");
  var publicWidget = require("web.public.widget");

  publicWidget.registry.DynamicAddCart = publicWidget.Widget.extend({
    selector: 'form[action="/shop/cart/update"]',
    events: {
      "click .o_wsale_product_btn": "_onClick",
    },
    init: function () {
      this._super.apply(this, arguments);
    },
    start: function () {
      return this._super.apply(this, arguments);
    },
    _onClick: async function (ev) {
      var self = this;
      ev.preventDefault(); // Prevent redirects
      ev.stopPropagation(); // Prevent Original E-commerce Event
      const add_qty_el = $("input[name='add_qty']", self.$el);
      const product_id_el = $("input[name='product_id']", self.$el);
      await ajax
        .jsonRpc("/shop/cart/update_json", "call", {
          product_id: parseInt(product_id_el.val()),
          add_qty: parseInt(add_qty_el?.val() ?? 1),
        })
        .then(function (data) {
          wSaleUtils.updateCartNavBar(data);
          add_qty_el?.val("1");
          var $navButton = $("header .o_wsale_my_cart").first();
          var animation = wSaleUtils.animateClone(
            $navButton,
            $(".oe_product_image", self.$el),
            25,
            40
          );
        });
    },
  });
});

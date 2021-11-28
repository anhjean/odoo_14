odoo.define("ws_product_popup.dynamic_product_popup", function (require) {
  "use strict";
  var Dialog = require("web.Dialog");
  var publicWidget = require("web.public.widget");
  publicWidget.registry.DynamicProductPopup = publicWidget.Widget.extend({
    selector: ".oe_product",
    events: {
      "click a.d-block.h-100": "_onClick",
    },
    _onClick: async function (ev) {
      var self = this;
      ev.preventDefault();
      await $.get(ev.currentTarget.href).then((data) => {
        let el = $("<div><div/>");
        el.html(data);
        let modalContent = $("#product_detail", el);
        let websitesale = new publicWidget.registry.WebsiteSale(self);
        websitesale.setElement(modalContent);
        let dialog = new Dialog(self, {
          size: "extra-large",
          backdrop: true,
          dialogClass:"p-3",
          $content: modalContent,
          technical: false,
          renderHeader: false,
          renderFooter: false,
        });
        dialog.open();
      });
    },
  });
});

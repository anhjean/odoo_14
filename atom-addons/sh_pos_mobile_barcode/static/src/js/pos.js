odoo.define("sh_pos_mobile_barcode.ProductScreen", function (require) {
    "use strict";
    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useBarcodeReader } = require("point_of_sale.custom_hooks");
    const { useListener } = require("web.custom_hooks");

    const BarcodeProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
            }
            switchPane() {
                if (this.mobile_pane === "left") {
                    $('.qr_barcode').css("display", "block");
                }else{
                    $('.qr_barcode').css("display", "none"); 
                }
                super.switchPane()
            }
        };	

    Registries.Component.extend(ProductScreen, BarcodeProductScreen);

    return BarcodeProductScreen;
});
odoo.define('pos_restaurant.ProductScanButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require("point_of_sale.ProductScreen");
    const { useListener } = require("web.custom_hooks");
    const Chrome = require("point_of_sale.Chrome");
    const codeReader = new ZXing.BrowserMultiFormatReader();
    const { Gui } = require('point_of_sale.Gui');
    
    
    class ProductScanButton extends PosComponent {
        mounted() {
          //  posbus.on('table-set', this, this.render);
        }
        willUnmount() {
           // posbus.on('table-set', this);
        }
        constructor() {
            super(...arguments);
            useListener("click-product-stop-icon", this.onClickStop);
            useListener("click-product-start-icon", this.onClickStart);
        }
        onClickStart() {
        	let selectedDeviceId;
            
            var contents = $(".product-list");

            codeReader.getVideoInputDevices().then(function (result) {
                //THEN METHOD START HERE
                const sourceSelect = document.getElementById("js_id_sh_sale_barcode_mobile_cam_select");

                $("#js_id_sh_sale_barcode_mobile_cam_select option").remove();

                _.each(result, function (item) {
                    const sourceOption = document.createElement("option");
                    sourceOption.text = item.label;
                    sourceOption.value = item.deviceId;
                    sourceSelect.appendChild(sourceOption);
                });
                $("#js_id_sh_sale_barcode_mobile_cam_select").change(function (e) {
                    selectedDeviceId = sourceSelect.value;
                });
            });
            //SHOW VIDEO
            console.log(">>>>>>>>",$("#js_id_sh_sale_barcode_mobile_vid_div"))
            $("#js_id_sh_sale_barcode_mobile_vid_div").show();

            //SHOW STOP/ HIDE START BUTTON
            $("#js_id_sh_sale_barcode_mobile_reset_btn").show();
            $("#js_id_sh_sale_barcode_mobile_start_btn").hide();

            //CALL METHOD
            //CONTINUOUS SCAN OR NOT.SystrayMenu
            if (this.env.pos.config.sh_pos_bm_is_cont_scan) {
                this.decodeContinuously(codeReader, selectedDeviceId);
            } else {
                this.decodeOnce(codeReader, selectedDeviceId);
            }

            $(".camera-list").show();
            $(".product-list").hide();
            $("#js_id_sh_sale_barcode_mobile_reset_btn").css("display", "block");
            $("#js_id_sh_sale_barcode_mobile_start_btn").css("display", "none");
        }
        decodeContinuously(codeReader, selectedDeviceId) {
            var self = this;
            codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, "video", (result, err) => {
                //RESULT
                if (result) {
                    var product = "";
                    if (self.env.pos.config.sh_pos_barcode_mobile_type == "barcode") {
                        product = self.env.pos.db.get_product_by_barcode(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "int_ref") {
                        product = self.env.pos.db.get_product_by_default_code(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "sh_qr_code") {
                        product = self.env.pos.db.get_product_by_qr(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "all") {
                        if (self.env.pos.db.get_product_by_barcode(result.text)) {
                            product = self.env.pos.db.get_product_by_barcode(result.text);
                        } else if (self.env.pos.db.get_product_by_default_code(result.text)) {
                            product = self.env.pos.db.get_product_by_default_code(result.text);
                        } else if (self.env.pos.db.get_product_by_qr(result.text)) {
                            product = self.env.pos.db.get_product_by_qr(result.text);
                        }
                    }
                    if (product) {
                        self.env.pos.get_order().add_product(product);
                        if (self.env.pos.config.sh_pos_bm_is_notify_on_success) {
                            $.iaoAlert({ msg: "Product: " + product.display_name + " Added to cart successfully.", type: "notification", mode: "dark", autoHide: true, alertTime: "3000", closeButton: true });
                        }
                        if (self.env.pos.config.sh_pos_bm_is_sound_on_success) {
                            Gui.playSound('bell');
                        }
                    } else {
                        if (self.env.pos.config.sh_pos_bm_is_notify_on_fail) {
                            $.iaoAlert({ msg: "Warning: Scanned Internal Reference/Barcode not exist in any product!", type: "error", autoHide: true, alertTime: "3000", closeButton: true, mode: "dark" });
                        }
                        if (self.env.pos.config.sh_pos_bm_is_sound_on_fail) {
                            Gui.playSound('error');
                        }
                    }

                    $("#js_id_sh_sale_barcode_mobile_vid_div").hide();
                    $("#js_id_sh_sale_barcode_mobile_vid_div").show();
                }

                if (err) {
                    console.log("ERROR", err);
                    if (err instanceof ZXing.NotFoundException) {
                        console.log("No QR code found.");
                    }
                    if (err instanceof ZXing.ChecksumException) {
                        console.log("A code was found, but it's read value was not valid.");
                    }

                    if (err instanceof ZXing.FormatException) {
                        console.log("A code was found, but it was in a invalid format.");
                    }
                }
            });
        }
        decodeOnce(codeReader, selectedDeviceId) {
            var self = this;
            codeReader.decodeFromInputVideoDevice(selectedDeviceId, "video").then((result) => {
                //RESULT
                var product = "";
                if (self.env.pos.config.sh_pos_barcode_mobile_type == "barcode") {
                    product = self.env.pos.db.get_product_by_barcode(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "int_ref") {
                    product = self.env.pos.db.get_product_by_default_code(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "sh_qr_code") {
                    product = self.env.pos.db.get_product_by_qr(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "all") {
                    if (self.env.pos.db.get_product_by_barcode(result.text)) {
                        product = self.env.pos.db.get_product_by_barcode(result.text);
                    } else if (self.env.pos.db.get_product_by_default_code(result.text)) {
                        product = self.env.pos.db.get_product_by_default_code(result.text);
                    } else if (self.env.pos.db.get_product_by_qr(result.text)) {
                        product = self.env.pos.db.get_product_by_qr(result.text);
                    }
                }
                if (product) {
                    self.env.pos.get_order().add_product(product);
                    if (self.env.pos.config.sh_pos_bm_is_notify_on_success) {
                        $.iaoAlert({ msg: "Product: " + product.display_name + " Added to cart successfully.", type: "notification", mode: "dark", autoHide: true, alertTime: "3000", closeButton: true });
                    }
                    if (self.env.pos.config.sh_pos_bm_is_sound_on_success) {
                    	Gui.playSound('bell');
                    }
                } else {
                    if (self.env.pos.config.sh_pos_bm_is_notify_on_fail) {
                        $.iaoAlert({ msg: "Warning: Scanned Internal Reference/Barcode not exist in any product!", type: "error", autoHide: true, alertTime: "3000", closeButton: true, mode: "dark" });
                    }
                    if (self.env.pos.config.sh_pos_bm_is_sound_on_fail) {
                        Gui.playSound('error');
                    }
                }
                //RESET READER
                codeReader.reset();

                //HIDE VIDEO
                $("#js_id_sh_sale_barcode_mobile_vid_div").hide();

                //HIDE STOP/ SHOW START BUTTON
                $("#js_id_sh_sale_barcode_mobile_reset_btn").hide();
                $("#js_id_sh_sale_barcode_mobile_start_btn").show();

                // HIDE CAMERA AND OPEN PRODUCTS
                $(".camera-list").hide();
                $(".product-list").show();
                $(".category-list").show();
            });
        }
        onClickStop() {
            //RESET READER
            codeReader.reset();
            //HIDE VIDEO
            $("#js_id_sh_sale_barcode_mobile_vid_div").hide();

            $(".camera-list").hide();
            $(".product-list").show();
            $("#js_id_sh_sale_barcode_mobile_reset_btn").css("display", "none");
            $("#js_id_sh_sale_barcode_mobile_start_btn").css("display", "block");
        }
    }
    ProductScanButton.template = 'ProductScanButton';

    Registries.Component.add(ProductScanButton);

    return ProductScanButton;
});
odoo.define("pos_restaurant.QRScreenButton", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const ProductScreen = require("point_of_sale.ProductScreen");
    const { useListener } = require("web.custom_hooks");
    const Registries = require("point_of_sale.Registries");
    const Chrome = require("point_of_sale.Chrome");
    const codeReader = new ZXing.BrowserMultiFormatReader();
    const { Gui } = require('point_of_sale.Gui');

    class QRScreenButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener("click-product-stop-icon", this.onClickStop);
            useListener("click-product-start-icon", this.onClickStart);
        }
        onClickStart() {
            let selectedDeviceId;
           
            var contents = $(".product-list");

            codeReader.getVideoInputDevices().then(function (result) {
                //THEN METHOD START HERE
                const sourceSelect = document.getElementById("js_id_sh_sale_barcode_mobile_cam_select");

                $("#js_id_sh_sale_barcode_mobile_cam_select option").remove();

                _.each(result, function (item) {
                    const sourceOption = document.createElement("option");
                    sourceOption.text = item.label;
                    sourceOption.value = item.deviceId;
                    sourceSelect.appendChild(sourceOption);
                });
                $("#js_id_sh_sale_barcode_mobile_cam_select").change(function (e) {
                    selectedDeviceId = sourceSelect.value;
                });
            });
            //SHOW VIDEO
            console.log(">>>>>>>>",$("#js_id_sh_sale_barcode_mobile_vid_div"))
            $("#js_id_sh_sale_barcode_mobile_vid_div").show();

            //SHOW STOP/ HIDE START BUTTON
            $("#js_id_sh_sale_barcode_mobile_reset_btn").show();
            $("#js_id_sh_sale_barcode_mobile_start_btn").hide();

            //CALL METHOD
            //CONTINUOUS SCAN OR NOT.SystrayMenu
            if (this.env.pos.config.sh_pos_bm_is_cont_scan) {
                this.decodeContinuously(codeReader, selectedDeviceId);
            } else {
                this.decodeOnce(codeReader, selectedDeviceId);
            }

            $(".camera-list").show();
            $(".product-list").hide();
            $("#js_id_sh_sale_barcode_mobile_reset_btn").css("display", "block");
            $("#js_id_sh_sale_barcode_mobile_start_btn").css("display", "none");
        }
        decodeContinuously(codeReader, selectedDeviceId) {
            var self = this;
            codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, "video", (result, err) => {
                //RESULT
                if (result) {
                    var product = "";
                    if (self.env.pos.config.sh_pos_barcode_mobile_type == "barcode") {
                        product = self.env.pos.db.get_product_by_barcode(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "int_ref") {
                        product = self.env.pos.db.get_product_by_default_code(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "sh_qr_code") {
                        product = self.env.pos.db.get_product_by_qr(result.text);
                    } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "all") {
                        if (self.env.pos.db.get_product_by_barcode(result.text)) {
                            product = self.env.pos.db.get_product_by_barcode(result.text);
                        } else if (self.env.pos.db.get_product_by_default_code(result.text)) {
                            product = self.env.pos.db.get_product_by_default_code(result.text);
                        } else if (self.env.pos.db.get_product_by_qr(result.text)) {
                            product = self.env.pos.db.get_product_by_qr(result.text);
                        }
                    }
                    if (product) {
                        self.env.pos.get_order().add_product(product);
                        if (self.env.pos.config.sh_pos_bm_is_notify_on_success) {
                            $.iaoAlert({ msg: "Product: " + product.display_name + " Added to cart successfully.", type: "notification", mode: "dark", autoHide: true, alertTime: "3000", closeButton: true });
                        }
                        if (self.env.pos.config.sh_pos_bm_is_sound_on_success) {
                            Gui.playSound('bell');
                        }
                    } else {
                        if (self.env.pos.config.sh_pos_bm_is_notify_on_fail) {
                            $.iaoAlert({ msg: "Warning: Scanned Internal Reference/Barcode not exist in any product!", type: "error", autoHide: true, alertTime: "3000", closeButton: true, mode: "dark" });
                        }
                        if (self.env.pos.config.sh_pos_bm_is_sound_on_fail) {
                            Gui.playSound('error');
                        }
                    }

                    $("#js_id_sh_sale_barcode_mobile_vid_div").hide();
                    $("#js_id_sh_sale_barcode_mobile_vid_div").show();
                }

                if (err) {
                    console.log("ERROR", err);
                    if (err instanceof ZXing.NotFoundException) {
                        console.log("No QR code found.");
                    }
                    if (err instanceof ZXing.ChecksumException) {
                        console.log("A code was found, but it's read value was not valid.");
                    }

                    if (err instanceof ZXing.FormatException) {
                        console.log("A code was found, but it was in a invalid format.");
                    }
                }
            });
        }
        decodeOnce(codeReader, selectedDeviceId) {
            var self = this;
            codeReader.decodeFromInputVideoDevice(selectedDeviceId, "video").then((result) => {
                //RESULT
                var product = "";
                if (self.env.pos.config.sh_pos_barcode_mobile_type == "barcode") {
                    product = self.env.pos.db.get_product_by_barcode(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "int_ref") {
                    product = self.env.pos.db.get_product_by_default_code(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "sh_qr_code") {
                    product = self.env.pos.db.get_product_by_qr(result.text);
                } else if (self.env.pos.config.sh_pos_barcode_mobile_type == "all") {
                    if (self.env.pos.db.get_product_by_barcode(result.text)) {
                        product = self.env.pos.db.get_product_by_barcode(result.text);
                    } else if (self.env.pos.db.get_product_by_default_code(result.text)) {
                        product = self.env.pos.db.get_product_by_default_code(result.text);
                    } else if (self.env.pos.db.get_product_by_qr(result.text)) {
                        product = self.env.pos.db.get_product_by_qr(result.text);
                    }
                }
                if (product) {
                    self.env.pos.get_order().add_product(product);
                    if (self.env.pos.config.sh_pos_bm_is_notify_on_success) {
                        $.iaoAlert({ msg: "Product: " + product.display_name + " Added to cart successfully.", type: "notification", mode: "dark", autoHide: true, alertTime: "3000", closeButton: true });
                    }
                    if (self.env.pos.config.sh_pos_bm_is_sound_on_success) {
                    	Gui.playSound('bell');
                    }
                } else {
                    if (self.env.pos.config.sh_pos_bm_is_notify_on_fail) {
                        $.iaoAlert({ msg: "Warning: Scanned Internal Reference/Barcode not exist in any product!", type: "error", autoHide: true, alertTime: "3000", closeButton: true, mode: "dark" });
                    }
                    if (self.env.pos.config.sh_pos_bm_is_sound_on_fail) {
                        Gui.playSound('error');
                    }
                }
                //RESET READER
                codeReader.reset();

                //HIDE VIDEO
                $("#js_id_sh_sale_barcode_mobile_vid_div").hide();

                //HIDE STOP/ SHOW START BUTTON
                $("#js_id_sh_sale_barcode_mobile_reset_btn").hide();
                $("#js_id_sh_sale_barcode_mobile_start_btn").show();

                // HIDE CAMERA AND OPEN PRODUCTS
                $(".camera-list").hide();
                $(".product-list").show();
                $(".category-list").show();
            });
        }
        onClickStop() {
            //RESET READER
            codeReader.reset();
            //HIDE VIDEO
            $("#js_id_sh_sale_barcode_mobile_vid_div").hide();

            $(".camera-list").hide();
            $(".product-list").show();
            $("#js_id_sh_sale_barcode_mobile_reset_btn").css("display", "none");
            $("#js_id_sh_sale_barcode_mobile_start_btn").css("display", "block");
        }
    }
    QRScreenButton.template = "QRScreenButton";

    ProductScreen.addControlButton({
        component: QRScreenButton,
        condition: function () {
            return !this.env.isMobile;
        },
    });

    Registries.Component.add(QRScreenButton);

    return QRScreenButton;
});

odoo.define("sh_pos_mobile_barcode.qr_scan", function (require) {
    "use strict";

    var core = require("web.core");
    var models = require("point_of_sale.models");
    var DB = require("point_of_sale.DB");

    var _t = core._t;
    var QWeb = core.qweb;
    var counter = 0;

    models.load_fields("product.product", ["sh_qr_code"]);
    models.load_fields("product.template", ["sh_qr_code"]);
    models.load_fields("pos.config", ["sh_pos_barcode_mobile_type", "sh_pos_bm_is_cont_scan", "sh_pos_bm_is_notify_on_success", "sh_pos_bm_is_notify_on_fail", "sh_pos_bm_is_sound_on_success", "sh_pos_bm_is_sound_on_fail"]);

    DB.include({
        init: function (options) {
            this._super.apply(this, arguments);
            this.product_by_default_code = {};
            this.product_by_qr = {};
        },
        add_products: function (products) {
            var self = this;
            this._super(products);
            var defined_product = false;
            for (var i = 0, len = products.length; i < len; i++) {
                var product = products[i];
                if (product.default_code) {
                    this.product_by_default_code[product.default_code] = product;
                }
                if (product.sh_qr_code) {
                    this.product_by_qr[product.sh_qr_code] = product;
                }
            }
        },
        get_product_by_default_code: function (default_code) {
            if (this.product_by_default_code[default_code]) {
                return this.product_by_default_code[default_code];
            } else {
                return undefined;
            }
        },
        get_product_by_qr: function (sh_qr_code) {
            if (this.product_by_qr[sh_qr_code]) {
                return this.product_by_qr[sh_qr_code];
            } else {
                return undefined;
            }
        },
    });
});

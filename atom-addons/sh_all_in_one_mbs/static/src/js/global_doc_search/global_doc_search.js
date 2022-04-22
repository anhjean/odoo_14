odoo.define('sh_all_in_one_mbs.global_doc_search', function (require) {
    "use strict";

    var core = require('web.core');
    var Widget = require('web.Widget');
    var SystrayMenu = require('web.SystrayMenu');
    var rpc = require('web.rpc')

    var _t = core._t;
    var QWeb = core.qweb


    
    let selectedDeviceId;
    
    var ShBarcodeScannerAdvSearchDocument = Widget.extend({
        template:'sh_all_in_one_mbs.global_doc_search',
        events: {
            'change input.js_cls_sh_barcode_scanner_adv_document_barcode': '_onChangeBarcode',   
            'change .js_cls_sh_barcode_scanner_adv_document_select': '_onChangeDocumentSelect',            
            'show.bs.dropdown': '_onShowDropdown',    
            'hide.bs.dropdown': '_onHideDropdown',            
            'click #js_id_sh_global_doc_search_mb_start_btn': '_onClickStartBtn',  
      	  	'click #js_id_sh_global_doc_search_mb_reset_btn': '_onClickShAttendanceBmResetBtn',            
            'change #js_id_sh_global_doc_search_mb_cam_select': '_onChangeCameraSelection',    
        },
	    jsLibs: [
	        '/sh_all_in_one_mbs/static/src/js/ZXing.js',
	    ],
        start: function () {
            var self = this;
            // ---------------------------
            // zxing barcode reader
            this.codeReader = new ZXing.BrowserMultiFormatReader();
            this.codeReader.getVideoInputDevices().then(function (result) {
              // Find camera Selection
          	  var $camSelect = self.$el.find("#js_id_sh_global_doc_search_mb_cam_select");
          	  if ($camSelect.length > 0) {
          		  //Add list of cameras as a options in selection.
                    _.each(result, function (item) {
                        var optionText = item.label;
                        var optionValue = item.deviceId;
                        $camSelect.append(new Option(optionText, optionValue));
                    });  
                    
                    //self.selectedDeviceId = $camSelect.val();
                    
          	  }
            	  //Trigger Start Click Button Here
                //$(".js_cls_sh_attendance_barcode_mobile_start_btn").trigger("click");
            });             
            
            // zxing barcode reader
            // ------------------------------
            var def = this._rpc({
                    model: 'sh_barcode_scanner_adv.search.document',
                    method: 'has_global_search_enabled',
                    args: [],
                })
                .then(function (result){
                	self.$el.find('.js_cls_sh_barcode_scanner_adv_document_select').html(result.options);
                	if (result.has_global_search_enabled){
                  		self.$el.removeClass('d-none');
                  	}else{
                  		self.$el.addClass('d-none');
                  	}
                });

            return Promise.all([def, this._super.apply(this, arguments)]);
        },
        
        /**
         * ****************************************
         * Decode Scanned Barcode Method
         * ****************************************
         */
         decodeOnce:function(codeReader, selectedDeviceId) {
        	 var self = this;
        	 this.codeReader
                .decodeFromInputVideoDevice(selectedDeviceId, "js_id_sh_global_doc_search_mb_video")
                .then((result) => {
                    // onchage barcode field
                	self.$el.find(".js_cls_sh_barcode_scanner_adv_document_barcode").val(result.text);
                	self.$el.find(".js_cls_sh_barcode_scanner_adv_document_barcode").change();
                	self.$el.find("#js_id_sh_global_doc_search_mb_reset_btn").click();
                	
                })
                .catch((err) => {
                    console.error(err);
                });
        },

        
        /**
         * ****************************************
         * Reset Camera Button
         * ****************************************
         */
        
        _onClickShAttendanceBmResetBtn: function (ev) {
        	var self = this;
          //RESET READER
          this.codeReader.reset();

          //HIDE VIDEO
          self.$el.find("#js_id_sh_global_doc_search_mb_vid_div").hide();

          //HIDE STOP BUTTON
          self.$el.find("#js_id_sh_global_doc_search_mb_reset_btn").hide();      	
           
        },        
        /**
         * ****************************************
         * Reset Camera Button
         * ****************************************
         */
        
        /**
         * ****************************************
         * Start Button
         * ****************************************
         */        
        _onClickStartBtn: function (ev) {
          	var self = this;
            //SHOW VIDEO
          	self.$el.find("#js_id_sh_global_doc_search_mb_vid_div").show();

            //SHOW STOP BUTTON
          	self.$el.find("#js_id_sh_global_doc_search_mb_reset_btn").show();

            this.decodeOnce(this.codeReader,selectedDeviceId);        	
        },
        /**
         * ****************************************
         * Start Button
         * ****************************************
         */           
        /**
         * ****************************************
         * Change Camera Selection
         * ****************************************
         */      
        _onChangeCameraSelection: function (ev) {
      	  var self = this;
          selectedDeviceId = $(ev.currentTarget).val();    	
          self.$el.find("#js_id_sh_global_doc_search_mb_reset_btn").click();
          self.$el.find("#js_id_sh_global_doc_search_mb_start_btn").click();      	  
        },
        /**
         * ****************************************
         * Change Camera Selection
         * ****************************************
         */   
        
        
     
        
        _onHideDropdown: function (ev) {
            if (ev.clickEvent) {
                ev.preventDefault();
              }
        },
        
        
        _onShowDropdown: function (ev) {        	
        	var barcodeInput = $(ev.target).closest('.o_mail_systray_item').find(".js_cls_sh_barcode_scanner_adv_document_barcode");        	
        	barcodeInput.val('');
        	
        	setTimeout(function(){ 
        	//var barcodeInput = $(ev.target).closest('.o_mail_systray_item').find(".js_cls_sh_barcode_scanner_adv_document_barcode");        	
        	//barcodeInput.val('');
        	barcodeInput.focus();
        	}, 300);
        },
        
        
	    /**
         * OnChange Document Select
         *
         * @private
         * @param {MouseEvent} ev
         */
        _onChangeDocumentSelect: function (ev) {
        	//ev.stopPropagation();
       	//var dropdown = $(ev.target).closest('.o_mail_systray_item').find(".js_cls_document_search_dropdown");  
       	//dropdown.dropdown("show");

       	//dropdown.dropdown('show');
       		//dropdown.addClass("show");
        	//dropdown.toggleClass('show');

        	//var searchbutton = $(ev.target).closest('.o_mail_systray_item').find('.js_cls_document_search_dropdown'); 
        	//searchbutton.dropdown('show');
        	//searchbutton.addClass("show");
        	
        },        
	    /**
         * Highlight selected color
         *
         * @private
         * @param {MouseEvent} ev
         */
        _onChangeBarcode: function (ev) {
            var self = this;
        	var barcode = $(ev.target).val().trim();
        	var doc_type = $(ev.target).closest('.js_cls_form_group_wrapper').find(".js_cls_sh_barcode_scanner_adv_document_select option:selected").val();

        	if(barcode != ''){
                rpc.query({
                    model: 'sh_barcode_scanner_adv.search.document',
                    method: 'search_document',
                    args: [barcode,doc_type]
                    }).then(function(result){
                    	if (result.action){
                    		// to hide dropdown when found document
                    		$(ev.target).closest('.o_mail_systray_item').find(".js_cls_document_search_btn").click();
                    		self.do_action(result.action);	
                    	}
                    	else{
                    		alert("Document not found for the barcode: " + barcode);
                    		$(ev.target).val('');
                    		$(ev.target).focus();
                    		
                    	}
                    	 
                    });            	
            	
            	
            }
        },

    });

    SystrayMenu.Items.push(ShBarcodeScannerAdvSearchDocument);

    return {
    	ShBarcodeScannerAdvSearchDocument: ShBarcodeScannerAdvSearchDocument,
    };
});

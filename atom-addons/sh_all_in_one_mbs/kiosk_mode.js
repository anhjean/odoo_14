odoo.define("sh_attendance_barcode_mobile.kiosk_mode", function (require) {
    "use strict";

    var AbstractAction = require("web.AbstractAction");
    var ajax = require("web.ajax");
    var core = require("web.core");
    var Session = require("web.session");
    var QWeb = core.qweb;
    var KioskMode = require("hr_attendance.kiosk_mode");
    
    let selectedDeviceId;
    const codeReader = new ZXing.BrowserMultiFormatReader();
    
    
    
    
    KioskMode.include({
    	
      events: _.extend({}, KioskMode.prototype.events, {
    	  'click .js_cls_sh_attendance_barcode_mobile_start_btn': '_onClickShAttendanceBmStartBtn',
    	  'click .js_cls_sh_attendance_barcode_mobile_reset_btn': '_onClickShAttendanceBmResetBtn',    	  
    	  'change .js_cls_sh_attendance_barcode_mobile_cam_select': '_onChangeCameraSelection',
      }),        
	  
      /**
       * Overwrite Start Method
       * In order to put softhealer custom logic.
       * call shUpdateCameraControl() custom method
       */
      start: function () { 	  
          var self = this;
          //core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
          self.session = Session;
          var def = this._rpc({
                  model: 'res.company',
                  method: 'search_read',
                  args: [[['id', '=', this.session.company_id]], ['name']],
              })
              .then(function (companies){
                  self.company_name = companies[0].name;
                  self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
                  self.$el.html(QWeb.render("HrAttendanceKioskMode", {widget: self}));

                  //Softhealer Update Camera Control
                  // self.shUpdateCameraControl();
                  
                  window.setTimeout(function(){
            		  self.shUpdateCameraControl();
                   }, 1000);                  
              
                  self.start_clock();
              });
          // Make a RPC call every day to keep the session alive
          self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
          return Promise.all([def, this._super.apply(this, arguments)]);
      },
    	  
      
      /**
       * Add list of cameras as a options in selection.
       * 
       */
      shUpdateCameraControl: function () {
          var self = this;
          codeReader
          .getVideoInputDevices()
          .then(function (result) {
              // Find camera Selection
        	  var $camSelect = $(document).find(".js_cls_sh_attendance_barcode_mobile_cam_select");
        	  /*
        	  if ($camSelect.length <= 0) {
        		  location.reload();
        	  }
        	  */
        	  if ($camSelect.length > 0) {
        		  //Add list of cameras as a options in selection.
                  _.each(result, function (item) {
                	  selectedDeviceId = item.deviceId;
                      var optionText = item.label;
                      var optionValue = item.deviceId;
                      $camSelect.append(new Option(optionText, optionValue));
                  });  
                  
                  // Make selected camera selected from local storage.
                  var selected_cam = localStorage.getItem('sh_attendance_barcode_mobile_selected_device_id') || false;
                  if (selected_cam && $camSelect.find('option[value='+ selected_cam +']').length ) {
                	  var cam_option = $camSelect.find('option[value='+ selected_cam +']');

                	  if (cam_option){
                		  cam_option.attr('selected', true);
                	  }
                  }

                  // TODO: local storage camera assign to selectedDeviceId

                  
                  
        	  }
          	  //Trigger Start Click Button Here
              $(".js_cls_sh_attendance_barcode_mobile_start_btn").trigger("click");
          }); 
      },      
      
      
      /**
       * ****************************************
       * Change Camera Selection
       * ****************************************
       */      
      _onChangeCameraSelection: function (ev) {
    	  selectedDeviceId = $(ev.currentTarget).val();   
    	  // Save Selected Camera in Session and load that camera in next scan.
    	  localStorage.setItem('sh_attendance_barcode_mobile_selected_device_id', selectedDeviceId );      
    	  
    	  $(document).find(".js_cls_sh_attendance_barcode_mobile_start_btn").trigger("click");

          
      },

      
      /**
       * ****************************************
       * Reset Camera Button
       * ****************************************
       */
      
      _onClickShAttendanceBmResetBtn: function (ev) {
      	var self = this;
        //RESET READER
        codeReader.reset();

        //HIDE VIDEO
        $(".js_cls_sh_attendance_barcode_mobile_vid_div").hide();

        //HIDE STOP BUTTON
        $(".js_cls_sh_attendance_barcode_mobile_reset_btn").hide();      	
         
      },
      
      
      /**
       * ****************************************
       * Start Camera Button
       * ****************************************
       */
      
      _onClickShAttendanceBmStartBtn: function (ev) {
      	var self = this;
        //SHOW VIDEO
        $(".js_cls_sh_attendance_barcode_mobile_vid_div").show();

        //SHOW STOP BUTTON
        $(".js_cls_sh_attendance_barcode_mobile_reset_btn").show();

        this.decodeOnce(codeReader, selectedDeviceId);
         
      },
    	
      /**
       * ****************************************
       * Decode Scanned Barcode Method
       * ****************************************
       */
       decodeOnce:function(codeReader, selectedDeviceId) {
           var selected_cam = localStorage.getItem('sh_attendance_barcode_mobile_selected_device_id') || selectedDeviceId;
           
          codeReader
              .decodeFromInputVideoDevice(selected_cam, "js_id_sh_attendance_bm_video")
              .then((result) => {
                  core.bus.trigger("barcode_scanned", result.text);
              })
              .catch((err) => {
                  console.error(err);
              });
      },

      /**
       * ****************************************
       * Overwrite
       * _onBarcodeScanned method
       * In order to put softhealer custom logic.
       * ****************************************
       */      
      _onBarcodeScanned: function(barcode) {
          var self = this;
          
          core.bus.off('barcode_scanned', this, this._onBarcodeScanned);
          this._rpc({
                  model: 'hr.employee',
                  method: 'attendance_scan',
                  args: [barcode, ],
              })
              .then(function (result) {
                  if (result.action) {
                      self.do_action(result.action);
                      
            			// softhealer custom code
                      	// play success sound
            			var src = "/sh_attendance_barcode_mobile/static/src/sounds/picked.wav";
            	        $('body').append('<audio src="'+src+'" autoplay="true"></audio>');	 
            	        // softhealer custom code
                      
                  } else if (result.warning) {
                	  
                    	// softhealer custom code
                    
                	  window.setTimeout(function(){
                    		if ( $("#js_id_sh_attendance_bm_video").length ){
                            	//Trigger Start Click Button Here
                                $(".js_cls_sh_attendance_barcode_mobile_start_btn").trigger("click");  	
                            }
                         }, 2000);
                    	
                    	//play failed sound
            			var src = "/sh_attendance_barcode_mobile/static/src/sounds/error.wav";
            	        $('body').append('<audio src="'+src+'" autoplay="true"></audio>');	    
            	        // softhealer custom code
            	                        	
                      self.do_warn(result.warning);
                      core.bus.on('barcode_scanned', self, self._onBarcodeScanned);
                  }
              }, function () {
                  core.bus.on('barcode_scanned', self, self._onBarcodeScanned);
              });
      },
      


    });
    
});

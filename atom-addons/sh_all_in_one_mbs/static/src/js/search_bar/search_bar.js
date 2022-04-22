odoo.define('sh_all_in_one_mbs/static/src/js/search_bar/search_bar.js', function (require) {
'use strict';

const components = {
		search_bar:  require('web.SearchBar'),
};

const { patch } = require('web.utils');
var core = require('web.core');
var Dialog = require('web.Dialog');
var _t = core._t;
var qweb = core.qweb;

patch(components.search_bar, 'sh_all_in_one_mbs/static/src/js/search_bar/search_bar.js', {
    jsLibs: [
        '/sh_all_in_one_mbs/static/src/js/ZXing.js',
    ],
    
    	
	//--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
      /**
       * Add list of cameras as a options in selection.
       * 
       */
      _shUpdateCameraControl: function () {
          var self = this;
          self.selectedDeviceId = null;
          self.codeReader
          .getVideoInputDevices()
          .then(function (result) {
              // Find camera Selection
        	  var $camSelect = self.dialog_scanner.$el.find("#js_id_sh_search_bar_barcode_mobile_cam_select");
        	  var flag = true;
        	  //alert("\n\n 1 $camSelect ==>" + self.dialog_scanner.$el.html() );
        	  if ($camSelect.length > 0) {
        		  //Add list of cameras as a options in selection.
                  _.each(result, function (item) {
                      var optionText = item.label;
                      var optionValue = item.deviceId;
                      if (flag){
                    	  flag = false;
                    	  self.selectedDeviceId = item.deviceId;
                      }
                      $camSelect.append(new Option(optionText, optionValue));
                  });  
                  
                  // Make selected camera selected from local storage.
                  var selected_cam = localStorage.getItem('sh_searchbar_barcode_mobile_selected_device_id') || false;
                  if (selected_cam && $camSelect.find('option[value='+ selected_cam +']').length ) {
                	  var cam_option = $camSelect.find('option[value='+ selected_cam +']');

                	  if (cam_option){
                		  cam_option.attr('selected', true);
                	  }
                  }

                  
                  
                  
                  
        	  }
        	  
        	  // Call decodeOnce method.
              self.decodeOnce();
              
          }); 
      },      
      
      

      
      /**
       * ****************************************
       * Decode Scanned Barcode Method
       * ****************************************
       */
       decodeOnce:function() {
           var self = this;    	   
    	   var selected_cam = localStorage.getItem('sh_searchbar_barcode_mobile_selected_device_id') || self.selectedDeviceId;

          self.codeReader
              .decodeFromInputVideoDevice(selected_cam, "js_id_dialog_search_bar_video")
              .then((result) => {
                  //core.bus.trigger("barcode_scanned", result.text);
           	
           	// select first search facets 	  
            self.state.inputValue = result.text;
            const wasVisible = self.state.sources.length;
            const query = self.state.inputValue.trim().toLowerCase();
            if (query.length) {
                self.state.sources = self._filterSources(query);
            } else if (wasVisible) {
                self._closeAutoComplete();
            }
            
            // select first autocomplete result or not things.
            var auto_select_first = localStorage.getItem('dialog_search_bar_search_autocomplete_setting') || "true";
            if (auto_select_first == "true") {                
                setTimeout(function(){ 
                	self.el.querySelector(".o_searchview_autocomplete li a").click();
                }, 400);
            }
            
           	// close the scanner dialog
           	self.dialog_scanner.close();

              })
              .catch((err) => {
                  console.error(err);
              });
      },
      
      
      
      


    /**
     * @private
     * @param {InputEvent} ev
     */
    _onclickBarcodeScanButton(ev) {
    	var self = this;
    	ev.stopPropagation();
        ev.preventDefault();    
        
        // --------------------------------------
        // Scan Dialog	
        self.dialog_scanner = new Dialog(null, {
            title: _t("Scan Barcode/QR Code"),
            size: 'large',
            $content:$(qweb.render('sh_all_in_one_mbs.dialog.search_bar')),            
        });        
        
            self.dialog_scanner.open().opened(function () {            	
            	//self.selectedDeviceId = null;
   				self.codeReader = new ZXing.BrowserMultiFormatReader();            	
            	self._shUpdateCameraControl();
                       	
            	// get setting checkbox values.
                var auto_select_first = localStorage.getItem('dialog_search_bar_search_autocomplete_setting') || "true";
                if (auto_select_first == "true") {    
                	// tick checkbox
                	self.dialog_scanner.$el.find('input[name="search_autocomplete_setting"]').prop( "checked", true );
                }else{
                	// untick checkbox
                	self.dialog_scanner.$el.find('input[name="search_autocomplete_setting"]').prop( "checked", false );
                }
                
            	// set setting checkbox values.
            	self.dialog_scanner.$el.on('change', '#sh_search_autocomplete_setting', function (ev) {                	
                	localStorage.setItem('dialog_search_bar_search_autocomplete_setting', $(ev.currentTarget).is(":checked") );
               	
                });
                
            	
            	// On change camera
            	self.dialog_scanner.$el.on('change', '#js_id_sh_search_bar_barcode_mobile_cam_select', function (ev) {                	
            		self.selectedDeviceId = $(ev.currentTarget).val(); 
            	    //RESET READER
//               	  self.selectedDeviceId = $(ev.currentTarget).val();    
            		localStorage.setItem('sh_searchbar_barcode_mobile_selected_device_id', $(ev.currentTarget).val() ); 
            		location.reload()
    	  
            	//	self.codeReader.reset();
               	
              	    // Call decodeOnce method.
                 //   self.decodeOnce();
            		
            		
                });
            	
     	
            	
            	
            });
        
                    
    	
        // --------------------------------------
        // Scan Dialog
            	
    	
    },
    
	
	// component ends here
});

});
//
//

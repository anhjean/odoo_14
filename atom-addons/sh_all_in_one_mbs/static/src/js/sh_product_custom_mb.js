$(document).ready(function () {
    
    let selectedDeviceId;
    let field_name='barcode';
    
	function decodeOnce(codeReader, selectedDeviceId) {
        codeReader
            .decodeFromInputVideoDevice(selectedDeviceId, "video")
            .then((result) => {
                console.log(result);
                $('input[name="' + field_name + '"]').val(result.text);
                $('input[name="' + field_name + '"]').change();
                //RESET READER
                codeReader.reset();

                //HIDE VIDEO
                $("#js_id_sh_product_custom_mb_vid_div").hide();

                //HIDE STOP BUTTON
                $("#js_id_sh_product_custom_mb_reset_btn").hide();

                //RESULT
                document.getElementById("js_id_sh_product_custom_mb_result").textContent = result.text;
            })
            .catch((err) => {
                console.error(err);
            });
    }

    function decodeContinuously(codeReader, selectedDeviceId) {
        codeReader.decodeFromInputVideoDeviceContinuously(selectedDeviceId, "video", (result, err) => {
            if (result) {
                // properly decoded qr code
                console.log("Found QR code!", result);
                $('input[name="barcode"]').val(result.text);
                $('input[name="barcode"]').change();

                //RESULT
                document.getElementById("js_id_sh_product_custom_mb_result").textContent = result.text;
            }

            if (err) {
                // As long as this error belongs into one of the following categories
                // the code reader is going to continue as excepted. Any other error
                // will stop the decoding loop.
                //
                // Excepted Exceptions:
                //
                //  - NotFoundException
                //  - ChecksumException
                //  - FormatException

                if (err instanceof ZXing.NotFoundException) {
                    console.log("No QR code found.");
                    //EMPTY INPUT
                    //$('input[name="barcode"]').val(result.text);
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

    //HIDE STOP BUTTON (SAFETY IN XML WE ALSO DO AND HERE ALSO.)
    $("#js_id_sh_product_custom_mb_reset_btn").hide();



    const codeReader = new ZXing.BrowserMultiFormatReader();
    //const codeReader = new ZXing.BrowserBarcodeReader()

    console.log("ZXing code reader initialized");
    codeReader
        .getVideoInputDevices()
        .then(function (result) {
            //THEN METHOD START HERE
            //const sourceSelect = $("#js_id_sh_product_custom_mb_cam_select");
            const sourceSelect = document.getElementById("js_id_sh_product_custom_mb_cam_select");

            //$('input[name="sh_product_custom_mb"]').val("");
            //$('input[name="sh_product_custom_mb"]').change();

            _.each(result, function (item) {
                //self._add_filter(item.partner_id[0], item.partner_id[1], !active_partner, true);
                const sourceOption = document.createElement("option");
                sourceOption.text = item.label;
                sourceOption.value = item.deviceId;
                sourceSelect.appendChild(sourceOption);
            });

            //CUSTOM EVENT HANDLER START HERE

            /*
             * =============================
             * ONCHANGE SELECT CAMERA
             * =============================
             */        
        	$(document).on('change', '#js_id_sh_product_custom_mb_cam_select', function(ev) {
        		  // Does some stuff and logs the event to the console
        		var cameraSelect = $(ev.currentTarget);
        		selectedDeviceId = cameraSelect.val(); 
        		//RESET READER
                //codeReader.reset();
                // trigger start button click to render video with selected camera.
        		$("#js_id_sh_product_custom_mb_reset_btn").click();
        		$("#js_id_sh_product_custom_mb_start_btn").click();
                
                
        	});  
        	
            
            /*
             * =============================
             * ONCHANGE SELECT Field
             * =============================
             */

            $(document).on("change", "#js_id_sh_product_custom_mb_field_select", function () {
                // Does some stuff and logs the event to the console
                field_name = $(this).val();
                // trigger start button click to render video with selected camera.
        		$("#js_id_sh_product_custom_mb_reset_btn").click();
        		$("#js_id_sh_product_custom_mb_start_btn").click();
            });          
            
            /*
             * ========================
             * WHEN CLICK START BUTTON.
             * ========================
             */
            $(document).on("click", "#js_id_sh_product_custom_mb_start_btn", function (event) {
                //EMPTY INPUT
                //$('input[name="sh_product_custom_mb"]').val("");
                //$('input[name="sh_product_custom_mb"]').change();

                //SHOW VIDEO
                $("#js_id_sh_product_custom_mb_vid_div").show();

                //SHOW STOP BUTTON
                $("#js_id_sh_product_custom_mb_reset_btn").show();
                
                //var field_name = $("#js_id_sh_product_custom_mb_field_select").val();
                
                
                //CALL METHOD
                //CONTINUOUS SCAN OR NOT.
                if ($('span[name="sh_invoice_bm_is_cont_scan"]').text() == "True") {
                    decodeContinuously(codeReader, selectedDeviceId);
                } else {
                    decodeOnce(codeReader, selectedDeviceId);
                }
            });

            /*
             * =============================
             * WHEN CLICK STOP/RESET BUTTON.
             * =============================
             */
            $(document).on("click", "#js_id_sh_product_custom_mb_reset_btn", function () {
                console.log("STOP CAMERA");
                document.getElementById("js_id_sh_product_custom_mb_result").textContent = "";

                //EMPTY VALUE
                //$('input[name="sh_product_custom_mb"]').val("");
                //$('input[name="sh_product_custom_mb"]').change();

                //RESET READER
                codeReader.reset();

                //HIDE VIDEO
                $("#js_id_sh_product_custom_mb_vid_div").hide();

                //HIDE STOP BUTTON
                $("#js_id_sh_product_custom_mb_reset_btn").hide();
            });

            // CUSTOM ENENT HANDLER ENDS HERE

            // THEN METHOD ENDS HERE
        })
        .catch(function (reason) {
            console.log("Error ==>" + reason);
        });
});

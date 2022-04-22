odoo.define('mid', function (require) {
    "use strict";
    $(document).ready(function () {

        function submitForm() {
            $.ajax({
                type: "GET",
                url: '/merchant_contact',
                success: function (data) {
                    console.log(typeof data);
                    console.log('Success! ' + data);
                    $(document).find("#merchant_contacts_test").html(data)

                },
                error: function (data) {
                    console.log(data);
                }

            });

        }

        submitForm();

    });
});
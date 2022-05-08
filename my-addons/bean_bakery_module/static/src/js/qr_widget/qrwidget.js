odoo.define('mypet.bold', function (require) {
    "use strict";
    // import packages
    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');
    
    // widget implementation
    var BoldWidget = basic_fields.CharImageUrl.extend({
        _renderReadonly: function () {
            this._super();
        console.log('elements: ---', this.$el)
            var old_html_render = this.$el.html();
            console.log('Old html element: ----- \n', old_html_render)
            var new_html_render = '<img style="max-height:100px; max-weight:100px" src="' + old_html_render + '"/>'
            this.$el.html( old_html_render) ;
        },
    });
    
    registry.add('qrcode', BoldWidget); // add our "bold" widget to the widget registry
});
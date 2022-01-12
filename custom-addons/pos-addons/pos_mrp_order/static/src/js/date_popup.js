odoo.define('point_of_sale.DateInputPopup', function(require) {
    'use strict';

    const { useState, useRef } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    // Convert current Date() to type 'Date' Input value
    Date.prototype.toDateInputValue = (function() {
        var local = new Date(this);
        local.setMinutes(this.getMinutes() - this.getTimezoneOffset());
        return local.toJSON().slice(0,10);
    });

    // formerly TextInputPopupWidget
    class DateInputPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({ inputValue: this.props.startingValue });
            this.inputRef = useRef('inputdate');
            // this.props.body = this.props.body.replace(/(\r\n|\n|\r)/gm, "<br>");
        }
        mounted() {
            this.inputRef.el.focus();
        }
        getPayload() {
            return this.state.inputValue;
        }

        
        

    }
    DateInputPopup.template = 'DateInputPopup';
    DateInputPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
        title: '',
        body: '',
        startingValue: new Date().toDateInputValue(),
    };

    Registries.Component.add(DateInputPopup);

    return DateInputPopup;
});

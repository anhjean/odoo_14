odoo.define('point_of_sale.DateInputPopup', function(require) {
    'use strict';

    const { useState, useRef } = owl.hooks;
    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');

    // formerly TextInputPopupWidget
    class DateInputPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);
            this.state = useState({ inputValue: this.props.startingValue });
            this.inputRef = useRef('inputdate');
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
        startingValue: Date.now(),
    };

    Registries.Component.add(DateInputPopup);

    return DateInputPopup;
});

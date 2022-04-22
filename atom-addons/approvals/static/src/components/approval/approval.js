odoo.define('approvals/static/src/components/approval/approval.js', function (require) {
'use strict';

const useStore = require('mail/static/src/component_hooks/use_store/use_store.js');

const { Component } = owl;

class Approval extends Component {

    /**
     * @override
     */
    constructor(...args) {
        super(...args);
        useStore(props => {
            const approval = this.env.models['approvals.approval'].get(props.approvalLocalId);
            return {
                approval: approval ? approval.__state : undefined,
            };
        });
    }

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @returns {approvals.approval}
     */
    get approval() {
        return this.env.models['approvals.approval'].get(this.props.approvalLocalId);
    }

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    async _onClickApprove() {
        await this.approval.approve();
        this.trigger('o-approval-approved');
    }

    /**
     * @private
     */
    async _onClickRefuse() {
        await this.approval.refuse();
        this.trigger('o-approval-refused');
    }

}

Object.assign(Approval, {
    props: {
        approvalLocalId: String,
    },
    template: 'approvals.Approval',
});

return Approval;

});

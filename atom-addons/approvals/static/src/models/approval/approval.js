odoo.define('approvals/static/src/models/approval/approval.js', function (require) {
'use strict';

const { registerNewModel } = require('mail/static/src/model/model_core.js');
const { attr, one2one } = require('mail/static/src/model/model_field.js');

function factory(dependencies) {

    class Approval extends dependencies['mail.model'] {

        //----------------------------------------------------------------------
        // Public
        //----------------------------------------------------------------------

        /**
         * Approves the current `approval.approver`.
         */
        async approve() {
            await this.async(() => this.env.services.rpc({
                model: 'approval.approver',
                method: 'action_approve',
                args: [[this.id]],
            }));
            if (this.activity) {
                this.activity.delete();
            }
            this.delete();
        }

        /**
         * Refuses the current `approval.approver`.
         */
        async refuse() {
            await this.async(() => this.env.services.rpc({
                model: 'approval.approver',
                method: 'action_refuse',
                args: [[this.id]],
            }));
            if (this.activity) {
                this.activity.delete();
            }
            this.delete();
        }

        //----------------------------------------------------------------------
        // Private
        //----------------------------------------------------------------------

        /**
         * @override
         */
        static _createRecordLocalId(data) {
            return `${this.modelName}_${data.id}`;
        }

    }

    Approval.fields = {
        activity: one2one('mail.activity', {
            inverse: 'approval',
        }),
        id: attr(),
        isCurrentPartnerApprover: attr({
            default: false,
            related: 'activity.isCurrentPartnerAssignee',
        }),
        status: attr(),
    };

    Approval.modelName = 'approvals.approval';

    return Approval;
}

registerNewModel('approvals.approval', factory);

});

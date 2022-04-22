odoo.define('approvals/static/src/models/activity/activity.js', function (require) {
'use strict';

const {
    registerClassPatchModel,
    registerFieldPatchModel,
} = require('mail/static/src/model/model_core.js');
const { one2one } = require('mail/static/src/model/model_field.js');

registerClassPatchModel('mail.activity', 'approvals/static/src/models/activity/activity.js', {
    //----------------------------------------------------------------------
    // Public
    //----------------------------------------------------------------------

    /**
     * @override
     */
    convertData(data) {
        const data2 = this._super(data);
        if ('approver_id' in data && 'approver_status' in data) {
            if (!data.approver_id) {
                data2.approval = [['unlink-all']];
            } else {
                data2.approval = [
                    ['insert', { id: data.approver_id, status: data.approver_status }],
                ];
            }
        }
        return data2;
    },
});

registerFieldPatchModel('mail.activity', 'approvals/static/src/models/activity/activity.js', {
    approval: one2one('approvals.approval', {
        inverse: 'activity',
    }),
});

});

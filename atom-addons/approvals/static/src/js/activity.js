odoo.define('approvals.Activity', function (require) {
    "use strict";

const field_registry = require('web.field_registry');

require('mail.Activity');

const KanbanActivity = field_registry.get('kanban_activity');

KanbanActivity.include({
    events: Object.assign({}, KanbanActivity.prototype.events, {
        'click .o_activity_action_approve': '_onValidateApproval',
        'click .o_activity_action_refuse': '_onRefuseApproval',
    }),
    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------
    /**
     * @private
     * @param  {Event} event
     */
    _onValidateApproval(event) {
        const approverID = $(event.currentTarget).data('approver-id');
        this._rpc({
            model: 'approval.approver',
            method: 'action_approve',
            args: [[approverID]],
        }).then(result => {
            this.trigger_up('reload', { keepChanges: true });
        });
    },
    /**
     * @private
     * @param  {Event} event
     */
    _onRefuseApproval(event) {
        const approverID = $(event.currentTarget).data('approver-id');
        this._rpc({
            model: 'approval.approver',
            method: 'action_refuse',
            args: [[approverID]],
        }).then(result => {
            this.trigger_up('reload', { keepChanges: true });
        });
    },
});

});

odoo.define('approvals/static/src/components/activity/activity.js', function (require) {
'use strict';

const components = {
    Activity: require('mail/static/src/components/activity/activity.js'),
    Approval: require('approvals/static/src/components/approval/approval.js'),
};

Object.assign(components.Activity.components, {
    Approval: components.Approval,
});

});

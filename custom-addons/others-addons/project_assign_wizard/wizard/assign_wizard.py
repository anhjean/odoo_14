import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class AssignWizard(models.TransientModel):
    _name = 'kw.project.assign.wizard'
    _description = 'Assign wizard '

    assign_stage = fields.Boolean(
        default=True, )
    stage_id = fields.Many2one(
        comodel_name='project.task.type', )
    assign_executor = fields.Boolean(
        default=False, )
    user_id = fields.Many2one(
        comodel_name='res.users', string='Executor',
        domain=[('share', '=', False)], )
    task_ids = fields.Many2many(
        comodel_name='project.task', )
    is_confirm_possible = fields.Boolean(
        default=False, compute='_compute_is_confirm_possible', )
    comment = fields.Text()

    @api.model
    def default_get(self, vals):
        res = super().default_get(vals)
        active_ids = self.env.context.get('active_ids')
        if self.env.context.get('active_model') == 'project.task':
            res['task_ids'] = active_ids
        return res

    @api.depends(
        'assign_stage', 'stage_id', 'assign_executor', 'user_id', 'task_ids')
    def _compute_is_confirm_possible(self):
        for obj in self:
            if not any([obj.assign_stage, obj.assign_executor,
                        self.comment and self.comment.strip()]):
                obj.is_confirm_possible = False
                continue
            if not obj.task_ids:
                obj.is_confirm_possible = False
                continue
            if obj.assign_stage and not obj.stage_id:
                obj.is_confirm_possible = False
                continue
            obj.is_confirm_possible = True

    def confirm_assign(self):
        self.ensure_one()
        data = {}
        if self.assign_stage:
            data['stage_id'] = self.stage_id.id
        if self.assign_executor:
            data['user_id'] = self.user_id.id
        self.task_ids.write(data)

        if self.comment and self.comment.strip():
            author_id = self.env.user.partner_id.id
            email_from = '"{}" <{}>'.format(
                self.env.user.partner_id.name,
                self.env.user.partner_id.email)
            for task in self.task_ids:
                self.env['mail.message'].sudo().create({
                    'model': 'project.task',
                    'res_id': task.id,
                    'message_type': 'comment',
                    'author_id': author_id,
                    'email_from': email_from,
                    'body': self.comment, })

from odoo import fields, models, api


class ResPartnerFee(models.Model):
    _name = 'res.partner.fee'
    _description = 'Fee'

    partner_id = fields.Many2one('res.partner', string="Merchant", readonly=True)
    card_type = fields.Selection(selection=[
        ('VISA', 'VISA'),
        ('MASTERCARD', 'MASTERCARD'),
        ('JCB', 'JCB'),
    ], string='Lọai thẻ')
    bank = fields.Many2one('res.bank')
    fee = fields.Float(string='Mức phí')
    from_date = fields.Datetime(string='Bắt đầu từ')
    active = fields.Boolean(string='Hiệu lực', default=False)
    industry_id = fields.Many2one('res.partner.industry',
                                  string='Ngành hàng',
    )

# selection=[
#         ("970425", "ABBANK"),
#         ("970416", "ACB"),
#         ("970405", "AGRIBANK"),
#         ("970409", "BAB"),
#         ("970488", "BIDV"),
#         ("970418", "BIDV"),
#         ("970438", "BVBANK"),
#         ("970446", "COOPBANK"),
#         ("970406", "DABANK"),
#         ("970431", "EXIMBANK"),
#         ("970408", "GPBANK"),
#         ("970437", "HDBANK"),
#         ("970442", "HLBANK"),
#         ("970434", "IVB"),
#         ("970452", "KLB"),
#         ("970422", "MB"),
#         ("970426", "MSB"),
#         ("970428", "NAMABANK"),
#         ("970419", "NCB"),
#         ("970448", "OCB"),
#         ("970430", "PGBANK"),
#         ("970412", "PVC"),
#         ("970429", "SCB"),
#         ("970440", "SEA"),
#         ("970400", "SGBANK"),
#         ("970424", "SHINHAN"),
#         ("970443", "SHB"),
#         ("970403", "SACOMBANK"),
#         ("970407", "TECHCOMBANK"),
#         ("970423", "TIENPHONGBANK"),
#         ("970458", "UOB"),
#         ("970427", "VAB"),
#         ("970460", "VC"),
#         ("970436", "VIETCOMBANK"),
#         ("970454", "VCCB"),
#         ("970441", "VIB"),
#         ("970432", "VPBANK"),
#         ("970421", "VRB"),
#         ("970415", "VIENTINBANK"),
#         ("970457", "WRB"),
#     ]

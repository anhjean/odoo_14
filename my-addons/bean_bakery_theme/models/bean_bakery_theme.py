from odoo import models


class ThemeBeanBakery(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_beanbakery_post_copy(self, mod):
        # Reset all default color when switching themes
        for nb in range(2, 9):
            self.disable_view('bean_bakery_theme.option_colors_%02d_variables' % nb)
            
        self.disable_view('website.template_header_default')
        self.enable_view('website.template_header_vertical')
        self.enable_view('website.template_header_default_align_right')
        self.enable_view('website.template_header_hamburger_align_right')
        self.enable_header_off_canvas()

        self.disable_view('website.footer_custom')
        self.enable_view('website.template_footer_centered')
        self.enable_view('website.template_footer_slideout')
        self.enable_view('website.option_footer_scrolltop')

        self.enable_view('website.option_ripple_effect')

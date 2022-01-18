from collections import defaultdict
from typing_extensions import Required
from odoo import models,fields

class LibraryBook(models.Model):
    # _name is the important field to define the global name of model
    _name = "library.book"
    # _descriptin is define the friendly name for model
    _description = "Library Book"
    # _order to define the sort order of Model
    _order = 'date_release desc,name'
    # _rec_name to define the record representation, it's will show on the breadcrum
    _rec_name = 'short_name'
    # constant SQL
    _sql_constraints = [
                    ('name_uniq', 'UNIQUE(name)', 'Book title must be unique.'),
                    ('positive_page', 'CHECK(pages>0)', 'No of pages must be positive')]


    name = fields.Char('Title',required=True)
    short_name = fields.Char('Short Title',translate=True,index=True)
    category_id = fields.Many2one('library.book.category')
    date_release = fields.Date('Release Date')
    author_ids = fields.Many2many('res.partner',string='Authors')

    #now add more field
    notes = fields.Text('Internal Note')
    state = fields.Selection([('draft','Not available'),
                            ('available','Available'),
                            ('lost','Lost')],
                            'State', default="draft")
    description = fields.Html('Description', sanitize=True, strip_style=False)
    cover =  fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_updated = fields.Datetime('Last Update')
    pages = fields.Integer('No. of Pages', 
                            groups="base.group_user",
                            states={'lost':[('readonly',True)]},
                            help = 'Total book page count', 
                            company_dependent = False
                            )
    reader_rating = fields.Float('Reader Average Rating',
                                digits=(14,4),#Optional precison decimals)
                                )
    # Pricing
    cost_price = fields.Monetary('Book Cost')
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary('Retail Price',
                            # optional: currency_field='currency_id', 
                            )
    # mapping to res.partner
    publisher_id = fields.Many2one('res.partner', 
                                    string='Publisher'
                                    #optional:
                                    # ondelete='set null',
                                    # context={},
                                    # domain=[],
                                    )


# add more field to res.partner model
class ResPartner(models.Model):
    _inherit = 'res.partner'
        
    published_book_ids = fields.One2many('library.book',
                                'publisher_id',
                                string=" Published Books")
    authored_book_ids = fields.Many2many( 'library.book',
                                string='Authored Books',
                                # optional:
                                # relation='library_book_res_partner_rel' 
                                
                                )

    # name_get() is a special Model function, that change the _rec_name to the result of name_get(self) function
    def name_get(self):
        result = []
        for record in self:
            rec_name = "%s (%s)"% (record.name, record.date_release)
            result.append((record.id,rec_name))
        return result
    

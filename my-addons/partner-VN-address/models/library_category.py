from odoo import models, api, fields
from odoo.exceptions import ValidationError

class BookCategory(models.Model):
    _name = 'library.book.category'
    _description = "Library Book Category"
    _parent_store = True
    _parent_name = 'parent_id' #optional if field is 'parent_id'
    
    

    name = fields.Char('Category')
    parent_id = fields.Many2one('library.book.category',string='Parent Categories',ondelete='restrict',index=True, domain="[('parent_id','!=','id')]")
    children_id = fields.One2many('library.book.category','parent_id',string='Child Categories', domain="[('children_id','!=','id')]")
    parent_path = fields.Char(index=True, readonly=True)
    #Methods
    @api.constrains ('parent_id') # Create constrain for parent_id column
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories')

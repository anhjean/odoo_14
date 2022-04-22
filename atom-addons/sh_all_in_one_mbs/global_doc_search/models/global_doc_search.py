# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, fields, api, _
from odoo.exceptions import Warning,UserError


class SearchDocument(models.Model):
    _name = "sh_barcode_scanner_adv.search.document"
    _description = "Search Document By Barcode"
    
    name = fields.Char(string="name")
    
    @api.model
    def has_global_search_enabled(self):      
        options = '<option value="all">All</option>'
        if self.env.company.sh_global_document_search_is_sale:
            options += '<option value="sale">Sale Order</option>'     
        if self.env.company.sh_global_document_search_is_purchase:         
            options += '<option value="purchase">Purchase Order</option>'          
        if self.env.company.sh_global_document_search_is_picking:
            options += '<option value="picking">Picking</option>'          
        if self.env.company.sh_global_document_search_is_invoice:
            options += '<option value="invoice">Invoice</option>'          
        if self.env.company.sh_global_document_search_is_product:
            options += '<option value="product">Product</option>'          
        if self.env.company.sh_global_document_search_is_lot:
            options += '<option value="lot">Lot</option>'          
        if self.env.company.sh_global_document_search_is_location:
            options += '<option value="location">Location</option>'  
        
        has_global_search_enabled = False            
        if self.env.company.sh_global_document_search_is_enable and self.env.user.has_group('sh_all_in_one_mbs.group_sh_all_in_one_mbs_global_document_search'):
            has_global_search_enabled = True
            
        result = {
            'has_global_search_enabled':has_global_search_enabled,
            'options':options,
            }
        return result
    

    @api.model
    def _search_document_all(self,barcode):
        result = {}        
        if self.env.company.sh_global_document_search_is_sale:
            result = self._search_document_sale(barcode)
        if not result and self.env.company.sh_global_document_search_is_purchase:
            result = self._search_document_purchase(barcode)            
        if not result and self.env.company.sh_global_document_search_is_picking:
            result = self._search_document_picking(barcode)  
        if not result and self.env.company.sh_global_document_search_is_invoice:
            result = self._search_document_invoice(barcode)  
        if not result and self.env.company.sh_global_document_search_is_product:
            result = self._search_document_product(barcode)  
        if not result and self.env.company.sh_global_document_search_is_lot:
            result = self._search_document_lot(barcode)  
        if not result and self.env.company.sh_global_document_search_is_location:
            result = self._search_document_location(barcode)   
            
        return result
                                                                             

            
    @api.model
    def _search_document_sale(self,barcode):       
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM sale_order
            WHERE name = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('sale.action_orders').read()[0]
            action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result        
        
            
    @api.model
    def _search_document_purchase(self,barcode):      
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM purchase_order
            WHERE name = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('purchase.purchase_form_action').read()[0]
            action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result

    @api.model
    def _search_document_picking(self,barcode):      
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM stock_picking
            WHERE name = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('stock.action_picking_tree_all').read()[0]
            action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result
    
    @api.model
    def _search_document_invoice(self,barcode):      
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM account_move
            WHERE name = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('account.action_move_out_invoice_type').read()[0]
#             action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('account.view_move_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result
    
    @api.model
    def _search_document_product(self,barcode):      
        result = {}         
        product_product_obj = self.env["product.product"]         
        self._cr.execute('''
            SELECT id
            FROM product_product
            WHERE barcode = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            product = product_product_obj.browse(int(data[0]))
            if product and product.product_tmpl_id and product.product_tmpl_id.product_variant_ids and len(product.product_tmpl_id.product_variant_ids) == 1:
                action = self.env.ref('product.product_template_action').read()[0]
                action['domain'] = []
                action['views'] = [(self.env.ref('product.product_template_only_form_view').id, 'form')]
                action['res_id'] = product.product_tmpl_id.id
                action["target"] = "new"
                result["action"] = action
            
            if product and product.product_tmpl_id and product.product_tmpl_id.product_variant_ids and len(product.product_tmpl_id.product_variant_ids) != 1:
                action = self.env.ref('product.product_normal_action_sell').read()[0]
                action['domain'] = []
                action['views'] = [(self.env.ref('product.product_normal_form_view').id, 'form')]
                action['res_id'] = data[0]
                action["target"] = "new"
                result["action"] = action
        return result
    
    @api.model
    def _search_document_lot(self,barcode):      
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM stock_production_lot
            WHERE name = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('stock.action_production_lot_form').read()[0]
#             action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('stock.view_production_lot_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result
    
    @api.model
    def _search_document_location(self,barcode):       
        result = {}                  
        self._cr.execute('''
            SELECT id
            FROM stock_location
            WHERE barcode = %s
        ''', [barcode])
        data = self._cr.fetchone()
        if data not in [None,False,'',""]:
            action = self.env.ref('stock.action_location_form').read()[0]
#             action['context'] = {}
            action['domain'] = []
            action['views'] = [(self.env.ref('stock.view_location_form').id, 'form')]
            action['res_id'] = data[0]
#                 action["target"] = "current"
            action["target"] = "new"
            result["action"] = action
        return result
    
                                
    @api.model
    def search_document(self, barcode,doc_type):
        
        search_doc_method = getattr(self,'_search_document_' + doc_type)
        result = search_doc_method(barcode)
        if result and result.get("action",False):
            action = result.get("action")
            action.update({
                "target": self.env.company.sh_global_document_search_action_target_type
                })
            result["action"] = action
        return result
     
            
import math
import re

#from _common import rounding

from openerp import tools
from openerp.osv import osv, fields
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

#class product_template(osv.osv):
#    _inherit = "product.template"
#    _description = "Product Template"
#    
#    
#    def _compute_amounts_margin2(self, cr, uid, ids, field_names, args, context=None):
#        """Compute the amounts in the currency of the user
#        """
#        if context is None:
#            context={}
#        currency_obj = self.pool.get('res.currency')
#        currency_rate_obj = self.pool.get('res.currency.rate')
#        user_currency_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.currency_id.id
#        currency_rate_id = currency_rate_obj.search(cr, uid, [('rate', '=', 1)], limit=1, context=context)[0]
#        base_currency_id = currency_rate_obj.browse(cr, uid, currency_rate_id, context=context).currency_id.id
#        res = {}
#        ctx = context.copy()
#        for item in self.browse(cr, uid, ids, context=context):
#            ctx['date'] = item.date
#            price_total = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_total, context=ctx)
#            price_average = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.price_average, context=ctx)
#            residual = currency_obj.compute(cr, uid, base_currency_id, user_currency_id, item.residual, context=ctx)
#            res[item.id] = {
#                'user_currency_price_total': price_total,
#                'user_currency_price_average': price_average,
#                'user_currency_residual': residual,
#            }
#        return res
#    
#    def _compute_amounts_margin(self, cr, uid, ids, field_names, args, context=None):
#        print """Compute the amounts in the currency of the user
#        """
#        if context is None:
#            context={}
#        res = {}
#        for product in self.browse(cr, uid, ids, context=context):
#            
#            real_price_before_margin    = product.real_price_before_margin
#            real_price_margin           = product.real_price_before_margin * (product.real_price_margin/ 100)
#            real_price_after_margin     = real_price_before_margin + real_price_margin 
#            
#            outlet_price_before_margin    = product.outlet_price_before_margin
#            outlet_price_margin           = product.outlet_price_before_margin * (product.outlet_price_margin/ 100)
#            outlet_price_after_margin     = outlet_price_before_margin + outlet_price_margin
#            
#            res[product.id] = {
#                #'user_currency_price_total': price_total,
#                'real_price_after_margin'   : real_price_after_margin,
#                'outlet_price_after_margin' : outlet_price_after_margin,
#            }
#        return res
#    
#    
#    _columns = {
#            'real_price_before_margin': fields.float('Real Price Before Margin', digits_compute=dp.get_precision('Product Price')),
#            'real_price_margin': fields.float('Real Margin (%)', digits_compute=dp.get_precision('Product Price')),
#            #'real_price_after_margin': fields.float('Real Price After Margin', digits_compute=dp.get_precision('Product Price')),
#            
#            'real_price_after_margin': fields.function(_compute_amounts_margin, string="Real Price After Margin", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
#            
#            
#            'outlet_price_before_margin': fields.float('Outlet Price Before Margin', digits_compute=dp.get_precision('Product Price')),
#            'outlet_price_margin': fields.float('Outlet Margin (%)', digits_compute=dp.get_precision('Product Price')),
#            'outlet_price_after_margin': fields.function(_compute_amounts_margin, string="Out Price After Margin", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
#                }
#
#product_template()

#===============================================================================
# class product_template(osv.osv):
#     _inherit = "product.template"
#     _description = "Product Template"
#     
#     def _compute_suggest_price(self, cr, uid, ids, field_names, args, context=None):
#         print """Compute the amounts in the currency of the user
#         """
#         if context is None:
#             context={}
#         res = {}
#         for product in self.browse(cr, uid, ids, context=context):
#             jkt_cost       = product.jkt_cost                       
#             margin          = product.jkt_cost * (product.margin/ 100)
#             suggest_price   = jkt_cost + margin
#             
#             
#             res[product.id] = {
#                     'suggest_price' : suggest_price,
#                     'real_price'    : suggest_price,
#                         }
#         return res
#     
#     
#     _columns = {
#             'jkt_cost'          : fields.float('JKT Cost', digits_compute=dp.get_precision('Product Price')),
#             'base_cost'         : fields.float('SG Cost', digits_compute=dp.get_precision('Product Price')),
#             'margin'            : fields.float('Margin (%)', digits_compute=dp.get_precision('Product Price')),
#             'suggest_price'     : fields.function(_compute_suggest_price, string="Suggest Price", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
#             'move_cost'         : fields.float('Product Real Price', digits_compute=dp.get_precision('Product Price')),                    
#             'real_price'        : fields.float('Product Real Price', digits_compute=dp.get_precision('Product Price')),                                
#             #'real_price'    : fields.function(_compute_suggest_price, string="Real Price", type='float', digits_compute=dp.get_precision('Account'), multi="_compute_amounts"),
#                 }
# 
# product_template()
#===============================================================================
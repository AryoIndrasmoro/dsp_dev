from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
from openerp import pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import openerp.addons.decimal_precision as dp
from openerp import netsvc


class sale_order(osv.osv):
    _inherit = "sale.order"
    
    _columns = { 
            'dsp_price_list_id': fields.selection([('real', 'Real Price'), ('outlet', 'Outlet Price')], 'DSP Price List'),
                }
        
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {'partner_invoice_id': False, 'partner_shipping_id': False,  'payment_term': False, 'fiscal_position': False}}

        part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])
        pricelist = part.property_product_pricelist and part.property_product_pricelist.id or False
        payment_term = part.property_payment_term and part.property_payment_term.id or False
        fiscal_position = part.property_account_position and part.property_account_position.id or False
        dedicated_salesman = part.user_id and part.user_id.id or uid
        
        dsp_price_list_id = part.dsp_price_list_id
        
        val = {
            'partner_invoice_id': addr['invoice'],
            'partner_shipping_id': addr['delivery'],
            'payment_term': payment_term,
            'fiscal_position': fiscal_position,
            'user_id': dedicated_salesman,
            'dsp_price_list_id' : dsp_price_list_id, 
            'sale_type' : 'real',
        }
        if pricelist:
            val['pricelist_id'] = pricelist
        return {'value': val}
    
    
    _defaults = {
            'dsp_price_list_id' : 'real',
                 }
  
sale_order()

class sale_order_line(osv.osv):
    
    _inherit = "sale.order.line"
    
    _columns = {
            'product_dsp_id': fields.many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True),
            'product_id': fields.many2one('product.product', 'Product', domain=[('sale_ok', '=', True)], change_default=True, invisible=True),
            'cons_doc': fields.many2one('stock.picking', 'Internal Moves'),
                }
    
    def onchange_product_dsp_id(self, cr, uid, ids, product_dsp_id, sale_type, price_list, partner_id, context=None):
        price_unit = 0.0
        discount = 0.0
        print "LLLLLLLLLLLLLLLLL", sale_type
        if not product_dsp_id:
            
            result = {'value': {
                    'product_id' : product_dsp_id,
                    }
                }
            
            return result
        partner_id = self.pool.get('res.partner').browse(cr, uid, partner_id, context=None)
        product = self.pool.get('product.product').browse(cr, uid, product_dsp_id, context=None)
            
        if sale_type == 'Promo':
            discount = 100
        else:
            discount = 0
        
        if price_list == 'standard':
            price_unit = product.suggest_price
        elif price_list == 'real':
            price_unit = product.real_price
        elif price_list == 'outlet':
            price_unit = product.jkt_cost + (product.jkt_cost * partner_id.outlet_margin/ 100)
                
        result = {'value': {
                    'product_id' : product_dsp_id,
                    'price_unit' : price_unit,     
                    'discount'   : discount               
                    }
                } 
        return result            
            
sale_order_line()

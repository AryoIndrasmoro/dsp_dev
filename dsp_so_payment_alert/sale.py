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
            'by_pass_payment'   : fields.boolean('By Pass Payment'),
            'note_pass_payment' : fields.text('Notes'),
                }
    
    def create(self, cr, uid, vals, context=None):
        ##############ARYA Payment Alert###############
        
        invoice_search  = self.pool.get('account.invoice').search(cr, uid, [('partner_id','=',vals['partner_id']), ('state','=','open')], context=None)
        invoice         = self.pool.get('account.invoice').browse(cr, uid, invoice_search, context=None)
        
        if invoice and vals['by_pass_payment'] == False:
            raise osv.except_osv(_('Out Standing Payment!'), _('You Can not Save if outlet have Out Standing payment'))
        
        ###############################################
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
        return super(sale_order, self).create(cr, uid, vals, context=context)
    
    def action_wait(self, cr, uid, ids, context=None):
        print "---------------------->123"
        context = context or {}
        
        ##############ARYA Payment Alert###############
        for inv in self.browse(cr, uid, ids, context=None):
            partner_id      = inv.partner_id.id
            by_pass_payment = inv.by_pass_payment
            
        invoice_search  = self.pool.get('account.invoice').search(cr, uid, [('partner_id','=',partner_id), ('state','=','open')], context=None)
        invoice         = self.pool.get('account.invoice').browse(cr, uid, invoice_search, context=None)
        
        if invoice and by_pass_payment == False:
            raise osv.except_osv(_('Out Standing Payment!'), _('You Can not Confirm if outlet have Out Standing payment'))
        ###############################################
        
        
        for o in self.browse(cr, uid, ids):
            if not o.order_line:
                raise osv.except_osv(_('Error!'),_('You cannot confirm a sales order which has no line.'))
            noprod = self.test_no_product(cr, uid, o, context)
            if (o.order_policy == 'manual') or noprod:
                self.write(cr, uid, [o.id], {'state': 'manual', 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
            else:
                self.write(cr, uid, [o.id], {'state': 'progress', 'date_confirm': fields.date.context_today(self, cr, uid, context=context)})
            self.pool.get('sale.order.line').button_confirm(cr, uid, [x.id for x in o.order_line])
        return True

sale_order()
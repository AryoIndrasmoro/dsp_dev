from openerp.osv import fields,osv
import pdb
import pprint

class sale_order(osv.osv):
    _inherit = "sale.order"
    _description = "Sales Order Inherit DSP"
    _columns ={
               'partner_id'     : fields.many2one('res.partner', 'Outlet/Customer', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, required=True, change_default=True, select=True, track_visibility='always'),
               'sale_type'      : fields.selection([('Promo', 'Promo'), ('Consignment', 'Consignment'),('Outlet (Direct Selling)','Outlet (Direct Selling)') ], 'Sale Type'),
               'person_name'    : fields.char('Person Name', size=128),
               'date_confirmed' : fields.date('Input Date'),
               'file_confirmed' : fields.binary('Input File'),    
    }
    
    def create(self, cr, uid, vals, context=None):
        
        if vals.get('sale_type')=='Promo':
            for  n in range(len(vals.get('order_line'))):
                vals['order_line'][n][2]['discount']=100
                    
        if vals.get('name','/')=='/':
            vals['name'] = self.pool.get('ir.sequence').get(cr, uid, 'sale.order') or '/'
        return super(sale_order, self).create(cr, uid, vals, context=context)    

    def write(self, cr, uid, ids, vals, context=None):

        for sale in self.browse(cr, uid, ids, context=context):
            if sale.sale_type =='Promo':
                for  n in range(len(vals.get('order_line'))):
                    if bool(vals['order_line'][n][2]):
                        vals['order_line'][n][2]['discount']=100
            
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)                                
        
    _defaults = {
                 'sale_type' : 'Outlet (Direct Selling)',
            }
    
sale_order()



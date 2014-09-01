# from datetime import datetime
# from dateutil.relativedelta import relativedelta
# import time
# from operator import itemgetter
# from itertools import groupby
# 
# from openerp.osv import fields, osv, orm
# from openerp.tools.translate import _
# from openerp import netsvc
# from openerp import tools
# from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
# import openerp.addons.decimal_precision as dp
# import logging
# #from openerp.addons.mail.static.scripts.openerp_mailgate import send_mail
# 
# _logger = logging.getLogger(__name__)
# 
# class stock_picking(osv.osv):
#     #_name = "stock.picking.in"
#     _inherit = "stock.picking"
#     
#     _columns = {
#             'journal_id'            : fields.many2one('account.journal', 'Bank/ Cash'),
#             'cost_component_line'   : fields.one2many('cost.component', 'picking_id', 'Contains'),
#             #'additional_cost'       : fields.selection([('no','Non Cost Component'), ('yes','With Cost Component')], 'Cost Component', readonly=False),
#             'additional_cost'          : fields.char('DescriptionMMMM', size=128, required=True),
#                 }  
#     
#     # FIXME: needs refactoring, this code is partially duplicated in stock_move.do_partial()!
#     def do_partial(self, cr, uid, ids, partial_datas, context=None):
#         print "Picking In>>>>>>>>>>>>>>>>>>>>>."
#         """ Makes partial picking and moves done.
#         @param partial_datas : Dictionary containing details of partial picking
#                           like partner_id, partner_id, delivery_date,
#                           delivery moves with product_id, product_qty, uom
#         @return: Dictionary of values
#         """
#         if context is None:
#             context = {}
#         else:
#             context = dict(context)
#         res = {}
#         move_obj = self.pool.get('stock.move')
#         product_obj = self.pool.get('product.product')
#         currency_obj = self.pool.get('res.currency')
#         uom_obj = self.pool.get('product.uom')
#         sequence_obj = self.pool.get('ir.sequence')
#         wf_service = netsvc.LocalService("workflow")
#         for pick in self.browse(cr, uid, ids, context=context):
#             new_picking = None
#             complete, too_many, too_few = [], [], []
#             move_product_qty, prodlot_ids, product_avail, partial_qty, product_uoms = {}, {}, {}, {}, {}
#             
#             
#             #_logger.debug("Print origin %s", pick.origin)
#             #_logger.error("Print origin %s", partial.picking_id.origin)  
# 
#             if not pick.origin:
#                 self.send_email(cr, uid, ids, context)
#                 #raise osv.except_osv(_('Warning!'),_('Origin cant be Null.'))
#                 
#                 
#             
#             # Create Cost COmponent Journal
#             
#             if pick.additional_cost == 'yes':
#                 
#                 move_pool = self.pool.get('account.move')
#                 move_line_pool = self.pool.get('account.move.line')
#                                 
#                 seq = sequence_obj.get_id(cr, uid, pick.journal_id.sequence_id.id)
#                 
#                 period_search = self.pool.get('account.period').search(cr, uid, [('date_start','<=',pick.date),('date_stop','>=',pick.date)])
#                 period_browse = self.pool.get('account.period').browse(cr, uid, period_search)
#                 
#                 print "pick.journal_id.id", pick.journal_id.id
#                 
#                 move = {
#                     'name'          : seq or '/',
#                     'journal_id'    : pick.journal_id.id,
#                     'narration'     : pick.purchase_id.name,
#                     'date'          : pick.date,
#                     'ref'           : pick.purchase_id.name,
#                     'period_id'     : period_browse[0].id,
#                     'partner_id'    : False
#                     }
#                 
#                 move_id = move_pool.create(cr, uid, move)
#                 
#                 total_credit = 0.0
#                 for cost_component_line in pick.cost_component_line:
#                     #print "+++++++++++++++++++++", cost_component_line.name or '/'
#                     debit = cost_component_line.quantity * cost_component_line.amount
#                     move_line = {
#                         'name'      : cost_component_line.name or '/',
#                         'debit'     : debit,
#                         'credit'    : 0.0,
#                         'account_id': cost_component_line.account_id.id,
#                         'move_id'   : move_id,
#                         'journal_id': pick.journal_id.id,
#                         'period_id' : period_browse[0].id,
#                         'partner_id': False,
#                         #'currency_id': 13,
#                         #'amount_currency': company_currency <> current_currency and -bts.amount or 0.0,
#                         'date'      : pick.date,
#                                 }
#                     total_credit += debit
#                     move_line_pool.create(cr, uid, move_line)
#                 
#                 #print "total_credit", total_credit
#                 move_line = {
#                         'name'      : seq or '/',
#                         'debit'     : 0.0,
#                         'credit'    : total_credit,
#                         'account_id': cost_component_line.account_id.id,
#                         'move_id'   : move_id,
#                         'journal_id': pick.journal_id.id,
#                         'period_id' : period_browse[0].id,
#                         'partner_id': False,
#                         #'currency_id': 13,
#                         #'amount_currency': company_currency <> current_currency and -bts.amount or 0.0,
#                         'date'      : pick.date,
#                                 }
#                 move_line_pool.create(cr, uid, move_line)
#                 
#                 move_pool.post(cr, uid, [move_id], context={})
#                 
#             
#             for move in pick.move_lines:
#                 if move.state in ('done', 'cancel'):
#                     continue
#                 partial_data = partial_datas.get('move%s' % (move.id), {})
#                 product_qty = partial_data.get('product_qty', 0.0)
#                 move_product_qty[move.id] = product_qty
#                 product_uom = partial_data.get('product_uom', False)
#                 product_price = partial_data.get('product_price', 0.0)
#                 product_currency = partial_data.get('product_currency', False)
#                 prodlot_id = partial_data.get('prodlot_id')
#                 prodlot_ids[move.id] = prodlot_id
#                 product_uoms[move.id] = product_uom
#                 partial_qty[move.id] = uom_obj._compute_qty(cr, uid, product_uoms[move.id], product_qty, move.product_uom.id)
#                 if move.product_qty == partial_qty[move.id]:
#                     complete.append(move)
#                 elif move.product_qty > partial_qty[move.id]:
#                     too_few.append(move)
#                 else:
#                     too_many.append(move)
# 
#                 # Average price computation
#                 if (pick.type == 'in') and (move.product_id.cost_method == 'average'):
#                     product = product_obj.browse(cr, uid, move.product_id.id)
#                     move_currency_id = move.company_id.currency_id.id
#                     context['currency_id'] = move_currency_id
#                     qty = uom_obj._compute_qty(cr, uid, product_uom, product_qty, product.uom_id.id)
# 
#                     if product.id in product_avail:
#                         product_avail[product.id] += qty
#                     else:
#                         product_avail[product.id] = product.qty_available
# 
#                     if qty > 0:
#                         new_price = currency_obj.compute(cr, uid, product_currency,
#                                 move_currency_id, product_price)
#                         new_price = uom_obj._compute_price(cr, uid, product_uom, new_price,
#                                 product.uom_id.id)
#                         if product.qty_available <= 0:
#                             new_std_price = new_price
#                         else:
#                             # Get the standard price
#                             amount_unit = product.price_get('standard_price', context=context)[product.id]
#                             new_std_price = ((amount_unit * product_avail[product.id])\
#                                 + (new_price * qty)) / (product_avail[product.id] + qty)
#                         # Write the field according to price type field
#                         product_obj.write(cr, uid, [product.id], {'standard_price': new_std_price})
# 
#                         # Record the values that were chosen in the wizard, so they can be
#                         # used for inventory valuation if real-time valuation is enabled.
#                         move_obj.write(cr, uid, [move.id],
#                                 {'price_unit': product_price,
#                                  'price_currency_id': product_currency})
# 
# 
#             for move in too_few:
#                 product_qty = move_product_qty[move.id]
#                 if not new_picking:
#                     new_picking_name = pick.name
#                     self.write(cr, uid, [pick.id],
#                                {'name': sequence_obj.get(cr, uid,
#                                             'stock.picking.%s' % (pick.type)),
#                                })
#                     new_picking = self.copy(cr, uid, pick.id,
#                             {
#                                 'name': new_picking_name,
#                                 'move_lines' : [],
#                                 'state':'draft',
#                             })
#                 if product_qty != 0:
#                     defaults = {
#                             'product_qty' : product_qty,
#                             'product_uos_qty': product_qty, #TODO: put correct uos_qty
#                             'picking_id' : new_picking,
#                             'state': 'assigned',
#                             'move_dest_id': False,
#                             'price_unit': move.price_unit,
#                             'product_uom': product_uoms[move.id]
#                     }
#                     prodlot_id = prodlot_ids[move.id]
#                     if prodlot_id:
#                         defaults.update(prodlot_id=prodlot_id)
#                     move_obj.copy(cr, uid, move.id, defaults)
#                 move_obj.write(cr, uid, [move.id],
#                         {
#                             'product_qty': move.product_qty - partial_qty[move.id],
#                             'product_uos_qty': move.product_qty - partial_qty[move.id], #TODO: put correct uos_qty
#                             'prodlot_id': False,
#                             'tracking_id': False,
#                         })
# 
#             if new_picking:
#                 move_obj.write(cr, uid, [c.id for c in complete], {'picking_id': new_picking})
#             for move in complete:
#                 defaults = {'product_uom': product_uoms[move.id], 'product_qty': move_product_qty[move.id]}
#                 if prodlot_ids.get(move.id):
#                     defaults.update({'prodlot_id': prodlot_ids[move.id]})
#                 move_obj.write(cr, uid, [move.id], defaults)
#             for move in too_many:
#                 product_qty = move_product_qty[move.id]
#                 defaults = {
#                     'product_qty' : product_qty,
#                     'product_uos_qty': product_qty, #TODO: put correct uos_qty
#                     'product_uom': product_uoms[move.id]
#                 }
#                 prodlot_id = prodlot_ids.get(move.id)
#                 if prodlot_ids.get(move.id):
#                     defaults.update(prodlot_id=prodlot_id)
#                 if new_picking:
#                     defaults.update(picking_id=new_picking)
#                 move_obj.write(cr, uid, [move.id], defaults)
# 
#             # At first we confirm the new picking (if necessary)
#             if new_picking:
#                 wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_confirm', cr)
#                 # Then we finish the good picking
#                 self.write(cr, uid, [pick.id], {'backorder_id': new_picking})
#                 self.action_move(cr, uid, [new_picking], context=context)
#                 wf_service.trg_validate(uid, 'stock.picking', new_picking, 'button_done', cr)
#                 wf_service.trg_write(uid, 'stock.picking', pick.id, cr)
#                 delivered_pack_id = new_picking
#                 back_order_name = self.browse(cr, uid, delivered_pack_id, context=context).name
#                 self.message_post(cr, uid, ids, body=_("Back order <em>%s</em> has been <b>created</b>.") % (back_order_name), context=context)
#             else:
#                 self.action_move(cr, uid, [pick.id], context=context)
#                 wf_service.trg_validate(uid, 'stock.picking', pick.id, 'button_done', cr)
#                 delivered_pack_id = pick.id
# 
#             delivered_pack = self.browse(cr, uid, delivered_pack_id, context=context)
#             res[pick.id] = {'delivered_picking': delivered_pack.id or False}
# 
#         return res    
# 
#     
#     #Send mail sans queue
#     def send_email(self, cr, uid, ids, context=None):
#         email_template_obj = self.pool.get('email.template')
#         template_ids = 13 #email_template_obj.search(cr, uid, [('model_id.model', '=', 'sale.order')])
#         if template_ids:
#             for id in ids:
#                 values = email_template_obj.generate_email(cr, uid, template_ids, id, context=context)
#                 print "values::  ", values 
#                 values['subject'] = "Test"
#                 values['email_to'] = "hilfforever@gmail.com"
#                 #values['email_cc'] = your_cc_address
#                 values['body_html'] = "your_body_html_part"
#                 #values['body'] = your_body_html_part
#     
#                 mail_mail_obj = self.pool.get('mail.mail')
#                 msg_id = mail_mail_obj.create(cr, uid, values, context=context)
#                 if msg_id:
#                     mail_mail_obj.send(cr, uid, [msg_id], context=context)
#         return True
#                 
#     
#     _defaults = {
#             'additional_cost' : 'no',
#                  }
# 
# stock_picking()
# 
# class stock_picking_in(osv.osv):
#     #_name = "stock.picking.in"
#     _inherit = "stock.picking.in"
#     
#     _columns = {
#             'journal_id'            : fields.many2one('account.journal', 'Bank/ Cash'),
#             'cost_component_line'   : fields.one2many('cost.component', 'picking_id', 'Contains'),
#             'additional_cost'       : fields.selection([('no', 'Non Cost Component'), ('yes', 'With Cost Component')], 'Cost Component', readonly=False),
#             
#                 }
#     
#     _defaults = {
#             'additional_cost' : 'no',
#                  }
# 
# stock_picking_in()
# 
# class cost_component(osv.osv):
#     _name = 'cost.component'
#     
#     _columns = {
#             'picking_id'    : fields.many2one('stock.picking.in', 'Picking ID', required=True),
#             'name'          : fields.char('Description', size=128, required=True),
#             'quantity'      : fields.float('Quantity', required=True),
#             'account_id'    : fields.many2one('account.account', 'Account', required=True),
#             'amount'        : fields.float('Amount', required=True),
#                 }
#     
#     _defaults = {
#             'quantity'  : 1,
#             'amount'    : 0.0,
#                 }
#     
# cost_component()
# 
# 
# 
# #class stock_picking_out(osv.osv):
# #    _inherit = "stock.picking.out"
# #    _columns = {
# #                 'date_confirmed': fields.datetime('Input Date', select=True),    
# #                 'person_name': fields.char('Person Name', size=70),
# #                 'datas': fields.binary('Image')
# ##                     'driver_id': fields.many2one('res.users', 'Driver', readonly=True, track_visibility='onchange', states={'draft':[('readonly',False)]}),            
# #                  }    
# # stock_picking_out()
#       
from openerp.osv import fields, osv
import openerp.addons.decimal_precision as dp


class res_partner(osv.osv):
    _inherit = 'res.partner'
    
    _columns = {
            'dsp_price_list_id' : fields.selection([('standard', 'Suggest Price'), ('real', 'Real Price'), ('outlet', 'Outlet Price')], 'DSP Price List'),
            'outlet_margin'     : fields.float('Outlet Margin (%)', digits_compute=dp.get_precision('Product Price')),
                }
    
    _defaults = {
            'dsp_price_list_id' : 'standard',
                 }
    
res_partner()
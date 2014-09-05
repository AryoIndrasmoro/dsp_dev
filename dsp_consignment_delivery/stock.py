from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from operator import itemgetter
from itertools import groupby

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp.tools import float_compare, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
import logging


class stock_picking(osv.osv):
    _inherit = 'stock.picking'

    _columns = {
            'consignment'   : fields.selection([('normal','Sale Order'), ('consignment','Consignment')], 'Consignment'),            
                }

stock_picking()
    

class stock_picking_out(osv.osv):
    _inherit = 'stock.picking.out'

    _columns = {
            'consignment'   : fields.selection([('normal','Sale Order'), ('consignment','Consignment')], 'Consignment'),
                }

stock_picking_out()
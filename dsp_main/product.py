# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields,osv
from datetime import datetime
import openerp.addons.decimal_precision as dp
#from openerp.tools.translate import _

class product_grape(osv.osv):
    _name = 'product.grape'
    _columns = {'name': fields.char('Name', size=128)}
product_grape() 

class product_region(osv.osv):
    _name = 'product.region'
    _columns = {
                'name': fields.char('Name', size=30),
                'preface': fields.text('Preface')
                }
product_region()

class product_type(osv.osv):
    _name = 'product.type'
    _columns = {'name': fields.char('Name', size=128)}
product_type()   

class product_appelation(osv.osv):
    _name = 'product.appelation'
    _columns = {'name': fields.char('Name', size=128)}
product_appelation() 

class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
        #'vintages': fields.boolean('Outlets/Customers', help="Check this box if this contact is a customer / outlet."),
        'vintages': fields.selection([(num, str(num)) for num in range(1970, (datetime.now().year) )], 'Vintages'),
        'classification': fields.char('Classification', size=128),
        'volume_l': fields.float('Volume (L)', digits_compute=dp.get_precision('Product Price')),
        'volume_alcohol': fields.float('Volume Alcohol (%)', digits_compute=dp.get_precision('Product Price')),
        'grape_id': fields.many2one('product.grape', 'Grape', required=False, ondelete='cascade',
            help="Product Grape."),   
        'country_id': fields.many2one('res.country', 'Country', required=False, ondelete='cascade',
            help="Product Country."),
        'region_id': fields.many2one('product.region', 'Region', required=False, ondelete='cascade',
            help="Product Region."),  
        'type_id': fields.many2one('product.type', 'Type', required=False, ondelete='cascade',
            help="Product Type."),   
        'appelation_id': fields.many2one('product.appelation', 'Appelation', required=False, ondelete='cascade',
            help="Product Appelation."),
        'classification': fields.char('Desc', size=128),                                                            
                                        
    }
    
    def name_get(self, cr, user, ids, context=None):
        if context is None:
            context = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        if not len(ids):
            return []
        def _name_get(d):
            name = d.get('name','')
            code = d.get('default_code',False)
            vintage = d.get('vintages',False)
            if code:
                name = '[%s] %s' % (code,name)
            if vintage:
                name = name + ' - ' + str(vintage)
            #else:
            #    name = name + ' - NV'
            if d.get('variants'):
                name = name + ' - %s' % (d['variants'],)
            return (d['id'], name)

        partner_id = context.get('partner_id', False)

        result = []
        for product in self.browse(cr, user, ids, context=context):
            sellers = filter(lambda x: x.name.id == partner_id, product.seller_ids)
            if sellers:
                for s in sellers:
                    mydict = {
                              'id': product.id,
                              'name': s.product_name or product.name,
                              'default_code': s.product_code or product.default_code,
                              'variants': product.variants,
                              'vintages': product.vintages
                              }
                    result.append(_name_get(mydict))
            else:
                mydict = {
                          'id': product.id,
                          'name': product.name,
                          'default_code': product.default_code,
                          'variants': product.variants,
                          'vintages': product.vintages
                          }
                result.append(_name_get(mydict))
        return result
    
product_product()
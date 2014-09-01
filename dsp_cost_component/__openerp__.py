# -*- coding: utf-8 -*-
##############################################################################
#
#    account_optimization module for OpenERP, Account Optimizations
#    Copyright (C) 2011 Thamini S.à.R.L (<http://www.thamini.com) Xavier ALT
#
#    This file is a part of account_optimization
#
#    account_optimization is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    account_optimization is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name": "Cost Component",
    "version": "1.1",
    "author": "Arya Adi Putra",
    'complexity': "High",
    "category": "Sale",
    "description": """
                Module ini digunakan untuk kalkulasi Cost Price Product
                    """,
    
    "images" : [],
    'depends': [ 'stock','purchase','sale','account','product','dsp_price_list'],
    'init_xml': [
    ],
    'demo_xml': [
    ],
    'update_xml': [
        'stock_view.xml',
        'product_view.xml'
        
    ],
    
    'installable': True,
    #'application': True,
    'auto_install': False,
    
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

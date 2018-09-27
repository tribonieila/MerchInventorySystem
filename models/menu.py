# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# ----------------------------------------------------------------------------------------------------------------------
# this is the main application menu add/remove items as required
# ----------------------------------------------------------------------------------------------------------------------
# if auth.has_membership(role="admin"):
#     response.menu.extend([(T('Admin?'), False, URL(c='appadmin'), [])])
# if (auth.user_id != None) & (auth.has_membership(role='administrator')):

# if (auth.user_id != None) & (auth.has_membership(role = 'root')):
#     response.menu = [
#         (T('Settings'), False, URL('default', '#'), [
#             (T('Prefix Data'), False, URL('default', 'pre_mas')),
#             (T('Division'), False, URL('default', 'div_mas')),
#             (T('Department'), False, URL('default', 'dept_mas')),
#             (T('Section'), False, URL('default', 'sec_mas')),
#             (T('Status'), False, URL('default', 'stat_mas')),
#             (T('Gender'), False, URL('default', 'gndr_mas')),
#         ]),
#         (T('Master Data'), False, URL('default', 'master_data'), [
#             (T('Product'), False, URL('default', 'prod_mas')),
#             (T('Sub-Product'), False, URL('default', 'subprod_mas')),
#             (T('Supplier'), False, URL('default', 'suplr_mas')),
#             (T('Group Line'), False, URL('default', 'groupline_mas')),
#             (T('Brand Line'), False, URL('default', 'brndlne_mas')),
#             (T('Brand Classification'), False, URL('default', 'brndclss_mas')),
#             (T('Fragrance Type'), False, URL('default', 'frgtype_mas')),
#             (T('Item Color'), False, URL('default', 'itmcol_mas')),
#             (T('Item Size'), False, URL('default', 'itmsze_mas')),
#             (T('Item Collection'), False, URL('default', 'itmcoll_mas')),
#             (T('Brand'), False, URL('default', 'brand_mas')),
#             (T('Transaction'), False, URL('default', 'trans_mas')),
#             (T('Voucher'), False, URL('default', 'vouc_mas')),
#             (T('Location'), False, URL('default', '#'))
#         ]),    
#     ]
# else:
#     response.menu = [
#         (T('Home'), False, URL('default', 'index'), []),
#         (T('Stock Request'), False, URL('default', '#'), []),
#         (T('Stock Transfer'), False, URL('default', '#'), []),
#         (T('Stock Receive'), False, URL('default', '#'), []),
#         (T('New Item'), False, '#', [
#             (T('BEAUTY DIVISION'), False, URL('default', '#')),
#             (T('FMCG DIVISION'), False, URL('default', 'fmcg_form')),
#             (T('RETAIL DIVISION'), False, URL('default', '#')),
#             (T('SUPPLY AND PERFUMES DIVISION'), False, URL('default', '#')),
#         ]),
#         (T('Reports'), False, URL('default', 'reports'), []),
#     ]

DEVELOPMENT_MENU = True


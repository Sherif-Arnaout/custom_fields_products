{
    'name': 'Custom Fields Products',
    'version': '1.0.0',
    'summary': 'Summary',
    'description': 'Description',
    'category': 'Category',
    'author': 'Sherif Ali',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'digest',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/custom_fields_product.xml',
        'views/custom_barcode_print.xml',
    ],
    'installable': True,
    'auto_install': False
}

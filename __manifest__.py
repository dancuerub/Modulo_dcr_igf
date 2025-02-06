{
    'name': 'Suplementos Nutricionales',  # Nombre amigable de tu módulo
    'version': '1.0',
    'category': 'Real Estate',
    'summary': 'Gestor de Suplementos Nutricionales',  # Breve descripción
    'description': """
    Módulo de Odoo para gestionar una tienda de suplementos.
    Permite gestionar inventario, compra y venta de productos nutricionales.
    """,
    'author': 'Daniel Cuenca Rubio e Iker González Fernández',  # Tu nombre
    'website': 'https://github.com/dancuerub/Modulo_dcr_igf',
    'depends': ['base'],  # Dependencia base mínima
    'data': [
        'security/ir.model.access.csv',  # Permisos de acceso
        'views/view_suplemento.xml',
        'views/view_proveedor.xml',
        'views/view_cliente.xml',
        'views/view_venta.xml',
        'views/view_factura.xml',
        'data/data.xml',
        'views/report_factura.xml',
		'views/view_compra.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'suplementos/static/src/css/kanban_styles.css',  # Ruta al archivo CSS para el estilo Kanban
        ],
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

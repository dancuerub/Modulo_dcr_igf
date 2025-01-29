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
    'website': 'https://www.nutripertec.com',
    'depends': ['base'],  # Dependencia base mínima
    'data': [
        'security/ir.model.access.csv',  # Permisos de acceso
        # Aquí irán los archivos XML de vistas y datos más adelante
        'views/view_suplemento.xml',
    ],
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
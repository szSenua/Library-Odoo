# Copyright <2025> Senua - email
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Library Senua",
    "summary": "Módulo Gestión de Biblioteca",
    "version": "18.0.1.0.0",
    "category": "Library",
    "website": "https://aeodoo.org",
    "author": "aeodoo, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base",
    ],
    "data": [
        'security/library_security.xml',
        'security/library_record_rules.xml',
        'security/ir.model.access.csv',           
        'views/library_edition_views.xml',        
        'views/library_book_views.xml',           
        'views/library_loan_views.xml',
        'views/library_menus.xml',
        'wizard/library_loan_wizard_views.xml',
    ],
}
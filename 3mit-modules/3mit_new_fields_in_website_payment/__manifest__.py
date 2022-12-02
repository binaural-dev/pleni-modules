{
	'name': '3mit New Fields in Website Payment',
	'summary': 'Adicion de nuevos campos al pago en el ecommerce.',
	'description': """14.0.0.3: Se agregaron los campos delivery_date y client_notes los cuales sobreescriben los campos scheduled_date_view, 
					expected_date y client_notes de la orden de venta.
					14.0.0.4: Se agrego el campo delivery_hour el cual sobreescribe el campo am_pm.
					\nColaborador: Carlos Marquez, Ricardo Sanchez""",
	'author': '3mit',
	'website': '',
	'category': 'Website/Ecommerce',
	'version': '14.0.0.4',
	'depends': ['website_sale', 'payment', 'pleni_custom_fields'],
	'data': ['templates/assets.xml', 'templates/payments.xml'],
	'installable': True,
	'application': True
}
# Copyright (c) 2021, deepesh@erpnext.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json

class APIJob(Document):
	pass


@frappe.whitelist(methods=['POST', 'PUT'])
def insert_api_job():
	args = frappe.form_dict
	for doc in args.get('doclist'):
		frappe.get_doc({
			'doctype': 'API Job',
			'record_id': doc.get('record_id'),
			'document': json.dumps(doc),
			'document_type': args.get('document_type')
		}).insert()

def enqueue_item_updates(doc, method):
	frappe.enqueue(add_item_taxes, item=doc)

def process_api_log():
	api_jobs = frappe.db.get_all('API Job', filters={'status': 'Pending'},
		fields=['name', 'document'], order_by='creation', limit=200)

	for job in api_jobs:
		frappe.db.set_value('API Job', job.name, 'status', 'In Progress')
		try:
			doc = frappe.get_doc(json.loads(job.document)).insert()
			response = {
				'status': 'Successful',
				'name': job.name
			}

			frappe.db.set_value('API Job', job.name, {
				'response': json.dumps(response),
				'status': 'Success'
			})
		except Exception as error:
			frappe.db.set_value('API Job', job.name, {
				'error': frappe.get_traceback(),
				'status': 'Failed'
			})

def add_item_taxes(item):
	templates = frappe.get_all('Item Tax Template', 
		filters={'title': ['in', ['In State GST', 'Out of State GST']]}, pluck='name')

	added_taxes = [d.item_tax_template for d in item.get('taxes')]
	for template in templates:
		if template not in added_taxes:
			item.append('taxes', {
				'item_tax_template': template
			})

	item.save()

# Copyright (c) 2026, Al-Salem Holding and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"fieldname": "name",
			"label": "ID",
			"fieldtype": "Link",
			"options": "Payment Entry",
			"width": 150
		},
		{
			"fieldname": "payment_type",
			"label": "Payment Type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "posting_date",
			"label": "Posting Date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "mode_of_payment",
			"label": "Mode of Payment",
			"fieldtype": "Link",
			"options": "Mode of Payment",
			"width": 150
		},
		{
			"fieldname": "party_type",
			"label": "Party Type",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"fieldname": "party",
			"label": "Party",
			"fieldtype": "Dynamic Link",
			"options": "party_type",
			"width": 150
		},
		{
			"fieldname": "paid_amount",
			"label": "Paid Amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "cost_center",
			"label": "Cost Center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 150
		}
	]


def get_data(filters):
	conditions, query_filters = get_conditions(filters)
	
	data = frappe.db.sql(
		f"""
		SELECT
			name,
			payment_type,
			posting_date,
			mode_of_payment,
			party_type,
			party,
			paid_amount,
			cost_center
		FROM `tabPayment Entry`
		WHERE payment_type != 'Receive'
		{conditions}
		ORDER BY posting_date DESC, name DESC
		""",
		query_filters,
		as_dict=1
	)
	
	return data


def get_conditions(filters):
	conditions = []
	query_filters = {}
	
	# Default to only submitted entries
	conditions.append("AND docstatus = 1")
	
	if filters:
		if filters.get("from_date"):
			conditions.append("AND posting_date >= %(from_date)s")
			query_filters["from_date"] = filters.get("from_date")
		
		if filters.get("to_date"):
			conditions.append("AND posting_date <= %(to_date)s")
			query_filters["to_date"] = filters.get("to_date")

		if filters.get("company"):
			conditions.append("AND company = %(company)s")
			query_filters["company"] = filters.get("company")

		if filters.get("cost_center"):
			conditions.append("AND cost_center = %(cost_center)s")
			query_filters["cost_center"] = filters.get("cost_center")
	
	return " " + " ".join(conditions) if conditions else "", query_filters



@frappe.whitelist()
def get_payments_by_cost_center(cost_center, from_date, to_date):
	"""
	Returns calculated payments (sum of paid_amount) for a given cost center and date range
	where payment_type != 'Receive'
	"""
	if not cost_center or not from_date or not to_date:
		return 0
	
	result = frappe.db.sql(
		"""
		SELECT
			SUM(paid_amount) as total_paid_amount
		FROM `tabPayment Entry`
		WHERE payment_type != 'Receive'
			AND cost_center = %(cost_center)s
			AND posting_date >= %(from_date)s
			AND posting_date <= %(to_date)s
			AND docstatus = 1
		""",
		{
			"cost_center": cost_center,
			"from_date": from_date,
			"to_date": to_date
		},
		as_dict=1
	)
	
	if result and result[0] and result[0].get("total_paid_amount"):
		return result[0].get("total_paid_amount") or 0
	
	return 0
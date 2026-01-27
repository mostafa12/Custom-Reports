# Copyright (c) 2026, Al-Salem Holding and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		# PO Section
		{
			"fieldname": "po_date",
			"label": "P.O date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"fieldname": "po_num",
			"label": "Num",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 120
		},
		{
			"fieldname": "status",
			"label": "Status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"fieldname": "supplier",
			"label": "Supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 150
		},
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120
		},
		{
			"fieldname": "material_request_number",
			"label": "Material request number",
			"fieldtype": "Link",
			"options": "Material Request",
			"width": 150
		},
		{
			"fieldname": "supplier_quotation_number",
			"label": "Supplier Quotation Number",
			"fieldtype": "Link",
			"options": "Supplier Quotation",
			"width": 150
		},
		{
			"fieldname": "owner",
			"label": "Owner",
			"fieldtype": "Link",
			"options": "User",
			"width": 120
		},
		{
			"fieldname": "item_code",
			"label": "Item code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120
		},
		{
			"fieldname": "item_name",
			"label": "Item name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "item_price",
			"label": "Item price",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "quantity",
			"label": "Quantity",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"fieldname": "amount",
			"label": "Amount",
			"fieldtype": "Currency",
			"width": 120
		},
		{
			"fieldname": "category",
			"label": "Category",
			"fieldtype": "Link",
			"options": "Item Group",
			"width": 120
		},
		{
			"fieldname": "uom",
			"label": "UOM",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 80
		},
		{
			"fieldname": "terms_and_conditions",
			"label": "Terms & conditions",
			"fieldtype": "Text",
			"width": 400
		},
		{
			"fieldname": "cost_center",
			"label": "Cost center",
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": 120
		},
		# MR Section
		{
			"fieldname": "requester",
			"label": "Requester",
			"fieldtype": "Link",
			"options": "User",
			"width": 120
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 120
		}
	]


def get_data(filters):
	conditions, query_filters = get_conditions(filters)
	
	# Get item-level data
	item_data = frappe.db.sql(
		f"""
		SELECT
			po.name as po_num,
			po.transaction_date as po_date,
			po.status,
			po.supplier,
			po.company,
			po.owner,
			po.terms as terms_and_conditions,
			poi.material_request as material_request_number,
			poi.supplier_quotation as supplier_quotation_number,
			poi.item_code,
			poi.item_name,
			poi.rate as item_price,
			poi.qty as quantity,
			poi.base_amount as amount,
			poi.item_group as category,
			poi.uom,
			poi.cost_center,
			mr.owner as requester,
			COALESCE(mr.department, emp.department) as department
		FROM
			`tabPurchase Order` po
		INNER JOIN
			`tabPurchase Order Item` poi ON poi.parent = po.name
		LEFT JOIN
			`tabMaterial Request` mr ON mr.name = poi.material_request
		LEFT JOIN
			`tabEmployee` emp ON emp.user_id = mr.owner
		WHERE
			po.docstatus = 1
			{conditions}
		ORDER BY
			po.transaction_date DESC, po.name DESC, poi.idx ASC
		""",
		query_filters,
		as_dict=1
	)
	
	# Group items by PO and create hierarchical structure
	grouped_data = {}
	for row in item_data:
		po_num = row.get("po_num")
		if po_num not in grouped_data:
			# Create parent row (PO level)
			parent_row = {
				"indent": 0,
				"po_date": row.get("po_date"),
				"po_num": po_num,
				"status": row.get("status"),
				"supplier": row.get("supplier"),
				"company": row.get("company"),
				"owner": row.get("owner"),
				"terms_and_conditions": row.get("terms_and_conditions"),
				# Item-specific fields should be empty in parent row
				"material_request_number": None,
				"supplier_quotation_number": None,
				"item_code": None,
				"item_name": None,
				"item_price": None,
				"quantity": None,
				"amount": None,
				"category": None,
				"uom": None,
				"cost_center": None,
				"requester": None,
				"department": None
			}
			grouped_data[po_num] = {"parent": parent_row, "items": []}
		
		# Create child row (item level)
		child_row = {
			"indent": 1,
			"po_date": row.get("po_date"),
			"po_num": row.get("po_num"),
			"status": row.get("status"),
			"supplier": row.get("supplier"),
			"company": row.get("company"),
			"owner": row.get("owner"),
			"terms_and_conditions": row.get("terms_and_conditions"),
			"material_request_number": row.get("material_request_number"),
			"supplier_quotation_number": row.get("supplier_quotation_number"),
			"item_code": row.get("item_code"),
			"item_name": row.get("item_name"),
			"item_price": row.get("item_price"),
			"quantity": row.get("quantity"),
			"amount": row.get("amount"),
			"category": row.get("category"),
			"uom": row.get("uom"),
			"cost_center": row.get("cost_center"),
			"requester": row.get("requester"),
			"department": row.get("department")
		}
		grouped_data[po_num]["items"].append(child_row)
	
	# Flatten the grouped data: parent row followed by its items
	data = []
	for po_num in sorted(grouped_data.keys(), reverse=True):
		data.append(grouped_data[po_num]["parent"])
		data.extend(grouped_data[po_num]["items"])
	
	return data


def get_conditions(filters):
	conditions = []
	query_filters = {}
	
	if filters:
		if filters.get("company"):
			conditions.append("AND po.company = %(company)s")
			query_filters["company"] = filters.get("company")
		
		if filters.get("supplier"):
			conditions.append("AND po.supplier = %(supplier)s")
			query_filters["supplier"] = filters.get("supplier")
		
		if filters.get("from_date"):
			conditions.append("AND po.transaction_date >= %(from_date)s")
			query_filters["from_date"] = filters.get("from_date")
		
		if filters.get("to_date"):
			conditions.append("AND po.transaction_date <= %(to_date)s")
			query_filters["to_date"] = filters.get("to_date")
		
		if filters.get("item_code"):
			conditions.append("AND poi.item_code = %(item_code)s")
			query_filters["item_code"] = filters.get("item_code")
		
		if filters.get("cost_center"):
			conditions.append("AND poi.cost_center = %(cost_center)s")
			query_filters["cost_center"] = filters.get("cost_center")
		
		if filters.get("material_request_number"):
			conditions.append("AND poi.material_request = %(material_request_number)s")
			query_filters["material_request_number"] = filters.get("material_request_number")
		
		if filters.get("supplier_quotation_number"):
			conditions.append("AND poi.supplier_quotation = %(supplier_quotation_number)s")
			query_filters["supplier_quotation_number"] = filters.get("supplier_quotation_number")
		
		if filters.get("po_owner"):
			conditions.append("AND po.owner = %(po_owner)s")
			query_filters["po_owner"] = filters.get("po_owner")
		
		if filters.get("material_request_requester"):
			conditions.append("AND mr.owner = %(material_request_requester)s")
			query_filters["material_request_requester"] = filters.get("material_request_requester")
		
		if filters.get("department"):
			conditions.append("AND COALESCE(mr.department, emp.department) = %(department)s")
			query_filters["department"] = filters.get("department")
	
	return " " + " ".join(conditions) if conditions else "", query_filters

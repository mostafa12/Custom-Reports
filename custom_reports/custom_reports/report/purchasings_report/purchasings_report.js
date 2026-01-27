// Copyright (c) 2026, Al-Salem Holding and contributors
// For license information, please see license.txt

frappe.query_reports["Purchasings Report"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_default("Company"),
			"width": "80"
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"options": "Supplier",
			"width": "80"
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"width": "80"
		},
		{
			"fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"options": "Item",
			"width": "80"
		},
		{
			"fieldname": "cost_center",
			"label": __("Cost Center"),
			"fieldtype": "Link",
			"options": "Cost Center",
			"width": "80"
		},
		{
			"fieldname": "material_request_number",
			"label": __("Material Request Number"),
			"fieldtype": "Link",
			"options": "Material Request",
			"width": "80"
		},
		{
			"fieldname": "supplier_quotation_number",
			"label": __("Supplier Quotation Number"),
			"fieldtype": "Link",
			"options": "Supplier Quotation",
			"width": "80"
		},
		{
			"fieldname": "po_owner",
			"label": __("PO Owner"),
			"fieldtype": "Link",
			"options": "User",
			"width": "80"
		},
		{
			"fieldname": "material_request_requester",
			"label": __("Material Request Requester"),
			"fieldtype": "Link",
			"options": "User",
			"width": "80"
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"width": "80"
		}
	]
};

// Copyright (c) 2026, Al-Salem Holding and contributors
// For license information, please see license.txt

frappe.query_reports["Leave Balance"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today().split("-")[0] + "-01-01",
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today().split("-")[0] + "-12-31",
			"reqd": 1
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company"),
		},
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"get_query": function() {
				var company = frappe.query_report.get_filter_value('company');
				return {
					"filters": {
						"company": company
					}
				};
			}
		},
		{
			"fieldname": "employee",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "Employee",
			"get_query": function() {
				var company = frappe.query_report.get_filter_value('company');
				var department = frappe.query_report.get_filter_value('department');
				var filters = {};
				if (company) filters["company"] = company;
				if (department) filters["department"] = department;
				return { "filters": filters };
			}
		},
		{
			"fieldname": "leave_type",
			"label": __("Leave Type"),
			"fieldtype": "Link",
			"options": "Leave Type",
		}
	]
};

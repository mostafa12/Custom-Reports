# Copyright (c) 2026, Al-Salem Holding and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = get_columns(filters)
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	year_label = ""
	if from_date and to_date:
		from_year = from_date[:4]
		to_year = to_date[:4]
		if from_year == to_year:
			year_label = f" ({from_year})"
		else:
			year_label = f" ({from_year}-{to_year})"
	
	return [
		{
			"fieldname": "employee",
			"label": "Employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 120
		},
		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"fieldname": "company",
			"label": "Company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120
		},
		{
			"fieldname": "department",
			"label": "Department",
			"fieldtype": "Link",
			"options": "Department",
			"width": 150
		},
		{
			"fieldname": "leave_type",
			"label": "Leave Type",
			"fieldtype": "Link",
			"options": "Leave Type",
			"width": 150
		},
		{
			"fieldname": "allocated_days",
			"label": f"Allocated Days{year_label}",
			"fieldtype": "Int",
			"width": 180
		},
		{
			"fieldname": "used_days",
			"label": f"Used Days{year_label}",
			"fieldtype": "Int",
			"width": 180
		},
		{
			"fieldname": "remaining_days",
			"label": f"Remaining Days{year_label}",
			"fieldtype": "Int",
			"width": 180
		},
	]


def get_data(filters):
	conditions = get_conditions(filters)
	
	data = frappe.db.sql("""
		SELECT
			la.employee AS employee,
			la.employee_name AS employee_name,
			la.company AS company,
			emp.department AS department,
			la.leave_type AS leave_type,
			la.new_leaves_allocated AS allocated_days,
			IFNULL(SUM(lap.total_leave_days), 0) AS used_days,
			(la.new_leaves_allocated - IFNULL(SUM(lap.total_leave_days), 0)) AS remaining_days
		FROM `tabLeave Allocation` la
		INNER JOIN `tabEmployee` emp
			ON la.employee = emp.name
		LEFT JOIN `tabLeave Application` lap
			ON la.employee = lap.employee
			AND la.leave_type = lap.leave_type
			AND lap.status = 'Approved'
			AND lap.from_date <= %(to_date)s
			AND lap.to_date >= %(from_date)s
		WHERE
			la.docstatus = 1
			AND la.from_date <= %(to_date)s
			AND la.to_date >= %(from_date)s
			{conditions}
		GROUP BY
			la.employee,
			la.employee_name,
			la.company,
			emp.department,
			la.leave_type,
			la.new_leaves_allocated
		ORDER BY
			la.employee,
			la.leave_type
	""".format(conditions=conditions), filters, as_dict=True)
	
	return data


def get_conditions(filters):
	conditions = ""
	
	if filters.get("company"):
		conditions += " AND la.company = %(company)s"
	
	if filters.get("department"):
		conditions += " AND emp.department = %(department)s"
	
	if filters.get("employee"):
		conditions += " AND la.employee = %(employee)s"
	
	if filters.get("leave_type"):
		conditions += " AND la.leave_type = %(leave_type)s"
	
	return conditions

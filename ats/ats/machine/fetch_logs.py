import frappe
from zk import ZK
from datetime import datetime, timedelta


# --------------------------------------------------
# Fetch biometric punches → Employee Checkin
# --------------------------------------------------
@frappe.whitelist()
def fetch_employee_checkins():

    devices = frappe.get_all(
        "Biometric Device",
        filters={"is_active": 1},
        fields=["name", "device_ip", "port", "log_type"]
    )

    total_new = 0
    total_duplicates = 0

    for dev in devices:
        if not dev.device_ip or not dev.port:
            continue

        log_type = dev.log_type or "IN"

        try:
            zk = ZK(dev.device_ip, port=int(dev.port), timeout=10)
            conn = zk.connect()

            attendances = conn.get_attendance()

            for att in attendances:
                employee = str(att.user_id)
                punch_time = att.timestamp

                if not employee or not punch_time:
                    continue

                if frappe.db.exists(
                    "Employee Checkin",
                    {
                        "employee": employee,
                        "time": punch_time,
                        "log_type": log_type
                    }
                ):
                    total_duplicates += 1
                    continue

                frappe.get_doc({
                    "doctype": "Employee Checkin",
                    "employee": employee,
                    "time": punch_time,
                    "log_type": log_type,
                    "device_id": dev.name
                }).insert(ignore_permissions=True)

                total_new += 1

            conn.disconnect()
            frappe.db.commit()

        except Exception as e:
            print(f"❌ {dev.name} error: {e}")

    return {
        "new_checkins": total_new,
        "duplicates": total_duplicates
    }


# --------------------------------------------------
# Calculate working hours
# --------------------------------------------------
def calculate_work_hours(in_time, out_time):
    if not in_time or not out_time:
        return 0
    return (out_time - in_time).total_seconds() / 3600


# --------------------------------------------------
# Attendance status logic
# --------------------------------------------------
def get_attendance_status(in_time, out_time):
    hours = calculate_work_hours(in_time, out_time)

    if hours >= 8:
        return "Present"
    elif hours >= 4:
        return "Half Day"
    return "Half Day"


# --------------------------------------------------
# Mark attendance for ONE date
# --------------------------------------------------
@frappe.whitelist()
def mark_attendance_for_date(attendance_date):

    if isinstance(attendance_date, str):
        attendance_date = datetime.strptime(attendance_date, "%Y-%m-%d").date()

    employees = frappe.db.sql("""
        SELECT DISTINCT employee
        FROM `tabEmployee Checkin`
        WHERE DATE(time) = %s
    """, attendance_date, as_dict=True)

    created = 0

    for row in employees:
        employee = row.employee

        checkins = frappe.get_all(
            "Employee Checkin",
            filters={
                "employee": employee,
                "time": ["between", [
                    f"{attendance_date} 00:00:00",
                    f"{attendance_date} 23:59:59"
                ]]
            },
            fields=["time", "log_type"],
            order_by="time asc"
        )

        in_time = None
        out_time = None

        for c in checkins:
            if c.log_type == "IN" and not in_time:
                in_time = c.time
            if c.log_type == "OUT":
                out_time = c.time

        if not in_time:
            continue

        if frappe.db.exists(
            "Attendance",
            {"employee": employee, "attendance_date": attendance_date}
        ):
            continue

        status = get_attendance_status(in_time, out_time)

        att = frappe.new_doc("Attendance")
        att.employee = employee
        att.attendance_date = attendance_date
        att.in_time = in_time
        att.out_time = out_time
        att.status = status
        att.insert(ignore_permissions=True)

        created += 1

    frappe.db.commit()
    return created


# --------------------------------------------------
# Mark attendance for previous day
# --------------------------------------------------
@frappe.whitelist()
def mark_attendance_for_previous_day():
    date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    count = mark_attendance_for_date(date)
    return f"✅ {count} attendance records created for {date}"


# --------------------------------------------------
# One-click FULL process
# --------------------------------------------------
@frappe.whitelist()
def fetch_and_mark_attendance():
    fetch_employee_checkins()
    return mark_attendance_for_previous_day()

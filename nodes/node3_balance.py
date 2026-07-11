"""
Node 3 — Balance. Spots pending choke points across registered
departments and assigns the task to whichever connected department
currently reports the lightest load, instead of blindly following a
fixed top-down assignment.
"""


class Node3Balance:
    def __init__(self):
        self.connected_departments = []  # DepartmentAI instances

    def register_department(self, department):
        self.connected_departments.append(department)

    def route_payload(self, payload):
        payload.setdefault("trace", []).append("node3_balance")

        if not self.connected_departments:
            payload["assigned_department"] = payload.get("department")
            return payload

        def load_of(dept):
            # Recent fire activity is a better proxy for "how busy is this
            # department right now" than its static nerve count.
            return sum(m.health_check().get("total_fires", 0) for m in dept.managers)

        least_loaded = min(self.connected_departments, key=load_of)
        payload["assigned_department"] = least_loaded.DEPARTMENT_ID
        return payload

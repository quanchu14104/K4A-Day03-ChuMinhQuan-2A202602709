"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Đã được định nghĩa mẫu sẵn cho Học viên tham khảo
    {
        "name": "academic_query",
        "description": "Tra cứu hồ sơ và thông tin học vụ của sinh viên VinUni bằng mã sinh viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần tra cứu (ví dụ: 'SV2026001')"
                }
            },
            "required": ["student_id"]
        }
    },
    
    # --------------------------------------------------------------------------
    # 1.2: HỌC VIÊN HOÀN THIỆN TOOL SCHEMA CHO 'schedule_appointment'
    # 🎯 YÊU CẦU THIẾT KẾ SCHEMA (JSON SCHEMA STANDARD):
    # 1. Tool dùng để đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.
    # 2. Thiết kế các tham số (properties) để LLM trích xuất:
    #    - student_id (string): Mã sinh viên cần đặt lịch (ví dụ: 'SV2026001')
    #    - datetime_str (string): Thời gian hẹn (ví dụ: '14:00 15/09/2026')
    #    - advisor_name (string): Tên cố vấn học tập
    # 3. Khai báo danh sách các trường bắt buộc (required).
    # --------------------------------------------------------------------------
    {
        "name": "schedule_appointment",
        "description": "Đặt lịch hẹn tư vấn học vụ với Cố vấn học tập VinUni.",
        "parameters": {
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "Mã sinh viên cần đặt lịch hẹn (ví dụ: 'SV2026001')"
                },
                "datetime_str": {
                    "type": "string",
                    "description": "Thời gian hẹn tư vấn (ví dụ: '14:00 15/09/2026')"
                },
                "advisor_name": {
                    "type": "string",
                    "description": "Tên cố vấn học tập cần gặp (ví dụ: 'PGS.TS Nguyễn Văn A')"
                }
            },
            "required": ["student_id", "datetime_str"]
        }
    },

    # ==========================================================================
    # ĐỀ TÀI 2.2: TRỢ LÝ HỖ TRỢ KỸ THUẬT IT HELPDESK
    # 1. Tool tra cứu: query_ticket
    # 2. Tool hành động: create_support_ticket
    # ==========================================================================
    {
        "name": "query_ticket",
        "description": "Tra cứu thông tin và tình trạng ticket sự cố kỹ thuật (mạng, VPN, tài khoản, phần mềm) bằng mã ticket hoặc mã nhân viên.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "string",
                    "description": "Mã ticket sự cố cần tra cứu (ví dụ: 'TK2026001')"
                },
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên cần tra cứu ticket (ví dụ: 'NV2026001')"
                }
            },
            "required": ["ticket_id"]
        }
    },
    {
        "name": "create_support_ticket",
        "description": "Tạo yêu cầu (ticket) hỗ trợ kỹ thuật IT Helpdesk mới khi nhân viên gặp sự cố mạng, tài khoản, phần cứng hoặc phần mềm.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "Mã nhân viên yêu cầu hỗ trợ (ví dụ: 'NV2026001')"
                },
                "issue_category": {
                    "type": "string",
                    "description": "Phân loại sự cố kỹ thuật (ví dụ: 'Sự cố Mạng / VPN', 'Tài khoản / Phân quyền', 'Phần cứng', 'Phần mềm')"
                },
                "description": {
                    "type": "string",
                    "description": "Mô tả chi tiết triệu chứng hoặc sự cố kỹ thuật gặp phải"
                },
                "priority": {
                    "type": "string",
                    "description": "Mức độ ưu tiên của ticket ('Low', 'Medium', 'High', 'Critical')",
                    "enum": ["Low", "Medium", "High", "Critical"]
                }
            },
            "required": ["employee_id", "issue_category", "description"]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

# Cơ sở dữ liệu mẫu cho Đề tài 1.1 (Academic)
MOCK_DATABASE = {
    "SV2026001": {
        "full_name": "Nguyễn Văn An",
        "class": "AI-K4",
        "gpa": 3.85,
        "email": "an.nv@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "PGS.TS Nguyễn Văn A"
    },
    "SV2026002": {
        "full_name": "Trần Thị Bình",
        "class": "AI-K4",
        "gpa": 3.60,
        "email": "binh.tt@vinuni.edu.vn",
        "status": "Đang học",
        "advisor": "TS. Lê Thị B"
    }
}

# Cơ sở dữ liệu mẫu cho Đề tài 2.2 (IT Helpdesk)
IT_TICKETS_DATABASE = {
    "TK2026001": {
        "ticket_id": "TK2026001",
        "employee_id": "NV2026001",
        "employee_name": "Chu Minh Quân",
        "category": "Sự cố Mạng / VPN",
        "description": "Không thể kết nối mạng VPN nội bộ từ xa để truy cập máy chủ R&D.",
        "status": "Đang xử lý (In Progress)",
        "priority": "High",
        "created_at": "09:15 12/09/2026",
        "assigned_to": "Kỹ thuật viên Lê Hoàng Nam (IT Tier-2)"
    },
    "TK2026002": {
        "ticket_id": "TK2026002",
        "employee_id": "NV2026002",
        "employee_name": "Trần Thị Bình",
        "category": "Tài khoản / Phân quyền",
        "description": "Tài khoản Single Sign-On bị khóa do nhập sai mật khẩu quá 5 lần.",
        "status": "Đã giải quyết (Resolved)",
        "priority": "Medium",
        "created_at": "14:30 10/09/2026",
        "assigned_to": "Kỹ thuật viên Phạm Minh Đức (IT Tier-1)"
    }
}


def execute_academic_query(student_id: str) -> str:
    """Thực thi tra cứu học vụ theo mã sinh viên"""
    student = MOCK_DATABASE.get(student_id.strip().upper())
    if student:
        return json.dumps({
            "status": "SUCCESS",
            "student_id": student_id,
            "data": student
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'"
        }, ensure_ascii=False)


def execute_schedule_appointment(student_id: str, datetime_str: str, advisor_name: str = "PGS.TS Nguyễn Văn A") -> str:
    """Thực thi đặt lịch hẹn tư vấn học vụ"""
    return json.dumps({
        "status": "SUCCESS",
        "booking_id": f"BK-{student_id}-99",
        "student_id": student_id,
        "datetime": datetime_str,
        "advisor": advisor_name,
        "message": f"Đặt lịch thành công cho sinh viên {student_id} với {advisor_name} vào lúc {datetime_str}."
    }, ensure_ascii=False)


def execute_query_ticket(ticket_id: str, employee_id: str = None) -> str:
    """[Đề tài 2.2] Thực thi tra cứu ticket sự cố kỹ thuật"""
    ticket_id_clean = ticket_id.strip().upper() if ticket_id else ""
    ticket = IT_TICKETS_DATABASE.get(ticket_id_clean)
    
    # Tìm kiếm theo employee_id nếu không tìm thấy bằng ticket_id
    if not ticket and employee_id:
        emp_clean = employee_id.strip().upper()
        for t in IT_TICKETS_DATABASE.values():
            if t.get("employee_id") == emp_clean:
                ticket = t
                break

    if ticket:
        return json.dumps({
            "status": "SUCCESS",
            "ticket_id": ticket["ticket_id"],
            "data": ticket
        }, ensure_ascii=False)
    else:
        return json.dumps({
            "status": "NOT_FOUND",
            "message": f"Không tìm thấy ticket sự cố có mã '{ticket_id}' trong hệ thống IT Helpdesk."
        }, ensure_ascii=False)


def execute_create_support_ticket(employee_id: str, issue_category: str, description: str, priority: str = "Medium") -> str:
    """[Đề tài 2.2] Thực thi tạo ticket yêu cầu hỗ trợ kỹ thuật mới"""
    new_ticket_id = f"TK-{employee_id.strip().upper()}-99"
    new_ticket = {
        "ticket_id": new_ticket_id,
        "employee_id": employee_id.strip().upper(),
        "employee_name": "Chu Minh Quân",
        "category": issue_category,
        "description": description,
        "priority": priority,
        "status": "Tiếp nhận mới (Open)",
        "created_at": "Hiện tại",
        "assigned_to": "Đội ngũ IT Helpdesk On-call",
        "sla": "Thời gian cam kết tiếp nhận và xử lý trong vòng 2 giờ làm việc."
    }
    IT_TICKETS_DATABASE[new_ticket_id] = new_ticket
    
    return json.dumps({
        "status": "SUCCESS",
        "ticket_id": new_ticket_id,
        "data": new_ticket,
        "message": f"Tạo ticket hỗ trợ kỹ thuật thành công! Mã ticket: {new_ticket_id}. Sự cố: '{issue_category}' ({priority}). IT Helpdesk sẽ xử lý trong vòng 2 giờ."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "academic_query": execute_academic_query,
    "schedule_appointment": execute_schedule_appointment,
    "query_ticket": execute_query_ticket,
    "create_support_ticket": execute_create_support_ticket
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)


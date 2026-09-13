# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Chu Minh Quân

> **Mã Sinh Viên / Mã Học viên:** 2A202602709

> **Chủ đề Lựa chọn:** Đề tài 2.2: Trợ lý Hỗ trợ Kỹ thuật IT Helpdesk (Tra cứu ticket sự cố mạng, tài khoản và tạo yêu cầu hỗ trợ kỹ thuật). 

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | 4 / 5 | Khi nhân viên báo lỗi (vd: "Không vào được mạng/VPN"), Agent phải tư duy nhiều bước tuần tự: (1) Phân tích triệu chứng và phân loại sự cố (mạng, tài khoản, hay phần mềm) (2) Tra cứu lịch sử ticket xem đã báo lỗi chưa (3) Kiểm tra trạng thái hệ thống/tài khoản (4) Hướng dẫn giải pháp nhanh hoặc tạo ticket chuyển cấp IT. |
| **2. Tool Interaction** | 5 / 5 | Hệ thống bắt buộc phải tương tác với MCP Server và DB/API nội bộ vì LLM không thể tự biết trạng thái hệ thống: cần ít nhất 2 Tools chính gồm query_ticket/check_account (tra cứu trạng thái mạng/tài khoản) và create_ticket (hành động ghi nhận ticket mới vào hệ thống quản lý sự cố). |
| **3. Dynamic Decision** | 5 / 5 | Luồng xử lý phân nhánh phụ thuộc trực tiếp vào kết quả trả về (Observation):
- Nếu hệ thống đang bảo trì diện rộng Thông báo nhân viên chờ, không tạo ticket trùng.
- Nếu tài khoản bị khóa do sai mật khẩu Đề xuất mở khóa/reset tài khoản.
- Nếu không tự khắc phục được Mới chuyển sang bước tạo ticket và gán mức độ ưu tiên (Priority: High/Medium). |
| **4. Long Horizon Goal** | 4 / 5 | Quá trình tiếp nhận và xử lý sự cố thường kéo dài qua nhiều lượt hội thoại (Multi-turn). Agent phải duy trì ngữ cảnh xuyên suốt: mã nhân viên, mô tả lỗi ban đầu, các bước đã thử nghiệm thất bại cho đến khi đạt được mục tiêu cuối cùng: Sự cố được giải quyết hoặc xuất thành công mã Ticket ID cho người dùng. |
| **TỔNG ĐIỂM AGENTIC FIT** | **18/ 20** | *Điểm số 18/20 (> 12/20): Bài toán IT Helpdesk cực kỳ phù hợp và phát huy tối đa sức mạnh của mô hình ReAct Agent kết hợp MCP Tools.* |

---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Hãy tra cứu tình trạng ticket sự cố mạng có mã TK2026001 giúp tôi.",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "query_ticket",
    "arguments": {
      "ticket_id": "TK2026001"
    },
    "observation": {
      "status": "SUCCESS",
      "ticket_id": "TK2026001",
      "data": {
        "ticket_id": "TK2026001",
        "employee_id": "NV2026001",
        "employee_name": "Chu Minh Quân",
        "category": "Sự cố Mạng / VPN",
        "description": "Không thể kết nối mạng VPN nội bộ từ xa để truy cập máy chủ R&D.",
        "status": "Đang xử lý (In Progress)",
        "priority": "High",
        "created_at": "09:15 12/09/2026",
        "assigned_to": "Kỹ thuật viên Lê Hoàng Nam (IT Tier-2)"
      }
    },
    "latency_ms": 2425.02
  },
  {
    "step": 2,
    "query": "Hãy tra cứu tình trạng ticket sự cố mạng có mã TK2026001 giúp tôi.",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Thông tin ticket TK2026001: Nhân viên Chu Minh Quân (NV2026001), Phân loại sự cố: Sự cố Mạng / VPN, Mô tả: 'Không thể kết nối mạng VPN nội bộ từ xa để truy cập máy chủ R&D.', Trạng thái: Đang xử lý (In Progress), Mức độ: High, Phụ trách: Kỹ thuật viên Lê Hoàng Nam (IT Tier-2).",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [x] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Google Gemini: `gemini-3.6-flash`).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 / 4 lượt (TC02: `query_ticket`, TC03: `create_support_ticket`, TC04: `query_ticket`, TC05: `query_ticket`).
- **Kết quả đẩy Repo nộp bài:** [ ] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!

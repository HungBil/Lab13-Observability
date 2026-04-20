# Day 13 Observability Lab Report

> **Instruction**: Fill in all sections below. This report is designed to be parsed by an automated grading assistant. Ensure all tags (e.g., `[GROUP_NAME]`) are preserved.

## 1. Team Metadata
- [GROUP_NAME]: 
- [REPO_URL]: 
- [MEMBERS]:
  - Member A: [Name] | Role: Logging & PII
  - Member B: [Name] | Role: Tracing & Enrichment
  - Member C: [Name] | Role: SLO & Alerts
  - Member D: [Name] | Role: Load Test & Dashboard
  - Member E: [Name] | Role: Demo & Report

---

## 2. Group Performance (Auto-Verified)
- [VALIDATE_LOGS_FINAL_SCORE]: /100
- [TOTAL_TRACES_COUNT]: 
- [PII_LEAKS_FOUND]: 

---

## 3. Technical Evidence (Group)

### 3.1 Logging & Tracing
- [EVIDENCE_CORRELATION_ID_SCREENSHOT]: [Path to image]
- [EVIDENCE_PII_REDACTION_SCREENSHOT]: [Path to image]
- [EVIDENCE_TRACE_WATERFALL_SCREENSHOT]: [Path to image]
- [TRACE_WATERFALL_EXPLANATION]: (Briefly explain one interesting span in your trace)

### 3.2 Dashboard & SLOs
- [DASHBOARD_6_PANELS_SCREENSHOT]: [Path to image]
- [SLO_TABLE]:
| SLI | Target | Window | Current Value |
|---|---:|---|---:|
| Latency P95 | < 3000ms | 28d | |
| Error Rate | < 2% | 28d | |
| Cost Budget | < $2.5/day | 1d | |

### 3.3 Alerts & Runbook
- [ALERT_RULES_SCREENSHOT]: [Path to image]
- [SAMPLE_RUNBOOK_LINK]: [docs/alerts.md#L...]

---

## 4. Incident Response (Group)
- [SCENARIO_NAME]: rag_slow
- [SYMPTOMS_OBSERVED]: Khách hàng phản hồi thời gian trả lời chat (latency) tăng vọt. Trên load test, latency bình bình là ~800ms đã tăng lên khoảng ~5300ms.
- [ROOT_CAUSE_PROVED_BY]: Log ghi nhận `latency_ms` nhảy lên mức >2650ms ở sự kiện `response_sent`. Nhìn sâu vào Langfuse trace (nếu có instrument) hoặc source code, hàm `mock_rag.retrieve` bị chặn lại trong 2.5s bằng lệnh `time.sleep(2.5)`. Do API chỉ chạy 1 luồng xử lý đồng thời, request bị dồn ứ khiến khách hàng phải chờ hơn 5 giây.
- [FIX_ACTION]: Tắt cờ sự cố (`/incidents/rag_slow/disable`). 
- [PREVENTIVE_MEASURE]: Cài đặt timeout cứng cho API truy xuất (Vector DB), đồng thời cấu hình cảnh báo SLO cho P95 Latency để phát hiện sớm. Tối ưu hóa xử lý bất đồng bộ (async) cho I/O bound. 

---

## 5. Individual Contributions & Evidence

### [MEMBER_A_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: (Link to specific commit or PR)

### [MEMBER_B_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_C_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

### [MEMBER_D_NAME]
- [TASKS_COMPLETED]: 
  - Khởi chạy tải giả lập (Load Testing) bằng `scripts/load_test.py` với nhiều mức độ concurrency.
  - Kích hoạt sự cố `rag_slow` (Incident Injection) và phân tích nguyên nhân gốc rễ (RCA) dựa trên Logs và Metrics.
  - Tổng hợp dữ liệu và viết biên bản xử lý sự cố.
  - (Sắp tới) Demo toàn bộ quy trình cho giảng viên.
- [EVIDENCE_LINK]: Link pull request hoặc commit log mô tả load test & incident analysis. 

### [MEMBER_E_NAME]
- [TASKS_COMPLETED]: 
- [EVIDENCE_LINK]: 

---

## 6. Bonus Items (Optional)
- [BONUS_COST_OPTIMIZATION]: (Description + Evidence)
- [BONUS_AUDIT_LOGS]: (Description + Evidence)
- [BONUS_CUSTOM_METRIC]: (Description + Evidence)

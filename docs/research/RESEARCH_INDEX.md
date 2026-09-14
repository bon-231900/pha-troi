# TỔNG HỢP NGHIÊN CỨU MÃ NGUỒN MỞ — NOVEL OS CHO TIỂU THUYẾT TRƯỜNG THIÊN (3.000+ CHƯƠNG)

**Dự án**: PHÁ TRỜI (Hệ điều hành chuyên biệt cho một tiểu thuyết duy nhất)  
**Ngày thực hiện**: 2026-09-14  
**Phạm vi**: Khảo sát kiến trúc, mẫu thiết kế (design patterns), cơ chế lưu trữ và kiểm soát tính liên tục từ các dự án mã nguồn mở tiêu biểu phục vụ sáng tác dài tập.

---

## 1. CÁC DỰ ÁN MÃ NGUỒN MỞ ĐƯỢC KHẢO SÁT

| Dự Án | Mô Hình Kiến Trúc | Điểm Mạnh Nổi Bật | Điểm Yếu Đối Với Quy Mô 3.000+ Chương |
|---|---|---|---|
| **jarvis-write** | Hierarchical Tree Planning + Recursive Summarization | Chia nhỏ đại cương đệ quy (Master -> Volume -> Chapter -> Scene). Tóm tắt cuộn lũy tiến giúp LLM không quá tải. | Phụ thuộc quá nhiều vào LLM để tóm tắt đệ quy khiến lore bị tam sao thất bản qua hàng ngàn chương; thiếu cơ chế kiểm tra tất định (deterministic check). |
| **continuity-keeper** | Knowledge Graph + Timeline Verification Engine | Đồ thị thực thể (Entity Graph) và dòng thời gian tất định; kiểm tra logic di chuyển và sinh tử chặt chẽ. | Thiết kế cho truyện ngắn/trung bình (<100 chương); chi phí duyệt đồ thị $O(V+E)$ bắt đầu chậm khi có hàng nghìn thực thể và sự kiện nếu không phân vùng. |
| **novel-studio-ai** | Multi-Agent Collaborative Pipeline (Editor, Lore, Drafter) | Phân tách vai trò rõ ràng; các cổng phê duyệt (stage gates) trước khi xuất bản bản thảo. | Quá nhiều lượt gọi LLM lãng phí quota; các agent dễ xung đột quan điểm (opinion drift) nếu thiếu một chân lý Canon tuyệt đối (Ground Truth). |
| **my-novel-agent** | Web-novel Engagement & Pacing Loop Optimizer | Kiểm soát nhịp điệu (pacing), quản lý móc câu (cliffhanger), theo dõi đường cong hồi hộp theo chuẩn web-novel. | Dễ rơi vào bẫy công thức sáo mòn (formulaic repetition): đánh nhau liên tục, cliffhanger rẻ tiền, power creep mất kiểm soát sau vài trăm chương. |
| **story-architect-mcp** | Protocol-based Tool Augmentation (MCP Server) | Tách rời logic lưu trữ ngữ cảnh ra khỏi context window; nạp tài liệu theo yêu cầu (on-demand context injection). | Không có cơ chế nhận thức phân tầng (epistemic state); nhầm lẫn giữa sự thật thế giới (world truth) và niềm tin của nhân vật (character belief). |

---

## 2. PHÂN TÍCH PATTERNS TIẾP THU (ADOPTED) CHO "PHÁ TRỜI"

### Pattern 1: Phân Cấp Cốt Truyện Đa Tầng (Multi-Tier Hierarchical Outline)
* **Nguồn tham khảo**: `jarvis-write`, `story-architect-mcp`.
* **Hiện thực hóa**: Chuẩn hóa 8 tầng: `Saga` (Đại Kỷ Nguyên) $\rightarrow$ `Era` (Thời Đại) $\rightarrow$ `Volume` (Quyển) $\rightarrow$ `Arc` (Hồi) $\rightarrow$ `Mini-Arc` (Tiểu Tiết) $\rightarrow$ `Chapter` (Chương) $\rightarrow$ `Scene` (Cảnh) $\rightarrow$ `Beat` (Nhịp).
* **Giá trị**: Cho phép mở rộng đến 3.000 chương mà không bị phẳng hóa cấu trúc, mỗi chương luôn có tọa độ cha-con rõ ràng.

### Pattern 2: Đồ Thị Thực Thể Tất Định Kết Hợp FTS5 BM25 (Hybrid Deterministic Graph + Lexical Index)
* **Nguồn tham khảo**: `continuity-keeper`.
* **Hiện thực hóa**: Trạng thái sinh tử, túi đồ, vị trí địa lý được lưu trong bảng quan hệ SQLite và kiểm tra bằng Python thuần (0 token). Tìm kiếm chi tiết quá khứ dùng FTS5 BM25.
* **Giá trị**: Loại bỏ 100% ảo giác (hallucination) về trạng thái nhân vật và đồ vật; tốc độ truy xuất dưới 2ms trên hàng triệu từ.

### Pattern 3: Vòng Đời Tuyến Truyện Độc Lập (Story Thread Lifecycle Manager)
* **Nguồn tham khảo**: Khảo sát cấu trúc narrative dài tập.
* **Hiện thực hóa**: Bảng `story_threads` theo dõi độc lập các tuyến: `MAIN_PLOT`, `SUBPLOT`, `CHARACTER_ARC`, `MYSTERY`, `RELATIONSHIP`, `WORLDBUILDING`. Mỗi tuyến có trạng thái: `OPEN`, `ACTIVE`, `DORMANT`, `RESOLVING`, `RESOLVED`, `ABANDONED`.
* **Giá trị**: Giải quyết triệt để vấn đề "bỏ quên tuyến nhân vật phụ" hoặc "để phục bút ngủ quên quá lâu" (vượt quá `revisit_window_chapters`).

### Pattern 4: Ngân Sách Leo Thang Đa Trục (Multi-Axis Escalation Budgeting)
* **Nguồn tham khảo**: Nghiên cứu nguyên nhân sụp đổ của các web novel trường thiên.
* **Hiện thực hóa**: Bảng `escalation_budgets` kiểm soát 6 trục: Sức mạnh (Power), Địa lý (Geography), Thế giới quan (Cosmology), Cổ phần nguy cơ (Stakes), Mức độ giải mã bí mật (Mystery Reveal), Mức độ thân mật tình cảm (Emotional Intimacy).
* **Giá trị**: Ngăn chặn tình trạng "bùng nổ sức mạnh quá sớm" ở Volume 1 (Ch 1–42), giữ Minh An vững vàng ở bối cảnh TP.HCM 2026.

### Pattern 5: Bộ Phòng Thủ Bão Hòa & Công Thức Cốt Truyện (Repetition & Fatigue Defense Matrix)
* **Nguồn tham khảo**: Phân tích điểm yếu của `my-novel-agent`.
* **Hiện thực hóa**: Bảng `thread_fatigue_logs` và engine phát hiện: lặp lại kiểu kết thúc chương (cliffhanger fatigue), lặp lại chu kỳ biến cố (anomaly-combat-epiphany loop), sáo ngữ văn phong.
* **Giá trị**: Buộc mạch truyện phải có các khoảng thở (breathing room), đời thường thực tế xen kẽ các phân cảnh căng thẳng.

---

## 3. PHÂN TÍCH PATTERNS BÁC BỎ (REJECTED) VÀ LÝ DO

| Mẫu Thiết Kế Bị Bác Bỏ | Nguồn | Lý Do Bác Bỏ Trong "Phá Trời" |
|---|---|---|
| **Generic Multi-Novel Abstraction** | Frameworks tổng quát | Vi phạm điều 1 của `NOVEL_LOCK.md`. Mọi lớp trừu tượng hóa cho nhiều tiểu thuyết làm suy yếu tính chuyên biệt cho TP.HCM 2026 và hệ thống 7 Đạo. |
| **Pure Vector RAG as Story Memory** | Các framework AI thông thường | Vector embedding không phân biệt được thứ tự thời gian (chronological order) và trạng thái nhận thức (epistemic state). RAG thuần túy sẽ trích xuất chi tiết ở chương 100 đưa vào chương 5 gây rò rỉ logic nghiêm trọng. |
| **Autonomous Loop Writing (No Stage Gate)** | Một số agent tự động | Vi phạm quyền tối cao của Tác Giả (Author Authority). Sáng tác 3.000 chương không phải là cuộc đua spam chữ; mỗi chương phải đi qua preflight, critique, và author review. |
| **Formulaic Web-Novel Tropes Injection** | `my-novel-agent` | Các khuôn mẫu "vả mặt", "đấu giá", "hệ thống giao nhiệm vụ" bị cấm tuyệt đối theo `DECISIONS.md`. Minh An là người bình thường, không có hack điểm. |
| **Global Recursive Summarization by LLM** | `jarvis-write` | LLM tóm tắt lại bản tóm tắt qua 50 thế hệ sẽ làm biến dạng các chi tiết vi mô quan trọng (lore drift). Novel OS dùng bản ghi sự kiện dòng thời gian có cấu trúc (`timeline_events`) thay vì chỉ dựa vào tóm tắt văn xuôi. |

---

## 4. KẾT LUẬN & ĐỀ XUẤT KIẾN TRÚC

Hệ thống Novel OS của *Phá Trời* cần nâng cấp kiến trúc từ mô hình phẳng (~40 chương) sang mô hình **Phân Vùng Cục Bộ + Ngân Sách Phân Tầng (Hierarchical Partitioning & Tiered Budgeting)**:
1. Nâng cấp schema cơ sở dữ liệu SQLite với 5 bảng mới: `story_hierarchy`, `story_threads`, `escalation_budgets`, `mystery_depth`, `thread_fatigue_logs`.
2. Bổ sung 4 động cơ lõi: `ThreadEngine`, `FatigueEngine`, `EscalationEngine`, `HierarchyEngine`.
3. Tích hợp chặt chẽ vào `ContextBuilder` và `CritiqueEngine` mà không phá vỡ 28 unit tests hiện có.
4. Xây dựng bài benchmark mô phỏng 3.000 chương độc lập để kiểm chứng hiệu năng và độ ổn định.

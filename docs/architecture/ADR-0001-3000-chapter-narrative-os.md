# ADR-0001: KIẾN TRÚC VẬN HÀNH TIỂU THUYẾT TRƯỜNG THIÊN 3.000+ CHƯƠNG (NOVEL OS UPGRADE)

* **Trạng thái**: ĐÃ DUYỆT (APPROVED)
* **Ngày quyết định**: 2026-09-14
* **Tác giả kiến trúc**: Antigravity Core & Author Direction
* **Phạm vi tác động**: Toàn bộ hệ thống lõi `system/engines/`, `database/novel_os.db`, quy trình Preflight và Critique.

---

## 1. BỐI CẢNH & VẤN ĐỀ (CONTEXT)

Tiểu thuyết *Phá Trời* đã hoàn thành 42 chương đầu tiên (107.288 từ) thuộc Quyển 1 / Hồi 1.
Kiến trúc ban đầu của Novel OS được thiết kế cho quy mô ~40–100 chương với bảng `plot_nodes` phẳng, ma trận nhận thức 2 chiều đơn giản, và phục bút cục bộ.

Khi quy mô hướng tới **3.000+ chương**, hệ thống đối mặt với 6 điểm nghẽn chí mạng (Bottlenecks):
1. **Phẳng hóa cấu trúc cốt truyện**: Bảng `plot_nodes` không phân định rõ ràng giữa Đại Kỷ Nguyên, Thời Đại, Quyển, Hồi, dẫn đến việc mất phương hướng vĩ mô.
2. **Thất lạc tuyến truyện (Thread Amnesia)**: Các tuyến nhân vật phụ, tuyến tình cảm, tuyến điều tra và thế lực bị phân tán, không có cửa sổ cảnh báo "tuyến bị bỏ quên" (`revisit_window_chapters`).
3. **Bùng nổ quy mô mất kiểm soát (Escalation Creep)**: Sức mạnh, địa lý và thế giới quan tăng tốc quá nhanh (như đã thấy dấu hiệu ở Ch 35–42), đe dọa phá vỡ tính chân thực của TP.HCM 2026.
4. **Bão hòa công thức tự sự (Narrative Fatigue)**: Nguy cơ lặp lại chu kỳ "phát hiện dị tượng $\rightarrow$ giải thích kỹ thuật $\rightarrow$ chạm trán nguy hiểm $\rightarrow$ kết thúc cliffhanger" gây nhàm chán cho độc giả dài hạn.
5. **Nhầm lẫn giữa bí mật và nhận thức**: Chưa có sự tách bạch rõ rệt giữa: *Sự Thật Thế Giới (World Truth)*, *Nhân Vật Tin (Character Belief)*, *Nhân Vật Nghi Ngờ (Character Suspicion)*, và *Độc Giả Biết (Reader Knowledge)*.
6. **Chi phí context window**: Nạp toàn bộ dữ liệu vào LLM sẽ làm bùng nổ token hoặc làm loãng sự tập trung.

---

## 2. QUYẾT ĐỊNH KIẾN TRÚC (DECISION)

Nâng cấp toàn diện Novel OS với 6 thành phần cốt lõi:

### 2.1. Phân Cấp 8 Tầng (8-Tier Story Hierarchy)
Thay thế quan hệ phẳng bằng bảng `story_hierarchy`:
$$\text{Saga} \rightarrow \text{Era} \rightarrow \text{Volume} \rightarrow \text{Arc} \rightarrow \text{Mini-Arc} \rightarrow \text{Chapter} \rightarrow \text{Scene} \rightarrow \text{Beat}$$
Mỗi tầng lưu trữ mục tiêu, cổ phần (stakes), tóm tắt lũy tiến và trạng thái phê duyệt.

### 2.2. Động Cơ Tuyến Truyện Độc Lập (Dedicated Story Thread Engine)
Bổ sung bảng `story_threads` theo dõi 6 loại tuyến truyện (`MAIN_PLOT`, `SUBPLOT`, `CHARACTER_ARC`, `MYSTERY`, `RELATIONSHIP`, `WORLDBUILDING`). Thiết lập cơ chế phát hiện tuyến ngủ quên (`audit_dormant_threads`) với ngưỡng `revisit_window_chapters` mặc định là 15 chương.

### 2.3. Ngân Sách Leo Thang Đa Trục (Multi-Axis Escalation Budget Controller)
Bổ sung bảng `escalation_budgets` kiểm soát 6 trục:
1. `POWER_CEILING`: Giới hạn mức độ bộc lộ sức mạnh và cảnh giới tại từng Hồi/Quyển.
2. `GEOGRAPHY_SCALE`: Phạm vi di chuyển địa lý (Bình Thạnh/Sài Gòn $\rightarrow$ Miền Nam $\rightarrow$ Việt Nam $\rightarrow$ Quốc tế $\rightarrow$ Vũ trụ).
3. `COSMOLOGY_DEPTH`: Mức độ tiếp cận bản chất vũ trụ 7 Đạo và đại chiến viễn cổ.
4. `STAKES_LEVEL`: Tầm ảnh hưởng của xung đột (Cá nhân $\rightarrow$ Bạn bè $\rightarrow$ Khu vực $\rightarrow$ Thế giới).
5. `MYSTERY_REVEAL`: Tầng giải mã bí mật được phép hé lộ.
6. `EMOTIONAL_INTIMACY`: Tốc độ phát triển tình cảm Minh An & Lâm Tịch (bảo đảm tính chất Extremely Slow Burn).
Mỗi trục có mức trần (`allowed_ceiling`) và thời gian làm nguội (`cooldown_chapters`).

### 2.4. Ma Trận Chiều Sâu Bí Mật 4 Tầng (4-Layer Mystery Depth Matrix)
Bổ sung bảng `mystery_depth` phân định:
- **Tầng 1 (Surface)**: Lời đồn, hiện tượng bề mặt mà công chúng/nhân vật cấp thấp nhìn thấy.
- **Tầng 2 (Intermediate)**: Lớp cơ chế kỹ thuật mà khảo sát ban đầu phát hiện được.
- **Tầng 3 (Deep)**: Bản chất quy tắc cổ xưa và sự thật lịch sử của Trái Đất bị phong ấn.
- **Tầng 4 (Ultimate Truth)**: Chân tướng tối hậu chỉ có trong Vault của Author.

### 2.5. Ma Trận Phòng Thủ Bão Hòa & Sáo Ngữ (Fatigue Defense Matrix)
Bổ sung bảng `thread_fatigue_logs` và `FatigueEngine` phát hiện tất định:
- Lặp lại công thức kết chương giật gân (Cliffhanger Fatigue).
- Lặp lại chu kỳ tình huống (Anomaly loop).
- Sáo ngữ cử chỉ, biểu cảm ("hít sâu một hơi", "đồng tử co rụt", "trong lòng run lên").

### 2.6. Tách Biệt Nhận Thức 4 Chiều (4-Tier Epistemic Separation)
Mở rộng `KnowledgeEngine` để theo dõi rõ ràng:
- `WORLD_TRUTH`: Quy luật khách quan của vũ trụ.
- `CHARACTER_BELIEF`: Điều nhân vật tin là thật (có thể sai lệch).
- `CHARACTER_SUSPICION`: Điều nhân vật nghi ngờ nhưng chưa dám khẳng định.
- `READER_KNOWLEDGE`: Những gì độc giả đã được tiết lộ qua POV của các nhân vật khác.

---

## 3. HỆ QUẢ (CONSEQUENCES)

### Điểm Tích Cực:
* **Khả năng mở rộng bền vững**: Hệ thống có thể xử lý 3.000 chương với thời gian phản hồi dưới 10ms trên mỗi truy vấn SQLite.
* **Bảo vệ Canon tuyệt đối**: Các quyết định trong `DECISIONS.md` được rào chắn bằng mã nguồn tất định, ngăn chặn hoàn toàn AI tự ý buff sức mạnh hoặc đốt cháy giai đoạn tình cảm.
* **Tối ưu hóa tài nguyên**: Giữ vững ngân sách token $O(1)$ cho mỗi chương viết mới thông qua Context Pack tinh gọn.

### Đánh Đổi (Trade-offs):
* Khâu chuẩn bị đại cương trước mỗi Hồi đòi hỏi định nghĩa rõ ràng các tuyến truyện và ngân sách leo thang.
* Preflight check trước mỗi chương cần thực hiện thêm bước đối chiếu ngân sách leo thang và kiểm tra nguy cơ bão hòa công thức.

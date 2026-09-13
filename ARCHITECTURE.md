# KIẾN TRÚC NOVEL OS CHO “PHÁ TRỜI”

## 1. Triết Lý Thiết Kế
1. **Single-Novel Dedicated Engine**: Không có lớp trừu tượng thừa. Tối ưu 100% cho cấu trúc vũ trụ, hệ thống tu luyện và bối cảnh TP.HCM 2026 của *Phá Trời*.
2. **Local-First & Data Durability**: Dữ liệu hoàn toàn trên máy cục bộ (`D:\tieu-thuyet`). Không phụ thuộc vào cloud AI service để lưu trữ state.
3. **Air-Gapped Author Secret Vault**: Thư mục `author_secret/` được cô lập logic ở cấp độ mã nguồn. Không một truy vấn retrieval thông thường nào cho văn bản draft được phép truy cập vào vault này.
4. **Epistemic State Tracking**: Nhận thức của nhân vật được theo dõi đa trạng thái: `KNOWN`, `SUSPECTED`, `BELIEVED`, `MISUNDERSTOOD`, `FALSE_BELIEF`, `UNKNOWN`, `FORGOTTEN`.

## 2. 17 Động Cơ Lõi (Core Engines)
- **CanonEngine**: Phân cấp 6 trạng thái (`LOCKED`, `CONFIRMED`, `PROVISIONAL`, `UNKNOWN`, `FORBIDDEN_ASSUMPTION`, `PROPOSED`).
- **WorldEngine**: Mô hình hóa vũ trụ theo đồ thị phân cấp từ *Đại Đại Giới -> Các Vực -> Các Tinh Hải -> Các Vị Diện -> Thế Giới -> Trái Đất*.
- **CharacterEngine**: Quản lý profile, thương tổn thể xác, linh hồn, túi đồ (inventory) và mục tiêu nhân vật.
- **KnowledgeEngine**: Kiểm soát phát ngôn nhân vật dựa trên ma trận nhận thức.
- **PowerEngine**: Quản lý 7 Đạo tu luyện chính và Khí Huyết Đạo trên Trái Đất. Chặn quy tắc "cảnh giới cao auto thắng".
- **TimelineEngine**: Dòng thời gian tuyệt đối & tương đối, kiểm soát sự kiện song song, tốc độ di chuyển giữa các địa điểm.
- **ForeshadowingEngine**: Quản lý sổ cái phục bút (Setup - Clue - Payoff) qua hàng ngàn chương.
- **ContextBuilder**: Lọc và đóng gói gói ngữ cảnh tối ưu theo ngân sách token (`minimal + relevant + sufficient`).
- **CoAuthorEngine**: Triển khai hợp đồng "Viết tiếp" với khả năng tự đưa ra quyết định sáng tạo hợp canon.
- **SelfCritiqueEngine**: Tự phản biện 11 chiều (Canon, Character, POV, Timeline, Location, Power, Relationship, Foreshadowing, Style, Narrative, Research).
- **RevisionEngine**: Sửa chữa chính xác theo phạm vi (câu, đoạn, cảnh, chương).
- **DocxPipeline**: Trình xuất file Word tự động theo quy chuẩn xuất bản sách.
- **ResearchVault**: Kho lưu trữ nghiên cứu đời thực (TP.HCM 2026, khoa học), phân định rõ ràng `RESEARCH != CANON`.
- **ProposalManager**: Cơ chế đề xuất ý tưởng lớn và chờ Author phê duyệt.
- **RelationshipEngine**: Theo dõi ma trận cảm xúc và lịch sử tương tác giữa các nhân vật.
- **PlotGraphEngine**: Quản lý cây cốt truyện (Master -> Volume -> Arc -> Chapter -> Scene).
- **NarrativeTestRunner**: Bộ kiểm thử tự động 20 tình huống phá vỡ continuity.

# -*- coding: utf-8 -*-
"""
Novel OS — Bootstrap Chapters 1-22 Fixture
Tách biệt dữ liệu mẫu hạt nhân của 22 chương đầu ra khỏi CoAuthorEngine.
"""
import sqlite3
import json

def apply_bootstrap_chapter(db_path: str, chapter_num: int):
    conn = sqlite3.connect(db_path, timeout=30.0)
    cur = conn.cursor()
    if chapter_num == 1:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Cơn mưa rào ngã tư Hàng Xanh và khoảnh khắc tàn hồn rơi", chapter_num, 1,
                     "2026-09-13T18:00:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Minh An tan sở trú mưa ở Ung Văn Khiêm, bị tàn hồn Lâm Tịch rơi trúng thức hải, trải qua cơn đau nhói và thoáng thấy ảo ảnh chiến trường viễn cổ.",
                     "Lâm Tịch hoàn tất neo đậu vào thức hải Minh An; Minh An ngỡ là trúng gió cảm mạo."))
    elif chapter_num == 2:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Thanh âm đầu tiên trong căn phòng trọ Bình Thạnh", chapter_num, 1,
                     "2026-09-13T20:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Minh An về phòng trọ sau mưa ngập, cảm nhận hàn ý và thấy đốm tro tàn trong mắt. Tàn hồn Lâm Tịch cất tiếng hỏi, xác nhận cảnh tượng biển máu là thật trước khi ngủ say.",
                     "Minh An xác định không phải bệnh lý tâm thần; thiết lập liên kết ý thức sơ khởi giữa hai người."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 2, "Phòng trọ Bình Thạnh", "Phàm nhân", "Bình thường, hơi lạnh sau gáy và bàn tay",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ"], ensure_ascii=False),
                     "Căng thẳng cảnh giác, bàng hoàng nhưng giữ được bình tĩnh"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 2, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Cảnh giác, kiêu hãnh nhưng mệt mỏi cùng cực, chìm vào ngủ say"))
        
        # Foreshadowing seed FSH-002
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-002", "Đốm tro tàn thoáng hiện trong đồng tử và hiện tượng sương giá ngưng đọng quanh cốc nước", 2, 1,
                     json.dumps(["Minh An"], ensure_ascii=False),
                     "Dấu hiệu nguyên thần Lâm Tịch vô thức rò rỉ hàn khí quy tắc ra môi trường xung quanh Minh An", 5, "PLANTED"))
    elif chapter_num == 3:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Đêm trắng đầu tiên và nhịp thở chia sẻ", chapter_num, 1,
                     "2026-09-14T03:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Minh An trải qua một đêm trắng tìm kiếm thông tin y khoa, nhận thức được sự hiện diện yếu ớt của Lâm Tịch. Nhịp tim và khí huyết phàm nhân vô thức che chở cho đốm lửa tàn. Sáng sớm, Minh An vẫn phải mặc áo sơ mi đi làm mưu sinh.",
                     "Minh An chấp nhận thực tại siêu nhiên nhưng giữ vững cuộc sống đời thường; bước đầu hình thành sự cộng hưởng khí huyết tự nhiên."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 3, "Phòng trọ Bình Thạnh -> Đi làm", "Phàm nhân", "Thiếu ngủ, mắt hơi thâm quầng nhưng tinh thần tĩnh táo khác thường",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Cà phê gói"], ensure_ascii=False),
                     "Trầm tĩnh, chấp nhận thực tế, kiên định"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 3, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Ngủ sâu bảo tồn nguyên thần, an tĩnh"))
        
        # Foreshadowing seed FSH-003
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-003", "Khí huyết sinh học của cơ thể phàm nhân vô thức nuôi dưỡng ngọn lửa tàn của nguyên thần viễn cổ", 3, 1,
                     json.dumps(["Minh An"], ensure_ascii=False),
                     "Nguyên lý sơ khai của con đường Khí Huyết Đạo tại Trái Đất bị phong ấn", 12, "PLANTED"))
    elif chapter_num == 4:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Bản hòa âm trần thế và tiếng vọng giữa trưa hè", chapter_num, 1,
                     "2026-09-14T12:15:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Minh An hòa vào nhịp sống công sở hối hả tại Quận 1, trải nghiệm sự tương phản giữa thực tại cơm áo gạo tiền và cõi sâu tâm thức. Buổi trưa tại quán cơm tấm, hạt băng bất ngờ ngưng kết trên thành cốc trà đá khi Lâm Tịch khẽ thức giấc đặt câu hỏi về nhân gian ồn ào.",
                     "Minh An giữ vững tâm tính phàm trần điềm tĩnh; sự hiện diện của Lâm Tịch dần hòa nhập vào trải nghiệm cảm quan đời thường mà không làm đảo lộn trật tự xã hội."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 4, "Văn phòng Quận 1 -> Quán cơm tấm hẻm Nguyễn Thị Minh Khai", "Phàm nhân", "Khí huyết dồi dào nhẹ, phản xạ nhanh nhạy hơn, thể lực ổn định",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Laptop công ty"], ensure_ascii=False),
                     "Điềm tĩnh, quan sát sâu sắc, thấu cảm"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 4, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Hiếu kỳ yếu ớt, ngạc nhiên trước trần thế không có linh khí, lại chìm vào giấc ngủ"))
        
        # Foreshadowing seed FSH-004
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-004", "Quy tắc hàn băng vi mô phát sinh tại môi trường nhiệt độ cao (giọt nước ngưng băng trên cốc trà đá giữa trưa)", 4, 1,
                     json.dumps(["Minh An"], ensure_ascii=False),
                     "Quy tắc Băng Phách của Lâm Tịch bắt đầu có hiện tượng rò rỉ thụ động ra vật chất ngoại cảnh khi nàng chuyển mình ý thức", 7, "PLANTED"))
    elif chapter_num == 5:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Cuộc đối thoại dưới ánh đèn đêm và lời giới thiệu tên họ", chapter_num, 1,
                     "2026-09-14T21:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Minh An trở về phòng trọ sau ngày làm việc. Trong đêm tĩnh mịch, Lâm Tịch tỉnh giấc lâu hơn, chính thức giới thiệu danh tự của mình và giải thích về đạo cơ vỡ nát cùng nguyên nhân hàn khí rò rỉ. Hai người chia sẻ góc nhìn về nhân sinh ngắn ngủi của phàm nhân và sự tịch diệt của chư thiên vị diện.",
                     "Hoàn tất thu hồi phục bút FSH-002; xác lập liên kết nhận thức sâu sắc giữa Minh An và Lâm Tịch; gieo mầm phục bút FSH-005 về thảm họa Phá Trời."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 5, "Phòng trọ Bình Thạnh", "Phàm nhân", "Khí huyết lưu chuyển hài hòa, bắt đầu có cảm ứng vi mô với nhiệt độ và sinh mệnh lực xung quanh",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Cốc trà sứ"], ensure_ascii=False),
                     "Trầm lắng, thấu cảm sâu sắc, bắt đầu gánh vác trọng trách vô hình"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 5, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Bớt cảnh giác, chấp nhận nương tựa, thoáng ngậm ngùi trước triết lý nhân gian"))
        
        # Payoff FSH-002
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-002'""")

        # Foreshadowing seed FSH-005
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-005", "Lời nhắc mơ hồ của Lâm Tịch về 'Bầu trời bị tha hóa' và thanh kiếm gãy chém đứt quy tắc", 5, 1,
                     json.dumps(["Minh An"], ensure_ascii=False),
                     "Bản chất của thảm họa diệt thế chư thiên: Thiên Đạo sinh ra ý chí độc hại nuốt chửng các vị diện", 20, "PLANTED"))
    elif chapter_num == 6:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Ngọn lửa dưới làn da và sự thật về Cố Thổ Khí Huyết", chapter_num, 1,
                     "2026-09-15T06:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Sáng sớm ngày thứ ba, Minh An phát hiện thể lực và phản xạ được củng cố tự nhiên. Lâm Tịch kinh ngạc nhận diện Trái Đất chính là Cố Thổ bị phong ấn của Khí Huyết Đạo từ thời viễn cổ. Minh An xác lập nhận thức bước đầu về con đường tôi luyện thể phách bằng ý chí.",
                     "Đánh thức tri thức cổ xưa về Khí Huyết Đạo; Minh An chấp nhận tôi rèn thể chất mà không dựa dẫm vào đường tắt; gieo mầm phục bút FSH-006 về phong ấn cổ xưa của Trái Đất."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 6, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Cảm ứng Khí Huyết vi mô)", "Thể lực tăng tiến, cơ bắp săn chắc nhẹ, hô hấp dài sâu, tinh thần minh mẫn",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ"], ensure_ascii=False),
                     "Tự tin, kiên định, bắt đầu có ý thức rèn luyện bản thân"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 6, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn cực độ suy kiệt, thân thể đã tan rã",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Kinh ngạc trước bí mật Cố Thổ, bắt đầu đóng vai trò người chỉ dẫn định hướng tinh thần"))
        
        # Foreshadowing seed FSH-006
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-006", "Nhận định của Lâm Tịch về Trái Đất là Cố Thổ cội nguồn của Khí Huyết Đạo viễn cổ bị phong ấn cô lập", 6, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Trái Đất vốn là cái nôi của Thể Đạo; phong ấn viễn cổ thực chất là bức tường thành bảo vệ nhân loại khỏi sự lây nhiễm của Thiên Đạo tha hóa", 25, "PLANTED"))
    elif chapter_num == 7:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Hàn ý giữa chảo lửa và phản xạ bảo vệ của Băng Phách", chapter_num, 1,
                     "2026-09-15T15:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Chiều 15/09/2026, Quận 1 nắng rát 37°C. Tại quán giải khát đông đúc giờ giải lao, sự cố bình nước sôi hất đổ hướng thẳng vào Minh An và đồng nghiệp. Quy tắc Băng Phách từ tàn hồn Lâm Tịch trong thức hải tự phát kích hoạt theo bản năng bảo hộ sinh mệnh cộng sinh, hạ nhiệt tức thì khối chất lỏng bỏng rát thành làn sương khói mát lạnh trong tích tắc, giải cứu cả hai người an toàn.",
                     "Hoàn tất thu hồi phục bút FSH-004 và FSH-001; xác nhận mối quan hệ cộng sinh hai chiều: Minh An dùng khí huyết phàm nhân nuôi dưỡng tàn hồn nàng, còn quy tắc của Lâm Tịch phản xạ che chắn hiểm nguy cho Minh An; gieo mầm phục bút FSH-007 về sự biến thiên nhiệt độ vật lý cục bộ."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 7, "Tòa nhà văn phòng & khu vực Nguyễn Huệ, Quận 1", "Phàm nhân (Thể phách ngưng luyện sơ bộ)", "Khí huyết sung mãn, thần kinh phản xạ nhạy bén, không hề bị tổn thương do nước sôi",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Cốc trà sữa"], ensure_ascii=False),
                     "Kinh ngạc, sau đó là sự thấu hiểu và gắn kết sâu sắc với Lâm Tịch"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 7, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn tiêu hao thêm một tia thần niệm sau phản xạ bảo vệ, nhưng được khí huyết ấm áp của Minh An ổn định tức thì",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Hơi mệt mỏi nhưng thanh thản, lần đầu gọi tên Minh An, thừa nhận mối quan hệ đồng hành sinh tử"))
        
        # Payoff FSH-001 & FSH-004
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id IN ('FSH-001', 'FSH-004')""")

        # Foreshadowing seed FSH-007
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-007", "Sự biến thiên nhiệt độ đột ngột tại hiện trường Quận 1 bị camera an ninh và cảm biến nhiệt môi trường ghi nhận", 7, 1,
                     json.dumps(["Minh An", "Bộ phận kỹ thuật tòa nhà"], ensure_ascii=False),
                     "Hiện tượng bất thường phi vật lý đầu tiên để lại dấu vết công nghệ ở thế giới hiện đại, đặt tiền đề cho các cơ quan nghiên cứu chú ý", 15, "PLANTED"))
    elif chapter_num == 8:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Tĩnh khí dưới mái tôn và bài học nhập môn Khí Huyết", chapter_num, 1,
                     "2026-09-15T21:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Tối 15/09/2026, Sài Gòn đổ mưa rào sau ngày nắng gắt. Minh An trở về phòng trọ, mua thức ăn bồi bổ thể lực. Dưới tiếng mưa rào trên mái tôn, Lâm Tịch chỉ dẫn cho anh phương pháp điều tức sơ đẳng 'Tĩnh Khí Quy Nguyên' để chủ động vận chuyển dòng máu và dưỡng chất. Minh An lần đầu cảm nhận sự ấm nóng lưu thông khắp kinh lạc phàm trần và phát hiện một màng ngăn vi mô trong xương tủy.",
                     "Chuyển hóa mối quan hệ cộng sinh từ bị động sang chủ động tương trợ; Minh An nắm bắt phương pháp dưỡng khí sơ cấp; gieo mầm phục bút FSH-008 về xiềng xích di truyền viễn cổ phong ấn tiềm năng nhân loại."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 8, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Nội luyện Khí Huyết sơ cấp)", "Cơ bắp thả lỏng hoàn toàn, hơi thở sâu và chậm, các giác quan thính giác và thị giác tinh tường, xuất hiện dòng nhiệt ấm áp tại đan điền",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Túi cam tươi"], ensure_ascii=False),
                     "Trầm tĩnh, tập trung cao độ, trân trọng từng nhịp thở và sự đồng hành của Lâm Tịch"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 8, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn kiệt sức)", "Tàn hồn được dưỡng ấm bởi khí huyết chủ động của Minh An, trạng thái chập chờn bắt đầu ổn định trở lại",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Bất ngờ trước khả năng ngộ tính phàm trần của Minh An, phong thái người dẫn đường cổ xưa dần hình thành tự nhiên"))
        
        # Foreshadowing seed FSH-008
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-008", "Cảm giác nghẽn tắc vi mô như màng đá vôi vô hình sâu trong tủy sống khi Minh An vận hành hơi thở sâu", 8, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Xiềng xích thể phách di truyền do trận đại chiến viễn cổ phong tỏa nhân loại Trái Đất, muốn vượt qua phải dùng ý chí đúc rèn khí huyết phá vỡ gông cùm", 18, "PLANTED"))
    elif chapter_num == 9:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Ánh bình minh bên dòng kênh và chiêm nghiệm giữa hai thế giới", chapter_num, 1,
                     "2026-09-16T06:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Sáng 16/09/2026, Minh An dậy sớm chạy bộ dọc bờ kênh Nhiêu Lộc - Thị Nghè, áp dụng nhịp thở Tĩnh Khí Quy Nguyên vào vận động thể thao thực tế. Lâm Tịch tỉnh giấc, quan sát đời sống bình dị và sự hòa hợp của con người Sài Gòn, chiêm nghiệm về sự đối lập giữa tu chân tàn khốc và nhân đạo ấm áp. Trên đường đi làm qua Quận 1, Minh An bắt gặp xe kiểm định kỹ thuật đang rà soát khu vực quán trà sữa.",
                     "Thể phách Minh An đạt tới trạng thái dẻo dai vượt trội so với người thường; tàn hồn Lâm Tịch ngưng tụ thành hình bóng mờ ảo sơ khai; gieo mầm phục bút FSH-009 về kiếm ngân trên tay áo hư ảnh."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 9, "Bờ kênh Nhiêu Lộc -> Văn phòng Quận 1", "Phàm nhân (Nội luyện Khí Huyết sơ cấp)", "Thể lực sung mãn, cơ bắp dẻo dai, nhịp thở sâu dài, hoàn toàn thích ứng với nhịp vận động cao",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Giày chạy bộ", "Thẻ nhân viên"], ensure_ascii=False),
                     "Thanh thản, tự tin, quan sát sâu sắc, trân trọng cuộc sống đời thường"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 9, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn ngưng tụ sơ khai)", "Tàn hồn thoát khỏi trạng thái tro tàn vô định, bắt đầu ngưng tụ phác thảo bóng dáng thiếu nữ áo choàng xám bạc",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Trầm tư trước vẻ đẹp bình dị của nhân gian, cảm nhận sự an toàn sâu sắc trong thức hải Minh An"))
        
        # Foreshadowing seed FSH-009
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-009", "Hoa văn kiếm ngân mờ ảo xuất hiện trên tay áo của bóng dáng tàn hồn Lâm Tịch trong thức hải", 9, 1,
                     json.dumps(["Minh An"], ensure_ascii=False),
                     "Dấu hiệu nguyên thần bắt đầu khôi phục năng lực bản mệnh kiếm ý, chuẩn bị cho khả năng hiển hóa hư ảnh trợ chiến trong tình thế hiểm nghèo", 22, "PLANTED"))
    elif chapter_num == 10:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Dòng sông Sài Gòn và sự khai sáng ý niệm Khí Huyết", chapter_num, 1,
                     "2026-09-16T13:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Trưa và chiều 16/09/2026. Minh An xử lý công việc văn phòng với hiệu suất vượt trội. Giờ nghỉ trưa trên sân thượng tòa nhà nhìn ra sông Sài Gòn, Lâm Tịch chỉ điểm về 'Ý niệm hòa quyện dòng máu', mượn hình tượng phù sa cuộn chảy để dẫn dắt khí huyết vận hành theo chu kỳ bán khép kín. Cuối giờ làm, an ninh tòa nhà liên hệ mời Minh An xác minh đoạn băng ghi hình sự cố nhiệt độ.",
                     "Minh An bước đầu nắm bắt ý niệm dẫn khí huyết tựa dòng trường giang; mối liên kết tâm thức với Lâm Tịch thêm bền chặt; gieo mầm phục bút FSH-010 về bóng mờ bán nguyệt trong dữ liệu camera an ninh."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 10, "Sân thượng tòa nhà văn phòng Quận 1", "Phàm nhân (Nội luyện Khí Huyết sơ cấp - Ý Niệm Lưu Chuyển)", "Khí huyết tuần hoàn theo nhịp bán hoàn chỉnh, năng lực tập trung trí não đỉnh cao, hô hấp sâu trầm ổn",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Cốc cà phê"], ensure_ascii=False),
                     "Điềm đạm, mẫn tuệ, thận trọng trước sự chú ý từ bộ phận an ninh"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 10, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn ngưng tụ sơ khai)", "Tàn hồn dần ổn định, hình bóng thiếu nữ áo choàng xám bạc thêm phần rõ nét",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Coi trọng ngộ tính của Minh An, chủ động phối hợp điều tức và cảnh báo hiểm nguy thế tục"))
        
        # Foreshadowing seed FSH-010
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-010", "Dữ liệu camera nhiệt của tòa nhà ghi nhận vệt bóng mờ hình bán nguyệt kỳ lạ bao quanh cơ thể Minh An", 10, 1,
                     json.dumps(["Minh An", "Bộ phận an ninh tòa nhà"], ensure_ascii=False),
                     "Vết tích vật lý của trường lực Băng Phách bị phân tích kỹ thuật số, khiến Minh An lọt vào diện theo dõi ngầm của chuyên gia cảm biến", 15, "PLANTED"))
    elif chapter_num == 11:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Căn phòng giám sát an ninh và bài thử thách thế tục", chapter_num, 1,
                     "2026-09-16T17:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Chiều 16/09/2026, Minh An xuống văn phòng an ninh tầng hầm B1 đối chiếu video camera sự cố nước sôi. Anh bình tĩnh giải thích bằng hiện tượng nước đá và gió máy lạnh, tạm thời vượt qua nghi vấn kỹ thuật số. Tuy nhiên, chuyên viên kiểm định đã lưu trữ đoạn clip dị thường vào cơ sở dữ liệu nghiên cứu. Minh An ý thức được sự giám sát của thế giới công nghệ, quyết tâm hoàn thành chu thiên Khí Huyết để tự chủ thân thể.",
                     "Vượt qua sự kiểm tra ban đầu của an ninh thế tục một cách êm thấm; gieo mầm phục bút FSH-011 về tệp dữ liệu lưu trữ NV-2026-X; tạo động lực tối thượng thúc đẩy Minh An bước vào chu thiên trọn vẹn ở Chương 12."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 11, "Phòng an ninh B1 -> Hầm giữ xe -> Cầu Thị Nghè", "Phàm nhân (Nội luyện Khí Huyết sơ cấp - Ý Niệm Vững Vàng)", "Tâm lý trầm tĩnh tột bậc, nhịp tim duy trì 60 nhịp/phút dù đối mặt thẩm vấn, khí huyết vận hành mượt mà",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Bút bi"], ensure_ascii=False),
                     "Cảnh giác cao độ, thấu hiểu sức mạnh và cạm bẫy của công nghệ hiện đại, kiên định"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 11, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn ngưng tụ sơ khai)", "Tàn hồn tĩnh lặng, thu liễm hoàn toàn dao động quy tắc để không bị thiết bị điện tử phát hiện",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Kinh ngạc trước mạng lưới ghi nhớ vĩnh viễn của máy móc phàm nhân, ngày càng tin cậy trí tuệ ứng biến của Minh An"))
        
        # Foreshadowing seed FSH-011
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-011", "Tệp video camera nhiệt sự cố được chuyên viên kỹ thuật lưu trữ vào thư mục hồ sơ mật mang mã số NV-2026-X", 11, 1,
                     json.dumps(["Chuyên viên kỹ thuật", "Minh An"], ensure_ascii=False),
                     "Dấu tích rò rỉ quy tắc đầu tiên chính thức đi vào hồ sơ nghiên cứu của một viện khoa học năng lượng phi truyền thống", 24, "PLANTED"))
    elif chapter_num == 12:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Khai mở then cài và chu thiên Khí Huyết đầu tiên", chapter_num, 1,
                     "2026-09-16T23:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Đêm 16/09/2026, tại phòng trọ Bình Thạnh. Minh An dùng ý chí kiên định và ý niệm trường giang, kiên trì mài giũa then cài phong ấn tại đốt sống lưng thứ bảy. Với sự hỗ trợ hàn ý thanh tỉnh từ Lâm Tịch, anh thành công phá nứt then cài, hoàn thành Vòng Chu Thiên Khí Huyết trọn vẹn đầu tiên, hình thành màng chắn tự chủ bao bọc thức hải.",
                     "Hoàn tất thu hồi phục bút FSH-003; Minh An chính thức bước vào ngạch cửa Khí Huyết Đạo sơ cấp (hoàn thành chu thiên); chấm dứt nguy cơ rò rỉ quy tắc thụ động ra thiết bị cảm biến; gieo mầm phục bút FSH-012 về dao động sinh học kích phát địa tầng."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 12, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhất Chu Thiên)", "Hoàn thành 1 chu thiên khép kín, bài xuất độc tố tầng biểu bì, kinh mạch thông suốt, thể lực và sức bền tăng vọt",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Khăn tắm", "Cốc sứ"], ensure_ascii=False),
                     "Tự tin, kiên định, thăng hoa về nhận thức bản thân, xác lập mối quan hệ đồng hành bình đẳng với Lâm Tịch"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 12, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn được bao bọc trong kén khí huyết chu thiên, chấm dứt tình trạng rò rỉ và tán loạn, hồi phục thêm một phần sinh cơ",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Thán phục trước ý chí phàm nhân, chính thức công nhận Minh An là người kế thừa tinh thần của Khí Huyết Đạo"))
        
        # Payoff FSH-003
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-003'""")

        # Foreshadowing seed FSH-012
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-012", "Dao động sinh học cực kỳ mờ nhạt từ khe nứt đốt sống thứ bảy thẩm thấu vào lòng đất Sài Gòn", 12, 1,
                     json.dumps(["Lâm Tịch"], ensure_ascii=False),
                     "Tín hiệu mở khóa Khí Huyết đầu tiên sau vạn năm kích hoạt cảm ứng vi mô của đại trận phong ấn Cố Thổ nằm sâu dưới lòng đất", 28, "PLANTED"))
    elif chapter_num == 13:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Kỳ tích sinh học và sự xuất hiện của ánh mắt quan sát", chapter_num, 1,
                     "2026-09-17T09:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Sáng 17/09/2026, Minh An trải nghiệm sự thăng hoa giác quan sau khi thông 1 Chu Thiên. Khi đến tòa nhà làm việc, máy quét tầm nhiệt không còn phát hiện bất kỳ dị thường nào nhờ màng chắn khí huyết hoàn hảo. Trong giờ làm việc tại khu vực bốc dỡ hàng tầng trệt, một sự cố trượt cáp xe nâng hàng đe dọa người công nhân già; Minh An kịp thời dùng lực cơ bắp thuần túy bộc phát chuẩn xác để giữ lấy càng nâng, cứu người an toàn trong giới hạn phàm nhân. Một vị khách lớn tuổi am hiểu nội gia quyền ngẫu nhiên chứng kiến và chú ý.",
                     "Khẳng định sức mạnh Khí Huyết dùng để bảo hộ cuộc sống; củng cố niềm tin tuyệt đối giữa Minh An và Lâm Tịch; gieo mầm phục bút FSH-013 về sự chú ý của giới võ học cổ truyền."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 13, "Khu vực tầng trệt tòa nhà Quận 1", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhất Chu Thiên Vững Chắc)", "Cơ bắp phát lực nhịp nhàng, phản xạ vượt bậc, không chịu bất kỳ chấn thương nào sau cú bộc phát kình lực",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Găng tay sợi"], ensure_ascii=False),
                     "Điềm đạm, sẵn sàng che chở người yếu thế, vững vàng trước mọi ánh nhìn"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 13, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn yên ấm bên trong kén khí huyết chu thiên, khí tức băng phách thu liễm tuyệt đối",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Cảm kích trước tấm lòng nhân hậu của Minh An, chính thức coi anh là đạo lữ đồng hành sinh tử"))
        
        # Foreshadowing seed FSH-013
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-013", "Ánh mắt kinh ngạc của vị khách cao tuổi mặc áo bà ba đen chứng kiến cú phát lực chặn xe nâng của Minh An", 13, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Một võ sư nội gia quyền thuộc môn phái cổ truyền nhận ra dấu vết kình lực Khí Huyết thất truyền, chuẩn bị cho cuộc hội ngộ ở Chương 16", 16, "PLANTED"))
    elif chapter_num == 14:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Tiếng trà góc phố và sự tương thông của hai thế hệ võ học", chapter_num, 1,
                     "2026-09-17T13:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich", "char_le_ba_khiem"], ensure_ascii=False),
                     "Trưa và đầu giờ chiều 17/09/2026, Minh An ghé quán trà góc đường Phùng Khắc Khoan. Võ sư Lê Bá Khiêm (ông Ba Khiêm) - người mặc áo bà ba đen ban sáng - chủ động tiếp cận, mời trà và đàm đạo về cú hãm lực xe nâng. Ông phân tích cơ chế trầm kiều tạ lực và kình phát tự tủy của nội gia quyền, trao đổi về triết lý vận kình trong cơ thể phàm nhân. Minh An khiêm nhường học hỏi, trong khi Lâm Tịch ngạc nhiên nhận ra sự tương đồng kỳ diệu giữa kinh nghiệm võ học thế tục và Khí Huyết Đạo.",
                     "Minh An lĩnh hội phương pháp điều phối gân cốt nội gia bổ khuyết cho Khí Huyết chu thiên; thiết lập mối giao hảo tao nhã với ông Ba Khiêm; nhận thông báo về việc viện nghiên cứu năng lượng đề nghị truy xuất camera nhiệt; gieo mầm phục bút FSH-014 về cổ thư chép tay võ phái."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 14, "Quán trà cổ đường Phùng Khắc Khoan, Quận 1", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Chu Thiên Dung Hợp Võ Học)", "Khí huyết lưu chuyển thuần thục, cơ bắp và khớp xương dung hợp kỹ pháp vận kình nội gia, thể trạng sung mãn hoàn hảo",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Điềm đạm, khiêm tốn, mở rộng tầm nhìn về võ đạo trần thế, cảnh giác trước sự chú ý của viện nghiên cứu"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 14, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn nằm yên trong kén khí huyết chu thiên, tiếp nhận góc nhìn võ học thế tục để chiêm nghiệm lại Thể Đạo viễn cổ",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Thán phục trí tuệ đúc kết của phàm nhân qua ngàn năm, gia tăng hảo cảm và thấu hiểu Minh An"))
        
        # Foreshadowing seed FSH-014
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-014", "Cuốn cổ thư chép tay của môn phái ông Ba Khiêm ghi chép về dị tượng địa chấn ngầm và những tiền bối huyết khí dị thường thời cận đại", 14, 1,
                     json.dumps(["Minh An", "Lâm Tịch", "Võ sư Lê Bá Khiêm"], ensure_ascii=False),
                     "Manh mối lịch sử thế tục kết nối giữa đại trận phong ấn Cố Thổ dưới lòng đất phương Nam và con đường Khí Huyết Đạo thất truyền", 26, "PLANTED"))
    elif chapter_num == 15:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Cuộc đối chiếu thực nghiệm hồ sơ NV-2026-X và phép thử quang phổ", chapter_num, 1,
                     "2026-09-17T16:00:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich", "char_trinh_hoai_nam"], ensure_ascii=False),
                     "Chiều 17/09/2026, Minh An được mời vào phòng họp kỹ thuật tầng 12 đối chiếu dữ liệu với đoàn chuyên gia Viện Nghiên Cứu Năng Lượng Đô Thị do Tiến sĩ Trịnh Hoài Nam dẫn đầu. Tiến sĩ Nam phân tích đồ thị sụt giảm nhiệt độ dị thường của tệp NV-2026-X và dùng máy quét quang phổ phân giải cao quét trực tiếp thân thể Minh An. Nhờ màng chắn Vòng Chu Thiên Khí Huyết sinh học tự chủ, các thông số bức xạ nhiệt của Minh An hoàn toàn bình thường, giải trừ nghi vấn trực diện của khoa học thế tục.",
                     "Hoàn tất thu hồi phục bút FSH-007 và FSH-010; khẳng định năng lực che chắn tuyệt đối của Chu Thiên Khí Huyết trước công nghệ cảm biến quang phổ; gieo mầm phục bút FSH-015 về xung dao động địa chấn ngầm ngoại ô Sài Gòn."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 15, "Phòng họp kỹ thuật tầng 12 tòa cao ốc Quận 1", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Chu Thiên Vững Vàng)", "Khí huyết lưu chuyển ổn định, thân nhiệt 36.8°C hoàn hảo, hô hấp sâu lắng, nhịp tim duy trì 62 nhịp/phút dưới máy đo",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Danh thiếp gỗ của ông Ba Khiêm", "Bút bi"], ensure_ascii=False),
                     "Điềm tĩnh, mẫn tuệ, bản lĩnh vững vàng trước các thiết bị đo lường công nghệ cao"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 15, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn nằm yên trong kén khí huyết chu thiên ấm áp, quy tắc Băng Phách thu liễm tuyệt đối không rò rỉ một tia gợn sóng",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Thán phục trước sự trầm tĩnh và tài ứng biến thế tục của Minh An, niềm tin đồng hành càng thêm bền chặt"))
        
        # Payoffs FSH-007 & FSH-010
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-007'""")
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-010'""")
        
        # Foreshadowing seed FSH-015
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-015", "Tiến sĩ Trịnh Hoài Nam nhắc đến dữ liệu cảm biến địa chấn ngầm ngoại ô phía Đông Nam Sài Gòn ghi nhận một xung dao động tần số thấp cùng thời điểm đêm 16/09", 15, 1,
                     json.dumps(["Minh An", "Lâm Tịch", "Tiến sĩ Trịnh Hoài Nam"], ensure_ascii=False),
                     "Mối liên kết giữa khe nứt phong ấn đốt sống thứ bảy của Minh An với sự dao động của đại trận cổ xưa dưới lòng đất Trái Đất (tiến triển FSH-012 tới Ch 28)", 28, "PLANTED"))
    elif chapter_num == 16:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Hội ngộ võ đường cổ truyền và bí ẩn cổ thư phương Nam", chapter_num, 1,
                     "2026-09-19T09:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich", "char_le_ba_khiem"], ensure_ascii=False),
                     "Sáng thứ Bảy 19/09/2026, Minh An ghé thăm võ đường của võ sư Lê Bá Khiêm bên hẻm đường Đinh Tiên Hoàng. Hai người giao lưu cảm nhận kình lực qua thôi thủ; Minh An dùng Chu Thiên Khí Huyết nhẹ nhàng hóa giải nội kình của bậc lão võ sư mà không hề lay động. Ông Ba Khiêm xúc động mang cuốn cổ thư chép tay của sư tổ cho Minh An xem, hé lộ đồ hình kinh mạch trùng khớp Chu Thiên và đoạn nhật ký năm 1920 ghi lại dấu tích phiến đá long xà phát ra nhịp đập sâu dưới lòng đất phương Nam.",
                     "Hoàn tất thu hồi phục bút FSH-013; củng cố mối giao hảo tri kỷ võ học giữa Minh An và ông Ba Khiêm; xác nhận dấu tích Thể Đạo cổ xưa từng tồn tại ở phương Nam; gieo mầm phục bút FSH-016 về phiến đá long xà và nhịp đập địa tầng."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 16, "Võ đường cổ truyền hẻm Đinh Tiên Hoàng, Bình Thạnh", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Chu Thiên Dung Hợp Quyền Thuật)", "Khí huyết lưu chuyển dồi dào, thấu suốt nguyên lý trầm kiều và thính kình, gân cốt dẻo dai tột bậc",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Danh thiếp gỗ của ông Ba Khiêm", "Bản sao đồ hình kinh mạch cổ"], ensure_ascii=False),
                     "Tâm thái rộng mở, tôn kính tiền nhân, thấu cảm sâu sắc mối liên kết giữa võ học trần thế và đại đạo"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 16, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn an trú yên bình bên trong kén khí huyết, xúc động trước tàn tích Thể Đạo còn lưu lại nhân gian",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Bùi ngùi hoài niệm về thời đại Thể Đạo chư thiên, xác quyết niềm tin vào con đường phàm nhân của Minh An"))
        
        # Payoff FSH-013
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-013'""")
        
        # Foreshadowing seed FSH-016
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-016", "Đoạn nhật ký năm 1920 trong cổ thư của ông Ba Khiêm nhắc đến phiến đá cổ long xà phát ra nhịp đập sâu dưới lòng đất đầm lầy Tây Nam", 16, 1,
                     json.dumps(["Minh An", "Lâm Tịch", "Võ sư Lê Bá Khiêm"], ensure_ascii=False),
                     "Manh mối dẫn tới trận nhãn phong ấn viễn cổ của Khí Huyết Đạo nằm tại vùng đồng bằng châu thổ phương Nam", 30, "PLANTED"))
    elif chapter_num == 17:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Đêm tĩnh lặng bên dòng kênh và rào cản huyệt Đại Chùy", chapter_num, 1,
                     "2026-09-19T21:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Tối 19/09/2026, Minh An trở về phòng trọ Bình Thạnh sau buổi gặp ông Ba Khiêm. Dưới ánh đèn bàn ấm áp, anh ghi chép đối chiếu cổ thư với chu thiên cơ thể. Khi tiến hành tĩnh tọa vận kình trong đêm, khí huyết dâng trào qua đốt sống thứ bảy và chạm phải rào cản màng đá vôi vô hình tại đốt sống cổ thứ ba (huyệt Đại Chùy). Lâm Tịch xác nhận đây là then cài phong ấn thứ hai của Cố Thổ (Khí Huyết Thấu Não). Minh An giữ tâm thái điềm đạm, mài giũa khí huyết chuẩn bị cho bước đột phá ở Chương 18.",
                     "Tiến triển then chốt cho phục bút FSH-008 trước thềm hồi báo ở Chương 18; củng cố triết lý tu thân kiên định của Minh An; gieo mầm phục bút FSH-017 về tàn vũ xám bạc của Lâm Tịch hóa thành sinh cơ dưỡng mạch."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 17, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Chu Thiên Đỉnh Điểm, Chạm Then Cài Thứ Hai)", "Khí huyết lưu chuyển dồi dào, vùng gáy và đốt sống cổ thứ ba căng tức nhẹ do chạm rào cản phong ấn Đại Chùy, thể trạng sung mãn",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Sổ tay ghi chép", "Bút bi", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Trầm tĩnh, kiên trì, không nôn nóng, chuẩn bị tâm thế vững vàng để mài giũa then cài thứ hai"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 17, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn được dưỡng ấm trong kén khí huyết, nguyên thần hồi phục thêm một tia sinh cơ, hư ảnh áo choàng xám bạc khẽ rung động",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Đồng cảm sâu sắc, chỉ điểm tận tình về cấu trúc phong ấn Đại Chùy, ngày càng gắn bó với Minh An"))
        
        # Foreshadowing seed FSH-017
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-017", "Một đóm tàn vũ xám bạc rơi ra từ vạt áo của Lâm Tịch tan vào dòng khí huyết nuôi dưỡng điểm nút Đại Chùy", 17, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Quy tắc chí cao nguyên thủy của Lâm Tịch vô thức dung hòa vào khí huyết Minh An, mở đường cho khả năng đồng bộ nguyên thần trong giao chiến ở Chương 22", 22, "PLANTED"))
    elif chapter_num == 18:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Khai mở then cài Đại Chùy và Vòng Nhị Chu Thiên Khí Huyết", chapter_num, 1,
                     "2026-09-20T23:45:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Đêm Chủ Nhật 20/09/2026, giữa cơn mưa rào Bình Thạnh, Minh An tiến hành công phá then cài phong ấn thứ hai tại đốt sống cổ thứ ba (huyệt Đại Chùy). Nhờ ý chí kiên định và sự hỗ trợ điều hòa từ tàn niệm Lâm Tịch, màng phong ấn nứt toác hoàn toàn; dòng khí huyết dâng trào thấu não qua đỉnh Bách Hội, khép kín Vòng Nhị Chu Thiên Trọn Vẹn. Giác quan và phản xạ thần kinh của Minh An thăng hoa vượt bậc.",
                     "Hoàn tất thu hồi phục bút FSH-008; Minh An chính thức bước vào cảnh giới Nhị Chu Thiên Khí Huyết (Khí Huyết Thấu Não); mở rộng trường cảm nhận sinh học vi mô; gieo mầm phục bút FSH-018 về hiện tượng đồng tử ngưng quang."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 18, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhị Chu Thiên Viên Mãn)", "Hoàn thành 2 chu thiên khép kín, khí huyết thấu não, thần kinh đại não thăng hoa, giác quan 3D nhạy bén trong bán kính 10m, thể phách vững chắc",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Sổ tay ghi chép", "Bút bi", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Điềm đạm, mẫn tuệ tột bậc, tự chủ hoàn toàn thể xác và tinh thần"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 18, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn được bao bọc trong kén khí huyết Nhị Chu Thiên dày dặn ấm áp gấp bội, phục hồi thêm sinh cơ nguyên thần, hư ảnh thiếu nữ thêm phần ngưng thực",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Vô cùng kinh ngạc trước tốc độ ngộ đạo và ý chí của Minh An, gắn kết tâm thức sâu sắc"))
        
        # Payoff FSH-008
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-008'""")
        
        # Foreshadowing seed FSH-018
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-018", "Tia hào quang màu hổ phách vi mô thoáng ngưng tụ sâu trong đáy đồng tử Minh An khi khí huyết tràn qua đỉnh Bách Hội", 18, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Dấu tích khai mở Thần Mục Thể Đạo sơ khai, chuẩn bị cho khả năng nhìn thấu quỹ đạo dòng năng lượng và quy tắc ở Chương 32", 32, "PLANTED"))
    elif chapter_num == 19:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Thế giới dưới tầng giác quan mới và khúc dạo đầu của bầu trời bị tha hóa", chapter_num, 1,
                     "2026-09-21T12:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Sáng và trưa thứ Hai 21/09/2026. Minh An trải nghiệm sự thăng hoa giác quan của Nhị Chu Thiên khi di chuyển qua ngã tư Hàng Xanh và giải quyết công việc kỹ thuật tại văn phòng Quận 1 với hiệu suất vượt bậc. Trong giờ nghỉ trưa trên sân thượng tòa nhà lộng gió nhìn ra sông Sài Gòn, Lâm Tịch hòa quyện cảm quan với Minh An, lần đầu tiên bùi ngùi nhắc về ký ức kinh hoàng khi 'Bầu trời bị tha hóa' nuốt chửng vị diện quê hương nàng.",
                     "Khẳng định sự hòa hợp tuyệt đối giữa năng lực Nhị Chu Thiên và cuộc sống thường nhật; tiến triển mạnh mẽ cho phục bút FSH-005 chuẩn bị hồi báo ở Chương 20; gieo mầm phục bút FSH-019 về hiệu ứng rẽ sóng khí động học của màng chắn Khí Huyết."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 19, "Sân thượng tòa cao ốc văn phòng Quận 1", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhị Chu Thiên Thuần Thục)", "Nhị Chu Thiên vận hành tự nhiên theo từng nhịp thở, năng lực xử lý thông tin và phản xạ thị giác cực đỉnh, tâm thần thư thái",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Hộp cơm trưa", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Bình thản, sâu sắc, thấu cảm với nỗi đau diệt thế của Lâm Tịch, sẵn sàng đối mặt với chân tướng sự thật"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 19, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định)", "Tàn hồn được sưởi ấm trong kén Nhị Chu Thiên, cộng hưởng cảm quan qua đôi mắt Minh An để ngắm nhìn bầu trời trần thế",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần vỡ vụn"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm)"], ensure_ascii=False),
                     "Bùi ngùi xúc động, trút bỏ gánh nặng cô độc ngàn năm, mở lòng chia sẻ về quá khứ bi tráng"))
        
        # Foreshadowing seed FSH-019
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-019", "Luồng gió mạnh trên sân thượng tòa cao ốc bị tách đôi rẽ sóng khí động học khi thổi qua thân mình Minh An", 19, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Hiện tượng màng chắn khí huyết Nhị Chu Thiên bắt đầu tương tác vật lý thụ động với trường khí quyển ngoại cảnh, chuẩn bị cho năng lực Ngự Khí Thể Đạo ở Chương 35", 35, "PLANTED"))
    elif chapter_num == 20:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Hoàng hôn Thủ Thiêm và ký ức Bầu Trời Bị Tha Hóa", chapter_num, 1,
                     "2026-09-21T18:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Chiều tối 21/09/2026, Minh An ra bờ sông Thủ Thiêm đón hoàng hôn ráng đỏ kỳ dị. Dưới sự cộng hưởng của Nhị Chu Thiên Khí Huyết, Lâm Tịch giải phóng tàn niệm viễn cổ về đại kiếp Bầu Trời Bị Tha Hóa. Minh An chứng kiến tàn ảnh kiếm gãy chém rách quy tắc Thiên Đạo; ý chí kiên cường của Minh An neo giữ vững vàng giúp cả hai vượt qua cơn chấn động thức hải. Thanh tàn kiếm rỉ sét phát ra tiếng kiếm ngân đầu tiên, rũ bỏ một lớp rỉ sét hé lộ cổ tự màu lam tuyết.",
                     "Hồi báo trọn vẹn phục bút then chốt FSH-005 (PAID); xác lập liên kết sinh tử sâu sắc giữa Minh An và Lâm Tịch; thanh tàn kiếm bắt đầu thức tỉnh linh tính; gieo mầm phục bút FSH-020 về hoa văn cổ tự tuyết lam."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 20, "Bờ sông Sài Gòn, bán đảo Thủ Thiêm", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhị Chu Thiên Trầm Ổn)", "Khí huyết cuộn trào mãnh liệt, ngực và trán hơi nóng ran sau đợt cộng hưởng tâm thức cực độ nhưng thể phách vững như bàn thạch",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Chấn động sâu sắc trước chân tướng diệt thế, ý chí kiên định bất khuất, quyết tâm bảo vệ Lâm Tịch và cõi nhân gian"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 20, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn hồi phục sinh cơ)", "Tàn hồn được sưởi ấm và neo giữ bởi ý chí kiên định của Minh An, thoát khỏi nỗi ám ảnh diệt thế ngàn năm, thanh tàn kiếm trong thức hải rũ bỏ một lớp rỉ sét",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần từng vỡ vụn (đang dần ngưng tụ lại)"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm, đã rũ một lớp rỉ sét, hé lộ cổ tự)"], ensure_ascii=False),
                     "Xúc động tột cùng, rũ bỏ nỗi cô độc thiên thu, hoàn toàn tin tưởng và đồng hành sinh tử cùng Minh An"))
        
        # Payoff FSH-005
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-005'""")
        
        # Foreshadowing seed FSH-020
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-020", "Tiếng kiếm ngân trong trẻo đầu tiên vang lên trong thức hải và lớp rỉ sét bong ra hé lộ một nét hoa văn cổ tự màu lam tuyết trên thân tàn kiếm", 20, 1,
                     json.dumps(["Minh An", "Lâm Tịch"], ensure_ascii=False),
                     "Thanh tàn kiếm của Lâm Tịch bắt đầu thức tỉnh linh tính dưới sự tẩm bổ của Khí Huyết Đạo thuần khiết, chuẩn bị cho kiếm khí sơ khởi ở Chương 38", 38, "PLANTED"))
    elif chapter_num == 21:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Đêm tĩnh lặng sau bão giông và khúc tự sự của thanh tàn kiếm", chapter_num, 1,
                     "2026-09-21T21:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Đêm 21/09 và rạng sáng 22/09/2026. Minh An trở về căn phòng trọ nhỏ ở Bình Thạnh sau biến cố đại kiếp ở Thủ Thiêm. Dưới ánh đèn bàn ấm áp và bữa ăn khuya thanh đạm, hai người có cuộc đối thoại sâu lắng về nguồn gốc Băng Phách Trảm Tuyết Kiếm và ý chí phàm trần. Thể chất Nhị Chu Thiên của Minh An hoàn tất đợt thích nghi sinh học vượt bậc sau áp lực cực hạn; hoa văn kiếm ngân trên tay áo Lâm Tịch bắt đầu hiện rõ hơn.",
                     "Khẳng định sự hòa hợp tuyệt đối giữa cuộc sống đời thường và hành trình tu thân; bước tiến quan trọng cho phục bút FSH-009 và FSH-017 chuẩn bị hồi báo ở Chương 22."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 21, "Phòng trọ Nơ Trang Long, Bình Thạnh", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhị Chu Thiên Cố Hóa)", "Đốt sống cổ thứ ba rắn chắc như ngọc thạch sau tôi luyện, khí huyết thuần dương lưu chuyển êm ả, tinh thần thư thái minh mẫn",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Laptop cũ", "Sổ tay ghi chép", "Bút bi", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Thanh thản, kiên định, bình yên sâu sắc giữa cuộc sống đời thường"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 21, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn an định, kiếm ý sơ phục)", "Tàn hồn được sưởi ấm trong kén khí huyết kết hợp kiếm quang lam tuyết, tay áo xuất hiện hoa văn kiếm ngân mờ ảo, tàn kiếm bớt đi một tầng rỉ sét",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần đang dần ngưng tụ lại"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm, đã hé lộ nét cổ tự tuyết lam)"], ensure_ascii=False),
                     "An yên, thấu cảm, trút bỏ hoàn toàn gánh nặng quá khứ, tin tưởng tuyệt đối vào Minh An"))
    elif chapter_num == 22:
        cur.execute("""INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, location_id, participants_json, summary, outcome)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (f"EVT-CH{chapter_num:03d}-01", "Hội nghị tầng mười và hiện tượng kiếm ý đồng bộ nguyên thần", chapter_num, 1,
                     "2026-09-22T09:30:00+07:00", "loc_hcmc", json.dumps(["char_minh_an", "char_lam_tich"], ensure_ascii=False),
                     "Sáng 22/09/2026, Minh An tham gia cuộc họp dự án số hóa cảm biến địa chất đô thị tại phòng họp tầng 10. Khi mạng lưới dữ liệu đo đạc sóng địa chấn ngầm gặp sự cố nghẽn tắc ma trận cực độ, Minh An can thiệp xử lý. Hiện tượng đồng bộ nguyên thần vi mô bùng nổ: hoa văn kiếm ngân trên tay áo Lâm Tịch rực sáng, hạt tàn vũ ở Đại Chùy kết nối kiếm ý bóc tách dữ liệu rác với tốc độ kinh hồn. Bản đồ địa chấn phục hồi hé lộ đồ hình sóng ngầm long xà hướng về đầm lầy Tây Nam.",
                     "Hồi báo thành công 2 phục bút FSH-009 và FSH-017 (PAID); Minh An chính thức gia nhập tổ chuyên trách liên ngành; phát hiện trùng khớp chấn động giữa số liệu khoa học hiện đại và cổ thư chép tay; gieo mầm phục bút FSH-021 về tập dữ liệu Sóng Ngầm Long Xà."))
        
        # Character states
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_minh_an", 22, "Phòng họp lớn tầng 10, tòa cao ốc văn phòng Quận 1", "Phàm nhân (Khí Huyết Đạo Sơ Khai - Nhị Chu Thiên Đỉnh Phong)", "Các khớp ngón tay và thần kinh đại não linh hoạt tột đỉnh, khí huyết thấu não kết hợp kiếm ý sắc bén, thể trạng tràn trề sinh lực",
                     json.dumps([], ensure_ascii=False),
                     json.dumps(["Điện thoại di động", "Ví tiền", "Chìa khóa xe Wave", "Thẻ nhân viên tổ chuyên trách", "Laptop công ty", "Danh thiếp gỗ của ông Ba Khiêm"], ensure_ascii=False),
                     "Tập trung cao độ, tự tin, kinh ngạc trước sự liên kết giữa khoa học thực nghiệm và tàn tích cổ xưa"))
        
        cur.execute("""INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("char_lam_tich", 22, "Thức hải Minh An", "Đỉnh cao vị diện (tàn hồn hồi phục sinh cơ, tâm kiếm cộng hưởng)", "Hoa văn kiếm ngân trên tàn y trắng phát sáng định hình rõ rệt, kết nối nguyên thần vi mô với khí huyết Minh An thông qua điểm nút Đại Chùy",
                     json.dumps(["Thân thể nát vụn hoàn toàn", "Đạo cơ vỡ nát", "Nguyên thần đang dần ngưng tụ lại"], ensure_ascii=False),
                     json.dumps(["Mảnh kiếm gãy (dạng ý niệm, cổ tự Tuyết tỏa ánh lam)"], ensure_ascii=False),
                     "Ngạc nhiên và thán phục trước trí tuệ phàm nhân thế giới này khi sử dụng mạng lưới máy móc để đo lường mạch đất"))
        
        # Payoffs FSH-009 and FSH-017
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-009'""")
        cur.execute("""UPDATE foreshadowing_ledger SET status = 'PAID' WHERE id = 'FSH-017'""")
        
        # Foreshadowing seed FSH-021
        cur.execute("""INSERT OR REPLACE INTO foreshadowing_ledger (id, seed_description, planted_chapter, planted_scene, notices_json, actual_meaning, payoff_chapter, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    ("FSH-021", "Tập dữ liệu địa chấn bất thường mang mã định danh 'Sóng Ngầm Long Xà' được trích xuất riêng biệt, liên kết với cổ đồ của ông Ba Khiêm", 22, 1,
                     json.dumps(["Minh An", "Lâm Tịch", "Tiến sĩ Trịnh Hoài Nam"], ensure_ascii=False),
                     "Xác nhận bằng số liệu khoa học công nghệ hiện đại về sự tồn tại của trận nhãn Khí Huyết Đạo dưới đầm lầy Tây Nam, chuẩn bị cho thực địa ở Chương 26", 26, "PLANTED"))

    conn.commit()
    conn.close()

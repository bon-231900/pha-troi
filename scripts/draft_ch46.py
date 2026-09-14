# -*- coding: utf-8 -*-
"""Script soạn thảo và kiểm duyệt bản thảo Chương 46: Vĩ Thanh Hồi 1 — Lời Thề Dưới Bình Minh Sài Gòn."""

import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, r"d:\tieu-thuyet")

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"
MANUSCRIPT_DIR = r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01"
CH46_PATH = os.path.join(MANUSCRIPT_DIR, "ch_046.md")

CHAPTER_CONTENT = """---
chapter: 46
title: "Lời Thề Dưới Bình Minh Sài Gòn"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Bán đảo Thanh Đa & Đỉnh cầu Sài Gòn, TP.HCM"
date: "2026-10-08"
word_count: 2750
---

# Chương 46: Lời Thề Dưới Bình Minh Sài Gòn

Năm giờ sáng thứ Năm, ngày mùng tám tháng Mười năm 2026.

Chuông báo thức trên chiếc điện thoại đặt đầu giường còn chưa kịp rung lên, đôi mắt tôi đã tự động mở ra giữa không gian mờ ảo của sớm mai.

Căn phòng trọ mười lăm mét vuông ở Bình Thạnh chìm trong bầu không khí se lạnh dễ chịu của buổi giao mùa. Tiếng gió sớm lùa qua kẽ rèm cửa sổ, mang theo mùi ngai ngái của đất ướt và hương hoa sứ thoang thoảng từ ban công nhà hàng xóm.

Tôi nằm im trên nệm mỏng, khẽ nhắm mắt lại để lắng nghe tâm thức của chính mình.

Thế nhưng, khác hẳn với thói quen suốt hai tháng qua, trong thức hải của tôi lúc này hoàn toàn không còn một tia động tĩnh. 

Không còn thanh âm lạnh lùng, nghiêm nghị của một nữ kiếm tiên từng đứng giữa chín tầng mây; không còn những tiếng nhắc nhở chỉnh đốn thế tấn, nhịp thở hay những lời phân tích sắc bén về các mắt xích trận pháp cổ xưa. Chiếc trâm ngọc cổ đặt ngay ngắn trên bàn làm việc bên cạnh ly nước lọc lạnh ngắt, ảm đạm không một gợn hào quang, tựa như một món trang sức bình dị đã nằm yên dưới đáy mồ suốt ngàn năm.

Lâm Tịch đã thực sự chìm vào giấc ngủ trầm miên sâu.

Nàng đã dốc cạn những sợi tàn lực nguyên thần cuối cùng để tung ra nhát kiếm Băng Phách Trảm Tuyết cứu nguy cho tôi và hai người lính đặc nhiệm hải quân dưới đáy sông bốn mươi mét chiều hôm qua. Nàng đã trao trọn niềm tin vào tôi, trao lại toàn bộ vận mệnh của con đường Thể Đạo cho một phàm nhân bằng xương bằng thịt.

Tôi đưa tay vuốt nhẹ lồng ngực, nơi trái tim đang đập từng nhịp trầm hùng, đều đặn.

Từ ngày hôm nay, tôi hiểu rằng mình sẽ phải hoàn toàn cô độc bước đi trên con đường này. Không còn chỗ dựa của một tàn hồn viễn cổ, không còn sự mách nước của những tri thức vượt ngoài thời đại. Mọi bước tiến, mọi ranh giới sinh tử sắp tới sẽ hoàn toàn phụ thuộc vào đôi bàn tay, ý chí và sự kỷ luật của chính bản thân tôi.

Nhưng trong lòng tôi không hề có một gợn hoang mang hay sợ hãi.

Trái lại, một sự thanh thản, tự do và kiên định chưa từng thấy đang cuộn trào trong từng ngóc ngách tâm hồn.

Tôi bật người ngồi dậy, xỏ chân vào đôi giày thể thao quen thuộc, khoác lên mình chiếc áo thun cotton màu xám rồi nhẹ nhàng mở cửa phòng trọ, bước xuống cầu thang hòa mình vào làn sương sớm của thành phố.

***

Năm giờ ba mươi phút sáng.

Bán đảo Thanh Đa đón tôi bằng dải sương mù mỏng manh lững lờ trôi trên mặt sông Sài Gòn.

Không khí nơi đây trong lành và mát rượi đến mức từng hơi thở hít vào đều khiến lồng ngực tôi căng tràn sảng khoái. Trên con đường rợp bóng dừa nước men theo bờ sông, vài cụ già đang thong thả đạp xe, những người dân lao động đi bộ tập thể dục sớm khẽ gật đầu chào nhau bằng những nụ cười hiền hậu. Phía xa xa trên mặt nước phù sa, tiếng mái chèo khua nước lách cách của một bác chài lưới sớm vang lên nhịp nhàng, bình dị.

Tôi bước vào một bãi cỏ xanh mướt trải dài sát mép nước, nơi những giọt sương mai còn đọng long lanh trên từng ngọn cỏ.

Đứng thẳng người, hai chân mở rộng bằng vai, hai bàn chân trần cắm sâu vào lớp đất ẩm ướt của bờ sông, tôi khép nhẹ mi mắt, bắt đầu vận hành bài quyền Tam Chu Thiên.

*Hít vào...*

Không khí mát lành của dòng sông tràn qua khoang mũi, đi thẳng xuống đáy phổi. Luồng nhiệt lượng từ đan điền bốc lên, nhẹ nhàng tưới tắm qua từng đốt sống lưng.

*Thở ra...*

Tôi chìm sâu vào thế giới bên trong cơ thể. 

Hai cẳng tay — nơi chiều qua còn chằng chịt những vết nứt rạn vi mô do phản chấn kiếm ý — giờ đây đã hoàn toàn khép miệng. Dưới sự nuôi dưỡng không ngừng nghỉ của tủy sống suốt một đêm dài, các mô xương bị tổn thương không những hồi phục hoàn toàn mà còn kết tinh lại dày đặc hơn, bền chắc hơn gấp nhiều lần so với trước khi bị rạn nứt!

Đó chính là chân lý tối thượng của Thể Đạo phàm nhân: Không có sự phá hủy thì không có sự tái sinh. Thân thể này không cần linh căn thần thánh ban tặng, mà được tôi luyện qua chính những nỗi đau đớn, những vết thương rách thịt gãy xương và ý chí sinh tồn quật cường của con người!

Tôi bắt đầu vung quyền.

*Vút... Vút... Vút!*

Từng đường quyền xé gió vang lên giòn giã giữa màn sương sớm. 

Khác với những ngày đầu bỡ ngỡ, từng động tác tấn bộ, gạt tay, xoay eo của tôi lúc này đã đạt tới độ chuẩn xác hoàn mỹ như một cỗ máy cơ học tinh vi. Khí huyết trong người tôi không còn là những luồng nhiệt lưu tản mát, mà đã cô đọng lại đặc quánh tựa như dòng thủy ngân lỏng, cuồn cuộn chảy xiết trong huyết quản!

Khi chu trình Tam Chu Thiên thứ ba hoàn tất ở thế quyền vươn thẳng lên trời, một sự biến chuyển kinh thiên động địa bỗng bùng nổ từ sâu trong xương tủy tôi:

*Keng... Keng... Keng!*

Hai trăm linh sáu mảnh xương trên toàn thân thể tôi đồng loạt ngân vang một tràng âm thanh thanh tao, trong trẻo như tiếng ngọc khánh gõ vào chuông đồng viễn cổ!

Lớp cốt màng mỏng manh bao quanh xương bỗng chốc cứng đanh lại, chuyển hóa sang một kết cấu kim thạch thuần khiết và vững chãi đến mức khó tin. Tủy xương ấm nóng bốc lên ngùn ngụt, sản sinh ra những dòng huyết dịch mới mang theo nguồn sinh lực dồi dào, tràn đầy sức sống mãnh liệt.

Một luồng kình lực vô hình từ hai bàn tay tôi phát xuất ra ngoài, làm rẽ đôi làn sương sớm trên mặt cỏ trong phạm vi ba mét!

Tôi từ từ hạ tấn, thu quyền về ngang eo, thở ra một làn bạch khí dài hơn một thước giữa không gian sớm mai.

Toàn thân tôi nhẹ bẫng như cánh chim, nhưng từng bước chân dẫm xuống đất lại vững chãi tựa như ngọn thái sơn. Đôi mắt tôi sáng rực, sâu thẳm và tĩnh lặng như đáy biển không một gợn sóng.

Sau bao thử thách sinh tử nơi hố móng Thủ Thiêm, sau nhát kiếm phản chấn dưới đáy sâu bốn mươi mét Nhà Bè, chiếc gông cùm sơ khai của thể xác phàm nhân đã chính thức bị phá vỡ hoàn toàn.

Tôi đã vượt qua cảnh giới sơ kỳ, chính thức bước chân vào **Luyện Cốt Trung kỳ — Cốt Nhược Kim Thạch**!

Một cột mốc nền tảng vĩ đại trên con đường Thể Đạo!

***

Sáu giờ ba mươi phút sáng.

Tôi chạy bộ qua những con phố rợp bóng cây cổ thụ của Bình Thạnh, tiến lên nhịp vòm giữa của chiếc cầu Sài Gòn hùng vĩ.

Gió sớm từ sông Sài Gòn thốc lên lồng lộng, thổi tung mái tóc đẫm mồ hôi của tôi. Tôi dừng bước, hai tay vịn nhẹ vào lan can thép của cầu, phóng tầm mắt nhìn về phía đường chân trời xa xôi.

Từ hướng bán đảo Thủ Thiêm và cửa biển Cần Giờ, một vầng thái dương đỏ rực như quả cầu lửa khổng lồ đang từ từ nhô lên khỏi tầng mây xám. 

Những tia nắng ban mai vàng óng ánh rực rỡ đầu tiên rải khắp mặt sông Sài Gòn, dát vàng lên từng con sóng phù sa đang cuộn trào xuôi về biển cả. 

Dưới chân cầu, nhịp đập của một ngày mới đã chính thức bắt đầu: Những đoàn tàu hàng rẽ sóng chở container tấp nập ngược xuôi; dòng xe máy và ô tô nối đuôi nhau ken đặc trên các ngả đường hướng vào trung tâm Quận 1; tiếng còi xe giục giã, tiếng cười nói của từng đoàn học sinh đạp xe đến trường, tiếng rao hàng xôi nóng bánh mì vang lên thân thương trong từng ngõ hẻm.

Đứng giữa đất trời lồng lộng, nhìn ngắm thành phố mười triệu dân đang bừng bừng sức sống dưới ánh nắng thu năm 2026, lòng tôi dâng lên một cảm xúc thiêng liêng khó tả.

Mới chỉ gần hai tháng trôi qua. 

Bốn mươi sáu chương đời đã đưa một chàng thanh niên công sở hai mươi lăm tuổi bình thường, chỉ biết quay cuồng với bảng tính lương thưởng và áp lực mưu sinh, bước vào một thế giới hoàn toàn khác biệt. 

Từ giếng cổ Ba Son đến hố móng Thủ Thiêm, từ Thủy Trấn Thạch đến Thủy Môn đáy sâu Nhà Bè... Tôi đã từng bước chạm tay vào những vết tích của một cõi giới cổ xưa bị phong ấn, chứng kiến sự hy sinh vĩ đại của tiền nhân và nếm trải sự tàn khốc của những thế lực tha hóa ngoài vũ trụ.

Nhưng tôi không hề hối hận.

Tôi đưa bàn tay phải áp lên ngực áo thun dã chiến, nơi chiếc trâm ngọc cổ của Lâm Tịch đang nằm im lìm trong túi áo trong.

Dù Lâm Tịch đã chìm vào giấc ngủ trầm miên, dù Trái Đất này là một cõi phong ấn tầng thứ sáu đang bước vào thời kỳ già cỗi rạn nứt, dù Biển Đông và những vùng cấm địa xa xôi ngoài kia đang âm thầm tích tụ những cơn bão táp diệt thế...

Thì giờ phút này đây, đứng dưới ánh bình minh chan hòa của Sài Gòn, tôi biết rõ sứ mệnh của đời mình là gì.

Tôi là một phàm nhân của thế kỷ hai mươi mốt. Tôi không có linh căn tu tiên, nhưng tôi có khối óc của khoa học hiện đại, có tình yêu thương sâu nặng với mẹ già ở quê hương, và có một khung xương kim thạch được rèn giũa từ dòng máu nóng Luyện Cốt của đất mẹ Việt Nam!

Tôi sẽ không lùi bước.

Tôi sẽ kiên trì rèn luyện, từng ngày từng giờ bồi bổ khí huyết, phá vỡ mọi gông cùm giới hạn của thể xác, tự tay rèn đúc nên một đền đài Thể Đạo bất khả xâm phạm.

Khi bóng tối ngoài khơi xa thực sự thức tỉnh, tôi sẽ là bức tường thành vững chãi nhất đứng chắn giữa nhân gian và vực sâu diệt thế!

"Lâm Tịch..." Tôi khẽ mỉm cười, thì thầm với chiếc trâm ngọc trong túi áo: "Cô hãy yên tâm ngủ say. Mảnh đất này, cõi nhân gian này... tôi sẽ bảo vệ trọn vẹn!"

*Tuuuuu... Tuuuuu...!*

Một hồi còi tàu viễn dương vang lên giòn giã dưới gầm cầu, rền vang khắp không gian sông nước bao la, như khúc tráng ca hào hùng báo hiệu sự khởi đầu của một đại kỷ nguyên mới!
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 46 (Vĩ thanh Hồi 1) vào manuscript...")
    with open(CH46_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã tạo tệp: {CH46_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 46 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=46,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an"],
        text=CHAPTER_CONTENT
    )
    print(f"    -> Kết quả kiểm duyệt: Passed={audit_res['passed']}, Tổng lỗi={audit_res['total_issues']}")
    if audit_res["issues"]:
        for iss in audit_res["issues"]:
            print(f"       * [{iss['category']} - {iss['severity']}]: {iss['description']}")
    
    if not audit_res["passed"]:
        print("[-] Kiểm duyệt thất bại! Có lỗi CRITICAL/HIGH.")
        return False

    # 3. Cập nhật Database
    print("[3/5] Đồng bộ trạng thái vào cơ sở dữ liệu novel_os.db...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().isoformat()
    word_count = len(CHAPTER_CONTENT.split())

    # 3.1 story_hierarchy
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, word_count, status, pov, created_at, updated_at)
    VALUES (?, 'chapter', 'mini_arc_01_03', 46, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_046", "Chương 46: Lời Thề Dưới Bình Minh Sài Gòn",
        "Rạng sáng 08/10/2026. Minh An thức dậy trong căn phòng trọ tĩnh lặng khi Lâm Tịch đã hoàn toàn trầm miên. Anh chạy bộ ra bờ sông Thanh Đa, luyện quyền Tam Chu Thiên trong sương sớm. Xương tủy tự tái tạo và kết tinh sau thử thách sinh tử, chính thức đột phá Luyện Cốt Trung kỳ (Cốt Nhược Kim Thạch). Minh An chạy lên đỉnh cầu Sài Gòn đón ánh bình minh rực rỡ, nhìn lại chặng đường 46 chương Hồi 1, lập lời thề kiên cường gánh vác sứ mệnh Người Gác Cổng Cô Độc bảo vệ thế giới nhân gian. Chính thức khép lại trọn vẹn Hồi 1 (Volume 1 / Arc 1), mở toang cánh cửa bước vào Hồi 2: Sóng Gió Biển Đông & Di Tích Phong Ấn.",
        word_count, now_iso, now_iso
    ))

    # Cập nhật trạng thái của Arc 1 và Volume 1 sang COMPLETED
    cur.execute("""
    UPDATE story_hierarchy SET status = 'COMPLETED', updated_at = ? WHERE id = 'mini_arc_01_03'
    """, (now_iso,))
    cur.execute("""
    UPDATE story_hierarchy SET status = 'COMPLETED', updated_at = ? WHERE id = 'arc_01'
    """, (now_iso,))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 46, 1, '2026-10-08T07:00:00+07:00', 46, 'loc_thanh_da', ?, ?, ?)
    """, (
        "EVT-CH046-01", "Vĩ thanh Hồi 1: Đột phá Luyện Cốt Trung kỳ và Lời thề dưới bình minh cầu Sài Gòn",
        json.dumps(["char_minh_an"], ensure_ascii=False),
        "Sáng sớm 08/10/2026 (05:00 - 07:00). Minh An rèn luyện Tam Chu Thiên ven sông Thanh Đa khi không còn Lâm Tịch hướng dẫn. Thân thể phá vỡ gông cùm, xương cốt ngân vang như ngọc khánh, chính thức đột phá Luyện Cốt Trung kỳ (Cốt Nhược Kim Thạch). Minh An lên đỉnh cầu Sài Gòn ngắm bình minh và dòng sông, xác lập lời thề bảo vệ nhân gian trước đại kiếp nạn rạn nứt phong ấn toàn cầu. Khép lại Arc 1.",
        "Đột phá Luyện Cốt Trung kỳ thành công; hoàn tất quá trình trưởng thành tự lập của nhân vật chính; khép lại trọn vẹn Hồi 1 (Arc 1); mở ra tiền đề vững chắc cho quy mô 3000+ chương."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 46, 'Đỉnh cầu Sài Gòn, TP.HCM', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Trung kỳ vững vàng: Cốt Nhược Kim Thạch, tủy ngân tiếng chuông, khí huyết cô đặc như thủy ngân)",
        "Thân thể đạt độ hoàn mỹ mới, các vết rạn xương hoàn toàn biến mất và kết tinh thành màng kim thạch dẻo dai, thể lực sung mãn đỉnh cao",
        json.dumps([], ensure_ascii=False),
        json.dumps(["Chiếc trâm ngọc cổ (Lâm Tịch đang trầm miên)", "Bộ đồ thể thao chạy bộ", "Điện thoại thông minh"], ensure_ascii=False),
        "Thanh thản, kiên định, tự tin tuyệt đối vào sức mạnh phàm nhân và tinh thần trách nhiệm bảo vệ cõi đất mẹ"
    ))

    # 3.4 story_threads
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 46, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Minh An chính thức đột phá Luyện Cốt Trung kỳ (Cốt Nhược Kim Thạch), hoàn thành trọn vẹn lộ trình Thể Đạo của Hồi 1.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 46, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-003'
    """, ("Khép lại vết rạn Nhà Bè, mở ra tầm nhìn toàn cầu về lưới phong ấn Trái Đất tầng 6 chuẩn bị cho Arc 2.", now_iso))

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 46...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH46_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 46.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_046.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 46: Lời Thề Dưới Bình Minh Sài Gòn",
        chapter_num=46,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT SOẠN THẢO CHƯƠNG 46 THÀNH CÔNG ===")
    else:
        sys.exit(1)

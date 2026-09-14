# -*- coding: utf-8 -*-
"""Script viết lại bản thảo Chương 44: Vết Rạn Phong Ấn Và Cái Giá Của Phàm Nhân."""

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
CH44_PATH = os.path.join(MANUSCRIPT_DIR, "ch_044.md")

CHAPTER_CONTENT = """---
chapter: 44
title: "Vết Rạn Phong Ấn Và Cái Giá Của Phàm Nhân"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Đáy ngã ba sông Nhà Bè (độ sâu 40m) & Buồng giải áp tàu Đại Dương 09, TP.HCM"
date: "2026-10-07"
word_count: 2980
---

# Chương 44: Vết Rạn Phong Ấn Và Cái Giá Của Phàm Nhân

Một giờ mười lăm phút chiều ngày mùng bảy tháng Mười năm 2026.

Dưới độ sâu bốn mươi mét lòng sông Soài Rạp, thế giới hoàn toàn chìm vào một cơn ác mộng đen tối và buốt giá.

Cơn lốc xoáy nước ngầm màu đen kịt cuộn trào hung hãn như một con cự long tà ác vừa thức tỉnh khỏi phong ấn. Luồng hắc khí Hư Không Tha Hóa rít lên từng hồi ghê rợn, cuốn theo từng tảng bùn khoáng chu sa và xé toạc các dây cáp tín hiệu phụ nối với thân tàu trên mặt nước. 

Ánh đèn chiếu điểm công suất lớn trên vai tôi chớp nháy liên hồi rồi vụt tắt ngấm dưới sự ăn mòn trường lực dị thường.

"Cậu An! Lặn 01 bất tỉnh rồi! Nhịp tim cậu ấy đang rơi tự do!" Tiếng người lính đặc nhiệm mang mã hiệu Lặn 02 — đồng chí Thành — gào lên qua tai nghe bộ đàm, âm thanh vỡ vụn vì nhiễu sóng cơ học cực mạnh: "Lớp vỏ titan của lồng lặn đang bị hắc khí gặm nhấm rỉ sét! Chúng ta phải phát tín hiệu tời kéo khẩn cấp lên mặt nước ngay!"

"Không được kéo lúc này!" Tôi quát lớn, hai chân bọc ủng cao su chuyên dụng cắm chặt vào tầng bùn nhão để giữ thăng bằng trước lực hút kinh hoàng của dòng xoáy: "Dòng xoáy hắc ám này có lực hút vượt quá năm tấn lực, nếu tàu phía trên dùng tời giật mạnh, cáp chịu lực sẽ đứt toạc, lồng lặn sẽ bị đập nát vào chân vòm đá! Đồng chí Thành, khóa chặt cửa lồng, bật van xả nhiệt lượng sưởi ấm tối đa để giữ thân nhiệt cho Dũng! Mọi việc còn lại cứ để tôi lo!"

"Nhưng cậu đang ở ngoài một mình..."

"Đóng cửa lại!" Tôi gầm lên dứt khoát.

*Rầm!*

Cánh cửa thép titan của lồng lặn khép chặt lại. Người lính đặc nhiệm hải quân dù dạn dày trận mạc cũng phải tuân lệnh kỷ luật chiến trường trước sự quyết đoán của tôi.

Khoảnh khắc cánh cửa thép đóng lại, tôi hoàn toàn đơn độc giữa lòng đáy sông tối tăm bốn mươi mét.

Áp suất năm atmosphere cùng luồng khí lạnh tha hóa bủa vây bốn bề, ép chặt vào lồng ngực tôi như muốn bóp nát từng cơ quan nội tạng. Khí thở Nitrox qua ống thở bỗng trở nên buốt giá như băng tuyết. Qua lớp kính mũ lặn mờ đục, tôi nhìn thấy vòm cổng Thủy Môn Cổ Phách đang rung chuyển dữ dội.

Trên đỉnh vòm móng rồng, viên cự thạch Huyết Ngọc Trấn Ba đang nứt ra từng vệt rạn đỏ sẫm. Những sợi tơ đen đặc quánh như hắc ín đang điên cuồng khoan sâu vào tâm viên ngọc, muốn xé toạc lõi phong ấn để mở toang cánh cửa dẫn thẳng ra rãnh biển sâu ngoài vịnh Cần Giờ!

Một khi Thủy Môn sụp đổ, toàn bộ luồng nước nhiễm độc tha hóa sẽ tràn ngược vào sông Sài Gòn và sông Đồng Nai. Mười triệu người dân thành phố, gia đình, bạn bè và cuộc sống bình yên của mảnh đất này sẽ bị hủy diệt trong một thảm họa không thể đảo ngược!

*"Minh An..."*

Thanh âm của Lâm Tịch vang lên từ sâu thẳm trong thức hải tôi. Giọng nói của nàng không còn sự bàng hoàng lúc ban đầu, mà đã lắng lại thành một sự bi tráng, kiên định đến thắt lòng:

*"Viên Huyết Ngọc Trấn Ba không thể chống đỡ thêm được ba phút nữa... Nếu để hắc khí phá vỡ mắt trận, toàn bộ cõi đất này sẽ vĩnh viễn biến thành một vùng đất chết bị tha hóa.*

*Ta sẽ dốc cạn toàn bộ tàn lực nguyên thần còn sót lại để kích hoạt một kiếm ý **Băng Phách Trảm Tuyết** tinh thuần nhất, cưỡng chế đóng băng luồng hắc khí này trong ba mươi nhịp thở.*

*Thế nhưng... ta là tàn hồn vô thể, kiếm ý này bắt buộc phải mượn thân xác và kinh mạch của ngươi làm vật dẫn để phát xuất.*

*Thể phách của ngươi mới chỉ ở Luyện Cốt sơ kỳ... Uy lực phản chấn của kiếm ý viễn cổ sẽ đè nặng lên từng khúc xương ngón tay, cánh tay và màng tủy của ngươi. Ngươi sẽ phải nếm trải nỗi đau rạn xương xé thịt chưa từng thấy... Thậm chí, nếu không trụ vững, hai cánh tay của ngươi có thể bị phế bỏ hoàn toàn!"*

Nghe những lời cảnh báo rợn người ấy, khóe môi tôi dưới lớp mặt nạ lặn bỗng khẽ nhếch lên một nụ cười kiêu hãnh.

"Lâm Tịch, cô đã nhìn thấy thành phố ngoài kia rồi đấy," tôi đáp lại nàng trong tâm thức, giọng nói trầm ổn như bàn thạch: "Những người phàm trần chúng tôi không có thần thông dời non lấp bể, nhưng chúng tôi biết bảo vệ đồng loại của mình. Nếu một người làm Giám đốc Kỹ thuật Dữ liệu như tôi, một người bước chân vào Thể Đạo như tôi còn sợ đau, sợ nứt xương mà lùi bước, thì ai sẽ đứng ra bảo vệ mẹ tôi ở quê nhà, bảo vệ mười triệu con người đang sống bình yên trên kia?

Ra kiếm đi! Xương của tôi... chịu được!"

*"Được lắm! Ngươi là một phàm nhân kiên cường nhất mà ta từng gặp trong suốt vạn năm qua!"*

Lâm Tịch cất tiếng quát vang trong thức hải. 

Ngay khoảnh khắc ấy, sâu trong tâm thức tôi, thanh kiếm tàn Băng Phách Trảm Tuyết bỗng nhiên bùng nổ một luồng ánh hào quang màu lam ngọc rực rỡ và thuần khiết đến tột độ!

Một luồng kiếm ý lạnh buốt nhưng mang theo uy thế cái thế nghìn đời từ thức hải trút thẳng xuống cột sống của tôi!

*Rắc! Rắc!*

Nỗi đau đớn khủng khiếp lập tức ập đến.

Từng đốt sống lưng của tôi phát ra những tiếng kêu răng rắc rợn người. Luồng kiếm ý sắc lẹm như hàng vạn lưỡi dao cạo quét qua các bó cơ bắp, ép thẳng vào tủy xương rồi cuộn trào ra hai bờ vai, rót mạnh xuống hai cánh tay tôi!

Tôi cắn chặt môi đến mức bật máu tươi trong khoang miệng. Cơn đau thấu tận tim gan khiến toàn thân tôi co giật dữ dội, nhưng hai bàn chân trần bọc ủng cao su vẫn găm chặt xuống tầng bùn ngàn cân, không lùi nửa bước!

"Tam Chu Thiên... Khí Huyết Hóa Kiếm!" Tôi gầm lên trong cổ họng.

Máu nóng Luyện Cốt trong cơ thể tôi sôi trào điên cuồng, hòa quyện làm một với kiếm ý lam tuyết của Lâm Tịch. Từ hai bàn tay bọc găng dã chiến của tôi, một luồng kiếm khí màu lam ngọc dài hơn ba mét rực sáng xé toạc màn nước đỏ ngầu!

*Vút!*

Tôi dồn toàn bộ sinh lực và ý chí sắt đá của mình, vung mạnh hai cánh tay chém một nhát kiếm ngang trời đáy nước!

*Ầm ầm ầm!*

Một tiếng nổ trầm hùng vang dội xé rách tầng đáy sông Soài Rạp.

Luồng kiếm khí Băng Phách mang theo quy tắc đông kết viễn cổ quét thẳng vào tâm điểm của cơn lốc xoáy hắc ám. Trước ánh sáng thần thánh của thanh kiếm tàn, luồng hắc khí Hư Không Tha Hóa rít lên những tiếng thét the thé ghê rợn. 

Toàn bộ dòng xoáy nước đen ngòm, những sợi tơ hắc ám và vùng nước quanh vòm Thủy Môn bỗng nhiên bị đóng băng hoàn toàn thành một khối băng tinh thể màu tím đen khổng lồ!

Dòng chảy đáy sông ngưng đọng lại trong ba mươi nhịp thở!

Thế nhưng, cái giá phải trả lập tức giáng xuống cơ thể tôi:

*Rắc... Rắc... Rắc!*

Lực phản chấn kinh hoàng từ quy tắc kiếm ý viễn cổ dội ngược trở lại. Tôi cảm nhận rõ ràng màng xương tủy ở hai cẳng tay và khớp cổ tay của mình bị xé rách, từng vết rạn nứt li ti lan tỏa trên bề mặt xương cánh tay như lớp men gốm bị búa gõ! Cơn đau đớn kịch liệt làm mắt tôi hoa lên, máu tươi ứa ra từ cánh mũi và khóe môi nhuộm đỏ một góc kính mũ lặn.

*"Minh An! Kiếm ý chỉ phong tỏa được ba mươi giây!"* Giọng Lâm Tịch vang lên yếu ớt tột độ, hơi thở của nàng đứt quãng như ngọn đèn trước gió: *"Nhìn sang chân phải vòm đá... Có một then cài bằng đồng đen... Đó là **Trấn Hải Khóa Trận**... Phải dùng khí huyết phàm trần ép then cài xoay ngược chiều kim đồng hồ để kích hoạt cơ chế tự phong bế của Thủy Môn... Nhanh lên!"*

Thời gian đang đếm ngược từng giây.

Tôi nghiến chặt răng, nén cơn đau buốt tận xương tủy, lê từng bước chân nặng như đeo chì qua lớp bùn nhão tiến về phía chân vòm đá.

Dưới luồng sáng mờ ảo của khối băng tím đen, một chiếc then cài bằng đồng đen hình đầu rồng ngậm ngọc hiện ra. Đó chính là chốt khóa cơ học ngàn năm mà tổ tiên phương Nam đã dày công thiết lập để khóa chặt cửa biển khi biến cố giáng lâm!

Không có thần thông, không có bùa phép hỗ trợ. Cổ nhân đúc then cài này yêu cầu chính bàn tay và khí huyết của nhân loại bản địa làm mồi lửa kích hoạt!

Tôi quỳ sụp một chân xuống bùn lầy, đưa hai bàn tay đang run rẩy vì rạn xương áp chặt lên đầu then đồng lạnh ngắt.

Dòng máu tươi thấm qua kẽ găng tay rách nát, chạm vào bề mặt kim loại đồng đen.

*Ong...*

Chiếc then cài cổ xưa bỗng rung lên một tiếng trầm hùng, như nhận ra dòng máu Khí Huyết Đạo kiên cường của người con đất Việt!

"Một... Hai... Ba... Khóa!" 

Tôi hét lên một tiếng xé lòng, vận dụng chút sinh lực Luyện Cốt sơ kỳ cuối cùng còn sót lại, dồn toàn bộ trọng lượng cơ thể và ý chí sinh tồn vặn mạnh then cài theo góc nghiêng bốn mươi lăm độ sang mạn thuyền!

*Cạch!*

Một tiếng then kim loại ăn khớp vang lên đanh gọn, chấn động cả tầng bùn sâu!

Ngay khoảnh khắc then cài sập chốt, viên cự thạch Huyết Ngọc Trấn Ba trên đỉnh vòm Thủy Môn như được tiếp thêm một nguồn sinh khí mới. Toàn bộ bột khoáng chu sa và thạch anh ngàn năm trong lòng đá bỗng bùng nổ một luồng thần quang màu đỏ rực chói lọi như vầng thái dương mọc giữa đáy biển sâu!

*Xèo xèo xèo!*

Luồng thần quang đỏ rực quét qua tới đâu, khối băng đen và toàn bộ những sợi tơ Hư Không Tha Hóa lập tức bốc hơi thành tro bụi hư vô tới đó! Khe nứt không gian đen ngòm dưới chân móng Thủy Môn từ từ khép chặt lại dưới sức nặng của hàng ngàn tấn đá thanh hoa. 

Dòng xoáy ngầm hung hãn biến mất, tiếng rít xé lòng dịu hẳn đi. Mặt nước ngã ba sông Nhà Bè từ từ trở lại một màu phù sa nâu đỏ hiền hòa quen thuộc.

Vết rạn phong ấn viễn cổ đã được khép lại an toàn!

Thế nhưng, sức lực cuối cùng trong cơ thể tôi cũng hoàn toàn cạn kiệt.

Hai cánh tay buông thõng xuống lớp bùn nhão, hoàn toàn mất đi cảm giác. Mắt tôi tối sầm lại, cả cơ thể nặng nề đổ gục xuống trước chân vòm đá Thủy Môn, nhịp tim rơi xuống ngưỡng báo động nguy kịch.

*Keng!*

Cánh cửa lồng lặn titan bật mở toang. Đồng chí Thành lao ra khỏi khoang lồng, hai tay ôm chặt lấy thân thể tôi kéo giật vào trong buồng an toàn.

"Cậu An! Cậu An tỉnh lại đi!" Tiếng Thành thất thanh gọi qua micro, bàn tay anh run rẩy giật mạnh chốt xả phao cứu sinh khẩn cấp và bấm nút còi hú báo động: "Tàu Đại Dương 09! Kéo lồng lặn khẩn cấp! Cậu An bị thương nặng! Đưa thẳng vào buồng giải áp y tế!"

*Vút!*

Dàn tời thủy lực trên boong tàu nhận tín hiệu khẩn cấp, cuộn cáp với tốc độ tối đa, nhấc bổng chiếc lồng titan xé toạc làn nước đỏ lao thẳng lên mặt sông!

Một giờ bốn mươi phút chiều.

Cửa lồng lặn mở tung trên sàn tàu `Đại Dương 09`.

Đại úy Hùng và hai bác sĩ quân y lập tức lao tới, nâng thân thể tôi đặt lên cáng cứu thương dã chiến. Mũ lặn được tháo rời, để lộ gương mặt tôi tái nhợt không còn giọt máu, máu tươi thấm ướt cổ áo bảo hộ.

"Đưa ngay vào buồng giải áp cao áp trên tàu! Bật oxy nguyên chất một trăm phần trăm! Cố định nẹp nẹp hai cẳng tay nghi rạn xương!" Tiếng bác sĩ quân y hô gấp gáp.

Cánh cửa buồng giải áp đóng lại. Tiếng khí oxy nén rít lên êm ả.

Nằm trên chiếc giường nệm của buồng giải áp, giữa lằn ranh mong manh của sự sống và cái chết, tôi khẽ hé đôi mắt mệt mỏi nhìn qua ô kính tròn nhỏ. 

Bên ngoài boong tàu, bầu trời ngã ba sông Nhà Bè đã trong xanh trở lại, những tia nắng vàng rực rỡ chiếu rọi mặt nước bình yên. Dưới đáy sâu bốn mươi mét kia, hiểm họa diệt thế đã bị đẩy lùi bởi xương tủy và dòng máu nóng của một người phàm trần.

Và sâu trong tâm thức tôi, một đốm sáng màu lam ngọc mờ ảo khẽ run rẩy một nhịp cuối cùng, trước khi chìm sâu vào một giấc ngủ tĩnh lặng vô tận.
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 44 viết lại vào manuscript...")
    with open(CH44_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã cập nhật tệp: {CH44_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 44 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=44,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich"],
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
    VALUES (?, 'chapter', 'mini_arc_01_03', 44, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_044", "Chương 44: Vết Rạn Phong Ấn Và Cái Giá Của Phàm Nhân",
        "Tại độ sâu 40m ngã ba sông Nhà Bè, luồng hắc khí Hư Không Tha Hóa đe dọa phá hủy Thủy Môn và nghiền nát lồng lặn. Lặn 01 bất tỉnh, Minh An lệnh cho Lặn 02 khóa cửa lồng an toàn rồi một mình đối mặt hiểm nguy. Lâm Tịch dốc cạn tàn lực thi triển kiếm ý Băng Phách Trảm Tuyết mượn thân xác Minh An làm vật dẫn đông kết dòng xoáy tha hóa trong 30 giây. Lực phản chấn khiến xương cẳng tay và màng tủy của Minh An rạn nứt dữ dội. Trong khoảnh khắc sinh tử, Minh An dùng máu nóng và ý chí kiên định xoay then đồng Trấn Hải Khóa Trận, kích hoạt viên Huyết Ngọc Trấn Ba bộc phát thần quang quét sạch hắc khí, khép kín miệng rạn phong ấn viễn cổ. Minh An kiệt sức ngã gục, được Lặn 02 kéo vào lồng và đưa gấp lên buồng giải áp cao áp tàu Đại Dương 09.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 44, 1, '2026-10-07T14:45:00+07:00', 44, 'loc_nha_be', ?, ?, ?)
    """, (
        "EVT-CH044-01", "Chiến đấu đáy sâu 40m, kích hoạt Trấn Hải Khóa Trận và đóng lại vết rạn phong ấn viễn cổ",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "Lặn 01 Dũng", "Lặn 02 Thành"], ensure_ascii=False),
        "Chiều 07/10/2026 (~13:15 - 14:45). Minh An một mình bọc hậu dưới đáy sông 40m. Lâm Tịch dẫn kiếm ý Băng Phách qua thân thể Minh An đông kết hắc khí tha hóa. Minh An gánh chịu phản chấn nứt xương cẳng tay, kiên cường xoay then đồng Ngạc Khảm kích hoạt thần quang Huyết Ngọc tiêu diệt tà khí, vá kín vết rạn phong ấn. Minh An ngất lịm, được kéo khẩn cấp lên tàu Đại Dương 09 đưa vào buồng giải áp cao áp điều trị.",
        "Khép kín thành công vết rạn phong ấn Thủy Môn; tiêu diệt hắc khí Hư Không Tha Hóa; bảo vệ toàn vẹn luồng hàng hải và hạ lưu Sài Gòn; Minh An bị rạn xương cẳng tay do phản chấn kiếm ý; Lâm Tịch tiêu hao cạn kiệt nguyên thần rơi vào hôn mê sâu."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 44, 'Buồng giải áp tàu Đại Dương 09, TP.HCM', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ cực hạn, tủy xương kích phát năng lực tự chữa lành vi mô)",
        "Kiệt sức hoàn toàn, hai cẳng tay và cổ tay bị rạn nứt xương do phản chấn kiếm ý viễn cổ, khóe miệng chảy máu, nhịp tim 55 bpm đang hồi phục trong buồng oxy cao áp",
        json.dumps(["Rạn nứt vi mô xương cẳng tay và cổ tay hai bên", "Chấn thương màng tủy do phản chấn kiếm ý viễn cổ"], ensure_ascii=False),
        json.dumps(["Bộ đồ lặn neoprene rách găng tay", "Nẹp cố định y tế hai tay", "Chiếc trâm ngọc cổ (mờ tối)"], ensure_ascii=False),
        "Thanh thản, kiêu hãnh vì đã bảo vệ được thành phố, cảm nhận sâu sắc sự tàn khốc của quy tắc vũ trụ và ý chí kiên định của Thể Đạo"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 44, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (nguyên thần cạn kiệt hoàn toàn sau khi xuất kiếm ý Băng Phách Trảm Tuyết, rơi vào trạng thái ngủ say bất tỉnh)",
        "Nguyên thần suy kiệt 99%, ý thức phong bế tuyệt đối để tự bảo tồn, không còn khả năng phát ra âm thanh hay truyền niệm",
        json.dumps(["Đạo cơ vỡ nát", "Nguyên thần cạn kiệt sức mạnh chìm vào hôn mê"], ensure_ascii=False),
        json.dumps(["Bản thể kiếm tàn Băng Phách Trảm Tuyết (hoàn toàn ảm đạm)"], ensure_ascii=False),
        "Thanh thản, khâm phục ý chí kiên cường và nhân cách phi phàm của Minh An"
    ))

    # 3.4 story_threads
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-003'
    """, ("Vết rạn phong ấn Thủy Môn Nhà Bè đã được đóng lại tạm thời nhờ Trấn Hải Khóa Trận, nhưng để lộ sự thật phong ấn Trái Đất đang già cỗi.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-001'
    """, ("Lâm Tịch cạn kiệt nguyên thần sau nhát kiếm đáy sông, rơi vào hôn mê sâu chuẩn bị bước vào giai đoạn trầm miên dài hạn.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Minh An nếm trải cái giá của phàm nhân, gánh chịu phản chấn rạn xương cẳng tay, ý chí Thể Đạo tôi luyện đạt bước nhảy vọt tâm tính.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 44, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-001'
    """, ("Thủy Môn Cổ Phách được bảo vệ nguyên vẹn, cơ chế phong tỏa cửa biển vận hành hoàn tất.", now_iso))

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 44...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH44_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 44.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_044.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 44: Vết Rạn Phong Ấn Và Cái Giá Của Phàm Nhân",
        chapter_num=44,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT VIẾT LẠI CHƯƠNG 44 THÀNH CÔNG ===")
    else:
        sys.exit(1)

# -*- coding: utf-8 -*-
"""Script soạn thảo và kiểm duyệt bản thảo Chương 43 theo đúng Canon và rào chắn Author."""

import os
import sys
import json
import sqlite3
from datetime import datetime

sys.path.insert(0, r"d:\tieu-thuyet")

if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

DB_PATH = r"d:\tieu-thuyet\database\novel_os.db"
MANUSCRIPT_DIR = r"d:\tieu-thuyet\manuscript\markdown\volume_01\arc_01"
CH43_PATH = os.path.join(MANUSCRIPT_DIR, "ch_043.md")

CHAPTER_CONTENT = """---
chapter: 43
title: "Vùng Nước Đỏ Và Ranh Giới Áp Suất"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Ngã ba sông Nhà Bè, TP.HCM"
date: "2026-10-07"
word_count: 2450
---

# Chương 43: Vùng Nước Đỏ Và Ranh Giới Áp Suất

Mười hai giờ bốn mươi phút trưa ngày mùng bảy tháng Mười năm 2026.

Gió từ cửa biển Cần Giờ thốc ngược vào lòng sông Soài Rạp mang theo vị mằn mặn nồng gắt của đại dương, xộc thẳng vào cánh mũi tôi. Khác hẳn với mùi rêu mốc ẩm ướt quen thuộc của những đoạn sông chảy qua Thanh Đa hay cầu Bình Lợi, không khí tại ngã ba sông Nhà Bè ngập tràn cảm giác khoáng đạt nhưng cũng đầy khắc nghiệt.

Cách mạn tàu `Đại Dương 09` chừng tám trăm mét về phía luồng hàng hải quốc tế, một chiếc tàu container khổng lồ dài hơn hai trăm mét mang cờ Panama đang chậm rãi xẻ sóng tiến về cụm cảng Hiệp Phước. Hồi còi tàu vang lên một tiếng trầm đục, rền rĩ kéo dài như tiếng thở dài của một sinh vật kim khí thời hiện đại, làm rung chuyển cả những vạt dừa nước lúp xúp ven bờ huyện Nhơn Trạch bên kia ranh giới Đồng Nai.

Tiếng còi tàu ấy đột ngột kéo phăng toàn bộ sự hưng phấn kỳ ảo của buổi sáng trở lại với mặt đất.

Chiếc điện thoại để trong túi áo bảo hộ dã chiến của tôi bỗng rung lên bần bật ba hồi dài. Tôi rút máy ra nhìn màn hình. Hai tin nhắn mới hiện lên cùng lúc: một tin nhắn từ sếp Huy trong nhóm chat marketing của công ty hỏi về tiến độ bản đề xuất truyền thông cho chiến dịch quý tư; tin còn lại là thông báo tự động từ ngân hàng nhắc nợ tiền điện và tiền rác tháng Mười của căn phòng trọ nhỏ trên đường Ung Văn Khiêm.

Tôi nhìn dòng thông báo trên màn hình điện thoại, khẽ nhếch môi thở ra một làn hơi nhẹ. Giữa lúc chân tôi đang đứng trên con tàu quân sự viễn thám trị giá hàng trăm tỷ đồng, chuẩn bị đối mặt với một cấu trúc ngầm bí ẩn chôn sâu dưới bùn đáy sông, thì cuộc sống đời thường của một thanh niên hai mươi lăm tuổi tại Sài Gòn vẫn không ngừng gõ cửa đòi nợ. 

Thế giới này không hề biến thành một cõi tiên bồng bềnh sau một đêm. Cơm áo, công việc, trách nhiệm và áp lực mưu sinh vẫn bám chặt lấy từng thớ thịt, từng nhịp thở của tôi như một sợi dây neo vô hình giữ chặt lấy bờ cõi hiện thực.

"Cậu An, uống ngụm trà nóng đi."

Tiếng nói trầm ấm của chú Phan Thanh Tùng cắt ngang dòng suy nghĩ của tôi. Chú bước tới bên lan can boong mũi, đưa cho tôi một chiếc ly giữ nhiệt bốc khói nghi ngút mùi trà sen thơm ngát.

"Cháu cảm ơn chú Tùng." Tôi đón lấy chiếc ly, hai bàn tay áp vào thân kim loại ấm áp.

Chú Tùng hướng ánh nhìn xa xăm về phía ngã ba sông mênh mông, nơi dòng phù sa nâu đỏ của sông Đồng Nai hòa lẫn vào sắc nước sông Sài Gòn rồi bỗng nhiên biến chuyển thành một vệt nước màu đỏ quạch như chu sa.

"Vùng nước Nhà Bè này từ xưa đã nổi tiếng hiểm trở." Chú Tùng chậm rãi nói, giọng nhuốm màu hoài niệm của một nhà nghiên cứu văn hóa dân gian: "Ca dao xưa có câu: *'Nhà Bè nước chảy chia hai, ai về Gia Định, Đồng Nai thì về'*. Các cụ ngày trước chỉ thấy nước chảy xiết tạo thành xoáy ngầm sâu hoắm nuốt chìm ghe thuyền, nên mới dựng những bè tre kết lại giữa sông làm nơi cứu tế nước ngọt và gạo cho người lỡ độ đường. Nhưng theo những mảnh tài liệu Hán Nôm dập rập từ thời chúa Nguyễn mà Viện vừa phục chế đêm qua, phía dưới tầng bùn sét bốn mươi mét nơi đáy sông này từng có một công trình kè đá quy mô phi thường. Người xưa gọi đó là cửa cống Trấn Ba."

"Cửa cống Trấn Ba..." Tôi lặp lại cụm từ ấy, mắt dõi theo vệt sương mù xám bạc đang bốc lên là là trên mặt nước đỏ.

"Đúng vậy. Nhưng đó là cách người xưa nhìn nhận theo nhãn quan phong thủy thời bấy giờ." Tiến sĩ Trịnh Hoài Nam từ trong cabin điều hành bước ra, trên tay cầm chiếc máy tính bảng quân sự đang hiển thị mặt cắt địa chấn 3D đáy sông: "Còn dưới góc độ địa kỹ thuật hiện đại, chúng tôi ghi nhận một đới đứt gãy kiến tạo cổ chạy ngầm dọc theo lũng sông Soài Rạp. Vệt nước màu đỏ thẫm mà chúng ta đang thấy không phải là do phù sa thông thường, cũng không phải tảo biển độc hại. Cảm biến quang phổ vừa phân tích mẫu nước bề mặt cho thấy hàm lượng oxit sắt, thạch anh vi tinh thể và hạt khoáng chu sa tăng vọt gấp hai mươi lần mức bình thường. Có một luồng áp lực thủy tĩnh cực lớn từ dưới tầng đáy sâu đang đùn những lớp khoáng vật ngàn năm này lên mặt nước."

Đại úy Trần Văn Hùng rảo bước tới, sắc mặt nghiêm nghị trong bộ quân phục dã chiến gọn gàng:

"Báo cáo Tiến sĩ Nam, cậu An. Cảng vụ Hàng hải TP.HCM vừa phát điện văn chấp thuận lập vùng cấm luồng tạm thời trong bán kính bốn trăm mét quanh tàu `Đại Dương 09`. Hai cano cao tốc của Thủy đoàn II Cảnh sát đường thủy và Trạm Biên phòng Cửa khẩu Nhà Bè đang duy trì phao tiêu phân luồng phía ngoài, bảo đảm các tàu hàng quốc tế không đi lệch vào vùng xoáy nước. Toàn bộ thiết bị lặn sâu chuyên dụng đã sẵn sàng trên sàn cẩu."

Tôi quay nhìn về phía sàn thao tác đuôi tàu. Chiếc lồng lặn áp lực cao bằng hợp kim titan hình trụ tròn màu cam sáng đang được dàn tời thủy lực nâng lên khỏi bệ đỡ. Bên cạnh đó, hai người nhái đặc nhiệm dày dạn kinh nghiệm của hải quân đang kiểm tra lần cuối các cụm van thở Nitrox, bình dưỡng khí nén hỗn hợp helium-oxy và dây rốn tín hiệu tích hợp camera độ phân giải cao.

Tôi hít một hơi không khí mang theo vị mặn của gió biển, rồi khẽ nhắm mắt lại.

Dưới lòng bàn chân trần áp sát mặt sàn boong tàu, tầng xương tủy của tôi khẽ rung lên từng chập.

Nhờ thành tựu Luyện Cốt sơ kỳ đạt được sau những đêm trui rèn gian khổ, khung xương của tôi giờ đây có khả năng dẫn truyền cơ học cực kỳ nhạy bén. Tôi không nhìn thấy những hình ảnh kỳ ảo viễn vông nào, nhưng qua từng đợt rung lắc của vỏ thép con tàu, tôi cảm nhận được một lực cản vật lý khổng lồ đang cuộn xoáy dưới độ sâu bốn mươi mét. Đó là một dòng chảy rối có vận tốc lên tới gần ba mét mỗi giây, va đập liên hồi vào một khối kiến trúc sừng sững nằm ngập trong bùn lầy, tạo nên một dải dao động tần số thấp rền rĩ như tiếng máy phát điện ngầm khổng lồ.

*"Minh An..."*

Một thanh âm trong trẻo nhưng mỏng manh tựa như làn khói thoảng qua vang lên sâu trong thức hải tôi.

Đó là giọng của Lâm Tịch. Nhưng không giống như vẻ uy nghiêm, trang trọng lúc sáng, giọng nàng lúc này lộ rõ sự mệt mỏi cùng cực. Từng âm tiết phát ra như phải vượt qua một tầng sương mù dày đặc che khuất tâm trí.

*"Cô Tịch? Cô có sao không?"* Tôi vội vàng tập trung ý niệm hỏi lại trong đầu.

Một thoáng im lặng kéo dài, rồi tiếng thở dài nhè nhẹ của nàng truyền đến:

*"Ta không sao... Chỉ là tàn hồn chưa lành lặn, lại liên tiếp tiêu hao nguyên thần để cộng hưởng kiếm ý, linh lực trong thức hải đã cạn kiệt phần lớn. Ký ức của ta về vùng nước này... rất mờ mịt. Ta chỉ lờ mờ nhớ rằng nơi này từng có một kết cấu phong tỏa dòng nước rất lớn, dùng để ngăn chặn sự xói mòn và giữ vững điểm tựa cho vùng châu thổ. Nhưng bản chất thực sự của nó bị chôn vùi quá sâu, chính ta lúc này cũng không thể nhìn thấu được..."*

Lâm Tịch dừng lại một nhịp, dường như phải cố gắng gom góp chút sức lực tàn dư để dặn dò tôi:

*"Ngươi phải nhớ kỹ... Ngươi mới chỉ bước qua ngưỡng Luyện Cốt sơ kỳ, thể xác phàm nhân này vẫn có giới hạn sinh học rõ ràng. Xuống tới bốn mươi mét nước, áp suất tương đương năm lần khí quyển sẽ đè nặng lên từng cen-ti-mét vuông da thịt. Nếu ngươi cậy mạnh dùng sức phàm chống lại nước, lồng ngực ngươi sẽ co thắt dẫn đến vỡ mạch máu phổi trước khi kịp chạm tới đáy bùn.*

*Khi xuống nước, hãy thu liễm mọi ý nghĩ phân tán. Vận hành luồng hơi thở Khí Huyết theo vòng Tam Chu Thiên chậm lại ba nhịp so với bình thường, để dòng máu ấm nuôi dưỡng màng tủy, để khung xương tự triệt tiêu lực ép của nước. Ngươi hiểu chưa?"*

*"Tôi hiểu rồi. Cảm ơn cô."* Tôi đáp thầm, trong lòng dâng lên một sự tôn trọng và ấm áp tĩnh lặng.

Lâm Tịch không phải là một vị thần toàn năng có thể giải quyết mọi rắc rối bằng một cái phẩy tay. Nàng là một tồn tại cổ xưa mang đầy thương tích, đang cùng tôi nương tựa vào nhau để sinh tồn. Sự nhắc nhở mộc mạc và chân thực của nàng quý giá hơn bất kỳ lời hứa hẹn thần thông rực rỡ nào.

"Cậu An, đã đến giờ." Đại úy Hùng bước tới, đưa cho tôi bộ đồ lặn chuyên dụng bằng cao su tổng hợp neoprene gia cường sợi chống đâm thủng: "Bộ đồ này trang bị mạch sưởi nhiệt điện trở và van xả áp tự động. Chúng tôi sẽ hạ lồng lặn xuống độ sâu ba mươi lăm mét, sau đó hai đồng chí người nhái giàu kinh nghiệm nhất sẽ cùng cậu rời lồng bằng dây cáp rốn an toàn để tiếp cận vị trí dị thường."

Tôi gật đầu dứt khoát:

"Rõ, Đại úy!"

Mười phút sau.

Tôi đã mặc xong toàn bộ trang bị lặn nặng gần ba mươi kilôgam. Mũ lặn composite có kính vòm quan sát rộng được khóa chặt vào cổ áo bằng khớp ren kim loại đanh gọn. Tiếng xì xào của van cấp khí Nitrox vang lên đều đặn bên tai, mang theo luồng dưỡng khí khô mát thổi thẳng vào khoang mũi.

Trên ngực tôi, một cụm cảm biến sinh học truyền dữ liệu nhịp tim và huyết áp trực tiếp về màn hình của Tiến sĩ Nam.

"Kiểm tra bộ đàm: Một, hai, ba, bốn." Tiếng tôi vang lên qua micro gắn trong mũ.

"Nghe rất rõ, cậu An!" Giọng Tiến sĩ Nam phản hồi lập tức: "Nhịp tim bảy mươi hai, huyết áp một trăm hai mươi trên tám mươi. Chỉ số sinh tồn hoàn hảo. Hãy nhớ, an toàn sinh mạng là ưu tiên số một. Nếu cảm thấy tức ngực hoặc choáng váng vì áp lực, lập tức giật dây tín hiệu để tời kéo lồng lên ngay!"

"Đã hiểu."

Tôi bước vào trong lồng lặn hình trụ cùng hai chiến sĩ đặc nhiệm hải quân mang mã hiệu Lặn 01 và Lặn 02. Cánh cửa thép nặng nề đóng sầm lại, các chốt an toàn xoay tròn khóa chặt.

*Két... Két...*

Cần cẩu thủy lực gầm lên. Chiếc lồng lặn từ từ nhấc bổng khỏi sàn tàu, vươn qua mạn sắt rồi bắt đầu hạ dần xuống mặt nước sông Soài Rạp.

Một giây trước khi mặt nước đỏ thẫm nuốt chửng tầm nhìn qua ô kính, tôi kịp nhìn thấy bầu trời phương Nam trong xanh lồng lộng phía trên đầu, thấy những nhành bần xanh rì ven bờ Nhà Bè, và bóng hình chú Tùng cùng Đại úy Hùng đang đứng nghiêm nghị dõi theo.

*Ùm!*

Một tiếng va đập lớn vang lên khi đáy lồng chạm nước.

Mặt sông khép lại trên nóc lồng lặn. Toàn bộ âm thanh ồn ã của còi tàu, tiếng máy nổ và gió biển lập tức biến mất, nhường chỗ cho một sự im lặng đặc quánh, thăm thẳm và đầy áp bức.

Nước sông Nhà Bè đục ngầu phù sa đỏ quạch. Dù dàn đèn pha halogen công suất cao gắn quanh lồng lặn đã bật sáng hết cỡ, tầm nhìn qua ô kính lặn vẫn bị thu hẹp chỉ còn chưa đầy một mét rưỡi. Những hạt bụi khoáng thạch màu đồng thau lấp lánh trôi lơ lửng trong làn nước, va chạm vào thành kính tạo nên những vệt sáng nhờ nhợ như đom đóm trong đêm tối.

*Mười mét...*

Đồng hồ đo độ sâu trên cổ tay tôi nhảy số. Tai tôi bắt đầu có cảm giác lùng bùng nghẹt lại vì chênh lệch áp suất. Tôi khẽ nuốt nước bọt, thực hiện thao tác cân bằng áp lực hòm nhĩ.

*Hai mươi mét...*

Dòng nước bên ngoài bắt đầu chảy xiết dữ dội. Chiếc lồng lặn bằng titan nặng hơn một tấn khẽ chao đảo, dây cáp chịu lực căng ra phát ra những tiếng *ken két* khô khốc. Nhiệt độ nước tụt nhanh từ ba mươi độ C xuống còn chưa đầy mười tám độ C. Cảm giác lạnh buốt bắt đầu thấm qua lớp cao su bảo hộ, bóp nghẹt lấy các đầu ngón chân.

*Ba mươi mét... Ba mươi lăm mét...*

"Áp lực ngoài khoang: bốn phẩy năm bar!" Tiếng kỹ sư Tuấn vang lên qua tai nghe, lẫn trong tiếng rè rè của sóng vô tuyến xuyên nước: "Lồng lặn đã tiếp cận độ sâu ba mươi lăm mét! Cách đáy bùn năm mét! Dòng xoáy ngầm đo được hai phẩy bốn mét trên giây! Độ đục vượt ngưỡng quan sát quang học!"

"Lặn 01 báo cáo: Mở cửa lồng lặn!" Tiếng người chiến sĩ đặc nhiệm đi cùng tôi vang lên bình tĩnh qua bộ đàm.

Cửa lồng bật mở.

Dòng nước đỏ ngầu cuộn xoáy lập tức ùa vào khoang ngập. Tôi bước chân ra khỏi lồng lặn, hai tay nắm chặt lấy dây cáp rốn định vị.

Một sức nặng kinh hoàng lập tức đè sụp lên toàn bộ cơ thể tôi!

Đó không phải là ảo giác, mà là sức nặng thuần túy của ba mươi lăm mét cột nước — tương đương gần năm kilôgam áp lực đè lên mỗi cen-ti-mét vuông trên lồng ngực. Không khí trong bình nén dường như trở nên đặc quánh hơn, mỗi lần hít vào đòi hỏi cơ hoành phải vận lực gấp ba lần bình thường. Cơn buốt nhức chạy dọc từ màng nhĩ xuống hai bên thái dương.

Nhớ lời dặn của Lâm Tịch, tôi lập tức nhắm nghiền hai mắt lại, không cố dùng sức cơ bắp để gồng mình chống cự.

Tôi chậm rãi dẫn dắt luồng nhiệt lưu Khí Huyết từ đan điền cuộn lên, luồn qua đốt sống Đại Chùy rồi tỏa đều vào hai trăm linh sáu mảnh xương tủy theo vòng Tam Chu Thiên. Nhịp thở của tôi hạ chậm lại ba nhịp. Từng thớ cơ bắp dần thả lỏng, để khung xương cứng cáp như kim thạch tự động gánh vác lấy sức ép của ngoại giới.

Cơn tức ngực dần dịu đi, nhịp tim từ một trăm mười nhịp chậm rãi hạ xuống mức bảy mươi nhịp ổn định.

Tôi mở mắt ra, bật chiếc đèn chiếu điểm công suất lớn cầm tay, bước theo hai người thợ lặn tiến sát xuống đáy bùn sâu ba mươi tám mét.

Dưới luồng sáng vàng xuyên thấu làn phù sa đỏ đục ngầu, đáy sông Nhà Bè dần dần hiện ra trước mắt tôi.

Đó không phải là một bãi bùn bằng phẳng.

Ngay trước mũi chân tôi chừng ba mét, một vách đá khổng lồ màu xám đen sừng sững vươn lên từ lớp phù sa cổ. Khối kiến trúc ấy được ghép từ những phiến đá thanh hoa nguyên khối dài hàng chục mét, phủ kín những lớp hà biển hóa thạch và gỉ đồng xanh thẫm dày cộp. 

Trên bề mặt phiến đá cổ ngập trong bùn lầy, một hoa văn móng rồng uốn lượn được đục đẽo tinh xảo hiện ra dưới ánh đèn rọi rực rỡ. Và ngay chính giữa vòm cửa ngầm ấy, một dòng nước xoáy đỏ rực đang bị hút mạnh vào một khe hở kẹt đầy thân cây gỗ mục và bùn khoáng ngàn năm.

Tại độ sâu gần bốn mươi mét dưới đáy dòng sông Sài Gòn, nơi ranh giới của áp suất và bóng tối tuyệt đối, cánh cửa Thủy Môn cổ xưa đã chính thức lộ diện trước mắt những con người của năm 2026.
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 43 vào manuscript...")
    with open(CH43_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã tạo tệp: {CH43_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 43 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=43,
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

    # 3. Cập nhật Database (Story Hierarchy, Timeline Events, Character States, Foreshadowing, Threads)
    print("[3/5] Đồng bộ trạng thái vào cơ sở dữ liệu novel_os.db...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().isoformat()
    word_count = len(CHAPTER_CONTENT.split())

    # 3.1 story_hierarchy
    cur.execute("""
    INSERT OR REPLACE INTO story_hierarchy (id, level, parent_id, order_index, title, summary, word_count, status, pov, created_at, updated_at)
    VALUES (?, 'chapter', 'mini_arc_01_03', 43, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_043", "Chương 43: Vùng Nước Đỏ Và Ranh Giới Áp Suất",
        "Minh An cùng đội đặc nhiệm hải quân trên tàu Đại Dương 09 tại ngã ba sông Nhà Bè chuẩn bị lặn ngầm. Minh An nhận tin nhắn đời thường từ công ty và tiền trọ nhắc nhở mỏ neo hiện thực. Lâm Tịch cảnh báo áp lực nước 5 bar và chỉ dẫn điều khí. Minh An mặc đồ lặn áp lực cao, chìm xuống 38m, đối mặt áp suất khắc nghiệt và tiếp cận vách đá Thủy Môn cổ phủ rêu phong dưới đáy bùn Soài Rạp.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 43, 1, '2026-10-07T13:30:00+07:00', 43, 'loc_nha_be', ?, ?, ?)
    """, (
        "EVT-CH043-01", "Chiến dịch hạ lồng lặn sâu 38m tại ngã ba sông Nhà Bè và chạm tới vách đá Thủy Môn Cổ",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "chú Tùng", "kỹ sư Tuấn"], ensure_ascii=False),
        "Trưa 07/10/2026 (~12:40 - 13:45). Tàu Đại Dương 09 neo tại ngã ba sông Nhà Bè, Cảng vụ Hàng hải và Cảnh sát đường thủy lập vành đai bảo vệ. Minh An nhận tin nhắn công ty và nợ tiền trọ Bình Thạnh. Lâm Tịch yếu ớt dặn dò điều hòa nhịp thở Tam Chu Thiên chống áp lực 5 bar. Minh An cùng 2 thợ lặn hải quân hạ lồng titan xuống 38m dưới bùn ngã ba Soài Rạp, vượt qua rét buốt và áp suất, chạm vào vách đá thanh hoa khắc móng rồng của Thủy Môn cổ kẹt thân cây mục.",
        "Tiếp cận thành công vách đá Thủy Môn ở độ sâu 38m; giải mã hiện tượng thủy triều đỏ do oxit sắt và chu sa bị đùn lên từ khe nứt cống ngầm (tiến triển FSH-027); đặt nền tảng cho việc tháo chốt ở Ch 44."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 43, 'loc_nha_be', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ, Tam Chu Thiên điều khí chống áp lực nước sâu 5 bar)",
        "Thể lực tiêu hao do chịu áp suất 38m nước, xương tủy kiên định chịu lực cơ học, phổi điều khí ổn định nhịp tim 70 bpm",
        json.dumps(["Ê ẩm màng nhĩ do chênh lệch áp suất hòm nhĩ", "Tê cóng nhẹ đầu ngón chân do nước lạnh 18 độ C"], ensure_ascii=False),
        json.dumps(["Điện thoại thông minh (nhận tin nhắn công ty & tiền trọ)", "Bộ đồ lặn áp lực cao neoprene", "Bình khí Nitrox & dây rốn tín hiệu", "Đèn chiếu điểm ngầm"], ensure_ascii=False),
        "Bình tĩnh, tỉnh táo, tôn trọng quy luật khắc nghiệt của tự nhiên, gạt bỏ mơ mộng kỳ ảo để tập trung sinh tồn"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 43, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (nguyên thần suy kiệt sau khi kích hoạt kiếm ý, cần chìm vào giấc ngủ phục hồi)",
        "Linh lực cạn kiệt, ký ức phân mảnh mờ mịt về cấu trúc Nhà Bè, duy trì liên lạc ý niệm tối thiểu",
        json.dumps(["Đạo cơ vỡ nát", "Nguyên thần suy kiệt"], ensure_ascii=False),
        json.dumps(["Thanh kiếm tàn Băng Phách Trảm Tuyết (ngủ say trong thức hải)"], ensure_ascii=False),
        "Thầm lặng, kiên nhẫn, lo lắng thực tế cho an nguy của Minh An dưới áp lực nước"
    ))

    # 3.4 story_threads touch
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 43, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-001'
    """, ("Minh An đã chạm vào vách đá Thủy Môn tại độ sâu 38m đáy sông Nhà Bè, phát hiện khe nứt bị nghẹt trầm tích.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 43, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-002'
    """, ("Khung xương Cốt Tủy Thông Minh của Minh An chịu đựng thành công áp lực nước 5 bar ở độ sâu gần 40m nhờ điều hòa Tam Chu Thiên.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 43, current_state = ?, updated_at = ? WHERE thread_id = 'TH-CHR-001'
    """, ("Minh An đối mặt với áp lực công việc cơ quan và hạn nộp tiền trọ tháng 10 qua tin nhắn điện thoại trước giờ lặn.", now_iso))

    # 3.5 foreshadowing update
    cur.execute("""
    UPDATE foreshadowing_ledger SET status = 'ACTIVE' WHERE id = 'FSH-027'
    """)

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 43...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH43_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 43.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_043.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 43: Vùng Nước Đỏ Và Ranh Giới Áp Suất",
        chapter_num=43,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT SOẠN THẢO CHƯƠNG 43 THÀNH CÔNG ===")
    else:
        sys.exit(1)

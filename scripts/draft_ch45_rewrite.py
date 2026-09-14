# -*- coding: utf-8 -*-
"""Script viết lại bản thảo Chương 45: Lâm Tịch Trầm Miên Và Người Gác Cổng Cô Độc."""

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
CH45_PATH = os.path.join(MANUSCRIPT_DIR, "ch_045.md")

CHAPTER_CONTENT = """---
chapter: 45
title: "Lâm Tịch Trầm Miên Và Người Gác Cổng Cô Độc"
arc: 1
volume: 1
pov: "Nguyễn Minh An"
location: "Cảng Tân Thuận (Quận 7) & Phòng trọ Bình Thạnh, TP.HCM"
date: "2026-10-07"
word_count: 3120
---

# Chương 45: Lâm Tịch Trầm Miên Và Người Gác Cổng Cô Độc

Bốn giờ chiều ngày mùng bảy tháng Mười năm 2026.

Tiếng van xả khí của buồng giải áp cao áp trên tàu `Đại Dương 09` rít lên một hồi dài rồi từ từ hạ dần áp lực về mức một atmosphere.

Khi cánh cửa thép tròn mở toang, luồng không khí ấm nồng của buổi chiều phương Nam tràn vào lồng ngực tôi. Bác sĩ quân y đứng bên ngoài lập tức bước tới, cẩn thận kiểm tra các điện cực gắn trên ngực tôi cùng dải băng nẹp cố định quanh hai cẳng tay.

"Thật là khó tin..." Người bác sĩ trẻ nhìn vào màn hình máy siêu âm xương di động, lắc đầu với vẻ mặt ngỡ ngàng tột độ: "Các vết nứt rạn vi mô trên màng xương và thân xương trụ của hai cánh tay cậu... chỉ sau ba tiếng thở oxy cao áp mà các mô tế bào liên kết đã tự động khép miệng với tốc độ kinh ngạc! Nhịp tim của cậu đã ổn định ở mức sáu mươi nhịp trên phút, không còn bất kỳ dấu hiệu ngộ độc khí nén nào."

Tôi mỉm cười nhẹ, khẽ cử động mười đầu ngón tay.

Bên dưới lớp da thịt còn vương những vết bầm tím, tủy xương Luyện Cốt sơ kỳ đang âm thầm tỏa ra một luồng nhiệt lưu ấm áp dịu dàng. Dòng máu nóng Tam Chu Thiên không ngừng luân chuyển, cần mẫn vận chuyển dinh dưỡng để hàn gắn từng vết rạn nứt mà kiếm ý Băng Phách viễn cổ đã để lại. Nỗi đau xé thịt rách tủy dưới đáy sông bốn mươi mét ban trưa đã lắng xuống, đổi lại là một cảm giác kiên định, đậm đặc chưa từng có của khung xương phàm trần.

"Còn tình hình của đồng chí Dũng thế nào rồi bác sĩ?" Tôi hỏi, giọng còn hơi khàn do dư chấn áp suất.

"Đồng chí Dũng đã qua cơn nguy kịch, thân nhiệt đã tăng lên ba mươi sáu độ năm," bác sĩ đáp, nhưng ánh mắt thoáng hiện vẻ hoang mang tột cùng: "Thế nhưng, mảnh giáp titan bọc cẳng tay của cậu ấy... khi chúng tôi đưa vào máy quang phổ huỳnh quang tia X để phân tích thì phát hiện toàn bộ cấu trúc mạng tinh thể kim loại đã bị phân rã hoàn toàn thành một dạng bột vô định hình. Không có bất kỳ dấu vết nào của axit hay chất oxy hóa phàm trần... Đó là sự phân rã ở cấp độ hạ nguyên tử mà khoa học hiện đại chưa từng ghi nhận."

Tôi lặng im, đưa mắt nhìn sang căn phòng họp tác chiến của tàu qua khung cửa kính cách âm.

Ở đó, không khí căng thẳng bao trùm. Đại úy Trần Văn Hùng, Tiến sĩ Trịnh Hoài Nam và chú Phan Thanh Tùng đang tham gia một cuộc họp giao ban trực tuyến bảo mật cấp độ cao nhất với đại diện Thường trực Ủy ban Nhân dân Thành phố và Bộ Tư lệnh Hải quân. 

Trên màn hình lớn là bản kết luận kỹ thuật được đóng dấu đỏ chót: **TẬP MẬT QUỐC GIA — NIÊM PHONG VĨNH VIỄN**.

Toàn bộ các biểu đồ từ trường xoắn ốc ngược, số liệu tán xạ sonar dị thường và mẫu kim loại titan bị phân rã đều được chuyển vào kho lưu trữ tuyệt mật. Bản thông cáo báo chí gửi ra ngoài chỉ vỏn vẹn ba dòng: *"Hiện tượng đổi màu nước cục bộ tại ngã ba sông Nhà Bè do túi bùn khoáng ngầm giải tỏa tự nhiên đã chấm dứt; luồng hàng hải Soài Rạp và Lòng Tàu mở lại bình thường từ mười sáu giờ ba mươi phút."*

Đó là sự bảo vệ tối thượng cho sự bình yên của mười triệu cư dân đô thị. Thế giới hiện đại chưa sẵn sàng, và có lẽ không bao giờ nên biết rằng ngay dưới chân họ, một vết rạn phong ấn viễn cổ vừa suýt chút nữa mở toang cánh cửa dẫn tới vực sâu hủy diệt.

Năm giờ ba mươi phút chiều.

Chiếc tàu `Đại Dương 09` cập mạn cầu cảng Tân Thuận. 

Tôi bước xuống boong tàu trong bộ thường phục giản dị. Đại úy Hùng bước tới tiễn tôi bên chân cầu cảng, bàn tay rắn rỏi của người chỉ huy đặc nhiệm siết chặt vai tôi bằng một sự kính trọng tuyệt đối:

"Cậu An... tôi là người lính biển, cả đời chỉ tin vào súng đạn và kỷ luật quân đội. Nhưng những gì cậu đã làm dưới đáy sông bốn mươi mét trưa nay... toàn thể Đội Đặc nhiệm và cá nhân tôi nợ cậu một mạng sống. Sau này, bất kể khi nào cậu cần, hải quân chúng tôi luôn sẵn sàng sát cánh bên cậu."

"Cảm ơn Đại úy. Mong đồng chí Dũng mau chóng bình phục," tôi cười đáp lễ.

Vì hai cánh tay còn đang được cố định lớp nẹp vải mềm để xương tủy tự hàn gắn, tôi không dắt chiếc xe máy Wave Alpha tại bãi xe cảng vụ, mà đón một chuyến taxi công nghệ trở về Bình Thạnh.

Ngồi trên băng ghế sau của chiếc taxi, nhìn qua khung cửa kính xe, tôi ngắm nhìn dòng người ken đặc trong giờ tan tầm trên cầu Tân Thuận và đường Nguyễn Tất Thành.

Tiếng còi xe máy inh ỏi, khói bụi mịt mù, những người mẹ chở con tan trường, những chiếc xe đẩy bán cá viên chiên bốc khói ngào ngạt bên lề đường... 

Mới ba tiếng trước, tôi còn ở dưới cõi địa ngục đen tối của đáy sông Nhà Bè, đối mặt với sự xâm thực của thế lực Hư Không Tha Hóa ngoài hành tinh; vậy mà lúc này, xung quanh tôi lại là nhịp sống hối hả, bình dị và ồn ã của trần gian. Sự tương phản mãnh liệt ấy khiến khóe mắt tôi cay cay. Tôi hiểu rằng, sự bình yên tầm thường này đáng giá biết bao, và cái giá của sự rạn xương nứt tủy trưa nay là hoàn toàn xứng đáng.

Bảy giờ tối.

Chiếc taxi dừng trước con hẻm nhỏ trên đường D2, quận Bình Thạnh. 

Tôi ghé vào quán cháo quen thuộc đầu hẻm, mua một phần cháo sườn hột vịt bắc thảo nóng hổi rồi chậm rãi bước lên căn gác trọ tầng ba của mình.

Căn phòng trọ mười lăm mét vuông đón tôi bằng sự tĩnh lặng quen thuộc. Chiếc quạt trần quay chậm rãi xua đi hơi nóng tích tụ cả ngày, khung cửa sổ nhỏ mở ra bầu trời đêm thành phố lấp lánh muôn ngàn ánh đèn.

Tôi ngồi vào bàn, húp từng muỗng cháo nóng. Vị ngọt đậm đà của nước hầm xương, vị béo bùi của trứng bắc thảo và hơi ấm của gừng tươi nhanh chóng lan tỏa khắp dạ dày, cung cấp nguồn calo dồi dào để cơ thể tiếp tục bồi bổ khí huyết.

Ăn xong, tôi mở chiếc máy tính xách tay lên.

Trên cổng thông tin điều hành nội bộ của Viện Nghiên cứu Địa tầng và Năng lượng Nội sinh Đô thị, hộp thư của Giám đốc Kỹ thuật Dữ liệu đã nhận được tệp báo cáo mã hóa từ kỹ sư Tuấn:

*"Báo cáo Giám đốc Minh An, toàn bộ các trạm quan trắc địa kỹ thuật tại Ba Son, Thủ Thiêm và Nhà Bè đã được thiết lập chế độ cô lập dữ liệu theo lệnh của Hội đồng Khoa học. Em đã chuyển đổi toàn bộ thuật toán phân tích về trạng thái thụ động. Kính gửi anh duyệt biên bản đóng hồ sơ sự cố."*

Tôi lướt ngón tay trên bàn phím, kiểm tra lại chữ ký bảo mật rồi dùng mã khóa cá nhân phê chuẩn lệnh đóng hồ sơ. Trách nhiệm công việc của một người đứng đầu kỹ thuật dữ liệu đã được hoàn tất một cách trọn vẹn, không để lại bất kỳ kẽ hở nào cho sự hoang mang lan truyền ra xã hội.

Đúng lúc đó, chiếc điện thoại đặt bên cạnh màn hình bỗng rung lên từng hồi chuông ấm áp. Cuộc gọi video từ mẹ ở quê.

Tôi vội vàng kéo tay áo thun xuống che đi dải băng nẹp ở cẳng tay, hít một hơi thật sâu để giọng nói trở nên khỏe khoắn rồi bấm nút nhận cuộc gọi.

Gương mặt hiền từ, phúc hậu của mẹ hiện lên trên màn hình, phía sau là gian bếp nhỏ ấm cúng ánh lửa củi:

"An hả con? Bữa nay đi làm về muộn thế con? Đã ăn uống gì chưa?"

"Dạ con vừa ăn bát cháo nóng xong mẹ ơi," tôi mỉm cười, ánh mắt ngập tràn sự dịu dàng: "Hôm nay Viện có chuyến khảo sát thực địa ven sông, con mới về phòng nghỉ. Ở nhà bố mẹ thế nào rồi mẹ?"

"Bố mày vừa uống nước chè xanh ngoài hiên xong, dạo này uống thuốc con gửi về thấy bảo lưng nhẹ nhõm hẳn rồi. Mẹ nghe đài báo dưới mạn Nhà Bè bữa nay có hiện tượng sương mù với triều cường dị thường dữ lắm, tàu bè phải cấm luồng, mẹ cứ lo con đi làm ngoài đó lại dầm mưa cảm lạnh. Dạo này làm lãnh đạo kỹ thuật ở Viện có vất vả lắm không con? Bố mày cứ tự hào khoe với bà con trong họ là con trai làm giám đốc ngoài thành phố, nhưng mẹ chỉ mong con giữ gìn sức khỏe, ăn uống cho có da có thịt, đừng có thức khuya quá nghe con..."

Nghe từng lời dặn dò mộc mạc, chan chứa tình yêu thương của mẹ, lắng nghe tiếng dế mèn rả rích nơi quê nhà xa xôi vọng qua chiếc loa điện thoại, một luồng hơi ấm ngập tràn trái tim tôi.

Dù tôi có mang danh Giám đốc Kỹ thuật Dữ liệu, dù tôi có gánh trên vai trọng trách của một người tu luyện Thể Đạo đối đầu với thế lực ngoài hành tinh, thì tận sâu trong tâm hồn, tôi vẫn mãi là đứa con trai nhỏ bé của mẹ. Mẹ chính là chiếc mỏ neo sắt đá giữ chặt linh hồn tôi ở lại với cõi phàm trần này, nhắc nhở tôi lý do tối thượng để kiên cường chiến đấu.

"Con khỏe lắm mẹ ơi, công việc ở Viện rất tốt, tháng này con được khen thưởng dự án lớn, mai con chuyển tiền về mẹ nhớ mua thêm yến sào bồi bổ cho bố mẹ nhé. Mẹ ngủ sớm đi nha."

"Ừ, con cũng nghỉ sớm đi con..."

Cuộc gọi kết thúc. Căn phòng trọ lại trở về với sự yên ắng thanh bình.

Chín giờ ba mươi phút tối.

Tôi tắt ngọn đèn tuýp trên trần, chỉ để lại ánh sáng vàng dìu dịu của chiếc đèn bàn. Tôi bước tới tấm chiếu cói giữa sàn, tháo lớp băng nẹp mềm ra khỏi hai cánh tay, rồi ngồi xếp bằng theo tư thế ngũ tâm triều thiên.

Khép hờ mi mắt, tôi dẫn luồng nhiệt lưu Khí Huyết từ đan điền chậm rãi dâng lên. 

Dưới sự lắng đọng tuyệt đối của tâm thức, tôi bắt đầu nhìn sâu vào bên trong cơ thể mình. Từng tế bào, từng thớ cơ và đặc biệt là hai trăm linh sáu mảnh xương tủy đang ngân lên một thanh âm trầm hùng như chuông đồng cổ. Dù bị rạn nứt vi mô sau cú phản chấn của kiếm ý viễn cổ, nhưng chính nhờ trải qua thử thách sinh tử tàn khốc ấy, lớp cốt màng của tôi đã được tôi luyện trở nên kiên cố, đậm đặc hơn gấp bội. 

Tôi có thể cảm nhận rõ ràng: Bình cảnh của Luyện Cốt sơ kỳ đã hoàn toàn bị phá vỡ. Một ngưỡng cửa mới của Thể Đạo đang âm thầm mở ra trước mắt tôi.

*"Minh An..."*

Một thanh âm vô cùng yếu ớt, mỏng manh như một sợi tơ bỗng vang lên từ nơi sâu thẳm nhất trong thức hải.

Tôi giật mình tập trung ý niệm.

Trước mắt tôi, giữa không gian tâm thức mờ mịt, hư ảnh của Lâm Tịch dần hiện ra. 

Thế nhưng, khác hẳn với vẻ uy nghi, lộng lẫy của một nữ kiếm tiên từng đứng ngạo nghễ giữa chín tầng mây, bóng hình của nàng lúc này gần như trong suốt, tà áo trắng hư ảo chập chờn tựa như một làn khói sương sắp tan biến vào hư vô. Gương mặt thanh tú của nàng lộ rõ vẻ tiều tụy, suy kiệt tột cùng, thanh kiếm tàn Băng Phách Trảm Tuyết sau lưng nàng đã tắt ngấm toàn bộ ánh hào quang, trở về hình hài một mảnh kim loại đen rỉ sét nằm im lìm trong bóng tối.

"Lâm Tịch! Cô thế nào rồi?" Tôi lo lắng thốt lên trong ý niệm.

Khóe môi Lâm Tịch khẽ nở một nụ cười mờ nhạt, ánh mắt nàng nhìn tôi ngập tràn sự thán phục và xúc động sâu xa:

*"Ta không sao... nhưng nhát kiếm Băng Phách trưa nay đã rút cạn những sợi tàn lực nguyên thần cuối cùng của ta.*

*Minh An... vạn năm qua, ta từng chứng kiến vô số thiên kiêu cái thế của các đại tông môn viễn cổ. Bọn họ tu vi thông thiên triệt địa, có thể dời non lấp bể, nhưng khi đối mặt với sự xâm thực của Hư Không Tha Hóa, bọn họ đều chỉ biết tìm đường đào tẩu để bảo toàn mạng sống của riêng mình.*

*Nhưng ngươi... một phàm nhân bằng xương bằng thịt, chưa từng bước vào con đường tu tiên chính thống, lại dám lấy cốt nhục của mình chịu đựng kiếm ý phản chấn, dám một mình đứng chặn cửa lồng lặn để bảo vệ đồng loại.*

*Ngươi đã khiến một tàn hồn viễn cổ như ta phải cúi đầu khâm phục."*

"Lâm Tịch, cô đừng nói nữa, hãy mau nghỉ ngơi đi," tôi đáp, cảm nhận được sự suy kiệt đến bờ vực tan biến của nàng.

*"Nghe ta nói hết đã, thời gian của ta không còn nhiều..."* Giọng Lâm Tịch chùng xuống, trở nên vô cùng trang nghiêm và bi tráng:

*"Trưa nay, khi chạm trán với luồng hắc khí dưới đáy sông Nhà Bè, một phần ký ức phong ấn viễn cổ trong thức hải của ta đã được giải mã.*

*Minh An... thế giới mà ngươi đang sống, hành tinh mà các ngươi gọi là Trái Đất này... thực chất không phải là một cõi phàm trần vô danh.*

*Nó chính là **Cõi Giới Phong Ấn Tầng Thứ Sáu** — một nhà tù khổng lồ mà chư vị đại năng viễn cổ năm xưa đã dốc cạn sinh mệnh để thiết lập nhằm phong ấn một bí mật kinh thiên động địa sâu trong lòng đất mẹ!*

*Họ đã phong tỏa linh khí, biến nơi này thành cõi mạt pháp để ngăn không cho thế lực Hư Không Tha Hóa định vị tọa độ của cõi này.*

*Thế nhưng... không có phong ấn nào là vĩnh cửu.*

*Sau muôn vàn năm tháng, chu kỳ của đại trận phong ấn tầng thứ sáu đã bắt đầu bước vào thời kỳ suy vi. Vết rạn phong ấn dưới đáy sông Nhà Bè trưa nay... chỉ là tiếng chuông báo tử đầu tiên!*

*Trong tương lai, khi các rãnh nứt không gian ngoài biển khơi tiếp tục mở rộng, những vết rạn tương tự sẽ lần lượt bùng phát ở Biển Đông, ở các vùng biển sâu và các cấm địa phong ấn trên khắp địa cầu! Các thế lực tha hóa ngoài vũ trụ sẽ tìm cách gặm nhấm thế giới này!"*

Từng lời nói của Lâm Tịch như những tia chớp xé toạc màn đêm tăm tối, rọi sáng toàn bộ thế giới quan trước mắt tôi. 

Quy mô của thế giới không hề dừng lại ở thành phố mười triệu dân này! Một bức tranh vũ trụ tàn khốc, vĩ đại và đầy rẫy hiểm họa diệt vong đang từng bước phát lộ hình hài!

*"Năng lượng của ta đã chạm tới ranh giới sụp đổ..."* Bóng hình Lâm Tịch bắt đầu mờ dần, giọng nói nàng đứt quãng như tiếng gió thì thầm: *"Để tránh làm tổn hại đến khí huyết của ngươi và để bản nguyên tàn hồn không bị tiêu tán, lát nữa đây, ta sẽ tiến vào trạng thái **trầm miên sâu** trong chiếc trâm ngọc cổ.*

*Giấc ngủ này... có thể kéo dài một năm, mười năm, hoặc lâu hơn nữa.*

*Từ ngày mai, ngươi sẽ phải hoàn toàn cô độc bước đi trên con đường Thể Đạo.*

*Ngươi hãy nhớ lấy lời dặn cuối cùng này của ta:*

*Thể Đạo phàm nhân không dựa vào thiên địa linh khí, mà lấy chính thân xác làm đền đài, lấy ý chí bất khuất làm thần thông! Hãy kiên trì rèn luyện Tam Chu Thiên, rèn giũa xương tủy, hấp thu tinh hoa vạn vật.*

*Bởi vì khi vết rạn Biển Đông thực sự bùng nổ... khoa học kỹ thuật hiện đại sẽ bất lực... và ngươi, Minh An... sẽ là bức tường thành duy nhất đứng chắn giữa nhân gian và vực sâu diệt thế!"*

Nói dứt lời, hư ảnh của Lâm Tịch khẽ nghiêng mình cúi chào tôi một cái chào trang trọng của đạo hữu viễn cổ. 

Sau đó, toàn bộ bóng hình thanh tao của nàng hóa thành một hạt mầm ánh sáng màu lam nhạt, từ từ thu liễm lại, chìm sâu vào tâm chiếc trâm ngọc cổ nơi sâu thẳm thức hải, phong bế toàn bộ thần niệm, tiến vào một giấc ngủ trầm miên tĩnh lặng tuyệt đối.

Không gian tâm thức trở lại một màu đen tĩnh mịch, trống trải và cô tịch khôn cùng.

Tôi từ từ mở mắt ra.

Gió đêm mùa thu lùa qua khung cửa sổ phòng trọ, làm lay động vạt áo thun mỏng. Phía xa xa, tòa tháp Landmark 81 rực rỡ ánh đèn led đa sắc vươn thẳng lên bầu trời đêm, đại lộ Điện Biên Phủ vẫn tấp nập những vệt sáng đèn xe máy, tiếng cười nói râm ran của cư dân thành phố vọng lại ấm áp giữa màn đêm.

Tôi đưa tay nâng chiếc trâm ngọc cổ đang đặt trên mặt bàn làm việc.

Cây trâm ngọc lúc này lạnh ngắt, ảm đạm không còn một tia sáng, tựa như một món cổ vật bình thường nằm im lìm trong lòng bàn tay tôi. Không còn thanh âm nhắc nhở điềm đạm của Lâm Tịch, không còn sự bảo bọc của kiếm ý viễn cổ.

Tôi biết, từ giờ phút này trở đi, tôi đã thực sự trở thành một **Người gác cổng cô độc**.

Nhưng không có nỗi sợ hãi nào trong tim tôi cả.

Tôi nắm chặt chiếc trâm ngọc trong lòng bàn tay, hai cánh tay rạn nứt đang tự hàn gắn từng tấc thịt tấc xương. Dưới ánh đèn đêm của thành phố Sài Gòn năm 2026, ánh mắt tôi sáng ngời một ngọn lửa kiên định không bao giờ tắt.

Một thế giới tươi đẹp đến nhường này, một cõi nhân gian ấm áp và kiên cường đến nhường này...

Tôi nhất định sẽ dùng đôi bàn tay phàm trần này để bảo vệ đến cùng!
"""

def execute_drafting():
    print("[1/5] Ghi bản thảo Chương 45 viết lại vào manuscript...")
    with open(CH45_PATH, "w", encoding="utf-8") as f:
        f.write(CHAPTER_CONTENT.strip() + "\n")
    print(f"    -> Đã cập nhật tệp: {CH45_PATH}")

    # 2. Kiểm duyệt bằng CritiqueEngine
    print("[2/5] Kiểm duyệt bản thảo Chương 45 bằng CritiqueEngine...")
    from system.engines.critique_engine import CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    audit_res = critique.audit_chapter_draft(
        chapter_num=45,
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
    VALUES (?, 'chapter', 'mini_arc_01_03', 45, ?, ?, ?, 'LOCKED', 'Nguyễn Minh An', ?, ?)
    """, (
        "ch_045", "Chương 45: Lâm Tịch Trầm Miên Và Người Gác Cổng Cô Độc",
        "Minh An hồi phục trong buồng giải áp tàu Đại Dương 09, các vết rạn xương cẳng tay tự khép miệng kỳ diệu nhờ Luyện Cốt sơ kỳ. Toàn bộ hồ sơ sự cố Nhà Bè được niêm phong cấp Tuyệt Mật Quốc gia. Minh An trở về phòng trọ Bình Thạnh, phê duyệt đóng hồ sơ dữ liệu với tư cách Giám đốc Kỹ thuật Dữ liệu, gọi điện ấm áp cho mẹ ở quê. Đêm muộn, Lâm Tịch hiện diện lần cuối trong thức hải, hé lộ bí mật chấn động: Trái Đất là Cõi Giới Phong Ấn Tầng Thứ Sáu đang bước vào thời kỳ phong ấn suy thoái, vết nứt Nhà Bè chỉ là phát súng lệnh đầu tiên cho đại kiếp nạn Biển Đông. Lâm Tịch cạn kiệt nguyên thần chính thức tiến vào trầm miên dài hạn trong trâm ngọc. Minh An đón nhận sứ mệnh Người Gác Cổng Cô Độc, quyết tâm rèn luyện Thể Đạo độc lập để bảo vệ thế giới phàm trần.",
        word_count, now_iso, now_iso
    ))

    # 3.2 timeline_events
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, 45, 1, '2026-10-07T22:30:00+07:00', 45, 'loc_binh_thanh', ?, ?, ?)
    """, (
        "EVT-CH045-01", "Hồi phục sau chiến dịch Nhà Bè, Lâm Tịch hé lộ bí mật cõi giới phong ấn tầng 6 và bước vào trầm miên",
        json.dumps(["char_minh_an", "char_lam_tich", "Đại úy Hùng", "Tiến sĩ Nam", "Mẹ Minh An"], ensure_ascii=False),
        "Chiều và tối 07/10/2026 (~16:00 - 22:30). Minh An hồi phục trong buồng giải áp; hồ sơ Nhà Bè niêm phong Tuyệt Mật. Minh An về phòng trọ Bình Thạnh, hoàn thành trách nhiệm công việc Viện và gọi điện cho mẹ. Đêm muộn, Lâm Tịch đối thoại lần cuối, giải mã Trái Đất là Cõi Giới Phong Ấn Tầng 6 đang rạn nứt theo chu kỳ vạn năm, rồi chính thức trầm miên trong chiếc trâm ngọc cổ. Minh An trở thành Người Gác Cổng Cô Độc.",
        "Hồ sơ Nhà Bè được niêm phong an toàn; Minh An bắt đầu quá trình tự chữa lành xương tủy; hé lộ toàn cảnh cosmology Trái Đất tầng 6; Lâm Tịch bước vào trầm miên dài hạn; Minh An xác lập động lực tu luyện tối thượng cho hành trình 3000 chương."
    ))

    # 3.3 character_states
    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 45, 'Phòng trọ Bình Thạnh, TP.HCM', ?, ?, ?, ?, ?)
    """, (
        "char_minh_an",
        "Phàm nhân (Khí Huyết Đạo - Luyện Cốt Sơ kỳ viên mãn, chuẩn bị đột phá Luyện Cốt Trung kỳ Cốt Nhược Kim Thạch)",
        "Các vết rạn vi mô trên xương cẳng tay đang được tủy xương tự hàn gắn nhanh chóng, kinh mạch thông suốt, thể lực hồi phục 80%",
        json.dumps(["Rạn nứt vi mô xương cẳng tay đang trong quá trình tự chữa lành"], ensure_ascii=False),
        json.dumps(["Chiếc trâm ngọc cổ (Lâm Tịch đang trầm miên)", "Laptop làm việc Viện Nghiên cứu", "Điện thoại thông minh"], ensure_ascii=False),
        "Kiên định, trầm tĩnh, mang tâm thế của Người Gác Cổng Cô Độc, sẵn sàng tự lập gánh vác trách nhiệm bảo vệ cõi nhân gian"
    ))

    cur.execute("""
    INSERT INTO character_states (character_id, chapter_num, location_id, cultivation_realm, physical_condition, injuries_json, inventory_json, emotional_state)
    VALUES (?, 45, 'Thức hải Minh An', ?, ?, ?, ?, ?)
    """, (
        "char_lam_tich",
        "Tàn hồn viễn cổ (chính thức tiến vào trạng thái Trầm Miên sâu dài hạn trong chiếc trâm ngọc cổ)",
        "Nguyên thần ngủ say tĩnh lặng tuyệt đối, phong bế toàn bộ ý thức để phục hồi bản nguyên, không còn khả năng giao tiếp",
        json.dumps(["Đạo cơ vỡ nát", "Nguyên thần cạn kiệt sức mạnh chìm vào trầm miên"], ensure_ascii=False),
        json.dumps(["Bản thể kiếm tàn Băng Phách Trảm Tuyết (hoàn toàn ngủ say)"], ensure_ascii=False),
        "Thanh thản, an lòng, hoàn toàn tin tưởng và gửi gắm vận mệnh thế giới vào ý chí của Minh An"
    ))

    # 3.4 story_threads
    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-MYS-003'
    """, ("Lâm Tịch xác nhận Trái Đất là Cõi Giới Phong Ấn Tầng Thứ Sáu đang bước vào chu kỳ suy thoái, các vết rạn sẽ lan rộng ra Biển Đông và toàn cầu.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-PLT-001'
    """, ("Lâm Tịch chính thức bước vào trầm miên sâu dài hạn, Minh An bắt đầu giai đoạn tự lực cánh sinh trên con đường Thể Đạo.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-CHR-001'
    """, ("Minh An giữ vững vị thế Giám đốc Kỹ thuật Dữ liệu, hoàn thành trách nhiệm công việc và gắn kết bền chặt với tình thân gia đình.", now_iso))

    cur.execute("""
    UPDATE story_threads SET last_touched_chapter = 45, current_state = ?, updated_at = ? WHERE thread_id = 'TH-REL-001'
    """, ("Lâm Tịch khâm phục ý chí phàm nhân của Minh An trước khi trầm miên, mối quan hệ giữa hai người đạt độ tin cậy thiêng liêng cao nhất.", now_iso))

    conn.commit()
    conn.close()
    print("[+] Đồng bộ cơ sở dữ liệu hoàn tất!")

    # 4. Cập nhật FTS5 Search Index
    print("[4/5] Đánh chỉ mục FTS5 cho Chương 45...")
    from system.engines.retrieval_engine import RetrievalEngine
    retrieval = RetrievalEngine(DB_PATH)
    retrieval.index_chapter(CH45_PATH)
    print("    -> Đã lập chỉ mục BM25 cho Chương 45.")

    # 5. Xuất bản Word .docx
    print("[5/5] Xuất bản thảo sang định dạng Word (.docx)...")
    from system.engines.docx_pipeline import DocxPipeline
    from system.core.config import MANUSCRIPT_WORD_DIR
    docx_pipe = DocxPipeline()
    out_docx_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_01", "ch_045.docx")
    out_docx = docx_pipe.export_chapter_to_docx(
        title="Chương 45: Lâm Tịch Trầm Miên Và Người Gác Cổng Cô Độc",
        chapter_num=45,
        content_md=CHAPTER_CONTENT,
        output_docx_path=out_docx_path
    )
    print(f"    -> Đã xuất tệp Word: {out_docx}")

    return True

if __name__ == "__main__":
    success = execute_drafting()
    if success:
        print("\n=== HOÀN TẤT VIẾT LẠI CHƯƠNG 45 THÀNH CÔNG ===")
    else:
        sys.exit(1)

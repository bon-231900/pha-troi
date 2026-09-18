# -*- coding: utf-8 -*-
"""Draft Chapter 75 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, severe physical and tactical realism, everyday warmth, and multi-tier foreshadowing."""

import os
import sys
import json
import sqlite3
import re

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.canon_engine import CanonEngine
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine

CHAPTER_NUM = 76
CHAPTER_TITLE = "Dạ Hành Quy Đô"
DATE = "2026-10-24"
LOCATION = "Sông Lòng Tàu (Cần Giờ) & Căn Hộ Phòng Trọ Đường Nơ Trang Long (Bình Thạnh, TP.HCM)"

ACT1 = '''Mười một giờ bốn mươi phút đêm ngày hai mươi ba tháng mười.

Tàu Tuần Tra Cao Tốc HQ-268 rẽ sóng ngược dòng sông Lòng Tàu, đưa chúng tôi rời xa vùng biển Cần Giờ mặn mòi để trở về với nhịp thở đô thị Sài Gòn.

Đêm trên sông Lòng Tàu dày đặc một màu sương lam quánh lạnh. Tiếng động cơ diesel cỡ lớn dưới khoang máy phát ra những nhịp rung trầm đục, đều đặn đẩy thân tàu tuần tra lướt đi êm ả giữa hai dải rừng ngập mặn Rừng Sác đen thẫm sừng sững đôi bờ. Những rặng đước, rặng mắm nghìn năm cắm bộ rễ chằng chịt xuống bãi bùn lầy, trông tựa như những bức tường thành tự nhiên che chắn cho cửa ngõ phía đông nam thành phố. Gió sông thốc vào mặt tôi, mang theo mùi ngai ngái của bùn phù sa, hương lá mục và cái lạnh thanh sạch của đất trời sau cơn giông lớn.

Tôi đứng tựa lưng vào lan can thép ở mũi tàu, hai tay khoanh trước ngực. Chiếc áo phông sẫm màu dán chặt vào lồng ngực vạm vỡ theo từng cơn gió thổi.

Toàn thân tôi lúc này đang trải qua một sự chuyển hóa kỳ diệu mà chỉ người tu Thể Đạo phàm nhân mới có thể cảm nhận được sâu sắc.

Trận huyết chiến dưới độ sâu một ngàn hai trăm mét nước ở rãnh nứt Cực Tù Hải Uyên đã nghiền ép cơ thể tôi đến giới hạn sinh học cùng cực. Nhưng chính áp suất thủy tĩnh kinh hoàng một trăm hai mươi át-mốt-phe ấy, kết hợp với tuyệt kỹ *Hoán Huyết Hóa Cương*, đã biến ba mươi ba đốt sống lưng của tôi thành một khối ngọc thạch đồng thau hoàn chỉnh. Từng khớp xương, từng thớ gân như được đúc lại bằng hợp kim cổ xưa, vững chãi tựa bàn thạch.

Trong lồng ngực tôi, quả tim đập chậm rãi, uy lực với nhịp độ bốn mươi lần một phút. Mỗi nhịp tống máu là một luồng Thuần Dương Cương Huyết nóng hổi màu đồng thau cuồn cuộn chảy qua mạng lưới huyết quản, tự động gột rửa những vi thương tổn li ti nơi màng cơ và khớp sụn. Dù vừa lặn sâu ngàn trượng trở về, tôi không hề cảm thấy một chút mỏi mệt nào, trái lại, tinh thần tôi sáng rỡ, các giác quan sắc bén đến mức có thể lắng nghe rõ từng tiếng cá quẫy đuôi dưới lớp nước sông đục ngầu cách mũi tàu ba mươi mét.

Nơi túi áo trong bên ngực trái, khối *Tỏa Long Huyền Tỷ* vừa thu đắc dưới đáy biển đang tỏa ra từng nhịp ấm áp dịu dàng. Khối ngọc bích chạm khắc chín con rồng vàng uốn lượn dường như đã hòa nhịp với nhịp tim của tôi, phát xuất những tần số vi mô xoa dịu thần kinh, đẩy lùi hoàn toàn những tàn dư của hàn sát âm trọc tích tụ nơi đáy vực.

*"Minh An, ngươi có cảm nhận được sự dịu đi của dòng sông không?"*

Tiếng nói của Lâm Tịch khẽ vang lên trong thức hải tôi. Thanh âm nàng trong trẻo tựa chuông ngọc, mang theo sự thư thái hiếm hoi sau những giờ phút căng thẳng tột độ.

"Có." Tôi truyền niệm đáp lại, mắt nhìn theo những vệt sóng bạc cuộn trào bên mạn thuyền. "Nước sông Lòng Tàu đêm nay chảy rất đằm. Không còn những xoáy ngầm hung hãn hay mùi tanh nồng của trọc khí rò rỉ như lúc chúng ta xuôi dòng ra biển sáng nay."

*"Đó là bởi vì cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ đã an định."* Lâm Tịch giải thích cặn kẽ. *"Hải Uyên là cửa thoát của toàn bộ mạng lưới thủy mạch phương Nam. Khi miệng nứt bazan dưới đáy vực được bịt kín bằng Thuần Dương Cương Huyết và Trấn Thủy Đoản Đao, trục cân bằng âm dương của Thủy Môn Thập Nhị Tiêu đã được khôi phục quá nửa. Bảy cọc tiêu vùng sông ngòi và duyên hải giờ đây đã liên hoàn thành một thế trận phong tỏa vững chắc, bảo vệ hơn mười triệu sinh linh Sài Gòn khỏi đại họa ngập úng trọc khí."*

Tôi thở phào một hơi nhẹ nhõm. Nhìn về phía chân trời xa xăm trước mũi tàu, qua khỏi ngã ba sông Soài Rạp và mũi Đèn Đỏ thuộc huyện Nhà Bè, những vệt sáng rực rỡ của đô thị bắt đầu hiện rõ.

Đó là những giàn đèn pha cao áp công suất lớn rực sáng tại cảng container quốc tế SP-SSA và cảng Tân Thuận. Những chiếc cần cẩu giàn khổng lồ màu đỏ cam đang miệt mài bốc dỡ hàng hóa lên những con tàu viễn dương vạn tấn. Phía xa hơn nữa, vươn cao kiêu hãnh giữa nền trời đêm đen thẫm là ngọn tháp Landmark 81 rực rỡ muôn màu ánh sáng đèn LED và tháp Bitexco duyên dáng tựa búp sen.

Thành phố hoa lệ vẫn đang sống, đang thở và chuyển động không ngừng nghỉ.

Những người công nhân bốc xếp ca đêm, những bác tài xế xe tải đường dài, những gia đình đang say giấc nồng trong những căn chung cư cao tầng hay những xóm nhỏ ven kênh... họ không hề hay biết rằng chỉ vài giờ trước, cách nơi họ sống chưa đầy bảy mươi cây số ngoài khơi xa, một biến cố địa chất kinh thiên động địa đã được ngăn chặn ngay dưới đáy biển ngàn mét bởi những người lính biển kiên trung và một phàm nhân tu Thể Đạo.

Hạnh phúc và sự bình yên của trần thế đôi khi mỏng manh như sương khói, và nó cần những người sẵn sàng đứng trong bóng tối để che chở.'''

ACT2 = '''Bốn giờ ba mươi phút sáng ngày hai mươi tư tháng mười.

Tàu HQ-268 cập bến tại cầu cảng quân sự Vùng 2 Hải quân gần phà Cát Lái. Màn đêm thành phố bắt đầu chuyển dần sang màu lam xám báo hiệu một ngày mới chuẩn bị bắt đầu.

Trên cầu cảng bê-tông ướt đẫm hơi sương sớm, Thuyền trưởng Lê Đình Hùng bắt chặt tay tôi và Tuấn. Bàn tay người sĩ quan hải quân dày dặn sương gió, ấm áp và rắn rỏi.

"Cảm ơn hai đồng chí kỹ sư của Viện Địa tầng!" Thuyền trưởng Hùng mỉm cười thân tình, ánh mắt lộ rõ vẻ cảm phục. "Chuyến hải trình đêm nay là một trong những nhiệm vụ đặc biệt và ngoạn mục nhất trong hơn hai mươi năm cầm lái của tôi. Cửa biển Cần Giờ đã yên bình trở lại. Khi nào có dịp công tác dưới Lữ đoàn, anh em thủy thủ tàu HQ-268 luôn mở rộng cửa đón chào các bạn!"

"Cảm ơn Thuyền trưởng và anh em thủy thủ đoàn đã hết lòng hỗ trợ!" Tôi đáp lễ chân thành. "Chúc con tàu luôn vững vàng tay lái trên mọi hải trình bảo vệ chủ quyền biển đảo."

Tuấn ôm chặt chiếc ba lô chống sốc đựng cụm ổ cứng quang học bọc titan thu được từ cỗ tàu lặn Kình Uyên 01. Đôi mắt anh quầng thâm vì thức trắng đêm, nhưng nét mặt rạng rỡ sự phấn khích nghề nghiệp:

"Minh An, tôi phải đi xe chuyên dụng của Bộ Tư lệnh về thẳng phòng thí nghiệm giải mã an ninh của Viện Địa tầng trên đường Hoàng Hoa Thám ngay bây giờ. Lượng dữ liệu địa chấn, hải đồ tác chiến và nhật ký viễn thông của Tập đoàn Cửu Long Thiên Hải trong ổ cứng này cực kỳ đồ sộ. Tôi sẽ dùng cụm máy chủ lượng tử để bẻ khóa sạch sẽ các tầng mã hóa còn lại, trích xuất toàn bộ tọa độ và nhân sự của chi nhánh nội địa chúng tại Đồng Nai. Tầm trưa nay tôi sẽ gửi báo cáo hoàn chỉnh cho cậu qua kênh truyền vệ tinh mã hóa!"

"Được, cậu nhớ nghỉ ngơi dưỡng sức một chút, đừng ép bản thân quá mức." Tôi vỗ vai bạn dặn dò.

Chia tay Tuấn trên đường Nguyễn Thị Định, tôi đi bộ ra đầu đường đón một chiếc xe ôm sớm. Người tài xế là một bác trung niên trạc năm mươi tuổi, mặc chiếc áo gió sờn vai, nhìn thấy tôi mang ba lô dã chiến phong trần thì xởi lởi cười:

"Chú em đi công tác khảo sát công trình về sớm thế? Lên xe đi, giờ này đường Mai Chí Thọ thông thoáng lắm, vèo một cái là qua cầu Sài Gòn tới Bình Thạnh ngay!"

Chiếc xe máy nổ máy giòn giã, lướt đi trong làn gió sớm mát rượi. Xe băng qua hầm Thủ Thiêm, vượt qua những đại lộ thênh thang rợp bóng cây xanh của thành phố Thủ Đức, rồi qua cầu Sài Gòn tiến vào địa phận quận Bình Thạnh.

Năm giờ mười lăm phút sáng.

Thành phố Sài Gòn thức giấc bằng những thanh âm bình dị và thân thương nhất của đời sống thị thành.

Dưới ánh đèn đường vàng vọt còn chưa tắt, tiếng chổi tre quét đường sàn sạt của các cô công nhân vệ sinh môi trường vang lên nhịp nhàng trên vỉa hè đường Bạch Đằng. Nơi góc ngã tư Nơ Trang Long và Phan Đăng Lưu, mùi khói than củi thơm lừng tỏa ra từ những chiếc lò nướng sườn của quán cơm tấm bình dân. Tiếng dao thớt lách cách chặt thịt, tiếng mỡ hành xèo xèo trên vỉ sắt, và tiếng nước dùng phở bò sôi sùng sục từ một gánh hàng rong đầu hẻm hòa quyện thành một khúc ca sớm mai tràn đầy sức sống.

Trước cửa một con hẻm nhỏ, quán cà phê cóc của bà Tư đã sáng đèn. Chiếc ấm nhôm đun nước sôi reo ùng ục trên bếp than tổ ong, những chiếc phin cà phê bằng nhôm đang tí tách nhỏ từng giọt đen nhánh đặc quánh xuống đáy ly thủy tinh chứa sẵn lớp sữa đặc ngọt ngào. Mấy bác hưu trí mặc áo thun trắng, quần soóc ngồi trên những chiếc ghế nhựa thấp lè tè, vừa nhâm nhi ly cà phê vừa mở đài bán dẫn nghe bản tin thời sự buổi sáng.

Tôi xuống xe ở đầu hẻm, trả tiền cước rồi mỉm cười chào bác tài. Hít một hơi thật sâu mùi hương cà phê và cơm tấm quen thuộc, tôi cảm thấy từng tế bào trong cơ thể mình như được tưới mát bởi chính hơi thở nồng hậu của quê hương.

Tôi rảo bước về phía căn nhà trọ ba tầng nằm sâu trong con hẻm yên tĩnh trên đường Nơ Trang Long.

Tra chìa khóa mở cánh cổng sắt quen thuộc, tôi bước lên cầu thang gác hai, mở cửa căn phòng trọ nhỏ bé của mình.

Căn phòng rộng chừng hai mươi mét vuông vẫn y nguyên như lúc tôi rời đi ba ngày trước: chiếc giường sắt trải ga xám đơn sơ, chiếc bàn gỗ ép đặt chiếc máy tính xách tay cũ kỹ, giá sách chất đầy tài liệu trắc địa công trình và cuốn sổ tay ghi chép thực địa, cùng chiếc quạt cây đứng lặng lẽ bên góc tường.

Đây chính là chốn dung thân mộc mạc của tôi giữa lòng đại đô thị triệu dân. Không xa hoa, không tráng lệ, nhưng nó mang lại cho tôi cảm giác an toàn và tự do tuyệt đối.

Tôi đặt chiếc ba lô dã chiến nặng trịch xuống sàn gạch bông, cởi bỏ bộ quần áo sặc mùi muối biển rồi bước vào phòng tắm.

Mở vòi sen, làn nước máy mát rượi dội xối xả lên đầu, lên vai, cuốn trôi đi lớp muối biển khô cứng bám trên da thịt và xua tan những tàn dư của hàn sát vực sâu. Tôi đứng dưới làn nước, nhắm nghiền hai mắt, thả lỏng toàn bộ cơ bắp. Dưới lớp da rám nắng khỏe khoắn, các múi cơ thắt chặt tựa thép nguội, từng đường vân gân cốt ẩn hiện mạch lạc tựa rễ tùng cổ thụ. Những vết cào xước do mảnh vụn bazan dưới đáy biển tạo ra giờ đây đã hoàn toàn liền sẹo, để lại bề mặt da mịn màng, dẻo dai và săn chắc.

Tắm rửa sạch sẽ xong, tôi mặc vào chiếc quần đùi thun và áo ba lỗ trắng khô ráo. Tôi cúi xuống gầm giường, lấy ra chiếc bình thủy tinh ngâm rượu thuốc Đoán Cốt gia truyền. Rót ra một chén con thứ rượu màu hổ phách sóng sánh thơm nồng mùi thảo mộc quy kinh, tôi ngửa cổ uống cạn.

Một luồng nhiệt khí ấm áp lập tức bốc lên từ dạ dày, lan tỏa khắp ba mươi ba đốt sống lưng, sưởi ấm từng ngóc ngách tủy xương. Tôi dùng chút rượu thuốc còn lại xoa bóp đều lên hai bả vai và khớp gối, cảm nhận sự thư thái tột cùng len lỏi vào từng tế bào.

Sáu giờ mười lăm phút sáng.

Ánh nắng ban mai màu vàng cam rực rỡ xuyên qua khung cửa sổ kính mờ, rọi những vệt sáng ấm áp lên mặt bàn gỗ.

Chiếc điện thoại đặt trên bàn bỗng rung lên khe khẽ. Màn hình hiện lên tên người gọi: "Mẹ".

Trái tim tôi bỗng mềm lại. Tôi vội vàng cầm máy, gạt phím nghe:

"A-lô, con nghe đây mẹ ơi!"

*"An hả con?"* Tiếng mẹ vang lên từ đầu dây bên kia, mộc mạc, ấm áp và đong đầy tình thương yêu của người mẹ thôn quê. *"Mẹ vừa thức dậy đi chợ sớm, nhớ lời con nhắn đêm qua nên gọi xem con đã về tới phòng trọ ở Sài Gòn chưa?"*

"Dạ, con vừa về tới phòng trọ lúc nãy mẹ ạ." Tôi ngồi xuống mép giường, giọng nói tràn đầy sự ấm áp, ngoan ngoãn như đứa con nhỏ ngày nào. "Chuyến khảo sát thủy văn ở Cần Giờ của con xong xuôi tốt đẹp cả rồi. Con tắm rửa ăn sáng rồi, mẹ đừng lo."

*"Ừ, mẹ mừng cho con. Mấy hôm nay ở quê mưa gió thất thường, mẹ xem ti vi thấy ngoài biển động mạnh, trong lòng cứ bồn chồn không yên."* Tiếng mẹ cười hiền hậu, phía sau vẳng lại tiếng gà gáy râm ran nơi xóm quê thanh bình. *"Con làm việc với cơ quan nghiên cứu thì tốt, nhưng phải chú ý ăn uống tẩm bổ nghe con. Nhìn con dạo này gầy đi đấy. Khi nào rảnh rỗi cuối tuần thì bắt xe đò về quê với mẹ, mẹ hái rau tập tàng nấu canh cua đồng với kho nồi cá bống cát cho con ăn."*

"Dạ, con nhớ rồi mẹ." Nơi khóe mắt tôi chợt cay cay. Một cảm giác ấm áp vô ngần lan tỏa trong lồng ngực. "Cuối tuần sau xong đợt khảo sát trên mạn miền Đông này, con nhất định sẽ về quê ăn cơm mẹ nấu!"

*"Ừ, thôi con nghỉ ngơi cho lại sức đi, mẹ đi chợ đây."*

"Dạ, mẹ đi chợ cẩn thận nghe mẹ."

Cúp máy, tôi ngồi lặng yên bên mép giường, lắng nghe tiếng chuông điện thoại ngắt nhịp.

Cuộc gọi của mẹ tựa như một mỏ neo tâm thức vô giá. Giữa thế giới ngầm đầy rẫy hiểm nguy, nơi những mưu toan cổ xưa và những luồng năng lượng tà ác chực chờ nuốt chửng linh hồn con người, chính tình yêu thương bình dị của gia đình và hơi thở trần gian mộc mạc này đã giữ cho tâm tính tôi không bao giờ bị tha hóa, không bao giờ sa đà vào sự lạnh lùng vô cảm của những kẻ tự xưng là tiên nhân ngàn năm.'''

ACT3 = '''Tám giờ ba mươi phút sáng ngày hai mươi tư tháng mười.

Nắng sớm đã lên cao, nhuộm vàng những rặng cây me cổ thụ trên đường Nơ Trang Long. Tiếng còi xe máy, tiếng động cơ xe buýt rộn rã ngoài phố lớn vọng vào căn phòng trọ, tạo nên một bản hòa âm sôi động của một ngày làm việc mới.

Tôi ngồi ngay ngắn bên chiếc bàn gỗ nhỏ cạnh cửa sổ, cẩn thận rót nước sôi vào chiếc ấm gốm Bát Tràng, hãm một ấm trà xanh Thái Nguyên mộc mạc. Hương trà chát dịu, thơm ngát mùi cốm non lan tỏa trong không gian tĩnh lặng.

Trước mặt tôi, màn hình chiếc máy tính xách tay chuyên dụng vừa nhận được gói dữ liệu giải mã an ninh cấp độ cao nhất từ Tuấn gửi qua kênh truyền vệ tinh quân sự.

Tập hồ sơ trinh sát mang tiêu đề: *Chi Nhánh Nội Địa Cửu Long Thiên Hải & Mục Tiêu Núi Chứa Chan (Đồng Nai)*.

Tôi nhấp một ngụm trà nóng, chăm chú lướt qua từng trang tài liệu trắc địa, không ảnh vệ tinh và nhật ký điều phối nhân sự của kẻ địch.

Mọi manh mối đen tối dần dần lộ rõ dưới ánh sáng khoa học:

Để che giấu hoạt động phá hoại cọc tiêu thứ tám của Thủy Môn Thập Nhị Tiêu, Tập đoàn Cửu Long Thiên Hải đã lập ra một công ty bình phong mang tên *Công ty TNHH Khai Thác Khoáng Sản & Du Lịch Sinh Thái Thiên Hải Cương*. Từ ba tháng trước, công ty này đã xin cấp phép đầu tư một dự án mở rộng khu du lịch sinh thái kết hợp tuyến cáp treo số hai trên sườn đông bắc Núi Chứa Chan thuộc huyện Xuân Lộc, tỉnh Đồng Nai.

Núi Chứa Chan — còn gọi là núi Gia Lào hay Gia Ray — là ngọn núi sót kỳ vĩ cao tám trăm ba mươi bảy mét so với mực nước biển, ngọn núi cao thứ hai ở toàn bộ vùng đất Nam Bộ, chỉ đứng sau đỉnh Núi Bà Đen ở Tây Ninh. Khác với vùng đồng bằng châu thổ phù sa mềm yếu của hạ lưu sông Sài Gòn, Núi Chứa Chan là một khối đá magma xâm nhập cổ xưa hình thành từ kỷ đệ tứ, cấu tạo chủ yếu bởi đá granite hoa cương và rhyolite có độ cứng đạt cấp tám theo thang Mohs.

Theo hồ sơ trắc địa của Tuấn, tâm điểm dự án của công ty Thiên Hải Cương không hề nằm ở các khu vực chùa chiền hay thắng cảnh du lịch thông thường, mà bị khoanh vùng nghiêm ngặt tại một khu vực hoang vu hiểm trở ở độ cao sáu trăm mét: *Thềm Đá Cổ Thần Quy*!

Đó là một thềm đá granite nguyên khối khổng lồ nhô ra giữa sườn vực sâu, có hình dáng tựa một con rùa thần khổng lồ đang phục quỳ hướng về phía đại dương phương Nam.

Dưới vỏ bọc xây dựng mố trụ cáp treo và hầm kỹ thuật, bọn chúng đã bí mật đưa lên núi bốn cỗ máy khoan hầm khí nén bánh xích hạng nặng cùng dàn thiết bị phát sóng xung kích tần số cực thấp. Đáng sợ hơn, trong hai tuần qua, các trạm quan trắc vi địa chấn của tỉnh Đồng Nai liên tục ghi nhận những đợt rung chấn nhân tạo cục bộ sâu trong lòng núi.

Chúng đang dùng xung kích cơ giới để cố tình kích hoạt các vết nứt địa tầng, mưu toan đập vỡ khối đá Thần Quy để giải phóng luồng tà khí cổ xưa bị giam cầm bên dưới!

Chỉ huy trực tiếp tại công trường Núi Chứa Chan là một nhân vật cộm cán trong giới tà đạo: *Tạ Lôi*, biệt danh *Lôi Báo*. Hắn là một kẻ tu luyện Thể Đạo biến dị theo nhánh Thiết Cốt tà môn, kết hợp với các loại vũ khí quân dụng và chất nổ công nghiệp. Tạ Lôi từng là thủ lĩnh lính đánh thuê khét tiếng hoạt động tại khu vực Tam Giác Vàng, tính tình hung bạo, thủ đoạn tàn độc và sở hữu sức mạnh cận chiến kinh hoàng.

Đang lúc tôi trầm ngâm suy tính, làn khói trà xanh bốc lên từ chiếc chén gốm bỗng khẽ xoay tròn.

Một luồng linh quang màu bạch ngọc thanh khiết ngưng tụ giữa không trung, hóa thành bóng hình thanh thoát, mờ ảo của Lâm Tịch. Nàng khoác trên mình bộ váy trắng cổ phong phiêu dật, mái tóc đen nhánh buông rủ ngang lưng, gương mặt thanh tú mang theo vẻ trang nghiêm tĩnh lặng.

*"Minh An, khối đá Thần Quy trên đỉnh Chứa Chan không phải là một cọc tiêu thủy mạch thông thường."* Giọng nói của Lâm Tịch vang lên, êm đềm nhưng ẩn chứa sức nặng của lịch sử ngàn năm.

"Ý nàng là sao?" Tôi đặt chén trà xuống bàn, chăm chú lắng nghe.

*"Bảy cọc tiêu trước đây ngươi từng vượt qua — từ cọc ngầm Lò Gốm, bến Phú Định cho đến đáy vực Hải Uyên — đều thuận theo tính chất của Nước. Nước thì mềm mại, uyển chuyển nhưng hiểm sâu khôn lường, đòi hỏi Thể Đạo của ngươi phải lấy sức nặng và sự dẻo dai của Cương Huyết để chế ngự."* Lâm Tịch khẽ đưa ngón tay ngọc chỉ vào hình ảnh vách đá granite trên màn hình máy tính. *"Nhưng cọc tiêu thứ tám Thần Quy Thạch lại là tính chất của Đá và Kiếm."*

Nàng khẽ thở dài, trong ánh mắt dường như phản chiếu lại những hình bóng từ ngàn năm xa xưa:

*"Vào thời kỳ thượng cổ, khi đại địa Nam Bộ còn chìm trong hồng hoang, một con nghiệt long mang bản tính thạch sát từ phương bắc tràn xuống, muốn dùng độc khí nghiền nát sinh linh phương Nam. Một vị kiếm tu Thể Kiếm Song Tu của tiền nhân — người được tôn xưng là Bạch Viên Kiếm Tôn — đã dùng một thanh cổ kiếm bằng thiên thạch chém đứt đầu ác long, ép thân xác nó hóa thành khối đá hoa cương sừng sững giữa bình nguyên, chính là ngọn núi Chứa Chan ngày nay."*

*"Sau trận chiến ấy, vị tiền nhân đó đã lưu lại một đạo Kiếm Ngân trấn áp trên lưng Thần Quy Thạch. Đạo kiếm ngân ấy trải qua hàng ngàn năm phong hóa vẫn bất diệt, phong tỏa tuyệt đối mạch ác long bên dưới. Cọc tiêu thứ tám chính là đạo Kiếm Ngân Thần Quy ấy!"*

Tôi lắng nghe từng lời của Lâm Tịch, trong lòng dâng lên sự kinh ngạc khôn xiết:

"Nói như vậy, cọc tiêu thứ tám không thể dùng bạo lực cơ bắp hay sức mạnh va đập để phong tỏa?"

*"Chính xác!"* Lâm Tịch gật đầu khẳng định. *"Kiếm ý viễn cổ lưu lại trên đá sắc bén vô cùng, mang bản tính Vô Ngân Kiếm Khí. Nếu ngươi dùng kình lực thô bạo xông vào, kiếm khí cổ xưa sẽ tự động phát kích, xé nát gân cốt của bất kỳ kẻ nào xâm phạm. Ngay cả lũ tà đạo Cửu Long Thiên Hải cũng không dám trực tiếp chạm vào kiếm ngân, mà chỉ dám dùng máy khoan rung chấn từ xa để làm nứt vỡ chân móng."*

*"Muốn cứu vãn cọc tiêu Thần Quy, ngươi phải dùng bản tâm thuần phác của Thể Đạo để lĩnh ngộ kiếm ý, đạt tới cảnh giới 'Dĩ Thể Vi Kiếm, Khí Quán Cửu Tiêu' — lấy chính thân thể tôi luyện bằng Cương Huyết làm vỏ kiếm, dung hòa và dẫn dắt kiếm ý cổ xưa trở lại trạng thái phong tỏa hoàn hảo!"*

"Lấy thân làm kiếm..." Tôi lẩm bẩm bốn chữ ấy, cảm nhận một chân trời võ đạo hoàn toàn mới mẻ đang mở ra trước mắt.

Thể Đạo không chỉ là nắm đấm và sức nặng cơ bắp. Khi ba mươi ba đốt sống lưng đã hóa thành ngọc thạch, khi Thuần Dương Cương Huyết đã lưu chuyển như sông dài, thì thân thể phàm nhân này hoàn toàn có thể trở thành một cỗ khí cụ sắc bén nhất giữa trời đất!

Tôi đứng dậy, bước ra góc phòng, bắt đầu chuẩn bị hành trang tác chiến cho chuyến hành trình mới.

Tôi lấy thanh Hắc Thiết Đoản Côn ra khỏi bao da. Dùng khăn mềm thấm dầu máy bảo dưỡng lau chùi cẩn thận từng tấc kim loại đen nhánh ánh chu sa đỏ sẫm, rồi quấn lại lớp da bò bọc ngoài chuôi côn cho thật êm và bám tay. Thanh đoản côn nặng ba ký hai này đã cùng tôi vào sinh ra tử, là người bạn đồng hành tin cậy nhất.

Tiếp đó, tôi kiểm tra lại chiếc ba lô dã chiến chuyên dụng. Thanh Trấn Thủy Đoản Đao, viên Hắc Thủy Huyền Thạch, Định Hải Huyền Châu và khối Tỏa Long Huyền Tỷ mới thu được đều được tôi bọc ba lớp vải nhung cách chấn, xếp ngay ngắn dưới đáy ba lô.

Tôi chuẩn bị thêm một bộ quần áo rằn ri dã chiến leo núi chống gai cào, đôi giày lính cổ cao có đế cao su bám đá granite, chiếc đèn pin quân sự chống nước, bình bi-đông inox chứa nước lọc, la bàn địa chất chuyên dụng và tấm bản đồ địa hình khu vực huyện Xuân Lộc tỷ lệ một trên hai mươi lăm ngàn.

Cuối cùng, tôi thay chiếc áo khoác gió sẫm màu, khoác ba lô lên vai.

Bước ra ban công căn phòng trọ, tôi đứng ngắm nhìn thành phố Sài Gòn rực rỡ dưới ánh nắng ban mai. Dòng người và xe cộ trên đường Phan Đăng Lưu và Nơ Trang Long đang hối hả xuôi ngược, bắt đầu một ngày mới đầy ắp những ước mơ và hy vọng.

Tôi mỉm cười nhẹ nhõm. Nơi khóe mắt ánh lên ngọn lửa kiên định và quả cảm.

Dưới tầng hầm nhà trọ, chiếc xe máy Wave Alpha màu đỏ thẫm quen thuộc đã được đổ đầy bình xăng. Chín mươi cây số theo Quốc lộ 1A ngược về hướng đông bắc đang chờ đợi bánh xe tôi lăn tới.

Một hành trình mới đã chính thức bắt đầu — rời xa sông nước biển sâu, bước vào đại ngàn non cao, nơi Thể Đạo phàm nhân sẽ đối đầu với đá cứng và kiếm ý viễn cổ trên đỉnh ngọn núi Chứa Chan hùng vĩ!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/5] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3000 or word_count > 5000:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,000 - 4,800 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words)
    print(f"[*] [2/5] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường)...")
    meta_patterns = [
        r"\bchương\s+\d+\b",
        r"\bhồi\s+\d+\b",
        r"\bquyển\s+\d+\b",
        r"\btác giả\b",
        r"\bhệ thống\b",
        r"\bbản thảo\b",
        r"\bcanon\b",
        r"\bdatabase\b",
        r"\bplot\b",
        r"\bforeshadowing\b"
    ]
    for pat in meta_patterns:
        matches = re.findall(pat, raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ ngữ meta '{matches}' trong văn bản bản thảo!")
            return False
    print(f"[+] Không phát hiện từ ngữ meta nào. Đạt chuẩn RULE-07 100%.")

    # 3. Đăng ký thực thể mới vào novel_os.db
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'artifact_toa_long_huyen_ty',
        'Tỏa Long Huyền Tỷ',
        'item',
        json.dumps(['Trận Nhãn thứ bảy', 'Hải Uyên Long Tỉ', 'Ngọc Tỷ Chín Rồng'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'material': 'Deep sea jade & archaic gold dragons', 'function': 'Trận nhãn cốt lõi của Hải Uyên Tỏa Long Trụ, trấn áp âm trọc Cực Tù'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'loc_nui_chua_chan',
        'Đỉnh Núi Chứa Chan (Đồng Nai)',
        'location',
        json.dumps(['Núi Chứa Chan', 'Gia Lào', 'Thềm Đá Cổ Thần Quy'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'elevation': '837m', 'terrain': 'Khối đá granite cổ kỷ đệ tứ', 'significance': 'Vị trí cọc tiêu thứ tám Thủy Môn Thập Nhị Tiêu'}, ensure_ascii=False)
    ))
    conn.commit()
    conn.close()

    # 4. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_tuan", "char_lam_tich", "char_le_dinh_hung"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [3/5] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 5. Xuất bản Markdown với YAML Frontmatter và Heading H1
    frontmatter = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {word_count}
date: "{DATE}"
location: "{LOCATION}"
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

"""
    full_markdown = frontmatter + raw_content
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
    print(f"[+] [4/5] Đã xuất tệp Markdown chuẩn Frontmatter + H1: {md_file_path}")

    # 6. Xuất bản Word (.docx)
    docx_pipe = DocxPipeline()
    docx_file_name = f"ch_{CHAPTER_NUM:03d}.docx"
    docx_file_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02", docx_file_name)
    os.makedirs(os.path.dirname(docx_file_path), exist_ok=True)
    docx_pipe.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=full_markdown,
        output_docx_path=docx_file_path
    )
    print(f"[+] [5/5] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 7. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 7.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Dạ Hành Quy Đô, Hơi Thở Bình Dị Nơ Trang Long & Khởi Động Chiến Dịch Núi Chứa Chan",
        CHAPTER_NUM,
        1,
        f"{DATE}T08:30:00+07:00",
        CHAPTER_NUM,
        "loc_phong_tro_no_trang_long",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_le_dinh_hung", "char_me_minh_an"]),
        "Minh An ngược dòng sông Lòng Tàu trong đêm sương lạnh trên tàu HQ-268, cảm nhận sự an định của thủy mạch và sự chuyển hóa kỳ diệu của 33 đốt sống lưng cùng Thuần Dương Cương Huyết sau khi thu đắc Tỏa Long Huyền Tỷ. Trở về căn phòng trọ Nơ Trang Long rạng sáng, đón nhận hơi thở đời thường Sài Gòn (cơm tấm, cà phê sữa, quét rác) và cuộc gọi yêu thương từ mẹ. Nhận gói giải mã dữ liệu tình báo từ Tuấn, vạch trần âm mưu của công ty vỏ bọc Thiên Hải Cương do tà tu Tạ Lôi cầm đầu đang nã xung kích vào Thềm Đá Cổ Thần Quy trên đỉnh Núi Chứa Chan. Lâm Tịch truyền thụ bí mật về Vô Ngân Kiếm Khí của Bạch Viên Kiếm Tôn, định hướng cảnh giới Dĩ Thể Vi Kiếm. Minh An chuẩn bị vũ khí và xe máy bắt đầu hành trình độc hành 90km tiến vào Đồng Nai.",
        "An định toàn diện sau chiến dịch Hải Uyên; neo giữ vững chắc bản tâm phàm nhân; giải mã toàn bộ mục tiêu thềm đá Núi Chứa Chan; chuẩn bị xuất phát hành trình mới."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An an định sau chiến dịch Hải Uyên, giải mã âm mưu cọc tiêu thứ tám Thần Quy Thạch tại Núi Chứa Chan (Đồng Nai) và chuẩn bị xuất phát."
    ))

    # 7.3 Cập nhật story thread TH-CHR-001 (Trách Nhiệm Đời Thường & Gia Đình)
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An trở về phòng trọ Nơ Trang Long, nhận cuộc gọi yêu thương của mẹ và hòa mình vào hơi thở bình dị của Sài Gòn sáng sớm."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T08:30:00+07:00"
        inv_data["current_location"] = "Phòng trọ Nơ Trang Long, Quận Bình Thạnh, TP.HCM"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ (33 Đốt Sống Ngọc Thạch / Thuần Dương Cương Huyết)"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json.")

    # 9. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> HOÀN TẤT TOÀN BỘ PIPELINE CHƯƠNG {CHAPTER_NUM} THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

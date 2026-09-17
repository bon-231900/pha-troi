# -*- coding: utf-8 -*-
"""Draft Chapter 69 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 69
CHAPTER_TITLE = "Ba Son Cổ Trận"
LOCATION = "Phòng trọ Nơ Trang Long, Viện Địa tầng Đô thị & Ụ tàu cổ Ba Son (TP.HCM)"
DATE = "2026-10-22"

ACT1 = '''Sáu giờ ba mươi phút sáng ngày hai mươi hai tháng Mười.

Những tia nắng ban mai xuyên qua tán lá bàng trước hiên, rọi từng vệt sáng màu mật ong lên sàn gạch hoa căn phòng trọ nhỏ trên đường Nơ Trang Long. Tiếng còi xe hối hả từ ngã tư Bình Hòa vọng lại, báo hiệu một ngày mới bắt đầu giữa nhịp sống tất bật của thành phố. Sau một đêm lặn ngụp dưới đáy rạch Bến Nghé lạnh buốt, cơ thể tôi không hề mỏi mệt mà tràn đầy sinh lực.

Tôi ngồi xếp bằng trên tấm phản gỗ, hai mắt khép hờ, toàn bộ tâm thức tập trung vào việc vận chuyển Thức thứ bảy *Ngọc Tủy Quy Nhất*.

Dọc ba mươi ba đốt xương sống, dòng tủy ngọc trong suốt lấp lánh lưu chuyển. Cạnh cột sống, Thanh Long Lân Kiếm thu nhỏ tựa dải thanh quang phỉ thúy lẳng lặng an tọa, tỏa kiếm khí hàn băng thanh lãnh gột rửa từng phiến xương, tôi luyện chất tủy cô đọng phi thường.

"Rắc! Rắc!"

Những âm thanh giòn giã khẽ vang lên từ các khớp xương. Luồng kình lực Thể Đạo lan tỏa khắp các đầu ngón tay ngón chân, tạo nên cảm giác vững chãi tựa bàn thạch. Cảnh giới Luyện Cốt trung kỳ của tôi sau khi dung nạp cọc tiêu số năm đã triệt để củng cố, đạt đến độ viên mãn ổn định.

Tôi từ từ thở ra một ngụm trọc khí màu trắng đục, rồi mở mắt ra.

Trên chiếc bàn gỗ nhỏ đầu giường, chiếc hộp đồng thau cổ vừa thu được từ đáy đàn tế Cầu Mống đang lẳng lặng nằm đó. Lớp gỉ đồng màu xanh lam bám chặt trên bề mặt, để lộ những đường gân chạm khắc tinh vi mô phỏng mai rùa thần. 

Tôi vươn tay mở nắp hộp.

Bên trong là một tấm da rùa cổ màu vàng sậm, kích thước chỉ bằng hai bàn tay ghép lại, dẻo dai và bóng mịn lạ lùng. Mặt trên tấm da rùa vẽ một bức họa đồ thủy đạo cổ xưa với những nét mực son đỏ thắm chưa hề phai mờ sau hàng ngàn năm chìm trong bùn lầy. Ở trung tâm, chín nhánh sông ngầm uốn lượn tựa chín con rồng vươn ra biển. Nổi bật nhất là đồ hình mai rùa cõng trụ đồng khổng lồ, đánh dấu mực son rực rỡ tại khúc uốn sông Sài Gòn đối diện bán đảo Thủ Thiêm.

Phía dưới hình vẽ khắc bốn chữ triện cổ sắc sảo: **Thủy Môn Chấn Tiêu**.

Trong thức hải, hoa sen ngọc bích khẽ rung rinh. Hình bóng thanh thoát của Lâm Tịch hiện ra, đôi mắt phượng trong veo dõi nhìn bức họa đồ qua thần thức của tôi. Nàng khẽ cất tiếng, thanh âm êm dịu như tiếng suối reo giữa rừng trúc:

*"Minh An, cọc tiêu số sáu này mang ý nghĩa vô cùng đặc biệt. Trong mười hai cọc tiêu của Thủy Môn Thập Nhị Tiêu, nếu năm cọc tiêu đầu tiên đóng vai trò nanh vuốt để phân nhánh, xua tan thủy sát tại các ngã ba kênh rạch, thì **Thủy Môn Chấn Tiêu** chính là chiếc cọc trung tâm điều phối dòng chảy của toàn bộ khúc quanh bán đảo Thủ Thiêm."*

Tôi chăm chú nhìn vào đồ hình mai rùa cõng trụ đồng: "Trụ đồng này có uy lực gì đặc biệt vậy nàng?"

Lâm Tịch khẽ gật đầu, giọng nói mang vẻ trang trọng:

*"Đó là khối trụ đồng cổ đúc từ thuở viễn cổ nặng hơn sáu vạn cân, cắm sâu xuyên thủng tầng đá gốc hơn bốn mươi mét. Thân trụ khắc vạn phù văn Trấn Ba, có khả năng định hải an bang, hấp thu long khí thượng nguồn sông Đồng Nai và sông Sài Gòn trước khi chia nhánh ra biển Cần Giờ."*

"Vị trí cọc tiêu số sáu này nằm ở đâu trên bản đồ hiện đại?" Tôi hỏi.

*"Chính là khu vực Xưởng đóng tàu Ba Son xưa kia,"* Lâm Tịch đáp. *"Nơi người phàm xây dựng ụ tàu khô số một từ hơn một trăm năm trước. Vùng đất ấy là nơi nanh rồng uốn lượn, tụ khí sinh tài. Ngươi cần nhanh chóng đến đó khảo sát trước khi kẻ thù kịp giở thủ đoạn mới."*

Tôi gật đầu, cẩn thận gấp tấm da rùa đặt lại vào hộp đồng, rồi cất sâu vào balo dã chiến cùng với thanh Trấn Thủy Đoản Đao và thanh Hắc Thiết Đoản Côn.'''

ACT2 = '''Tám giờ ba mươi phút sáng.

Tôi lái chiếc xe Wave cũ đến trụ sở Viện Địa tầng Đô thị trên đường Lý Tự Trọng. Nắng sớm rực rỡ xuyên qua những tán me cổ thụ, rải bóng mát rượi xuống khoảng sân gạch rêu phong. Khi tôi bước lên tầng hai, không khí trong phòng làm việc của Viện trưởng Trịnh Hoài Nam đã rộn ràng tiếng trao đổi kỹ thuật.

Kỹ sư Tuấn đang ngồi trước dàn máy tính phân tích dữ liệu, trên tay cầm cốc cà phê đen bốc khói nghi ngút. Nhìn thấy tôi, mắt anh sáng bừng lên, vội vã vẫy tay:

"Minh An, em đến rồi à! Tin mừng lớn đây! Tám giờ sáng nay, Sở Giao thông Vận tải và Ban Quản lý Dự án đã hoàn tất việc cho đoàn xe tải nặng sáu mươi tấn lăn bánh thử tải trọng trên Cầu Mống. Toàn bộ bốn cụm cảm biến gia tốc ba trục của Viện đặt dưới mố cầu đều ghi nhận biên độ rung chấn nằm trong giới hạn an toàn tuyệt đối! Không hề có hiện tượng trồi bùn hay nứt vỡ chân đá móng như đêm trước!"

Tôi mỉm cười ngồi xuống: "Thế thì tốt quá rồi anh Tuấn. Công sức đêm qua không uổng phí."

Cửa phòng mở ra, Viện trưởng Trịnh Hoài Nam bước ra, trên tay ôm xấp tài liệu kỹ thuật bìa da sờn cũ ố vàng theo năm tháng, nét mặt rạng rỡ phấn chấn.

"Hai cậu vào đây cả đi," Viện trưởng Nam vẫy tay gọi chúng tôi. "Sáng nay sau khi nhận báo cáo thử tải thành công của Cầu Mống, tôi đã vào kho lưu trữ tài liệu mật của Viện tìm kiếm lại toàn bộ hồ sơ địa chất các công trình ngầm ven sông Sài Gòn. Và tôi phát hiện một tài liệu vô cùng chấn động."

Tôi và Tuấn lập tức đứng dậy bước vào phòng làm việc của Viện trưởng. 

Trên bàn hội nghị, Viện trưởng Nam trải rộng bản vẽ kỹ thuật vẽ tay bằng mực nho trên giấy can cổ — bản thiết kế mặt cắt địa tầng Xưởng đóng tàu Ba Son do kỹ sư hàng hải Pháp lập năm 1863 khi xây dựng ụ tàu khô số một bằng đá hoa cương.

"Các cậu nhìn vào lát cắt địa chất sâu bốn mươi mét dưới đáy ụ tàu số một xem," Viện trưởng Nam trỏ ngón tay có vết đồi mồi vào một biểu tượng hình trụ màu đen kỳ lạ nằm sâu dưới tầng đá bazan. "Năm 1863, khi đào đất móng đá để xây ụ tàu, các kỹ sư Pháp đã dùng máy khoan hơi nước hiện đại nhất thời bấy giờ để cắm cọc tiêu sâu. Nhưng khi mũi khoan xuống đến độ sâu bốn mươi hai mét, nó bất ngờ đâm phải một vật thể kim loại ngầm cứng rắn đến mức làm gãy vụn liên tiếp ba mũi khoan hợp kim vonfram!"

Kỹ sư Tuấn trố mắt ngạc nhiên: "Một khối kim loại nằm sâu bốn mươi hai mét dưới lòng đất từ thế kỷ mười chín sao bác? Chẳng lẽ là quặng kim loại tự nhiên?"

"Không phải quặng tự nhiên," Viện trưởng Nam lắc đầu quả quyết, giọng ông trầm xuống đầy vẻ bí ẩn. "Trong nhật ký thi công bằng tiếng Pháp, kỹ sư trưởng Jean-Baptiste ghi rõ: đó là khối trụ tròn bằng đồng nguyên khối đường kính hơn hai mét, khắc ký hiệu hình học kỳ bí. Người Pháp không thể phá vỡ hay di dời, đành đổ khối bê tông bọc thép dày ba mét bọc kín xung quanh làm bệ đỡ chịu lực cho ụ tàu và tháp thủy đài!"

Nghe những lời kể của Viện trưởng Nam, tim tôi khẽ nảy lên một nhịp. Khối trụ đồng ngàn năm mà người Pháp chạm phải vào năm 1863 chính là **Thủy Môn Chấn Tiêu** mà tấm da rùa cổ đã chỉ dẫn!

Viện trưởng Nam lật tiếp một trang tài liệu chép bằng chữ Nôm cổ trên giấy bản:

"Không chỉ có người Pháp ghi chép. Tài liệu lưu trữ về Thủy trại Chu Sư thời chúa Nguyễn cuối thế kỷ mười tám cũng từng nhắc đến vùng đất Ba Son này. Tương truyền khi lập xưởng đóng thuyền, quan Tiền quân Nguyễn Văn Thành từng cho thợ lặn yểm trụ đồng trấn thủy sát bảo vệ chiến thuyền. Nhưng niên đại thực tế của khối trụ này có từ thời tiền sử hàng ngàn năm trước!"

Tôi gật đầu, đưa mắt nhìn Tuấn: "Anh Tuấn, hiện nay khu vực ụ tàu cổ số một và tháp thủy đài Ba Son thuộc quyền quản lý của đơn vị nào?"

"Hiện nay toàn bộ khu vực Ba Son đã được quy hoạch thành quần thể đô thị hiện đại ven sông," Tuấn nhanh nhảu đáp. "Tuy nhiên, ụ tàu khô số một và tháp thủy đài cổ bằng gạch đỏ xây từ thế kỷ mười chín được xếp hạng di tích lịch sử văn hóa cấp quốc gia, thuộc diện bảo tồn nghiêm ngặt. Sáng nay bên Ban Quản lý Di tích vừa gửi công văn đề nghị Viện chúng ta cử cán bộ đến khảo sát định kỳ độ lún nền móng của tháp thủy đài. Em có muốn đi cùng anh chiều nay không?"

"Chắc chắn rồi anh Tuấn," tôi đáp ngay không một giây do dự.'''

ACT3 = '''Một giờ ba mươi phút chiều.

Cái nắng phương Nam gay gắt rọi thẳng xuống những tòa tháp chọc trời bằng kính và thép dọc trục đường Tôn Đức Thắng. Tôi và kỹ sư Tuấn đi trên chiếc xe bán tải của Viện Địa tầng, tiến vào cổng bảo vệ của khu phức hợp Ba Son. 

Băng qua những con đường nội khu rợp bóng cây xanh, xe dừng lại trước khuôn viên di tích ụ tàu cổ số một và tháp thủy đài lịch sử.

Tháp thủy đài cổ sừng sững vươn cao hơn hai mươi mét giữa trời xanh. Thân tháp xây bằng gạch nung đỏ sẫm từ thời Pháp phủ rêu phong trầm mặc. Cách đó chừng ba mươi mét là lòng ụ tàu khô số một dài hơn trăm mét với vách đá hoa cương ghép mộng vuông vức sâu hun hút, nơi từng sửa chữa những chiến hạm viễn dương lớn nhất Đông Dương.

Tôi bước xuống xe, hai chân vừa chạm mặt đất bê tông, tủy ngọc trong cột sống tôi bỗng nhiên rung động nhẹ nhàng!

"Uông... uông..."

Thanh Long Lân Kiếm dọc sống lưng khẽ rung lên những xung dao động trầm đục, tỏa kiếm khí mát lạnh lan tỏa khắp các khớp xương tựa tri kỷ ngàn năm hội ngộ. 

Tôi khép hờ mắt, kích hoạt trực giác Thể Đạo. Dưới độ sâu bốn mươi hai mét của lòng đất, xuyên qua các tầng sét nén và khối bê tông bọc thép dày đặc, một luồng từ trường màu hoàng kim đồng thau đồ sộ tựa như một ngọn núi ngầm đang tỏa ra uy áp trầm hùng. Tần số dao động của nó chậm rãi, trầm mặc, đúng không phẩy mười hai Hertz, đồng điệu tuyệt đối với nhịp đập của quả tim và mạch đất mẹ mà tôi từng cảm nhận ở Cầu Mống.

"Kỳ lạ thật," Tuấn xách chiếc vali chứa máy quét địa vi sai và cảm biến siêu âm bước lại gần tôi, trỏ ngón tay vào màn hình cảm ứng. "Minh An nhìn này, máy đo từ trường vừa đi qua cổng đã nhảy vọt lên mức ba ngàn nano-Tesla. Cường độ từ trường dưới lòng đất ở đây cao gấp năm lần mức trung bình của toàn thành phố!"

"Dưới chân tháp thủy đài này có một đường hầm kỹ thuật ngầm đúng không anh Tuấn?" Tôi nhìn vào cánh cửa sắt dày đóng chặt dưới chân tháp.

"Đúng vậy," Tuấn mở tập hồ sơ giấy phép ra. "Tầng hầm này sâu mười hai mét, trước đây người Pháp dùng làm bể chứa nước áp lực cao và trạm bơm xả nước cho ụ tàu khô. Ban Quản lý vừa cấp chìa khóa điện tử cho chúng ta để xuống đo đạc độ võng của móng tháp."

Hai chúng tôi đang chuẩn bị bước tới cánh cửa sắt thì một luồng khí tức lạnh lẽo bất ngờ lướt qua gáy tôi.

Trực giác Thể Đạo của tôi lập tức cảnh báo!

Tôi vờ như đang cúi người buộc lại dây giày thể thao, ánh mắt liếc nhanh qua bờ công viên ven sông Sài Gòn cách đó chừng năm mươi mét. Dưới bóng râm của hàng cây bàng vuông, một chiếc xe bán tải màu xám tro không biển số đang đậu lẳng lặng. Kính xe dán phim cách nhiệt đen tuyền, nhưng bằng thị lực tinh tường của người đạt cảnh giới Luyện Cốt trung kỳ, tôi nhìn xuyên qua lớp kính tối, thấy rõ một gã đàn ông ngồi ở ghế lái.

Gã mặc áo khoác đen, cổ lộ hình xăm chim ưng xanh ngọc quắp đầu rồng — ấn ký của toán sát thủ Hắc Giao Đường Ma Cao mà tôi vừa chạm trán đêm qua!

Gã đang cầm một ống nhòm quân sự tầm nhiệt theo dõi nhất cử nhất động của tôi và Tuấn.

"Đám tàn dư Cửu Long Thiên Hải bám theo nhanh thật," tôi thầm nhủ trong lòng. Rõ ràng sau thất bại cay đắng ở Cầu Mống, tổ chức ngầm này đã đoán ra mục tiêu tiếp theo của tôi chính là cọc tiêu số sáu tại Ba Son. Bọn chúng đã bố trí tai mắt bao vây khu vực này từ trước.

"Minh An, xong chưa em? Mình mở cửa xuống hầm thôi!" Tiếng Tuấn gọi tôi.

"Em tới ngay đây anh Tuấn," tôi đứng thẳng dậy, vờ như không phát hiện ra kẻ theo dõi, bình thản bước theo Tuấn tiến vào cánh cửa sắt dưới chân tháp thủy đài.'''

ACT4 = '''Cánh cửa sắt nặng nề kêu lên tiếng ken két chói tai khi Tuấn quét thẻ từ mở chốt khóa điện tử.

Hai chúng tôi bước vào bên trong, Tuấn tiện tay gạt cầu dao điện. Ánh sáng vàng vọt từ những bóng đèn sợi đốt chống ẩm gắn dọc trần hầm bật sáng, soi rọi lối cầu thang xoắn ốc bằng gang đúc dẫn sâu xuống lòng đất tối tăm. Không khí dưới hầm ẩm ướt và lạnh ngắt, thoang thoảng mùi rêu mốc và hơi nước ngưng đọng lâu ngày.

Đi hết ba mươi sáu bậc cầu thang gang, chúng tôi đặt chân xuống sàn hầm kỹ thuật ở độ sâu mười hai mét.

Căn hầm tròn rộng chừng hai trăm mét vuông, tường gạch vồ dày hơn mét gia cố bằng dầm thép. Ở trung tâm là miệng giếng kỹ thuật đường kính ba mét, đậy kín bằng nắp thép tròn siết chặt mười hai bu-lông lớn dẫn xuống đáy địa tầng bốn mươi mét.

"Đây rồi," Tuấn đặt vali thiết bị xuống sàn gạch, lấy ra các đầu dò sóng âm và máy đo biến dạng quang học. "Anh sẽ gắn cảm biến quanh mười hai góc chịu lực của sàn hầm để đo độ võng kết cấu. Em cầm đầu dò vi chấn đặt sát mép nắp thép kia giúp anh nhé."

"Để em làm cho," tôi đáp.

Tôi bước lại gần nắp thép tròn khổng lồ ở tâm căn hầm. Khi khoảng cách thu hẹp lại chỉ còn ba bước chân, dòng tủy ngọc trong người tôi bỗng cuộn trào mạnh mẽ. Thanh Thanh Long Lân Kiếm bên cạnh cột sống phát ra tiếng ngân vang khe khẽ nhưng dồn dập. Cùng lúc đó, trong chiếc túi nhung đen dưới đáy balo dã chiến sau lưng tôi, viên Định Hải Huyền Châu và Trấn Giang Huyền Tỷ cũng đồng loạt tỏa ra luồng nhiệt ấm áp tương liên!

Tôi ngồi xổm xuống, áp lòng bàn tay phải lên mặt nắp thép lạnh toát.

"Ong..."

Kình lực Thể Đạo từ tủy ngọc truyền thẳng qua khối kim loại, xuyên sâu xuống lòng đất.

Trong khoảnh khắc ấy, thị giác tâm linh của tôi mở rộng tột độ. Xuyên qua ba mươi mét đất đá bazan và lớp bê tông bảo hộ dày đặc, hình ảnh chân thực của cọc tiêu số sáu hiện lên tráng lệ và uy nghiêm trước mắt tôi!

Đó là khối trụ đồng cổ màu xanh thau sẫm đường kính hơn hai mét, sừng sững tựa cột chống trời dưới lòng đất, khắc nổi hàng vạn minh văn mặt trời, chim lạc và sóng thần. Nhưng quanh thân trụ lúc này bị quấn chặt bởi những sợi xích hợp kim đen ngòm dày đặc.

Từ những sợi xích hợp kim ấy, từng luồng hắc khí tà đạo u tối đang liên tục thẩm thấu vào các thớ đồng cổ, tạo nên một kết giới phong tỏa nhân tạo nhằm cô lập sự liên kết giữa cọc tiêu và mạch đất sông Sài Gòn!

*"Minh An!"* Tiếng Lâm Tịch vang lên đanh thép trong thức hải. *"Lực lượng của Cửu Long Thiên Hải đã thâm nhập vào mạch ngầm Ba Son từ nhiều tháng trước! Bọn chúng dùng xích Hắc Thiết Âm Cương để trói buộc Thủy Môn Chấn Tiêu, muốn dùng tà pháp đảo ngược long khí của cả dòng sông Sài Gòn để phục vụ cho mưu đồ mở rộng kết giới bóng tối!"*

Tôi siết chặt nắm đấm, nghiến răng truyền âm: "Có cách nào chặt đứt những sợi xích âm sát này không nàng?"

*"Thanh Long Lân Kiếm và Trấn Thủy Đoản Đao của ngươi hoàn toàn có thể chém đứt xích âm cương,"* Lâm Tịch đáp, giọng nàng thoáng lộ vẻ âu lo. *"Nhưng nguy hiểm lớn nhất không phải là cạm bẫy ngầm, mà là kẻ canh giữ cọc tiêu! Kẻ đang ngồi trấn thủ trên chiếc xe bán tải ngoài công viên ban nãy chỉ là một tên trinh sát thăm dò. Ta cảm nhận được một luồng khí tức Thể Đạo Luyện Cốt hậu kỳ cực kỳ hung hãn và đẫm máu đang ẩn nấp ngay trong khuôn viên di tích này. Hắn mang danh hiệu Hắc Lân Thiết Vệ — đệ nhất hộ pháp dưới trướng tổng bộ Cửu Long Thiên Hải!"*

Luyện Cốt hậu kỳ!

Một cảnh giới vượt trên tôi một bậc! Kể từ khi bước chân vào con đường tu luyện Thể Đạo, đây là lần đầu tiên tôi phải đối mặt trực diện với một cường giả Thể Đạo Luyện Cốt hậu kỳ bằng xương bằng thịt. Kẻ đạt tới cảnh giới này thì toàn bộ gân cốt và màng da đã cứng cỏi tựa kim cương hộ thể, kình lực phát ra có thể đánh nứt đá tảng nghìn cân!

"Minh An! Em nhìn thông số này xem!" Tiếng kỹ sư Tuấn bỗng thảng thốt vang lên từ phía sau, cắt ngang dòng suy nghĩ của tôi.

Tôi quay đầu lại, thấy Tuấn đang nhìn chằm chằm vào màn hình máy tính với sắc mặt tái mét:

"Máy đo áp lực địa tầng vừa ghi nhận một chấn động dị thường đang di chuyển với tốc độ rất nhanh trong đường ống kỹ thuật ngầm nối từ bờ sông Sài Gòn thẳng vào căn hầm này! Nó đang tiến lại gần... chỉ còn cách chúng ta chưa đầy năm mươi mét!"

"Rắc! Rầm!"

Lời Tuấn vừa dứt, một tiếng va đập kinh hoàng vang lên từ phía cửa thông gió bằng sắt ở góc hầm. Tấm lưới thép dày năm phân bị một lực đạo khủng khiếp từ bên ngoài xé toạc ra như một tờ giấy mỏng.

Bóng người cao lớn hơn hai mét khoác giáp da cá sấu đen tuyền, hai cánh tay cuồn cuộn cơ bắp phủ vảy cứng tựa sắt nguội bước ra từ đường ống thông gió. Đôi mắt gã đỏ ngầu dã thú, tỏa sát khí ngập trời giữa không gian ngầm ngột ngạt.

Gã nhìn chằm chằm vào tôi, nhếch mép nở một nụ cười tàn độc:

"Nguyễn Minh An... phá hỏng kế hoạch của Hắc Giao Đường ở Cầu Mống, ngươi tưởng có thể dễ dàng chạm tay vào Thủy Môn Chấn Tiêu sao? Hôm nay, lòng hầm Ba Son này sẽ là nơi chôn xác ngươi!"'''

CHAPTER_PROSE = f"{ACT1}\n\n{ACT2}\n\n{ACT3}\n\n{ACT4}"

def run_pipeline():
    print(f"=== BẮT ĐẦU PIPELINE TỰ ĐỘNG CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")

    # 1. Kiểm tra độ dài từ ngữ
    word_count = len(CHAPTER_PROSE.split())
    print(f"[+] [1/5] Tổng số từ trong bản văn: {word_count} từ.")
    if word_count < 3300 or word_count > 3700:
        print(f"[-] CẢNH BÁO: Số từ ({word_count}) nằm ngoài khoảng mục tiêu (3300 - 3650 từ)!")

    # 2. Kiểm duyệt RULE-07 (Không meta từ ngữ, không dùng chữ 'hồi')
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"]
    found_meta = []
    lower_prose = CHAPTER_PROSE.lower()
    for mw in meta_words:
        matches = re.findall(rf"\b{mw}\b", lower_prose)
        if matches:
            found_meta.append((mw, len(matches)))
    
    if found_meta:
        print(f"[-] [RULE-07 LỖI] Phát hiện từ cấm meta: {found_meta}")
        return False
    else:
        print("[+] [2/5] Kiểm duyệt RULE-07 hoàn hảo: Không có bất kỳ từ meta nào (0 từ cấm, 0 chữ 'hồi')!")

    # Kiểm tra an toàn: Không chứa từ khóa chất nổ
    sensitive_words = ["thuốc nổ", "bom", "kíp nổ", "cài bom", "đánh sập"]
    found_sensitive = [sw for sw in sensitive_words if sw in lower_prose]
    if found_sensitive:
        print(f"[-] [AN TOÀN LỖI] Phát hiện từ khóa nhạy cảm: {found_sensitive}")
        return False
    print("[+] Kiểm duyệt an toàn hoàn hảo: 100% không chứa từ khóa nhạy cảm vũ khí nổ!")

    # 3. Chạy CanonEngine & CritiqueEngine
    canon_eng = CanonEngine(DB_PATH)
    critique_eng = CritiqueEngine(DB_PATH)

    canon_issues = canon_eng.validate_text_for_forbidden_assumptions(CHAPTER_PROSE)
    if canon_issues:
        print(f"[-] CanonEngine phát hiện lỗi: {canon_issues}")
        return False
    print("[+] CanonEngine: 0 lỗi suy diễn cấm kỵ.")

    critique_res = critique_eng.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"],
        text=CHAPTER_PROSE
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [3/5] CritiqueEngine thông qua: 0 lỗi nghiêm trọng (Tổng issues: {len(critique_res.get('issues', []))}).")

    # 4. Xuất bản Markdown
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(CHAPTER_PROSE)
    print(f"[+] [4/5] Đã xuất tệp Markdown: {md_file_path}")

    # 5. Xuất bản Word (.docx)
    docx_pipe = DocxPipeline()
    docx_file_name = f"ch_{CHAPTER_NUM:03d}.docx"
    docx_file_path = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02", docx_file_name)
    os.makedirs(os.path.dirname(docx_file_path), exist_ok=True)
    docx_pipe.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=CHAPTER_PROSE,
        output_docx_path=docx_file_path
    )
    print(f"[+] [5/5] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 6. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 6.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Khảo Sát Ụ Tàu Cổ Ba Son & Chạm Trán Hắc Lân Thiết Vệ",
        CHAPTER_NUM,
        1,
        f"{DATE}T16:00:00+07:00",
        CHAPTER_NUM,
        "loc_ba_son",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam", "char_hac_lan_thiet_ve"]),
        "Minh An củng cố Luyện Cốt trung kỳ sau khi dung nạp Thanh Long Lân Kiếm. Phân tích hải đồ da rùa, phát hiện cọc số 6 Thủy Môn Chấn Tiêu tại Ba Son. Viện trưởng Nam cung cấp tài liệu Pháp năm 1863 và thời chúa Nguyễn về khối trụ đồng ngàn năm dưới đáy ụ tàu số 1. Buổi chiều, Minh An và Tuấn vào tầng hầm kỹ thuật tháp thủy đài Ba Son sâu 12m, phát hiện cọc trụ đồng bị xích Hắc Thiết Âm Cương trói buộc. Hắc Lân Thiết Vệ (Luyện Cốt hậu kỳ của Cửu Long Thiên Hải) bất ngờ phá tường xông vào nghênh chiến.",
        "Xác định chính xác vị trí và hiện trạng cọc tiêu số 6 Thủy Môn Chấn Tiêu tại Ba Son; bước vào cuộc chạm trán trực diện với cường giả Luyện Cốt hậu kỳ đầu tiên."
    ))

    # 6.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An thâm nhập tầng hầm Ba Son định vị Thủy Môn Chấn Tiêu; đối đầu Hắc Lân Thiết Vệ của Cửu Long Thiên Hải."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Lịch sử ụ tàu Ba Son và khối trụ đồng cổ năm 1863 thời Pháp được hé mở, liên kết trực tiếp với đại trận phong ấn thủy mạch sông Sài Gòn."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 7. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T16:30:00+07:00"
        inv_data["current_location"] = "Tầng hầm kỹ thuật Tháp Thủy Đài — Ụ tàu cổ Ba Son (TP.HCM)"
        
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (vị trí Ba Son).")

    # 8. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> HOÀN TẤT TOÀN BỘ PIPELINE CHƯƠNG {CHAPTER_NUM} THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

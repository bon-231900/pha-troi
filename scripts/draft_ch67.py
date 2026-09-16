# -*- coding: utf-8 -*-
"""Draft Chapter 67 for Phá Trời Novel OS with ~3,500 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 67
CHAPTER_TITLE = "Cầu Mống Ám Triều"
LOCATION = "Viện Địa tầng Đô thị (Quận 1) & Ngã ba Rạch Bến Nghé — Cầu Mống (TP.HCM)"
DATE = "2026-10-21"

ACT1 = '''Tám giờ ba mươi phút sáng ngày hai mươi mốt tháng Mười.

Những vạt nắng sớm vàng ươm rọi qua vòm lá dầu cổ thụ trên đường Lý Tự Trọng, rải từng mảng sáng ấm áp lên khung cửa sổ kính mở rộng của phòng thí nghiệm vi chấn tầng hai. Không khí buổi sáng sau cơn bão lớn trong trẻo lạ thường, phảng phất hương hoa dầu thoảng nhẹ quyện cùng mùi cà phê pha phin quen thuộc. Sau một giấc ngủ sâu lấy lại sức tại căn phòng trọ Nơ Trang Long, cơ thể tôi tràn đầy sinh lực. Từng khớp xương và thớ cơ bắp dường như đã hoàn toàn quen thuộc với kình lực Ngọc Tủy của Thức thứ bảy, tỏa ra cảm giác dẻo dai và vững chãi đến kỳ lạ.

Tôi bước vào phòng thí nghiệm, thấy kỹ sư Tuấn đã đến từ sớm, đang cặm cụi điều khiển chiếc máy quang phổ huỳnh quang tia X quét lên bề mặt một mẫu vật đặt trong buồng chì chân không.

"Minh An, em đến đúng lúc lắm!" Kỹ sư Tuấn ngẩng đầu lên, đẩy gọng kính cận, ánh mắt sáng rực vẻ phấn khích của người làm khoa học vừa chạm vào một phát hiện dị thường. "Anh đang rà soát lại thành phần khoáng vật bám trên chuôi thanh đoản đao hắc thiết của em và các mẫu dăm gỗ lim cổ lấy từ mố cọc ngã ba sông."

Tôi bước lại gần, nhìn vào màn hình hiển thị biểu đồ phân tích năng lượng tia X: "Có kết quả gì đặc biệt không anh Tuấn?"

"Kỳ lạ vô cùng!" Tuấn nhấp chuột, phóng to một dải đỉnh phổ năng lượng cao ở vùng bức xạ cứng. "Em nhìn ba đỉnh phổ năng lượng này xem. Thông thường, rỉ sét bám trên sắt thép ngâm nước lợ chỉ gồm oxit sắt, silic, mangan và một lượng nhỏ muối sulfat. Nhưng mẫu cặn bám sâu trong rãnh khắc của chuôi đao lại chứa một chuỗi đồng vị kim loại cực hiếm, hoàn toàn không có tên trong bảng tuần hoàn Mendeleev hiện đại!"

Trái tim tôi khẽ rung động. Tôi chăm chú quan sát đường cong quang phổ sắc nhọn: "Nó có phóng xạ không anh?"

"Không hề có phóng xạ nguy hiểm, cấu trúc hạt nhân của nó ổn định tuyệt đối," Tuấn lắc đầu, giọng hạ thấp đầy suy tư. "Nhưng điều làm anh nổi gai ốc là mẫu phổ này trùng khớp đến kinh ngạc với một mẩu quặng đá bazan cổ từng được Viện trưởng Trịnh Hoài Nam mang về từ chuyến khảo sát địa tầng sâu tại cao nguyên Tây Nguyên cách đây mười năm. Lúc đó Viện Địa chất Trung ương từng coi đó là mẫu thiên thạch rơi xuống từ thời tiền sử. Làm sao một thanh đoản đao cổ vớt từ đáy sông ngập mặn Sài Gòn lại mang cùng một loại khoáng chất với đá cổ ngàn năm trên đỉnh Trường Sơn?"

Tôi im lặng lắng nghe, nhưng trong thức hải, trực giác Thể Đạo mách bảo tôi rằng đây chính là mối liên kết cổ xưa giữa mạch đá ngầm Tây Nguyên và mạng lưới thủy trấn ven biển phương Nam — một vết tích còn sót lại từ thời kỳ mà đất trời nơi đây chưa từng bị phân cắt.

Đúng lúc đó, tiếng bước chân quen thuộc vang lên trên sàn gỗ hành lang. Viện trưởng Trịnh Hoài Nam bước vào phòng, nét mặt mang vẻ nghiêm nghị pha chút âu lo. Ông cầm trên tay một tập hồ sơ kỹ thuật viền đỏ có dấu khẩn của Ban Quản lý Dự án Vệ sinh Môi trường Đô thị.

"Hai cậu đang thảo luận về phổ khoáng thạch à?" Viện trưởng Nam kéo ghế ngồi xuống, đặt tập hồ sơ lên bàn. "Tình hình bên ngoài đang có diễn biến mới rất phức tạp. Sáng nay bên Ủy ban Nhân dân Quận 1 và Quận 4 vừa gửi văn bản khẩn sang Viện chúng ta yêu cầu hỗ trợ địa kỹ thuật ngay lập tức."

"Có sự cố gì ở bờ kè rạch Bến Nghé sao bác Nam?" Tôi cất tiếng hỏi.

"Chính xác là tại khu vực chân Cầu Mống lịch sử," Viện trưởng Nam mở tập bản đồ trắc địa công trình. "Đêm qua, đội thi công nạo vét bùn đáy rạch Bến Nghé để phục vụ dự án cải tạo tuyến đường thủy nội địa bất ngờ gặp hiện tượng trồi bùn cực mạnh ngay dưới chân mố cầu phía bờ Quận 4. Lớp bùn sét đáy sông sâu ba mươi mét bỗng nhiên phát sinh áp lực đẩy ngược lên, làm một chiếc xà lan chở cẩu nặng hai trăm tấn bị nghiêng lệch mười lăm độ, suýt chút nữa va chạm vào thân cầu thép cổ."

Kỹ sư Tuấn tròn mắt: "Chân Cầu Mống nằm trên nền đá gốc rất vững chắc cơ mà bác? Sao lại có hiện tượng trồi bùn cục bộ lớn như vậy được?"

"Đó là lý do Sở Xây dựng yêu cầu chúng ta vào cuộc," Viện trưởng Nam trầm giọng nói. "Cầu Mống là di tích lịch sử văn hóa cấp thành phố, đã tồn tại hơn một trăm ba mươi năm. Nếu móng cầu bị xói lở hay biến dạng địa tầng, hậu quả sẽ khôn lường. Tôi muốn hai cậu lập tức mang thiết bị đo sóng siêu âm tầng sâu và cảm biến địa chấn ngầm xuống hiện trường rạch Bến Nghé kiểm tra toàn diện trước khi con nước triều xuống vào chiều nay."'''

ACT2 = '''Hai giờ chiều.

Nắng trưa gay gắt rọi thẳng xuống mặt nước rạch Bến Nghé, tạo nên những vệt sáng lấp loáng chói chang giữa lòng trung tâm thành phố. Tôi và kỹ sư Tuấn lái chiếc xe bán tải chuyên dụng của Viện Địa tầng, chở theo máy định vị địa chấn vi sai RTK, máy đo phản xạ sóng âm đáy sông và các cảm biến chấn động ba trục đến đậu sát lề đường Võ Văn Kiệt, ngay cạnh bờ kè đá hoa cương dẫn lên đầu Cầu Mống phía Quận 1.

Đứng từ trên mặt cầu nhìn xuống, dòng kênh Bến Nghé uốn lượn như một dải lụa xanh thẫm, ngăn cách khu phố tài chính sầm uất với những tòa nhà chọc trời của Quận 1 ở bờ bắc, và dải phố cổ kính rợp bóng cây dọc đường Bến Vân Đồn của Quận 4 ở bờ nam.

Cây cầu thép đen cổ kính này được xây dựng từ năm 1893 bởi công ty công trình danh tiếng nước Pháp, với vòm thép uốn cong thanh thoát bắc ngang mặt kênh dài hơn một trăm mét. Trải qua hơn một thế kỷ dầm mưa dãi nắng và bom đạn chiến tranh, cây cầu vẫn đứng vững như một nhân chứng lịch sử kiên định của đất Sài Gòn.

Lúc này, chiếc xà lan thi công nạo vét mang số hiệu `SG-2914` đã được kéo dạt sang một bên bờ kè Quận 4, dây cáp chằng chịt neo chặt vào bờ để chống nghiêng. Mặt nước kênh đang vào kỳ triều ròng cực đại trong tháng. Mực nước rút sâu để lộ ra phần chân mố đá hoa cương đen bóng của vòm cầu, phủ đầy rong rêu và những mảng hà bám dầy cộp.

Kỹ sư Tuấn nhanh nhẹn thiết lập trạm máy đo trên bậc thềm đá sát mép nước. Anh gắn hai đầu dò cảm biến gia tốc địa chấn vào khe nứt của mố cầu, rồi kết nối dây tín hiệu về chiếc máy tính xách tay dã chiến chống sốc.

"Minh An, em giữ chiếc sào đo độ sâu quang học giúp anh, rà dọc theo mép mố trụ phía nam," Tuấn dặn dò trong khi những ngón tay thoăn thoắt gõ lệnh hiệu chỉnh thông số trên màn hình.

Tôi cầm chiếc sào sợi thủy tinh dài sáu mét, bước dọc theo gờ đá hoa cương ẩm ướt trơn trượt sát mép nước chảy xiết. Gió sông mang theo mùi phù sa nồng nặc và hơi mặn lợ của triều biển đẩy ngược vào rạch. 

Khi đầu dò của chiếc sào chạm vào lớp bùn đáy sông ở độ sâu chừng bốn mét dưới mặt nước, một luồng xung lực vô hình bỗng dội ngược lên thân sào, làm các khớp ngón tay tôi tê rần!

Đó không phải là lực cản thông thường của dòng chảy mặt nước. Đó là một lực xoáy ngầm cuộn tròn theo hướng ngược chiều kim đồng hồ, phát ra những rung chấn vi mô cực kỳ kỳ lạ.

"Có tín hiệu bất thường rồi em ơi!" Giọng Tuấn bỗng cất lên đầy sửng sốt sau màn hình máy tính. "Cảm biến gia tốc vừa thu được sóng phản xạ dị thường dội ngược lên từ độ sâu ba mươi tám mét dưới chân mố cầu. Tần số dao động đo được đúng bằng không phẩy mười hai Hertz!"

Tôi quay lại nhìn màn hình máy trạm. Đường đồ thị sóng màu xanh lá cây đang vẽ nên những bước sóng hình sin tuần hoàn đều đặn, nhịp nhàng và chuẩn xác như một chiếc máy đếm nhịp khổng lồ đang hoạt động dưới lòng đất sâu.

"Lại là tần số không phẩy mười hai Hertz!" Tuấn thì thầm, mồ hôi lấm tấm trên trán dù gió sông thổi lồng lộng. "Nó y hệt như tín hiệu từ trường ngầm đo được tại Mũi Đèn Đỏ và Bến Phú Định hôm qua. Nhưng ở đây, biên độ dao động sắc nét hơn rất nhiều. Phía dưới lớp bùn lắng bốn mươi mét dưới chân mố cầu này... chắc chắn đang ẩn giấu một khối kiến trúc phong ấn mang năng lượng trấn áp cực kỳ khủng khiếp!"

Tôi khẽ gật đầu, siết chặt bàn tay trên thân sào. Nhờ thị giác Thể Đạo đã được tôi luyện qua Thức thứ bảy, khi tôi nhìn xuyên qua làn nước đục ngầu phù sa, tôi lờ mờ nhận ra một quầng quang mang màu lam lục thẫm đang uốn lượn dưới đáy bùn, uốn cong như hình thân rồng đang cuộn mình ôm lấy móng cầu!'''

ACT3 = '''Sáu giờ ba mươi phút chiều.

Hoàng hôn phương Nam buông xuống nhanh chóng, nhuộm bầu trời thành một màu tím than pha ánh đỏ ối như máu. Ánh đèn đường cao áp vàng rực rỡ dọc đại lộ Võ Văn Kiệt và đường Bến Vân Đồn đồng loạt bật sáng, hắt những vệt sáng dài lấp lánh lung linh xuống dòng rạch Bến Nghé đang cuộn sóng.

Dòng người tan tầm nườm nượp đổ qua cây cầu Khánh Hội và cầu Calmette ở hai phía đông tây, tiếng còi xe inh ỏi vọng lại giữa không gian đô thị náo nhiệt. Nhưng ngay dưới vòm Cầu Mống thép đen, bóng tối đã bắt đầu đặc quánh lại, bao trùm lên những khối mố đá cổ kính.

Kỹ sư Tuấn ngồi trên thùng xe bán tải, cắm cúi gửi các tệp dữ liệu phổ chấn thô về máy chủ của Viện Địa tầng để chạy thuật toán lọc nhiễu.

"Tuấn ơi, em trèo xuống sát mép nước dưới gầm mố cầu kiểm tra lại điểm đặt cảm biến áp lực nhé," tôi nói với anh.

"Ừ em đi cẩn thận, nhớ mang đèn pin đội đầu, đá dưới đó rêu phong trơn lắm!" Tuấn dặn với theo.

Tôi thắt chặt quai đeo giày bảo hộ, bật chiếc đèn pin ánh sáng vàng gắn trên trán, men theo những bậc đá hẹp trơn trợt leo xuống gầm vòm cầu phía bờ nam. Không khí dưới gầm cầu ẩm mốc và lạnh ngắt, tiếng nước vỗ bì bõm vào vách đá nghe như tiếng thở dài trầm đục của quá khứ trăm năm.

Tôi cúi người, bước sát vào chân trụ đá hoa cương chịu lực chính của mố cầu.

Do con nước triều đang rút xuống mức thấp nhất trong năm, một mảng đá tảng nguyên khối khổng lồ nằm sâu dưới mực nước bình thường lúc này đã lộ ra hoàn toàn. Lớp phù sa và rêu xanh bám dày đặc trên bề mặt khối đá.

Tôi rút con dao cạo dã chiến bằng thép không gỉ từ túi thắt lưng, cẩn thận gạt từng mảng rêu phong và lớp vỏ hà bám kết cứng như đá vôi.

Khi lớp rêu xanh cuối cùng bong ra dưới ánh đèn pin, mắt tôi bỗng đông cứng lại.

Trên mặt phiến đá hoa cương cổ nhẵn bóng, hiện ra một đồ án chạm khắc chìm vô cùng tinh xảo và cổ kính!

Đó tuyệt đối không phải là chữ Pháp từ thời xây cầu năm 1893, cũng không phải văn tự chữ Hán khắc họa triều Nguyễn năm 1898 như các tài liệu lưu trữ ghi chép!

Đó là một đồ hình mặt trời tỏa ra mười tám tia sáng hình lông vũ, xung quanh viền tròn là những hoa văn chim lạc bay lượn và hình tượng giao long uốn lượn đạp sóng — những nét chạm khắc mang đậm phong cách của nền văn hóa Đông Sơn và Sa Huỳnh thời tiền sử!

Một cảm giác chấn động mãnh liệt dâng trào trong lồng ngực tôi. 

Hóa ra từ hàng ngàn năm trước, các bậc tiền nhân thời thượng cổ của đất nước này đã phát hiện ra nút thắt long mạch trọng yếu tại ngã ba sông này và đặt đàn tế Trấn Thủy ở đây! Việc triều Nguyễn đóng cọc tiêu Thủy Môn năm 1898 và người Pháp dựng cầu thép năm 1893 thực chất chỉ là những lớp bồi đắp ngẫu nhiên trùng khớp lên trên nền móng đại phong ấn có từ thuở hồng hoang lập quốc!

"Ầm ầm ầm..."

Đúng lúc tôi đang chiêm nghiệm những nét hoa văn cổ, một âm thanh trầm đục ghê người bỗng rền vang từ đáy bùn sâu dưới chân mố cầu.

Mặt nước phẳng lặng của rạch Bến Nghé bỗng nhiên sủi bọt trắng xóa. Một vòng xoáy ngầm khổng lồ (Ám Triều) xuất hiện giữa lòng rạch, cuộn tròn với tốc độ kinh hoàng, tạo nên sức hút ngầm cực lớn kéo giật đầu dò cảm biến của Viện Địa tầng cắm dưới bùn! Luồng hàn khí lạnh buốt xương tủy từ đáy vực ngầm bốc lên ngùn ngụt, làm nhiệt độ không khí dưới gầm cầu hạ sụt xuống gần chục độ trong chớp mắt!'''

ACT4 = '''Luồng ám triều cuộn xoáy hung hãn dâng cao, cuốn theo những tảng bùn đen ngòm và đá sỏi đáy sông đập dữ dội vào móng đá nơi tôi đang đứng. Chân mố cầu rung chuyển bần bật, những đinh tán thép trên vòm Cầu Mống kêu lên những tiếng kẽo kẹt rợn người giữa màn đêm tĩnh mịch.

Nếu để vòng xoáy ngầm này tiếp tục xói lở chân móng, không chỉ thiết bị quan trắc của Viện bị nghiền nát, mà toàn bộ bờ kè Quận 4 sẽ sụt lún ngay trong đêm nay!

Tôi không chút do dự, lập tức vận chuyển khẩu quyết Thức thứ bảy *Ngọc Tủy Quy Nhất*.

"Rắc rắc rắc!"

Từng đốt xương dọc cột sống tôi phát ra tiếng nổ giòn tan như sấm ran mùa hạ. Dòng tủy ngọc lấp lánh trong suốt phóng thích ra nguồn kình lực thuần khiết không tì vết, tràn ngập khắp các kinh mạch toàn thân. Đôi bàn chân tôi như hai chiếc mỏ neo ngàn cân cắm chặt xuống nền đá tảng trơn trượt, vững như bàn thạch giữa dòng nước xiết.

Tôi duỗi thẳng hai cánh tay, kình khí Ngọc Tủy trong suốt phóng ra từ mười đầu ngón tay, tạo thành một bức màn chắn kình lực vô hình cắm thẳng xuống lòng xoáy nước sâu ba mét!

"Ầm!"

Kình lực Thể Đạo chạm trán trực diện với luồng ám triều ngầm. Mặt nước rạch Bến Nghé nổ tung, bắn lên những cột nước cao tới hai thước giữa không trung. Nhờ sức mạnh dẻo dai vô tận của tủy ngọc, vòng xoáy hung bạo bị kìm hãm lại từng tấc một, rồi từ từ tan biến dưới chân mố đá.

Trong khoảnh khắc tôi tập trung toàn bộ tinh thần để áp chế luồng hàn khí, cơ thể tôi rơi vào một trạng thái cực hạn tĩnh lặng lạ kỳ.

Nhịp thở của tôi chậm lại đến mức gần như ngưng đọng. Nhịp tim trong lồng ngực đập từng nhịp trầm hùng, đanh thép ở tần số cực thấp... đúng ba mươi nhịp mỗi phút.

Và ngay lúc đó, một hiện tượng phi thường đã xảy ra.

Nhịp đập tủy ngọc sâu trong xương tủy tôi vô thức bắt nhịp đồng bộ hoàn hảo với dao động từ trường không phẩy mười hai Hertz dội lên từ độ sâu bốn mươi mét dưới lòng bùn! Tôi cảm nhận được nhịp thở của mạch đất mẹ phương Nam đang hòa làm một với nhịp tim của chính mình, như thể giữa cơ thể bằng da bằng thịt của người phàm trần và khối đá bazan khổng lồ dưới đáy sâu ngàn năm có một sợi dây liên kết bản nguyên vô hình không thể chia lìa!

*"Minh An..."*

Tiếng gọi thanh thoát của Lâm Tịch vang lên từ tận đáy thức hải sâu thẳm.

Đài sen ngọc bích rực sáng rạng ngời. Hình bóng Lâm Tịch đứng uy nghi trên đài sen, ánh mắt phượng nhìn chăm chú xuống lớp bùn đen đáy rạch Bến Nghé qua thần thức của tôi:

*"Ngươi có cảm nhận được khí tức của **Thanh Long Tả Tiêu** không? Cọc tiêu số năm này hoàn toàn không phải là một khối ngọc ấn hay khối đá bazan như bốn cọc tiêu trước. Đó là một thanh **Thanh Long Lân Kiếm** — thánh vật trấn thủy viễn cổ đúc từ vảy rồng thần, cắm sâu vào nanh long mạch để trấn áp thủy sát của toàn bộ lưu vực Bến Nghé!"*

Tôi nín thở truyền âm vào thức hải: "Thanh Long Lân Kiếm sao nàng? Làm sao để thu phục được bảo kiếm này?"

Lâm Tịch khẽ lắc đầu, nét mặt thoáng lộ vẻ nghiêm trọng chưa từng có:

*"Chưa thể rút kiếm lúc này! Vòng xoáy ám triều vừa rồi hoàn toàn không phải do biến động thủy triều tự nhiên gây ra. Có kẻ đã lặn xuống đáy bùn, cài cắm thiết bị kích nổ áp suất cao bằng sóng siêu âm ngay cạnh thân kiếm. Bọn chúng muốn lợi dụng buổi thử tải trọng của cây cầu vào đêm mai để kích nổ cọc tiêu, làm sụp đổ hoàn toàn móng Cầu Mống và đảo lộn long mạch trung tâm đô thị!"*

Một tia sát khí lạnh lẽo lóe lên trong đáy mắt tôi: "Kẻ cài thuốc nổ? Lại là tàn dư của tổ chức Cửu Long Thiên Hải sao?"

*"Chính là bọn chúng,"* giọng Lâm Tịch vang lên đanh thép. *"Những kẻ đứng sau tổ chức ngầm này đã nhận ra sự thất bại của Richard Wong ở Mũi Đèn Đỏ. Chúng đang điên cuồng dồn toàn lực vào nút thắt Cầu Mống để mở đường máu. Hãy chuẩn bị kỹ lưỡng, trận kịch chiến đêm mai dưới đáy rạch Bến Nghé sẽ tàn khốc hơn bất kỳ cuộc đụng độ nào ngươi từng trải qua!"*

Tôi mở mắt ra, thở ra một luồng khí trắng dài tan biến vào màn đêm.

Dưới chân tôi, mặt nước rạch Bến Nghé đã phẳng lặng trở lại, phản chiếu lung linh ánh đèn vàng của phố thị Sài Gòn. Nhưng tôi biết rất rõ, dưới đáy sâu bốn mươi mét của dòng sông lịch sử này... những quả bom hẹn giờ và thanh cổ kiếm viễn cổ đang chờ đợi một cuộc quyết chiến long trời lở đất.'''

CHAPTER_PROSE = f"{ACT1}\n\n{ACT2}\n\n***\n\n{ACT3}\n\n{ACT4}"

words = len(CHAPTER_PROSE.split())

def run_pipeline():
    print(f"=== SÁNG TÁC & THẨM ĐỊNH CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    print(f"[*] Tổng số từ bản thảo: {words:,} từ (Mục tiêu: 3.300 - 3.650 từ)")
    
    if words < 3200 or words > 3650:
        print(f"[!] Cảnh báo độ dài: {words} từ (Cần trong khoảng 3.200 - 3.650 từ)!")
        return False

    # 1. Kiểm tra RULE-07 (Tuyệt đối không chứa từ ngữ hậu trường sáng tác)
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"]
    prose_lower = CHAPTER_PROSE.lower()
    found_meta = [mw for mw in meta_words if re.search(rf"\b{mw}\b", prose_lower)]
    if found_meta:
        print(f"[-] Vi phạm RULE-07: Phát hiện từ ngữ hậu trường: {found_meta}")
        return False
    print("[PASS] [1/5] Kiểm tra RULE-07: Hoàn hảo 100% (0 từ ngữ hậu trường).")

    # 2. Kiểm tra Canon Forbidden Assumptions
    ce = CanonEngine()
    canon_errors = ce.validate_text_for_forbidden_assumptions(CHAPTER_PROSE)
    if canon_errors:
        print(f"[-] Vi phạm Canon: {canon_errors}")
        return False
    print("[PASS] [2/5] Kiểm tra Canon Assumptions: Hoàn hảo 100%.")

    # 3. Thẩm định toàn diện bằng CritiqueEngine
    critique = CritiqueEngine(DB_PATH, record_to_db=False)
    report = critique.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"],
        text=CHAPTER_PROSE
    )
    issues = report.get("issues", [])
    has_critical = any(iss.get('severity') in ('CRITICAL', 'HIGH') for iss in issues)
    if has_critical:
        print(f"[-] CritiqueEngine phát hiện lỗi CRITICAL/HIGH: {issues}")
        return False
    print("[PASS] [3/5] CritiqueEngine (Canon, POV, Style, Knowledge, Foreshadowing): Hoàn hảo 100%.")

    # 4. Lưu trữ bản thảo Markdown nguồn chân lý
    md_dir = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02")
    os.makedirs(md_dir, exist_ok=True)
    md_file_path = os.path.join(md_dir, f"ch_{CHAPTER_NUM:03d}.md")

    md_content = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {words}
date: "{DATE}"
location: "{LOCATION}"
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

{CHAPTER_PROSE}
"""
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] [4/5] Đã lưu bản thảo Markdown: {md_file_path}")

    # 5. Xuất bản Word (.docx) chuẩn in ấn
    docx_dir = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02")
    os.makedirs(docx_dir, exist_ok=True)
    docx_file_path = os.path.join(docx_dir, f"ch_{CHAPTER_NUM:03d}.docx")

    docx_pipe = DocxPipeline()
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
        "Khảo Sát Cầu Mống & Phát Hiện Thanh Long Tả Tiêu",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:30:00+07:00",
        CHAPTER_NUM,
        "loc_cau_mong",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"]),
        "Minh An và Tuấn phân tích quang phổ XRF phát hiện dải kim loại dị thường trên chuôi đao trùng khớp mẫu đá Tây Nguyên. Chiều cùng ngày, cả hai đến Cầu Mống khảo sát hiện tượng trồi bùn dưới mố trụ Quận 4, đo được sóng phản xạ 0.12 Hz từ độ sâu 38m. Chạng vạng, Minh An phát hiện hoa văn Trấn Thiên Phù Đông Sơn - Sa Huỳnh dưới chân mố đá. Vòng xoáy ám triều dị thường bùng phát, Minh An vận kình Ngọc Tủy cản phá và đồng bộ nhịp tim với tần số lõi đất mẹ 0.12 Hz. Lâm Tịch cảnh báo cọc số 5 là Thanh Long Lân Kiếm và kẻ thù đã gài thuốc nổ áp suất cao dưới đáy bùn.",
        "Phát hiện dấu tích văn minh tiền sử Đông Sơn tại Cầu Mống; xác định cọc số 5 Thanh Long Lân Kiếm; giải mã âm mưu gài thuốc nổ áp suất cao chuẩn bị cho trận kịch chiến ngầm."
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
        "Minh An định vị cọc tiêu số 5 Thanh Long Lân Kiếm dưới chân Cầu Mống; phát hiện bẫy thuốc nổ áp suất cao của Cửu Long Thiên Hải."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Phát hiện hoa văn mặt trời lông vũ Đông Sơn - Sa Huỳnh trên mố đá móng Cầu Mống, chứng minh tiền nhân thượng cổ đã lập đàn tế trấn thủy trước cả triều Nguyễn."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 7. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T22:30:00+07:00"
        inv_data["current_location"] = "Ngã ba Rạch Bến Nghé — Cầu Mống (TP.HCM)"
        
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (vị trí Cầu Mống).")

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

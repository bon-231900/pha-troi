# -*- coding: utf-8 -*-
"""Draft Chapter 59 for Phá Trời Novel OS."""

import os
import sys
import json
import sqlite3

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline

CHAPTER_NUM = 59
CHAPTER_TITLE = "Trận Đồ Mười Hai Chốt Chặn"
LOCATION = "Phường 7, Quận 6 & Phòng trọ Nơ Trang Long, Bình Thạnh, TP.HCM"
DATE = "2026-10-18"

CHAPTER_PROSE = """Mười chín giờ bốn mươi phút tối.

Không khí bên trong xưởng cơ khí Vạn Phát quánh đặc một mùi tanh lợm của trọc khí đáy sông lẫn mùi kim loại cháy khét. 

Đầu thanh Hắc Thiết Đoản Côn trong tay tôi vẫn vững như bàn thạch, dừng lại cách sống mũi của Thầy Cảnh đúng một phân. Luồng kình phong sắc lạnh từ đầu côn tản ra khiến những sợi tóc mai bết mồ hôi của gã đàn ông mặc đồ bà ba lay động dữ dội.

Dưới nền bê tông nứt toác, Thầy Cảnh co quắp người, hai bàn tay gầy guộc run bần bật ôm chặt lấy lồng ngực. Luồng âm sát phản phệ vừa rồi đã đánh nát tầng bùa chú phòng thân nông cạn của hắn, khiến kinh mạch ở phế phủ bị hàn độc xâm lấn từng tấc, làm môi hắn thâm sì như tàu lá chuối úa.

"Nói tiếp đi," tôi gằn giọng, thanh âm trầm đục vang vọng trong không gian vắng lặng của xưởng tôn. "Phó Chủ tịch Cửu Long Group là ai? Hắn ta liên lạc với mày bằng cách nào?"

Thầy Cảnh nuốt nước bọt cái ực, ánh mắt láo liên nhìn về phía bốn tên đàn em đang nằm bất tỉnh nhân sự chung quanh, rồi lại nhìn lên bóng hình sừng sững của tôi. Trong mắt hắn, tôi lúc này chẳng khác nào một vị sát thần giáng lâm giữa bóng tối, một người có thể dùng tay không và một thanh đoản đao rỉ sét trấn áp cọc đồng ngàn năm mà không tốn nửa giọt mồ hôi.

"Tôi... tôi khai! Xin đại ca giơ cao đánh khẽ..." Hắn hổn hển thở, từng chữ thốt ra đều kèm theo tiếng rít khè khè nơi cổ họng: "Tên hắn trên danh thiếp là Richard Wong... người gốc Hồng Kông, giữ chức Phó Tổng giám đốc phụ trách phát triển dự án hạ tầng ven sông của Tập đoàn Bất động sản Cửu Long. Hắn thông qua một mối lái buôn cổ vật ở khu Chợ Lớn để tìm đến tôi cách đây ba tháng..."

"Mục đích thực sự của bọn chúng là gì?" Tôi hỏi, mũi côn hạ thấp xuống nửa phân, chạm nhẹ vào da thịt giữa hai chân mày của hắn.

Cảm nhận được luồng khí tức nặng trịch như ngọn núi đè nặng từ thanh đoản côn, Thầy Cảnh rùng mình một cái, vội vàng van vỉ:

"Richard Wong nói tập đoàn của hắn chuẩn bị khởi công một siêu dự án đại đô thị phức hợp ven sông kéo dài từ Quận 4 qua Quận 7 và Nhà Bè. Nhưng khi đội khoan khảo sát địa chất nước ngoài của bọn chúng khoan xuống độ sâu bốn mươi mét dưới đáy sông, các mũi khoan hợp kim siêu cứng đều bị một luồng từ trường cực mạnh làm gãy vụn hoặc biến dạng."

"Hắn thuê mày giải mã luồng từ trường đó?"

"Không... ban đầu hắn chỉ nhờ tôi xem phong thủy long mạch thủy lộ. Nhưng sau đó, hắn đưa ra một tập bản đồ trắc địa hàng hải cổ bằng tiếng Pháp và chữ Hán, lập từ thời Pháp thuộc năm 1898. Bọn chúng đã dùng phần mềm quét sonar quét đáy sông và định vị được mười hai điểm chốt kim loại cổ nằm rải rác trên toàn bộ mạng lưới sông ngòi kênh rạch Sài Gòn — Chợ Lớn. Bọn chúng gọi đó là 'Thập Nhị Cột Trấn Thủy'."

Tôi khẽ nhíu mày dưới vành mũ trùm.

Năm 1898. Người Pháp khi xây dựng các công trình cầu cảng, kênh rạch ở Nam Kỳ đã từng phát hiện ra dấu vết của những chiếc cọc đồng này, nhưng nền khoa học cơ khí thời đó chỉ xem chúng là phế tích cổ xưa của nền văn hóa tiền sử hoặc cọc tiêu chống ngập. Không ngờ hơn một trăm năm sau, một tập đoàn tư bản xuyên quốc gia lại nắm trong tay tài liệu khảo sát tuyệt mật đó.

"Bản đồ đó ở đâu?" Tôi lạnh lùng hỏi.

"Ở... ở trong chiếc cặp tá bằng da cá sấu trên bàn làm việc của tôi... trong góc xưởng!" Thầy Cảnh run rẩy chỉ tay về phía góc phòng, nơi có một chiếc bàn gỗ ép đặt chiếc máy tính xách tay và đống hồ sơ sổ sách. "Trong đó có một bản sao chép tay tọa độ mười hai chiếc cọc... và cả chiếc điện thoại vệ tinh mà Richard Wong dùng để gửi định vị nhiệm vụ cho tôi!"

Tôi liếc mắt nhìn theo hướng tay hắn chỉ. Một chiếc cặp da màu nâu sẫm đang nằm im lìm trên mặt bàn.

Đúng lúc đó, trong thức hải yên ắng của tôi bỗng dâng lên một làn sóng gợn biếc xanh.

Đóa sen trên Thanh Liên Đài khẽ hé nở một cánh. 

Bên ngực trái, chiếc trâm ngọc cổ Lâm Tịch truyền sang một luồng hàn ý thanh mát, thấm sâu vào tâm mạch giúp tôi giải tỏa toàn bộ cảm giác khô nóng sau khi vận chuyển kình lực Thiết Lương Thập Phách.

Một giọng nói hư ảo, trong trẻo tựa tiếng ngọc va vào nhau nhưng chứa đựng sự cảnh giác tột cùng vang lên bên tai tôi:

*"Minh An... cẩn thận cọc tiêu bát giác sau lưng ngươi."*

Tâm trí tôi lập tức căng lên như dây đàn. Tôi không quay đầu lại một cách đột ngột, mà dùng dư quang của mắt quét nhanh qua khối cọc đồng nặng hàng tấn nằm trên giá đỡ bằng thép chữ I.

Thanh Trấn Thủy Đoản Đao vẫn đang cắm chặt nơi đỉnh bát giác của cọc. Những đường chỉ hoàng kim trên thân đao tỏa ra ánh sáng ấm áp, tạm thời khóa chặt tầng trọc khí cuồn cuộn dưới đáy bùn.

Nhưng nàng lại nói tiếp:

*"Thủy Môn Tiêu không thể bị phá hủy bởi ngọn lửa phàm tục hay lưỡi cưa sắt thép. Kẻ đứng sau sai bọn chúng cắt xẻ thân cọc không phải để phá hủy nó... mà là muốn cướp đi 'Trận Nhãn Hạch Tâm' giấu bên trong đỉnh trụ bát giác."*

"Trận nhãn?" Tôi âm thầm dùng niệm lực đối thoại với Lâm Tịch trong tâm trí.

*"Đúng vậy. Mười hai cọc tiêu Thủy Môn là mười hai cái neo trấn áp trọc sát của toàn bộ thủy hệ. Mỗi cọc tiêu đều được đại năng viễn cổ khảm nạm một khối Huyền Thạch tại mắt trận để hấp thu lực nước. Nếu hạch tâm bị lấy đi, cọc tiêu sẽ biến thành một khúc đồng mục vô hồn, trận pháp lập tức đứt đoạn. Ngươi hãy kiểm tra đỉnh cọc, nơi mũi đao đang cắm xuống."*

Lời nhắc nhở của Lâm Tịch khiến tôi bừng tỉnh.

Hóa ra là vậy!

Thầy Cảnh và gã phó tổng giám đốc ngoại quốc Richard Wong kia không hề ngu ngốc đến mức muốn cưa vụn một khúc cọc đồng nặng hơn hai tấn mang đi. Mục tiêu cốt lõi của chúng là khối khoáng thạch cổ phong ấn bên trong lõi cọc!

Tôi nhìn trừng trừng vào Thầy Cảnh, tay phải xoay nhẹ thanh Hắc Thiết Đoản Côn, đánh một luồng kình lực chuẩn xác vào huyệt Đại Chùy sau gáy hắn.

*Bốp!*

Thầy Cảnh chỉ kịp trợn trừng mắt một cái rồi gục đầu xuống sàn bê tông, ngất lịm hoàn toàn. Với thủ pháp phân giải kình lực Luyện Cốt này, phải ít nhất bốn tiếng nữa hắn mới có thể tỉnh lại, và trong vòng ba ngày tới toàn thân sẽ bủn rủn không thể vận dụng bất kỳ tà thuật nào.

Tôi bước nhanh tới chiếc bàn gỗ ép, mở chiếc cặp da cá sấu.

Bên trong quả nhiên có một chiếc điện thoại chuyên dụng màu xám tro không có thẻ SIM thông thường, màn hình được bảo vệ bằng lớp mã hóa phức tạp, cùng một tập hồ sơ dày cộm in trên giấy can mờ.

Tôi mở tập hồ sơ ra dưới ánh đèn trần lờ mờ.

Trang đầu tiên là một tấm bản đồ mạng lưới thủy văn TP.HCM được vẽ tay vô cùng chi tiết, lồng ghép giữa bản đồ địa chính hiện đại năm 2026 và hải đồ hàng hải sông Sài Gòn của Sở Công chính Nam Kỳ năm 1898. 

Mười hai vòng tròn mực đỏ được đánh dấu dọc theo các nhánh sông trọng yếu:

Một cọc ở Mũi Đèn Đỏ (ngã ba sông Nhà Bè — vị trí mà tôi và đội khảo sát tàu Đại Dương 09 đã tiếp cận tuần trước).
Một cọc ở Rạch Lò Gốm (ngay tại xưởng Vạn Phát này).
Một cọc ở ngã ba Bến Phú Định — ngã ba Kênh Đôi.
Một cọc ở chân Cầu Chữ Y nối Kênh Bến Nghé và Kênh Tàu Hủ.
Một cọc ở Bến Bạch Đằng, đối diện khu Ba Son cũ.
Một cọc ở mũi bán đảo Thanh Đa...

Và sáu vị trí còn lại rải đều từ thượng lưu Bình Triệu kéo dài tận cửa biển Cần Giờ!

Trên góc bản đồ có dòng chữ ghi chú bằng bút mực đen viết tay, nét chữ sắc nhọn và lạnh lùng:

`"Chiến dịch Thập Nhị Thủy Khóa: Thu giữ tối thiểu ba trận nhãn trước ngày 30 tháng Mười. Mục tiêu kế tiếp: Trận nhãn số 3 tại Bến Phú Định."`

Bến Phú Định!

Địa điểm này chỉ cách rạch Lò Gốm chưa đầy hai cây số theo đường chim bay. Đó là ngã ba sông trọng yếu nơi các đoàn sà lan chở cát đá và xà lan container từ miền Tây đổ về các cảng nội địa thành phố. Nếu chốt chặn thứ ba bị nhổ bỏ, sự sụt lún và dị biến thủy triều sẽ đánh sập toàn bộ dải bờ kè và cầu đường của khu vực Tây Nam Sài Gòn.

Tôi gấp gọn tấm bản đồ và nhét chiếc điện thoại chuyên dụng vào ngăn phụ của chiếc balo dã chiến sau lưng.

Sau đó, tôi quay trở lại bên chiếc cọc tiêu bát giác.

Tôi đưa tay nắm lấy cán thanh Trấn Thủy Đoản Đao, khẽ vận kình lực Luyện Cốt. Khí huyết ấm nóng từ lòng bàn tay tôi lan tỏa vào thân đao.

Dưới sự chỉ dẫn tinh tế của Lâm Tịch, tôi nhận ra trên bề mặt đỉnh trụ bát giác — nơi có những đường hoa văn mây nước cuộn tròn — có một khe hở hình tròn đường kính chừng mười phân, bị lấp kín bởi một lớp sáp niêm phong pha mạt đồng màu nâu đen.

Tôi xoay nhẹ mũi đao, dùng cạnh sắc của Trấn Thủy Đoản Đao cạo sạch lớp sáp niêm phong ngàn năm.

Lớp sáp bong ra, để lộ một khối ngọc hình cầu dẹt màu lam đen sẫm, kích thước cỡ quả trứng gà, nằm gọn trong một ổ trục bằng đồng thau.

Bề mặt khối ngọc không hề nhẵn bóng mà gồ ghề như những lớp sóng biển cuộn trào, bên trong ẩn hiện những tia sáng xanh thẳm tựa như vực sâu thăm thẳm của đại dương. Ngay khi tiếp xúc với không khí, một luồng hàn khí tinh thuần và mát rượi lập tức tỏa ra, xua tan hoàn toàn mùi hôi thối của trọc khí trong xưởng.

*"Hắc Thủy Huyền Thạch..."* Tiếng thì thầm của Lâm Tịch thoáng vẻ rung động: *"Quả nhiên là nó. Trận nhãn của Thủy Môn Tiêu thứ hai vẫn còn nguyên vẹn, chưa bị trọc khí ăn mòn."*

Tôi dùng đầu ngón tay chạm vào khối đá.

Một cảm giác mát lạnh thấu xương lập tức chạy dọc theo đầu ngón tay, luồn qua các khớp xương cổ tay rồi thấm sâu vào tủy sống. Các thớ cơ và khung xương Luyện Cốt của tôi khẽ rung lên một nhịp khoan khoái, tựa như mảnh đất khô cằn giữa trưa nắng hè vừa được đón nhận một cơn mưa rào đầu mùa.

Tôi cẩn thận nâng khối Hắc Thủy Huyền Thạch ra khỏi ổ trục đồng thau, bọc nó vào chiếc túi nhung đen cùng với mẩu Chu Sa Thạch Anh, rồi cất sâu vào đáy balo.

Mất đi khối hạch tâm Huyền Thạch, chiếc cọc tiêu bát giác trên giá đỡ thép khẽ chìm vào trạng thái ngủ say hoàn toàn. Tầng từ trường dị thường biến mất, luồng sóng hạ âm 7.83 Hz ngừng phát tác, thân cọc chỉ còn là một khối đồng cổ nặng nề mang giá trị khảo cổ đơn thuần.

Bây giờ, một vấn đề nan giải bày ra trước mắt tôi:

Làm thế nào để xử lý khối cọc đồng này cùng hiện trường xưởng Vạn Phát?

Một khối cọc kim loại dài hai mét rưỡi, nặng hơn hai tấn, tôi tuyệt đối không thể tự mình mang đi bằng chiếc xe Wave Alpha. 

Nếu tôi cứ thế bỏ đi, khi Thầy Cảnh tỉnh lại hoặc đám người của Cửu Long Group tìm tới, bọn chúng vẫn có thể mang thân cọc đi nung chảy hoặc thủ tiêu dấu vết. 

Nhưng nếu tôi báo cảnh sát theo cách thông thường, thân phận của tôi sẽ lập tức bị lộ diện. Một chuyên viên kỹ thuật dữ liệu của Viện Địa tầng xuất hiện tại xưởng cơ khí lậu lúc tám giờ tối, hạ gục năm tên giang hồ bằng tay không và nắm giữ cổ vật... điều đó sẽ dẫn tới hàng loạt cuộc điều tra hành chính và thẩm vấn an ninh, phá vỡ hoàn toàn vỏ bọc bình thường mà tôi đang dày công bảo vệ.

Tôi đứng lặng giữa xưởng tôn tối om, ánh mắt lóe lên tia sáng tính toán sắc sảo của một kỹ sư trắc địa.

Đúng rồi. Tôi có một danh tính hợp pháp và một lý do hoàn toàn chính đáng!

Chiều nay, Viện trưởng Nguyễn Hoài Nam đã chính thức giao cho tôi nhiệm vụ khảo sát hiện trường sụt lún địa tầng trên đường Lò Gốm theo đề nghị của UBND Quận 6.

Và quan trọng hơn, kỹ sư Tuấn — đồng nghiệp thân thiết của tôi tại Viện Địa tầng — hiện đang trực ca đêm tại phòng trung tâm dữ liệu vi chấn thành phố, phối hợp với Ban Chỉ huy Phòng chống thiên tai và Công an kinh tế thụ lý vụ bãi phế liệu Ba Láng!

Tôi rút chiếc điện thoại thông minh cá nhân của mình ra, mở ứng dụng đo đạc trắc địa nội bộ của Viện Địa tầng.

Tôi kích hoạt tính năng gửi cảnh báo dị thường khẩn cấp, chụp ảnh định vị GPS của xưởng Vạn Phát kèm bức ảnh chụp góc nghiêng của chiếc cọc đồng cổ nằm trên giá đỡ, ghi rõ báo cáo kỹ thuật:

`"Phát hiện điểm sụt lún nghiêm trọng tại tọa độ rạch Lò Gốm do hoạt động đào bới và tàng trữ dị vật kim loại khối lượng lớn không rõ nguồn gốc trong xưởng cơ khí Vạn Phát. Hiện trường có dấu hiệu nứt toác nền đất và tranh chấp cơ học. Đề nghị Phòng dữ liệu báo cáo khẩn với Viện trưởng Nam và chuyển giao ngay cho Công an Quận 6 cùng Đội Thanh tra xây dựng phong tỏa hiện trường, thu giữ tang vật để ngăn chặn nguy cơ vỡ bờ kè rạch Lò Gốm."`

Tôi nhấn nút gửi trực tiếp vào hòm thư trực chỉ huy của Tuấn và Viện trưởng Nam.

Với uy tín dữ liệu của tôi tại Viện, chỉ trong vòng mười lăm đến hai mươi phút nữa, lực lượng liên ngành gồm Công an Phường 7, Cảnh sát cơ động Quận 6 và các chuyên gia bảo tồn di sản văn hóa sẽ có mặt tiếp quản toàn bộ xưởng Vạn Phát.

Cọc tiêu Trấn Thủy sẽ được niêm phong chính thức dưới danh nghĩa tang vật vụ án quốc gia, được lực lượng chức năng bảo vệ nghiêm ngặt tại bảo tàng hoặc kho lưu trữ chuyên dụng của thành phố. 

Cửu Long Group dù có thế lực ngập trời đến đâu cũng tuyệt đối không dám xông vào kho tang vật của cơ quan nhà nước để cướp đoạt. Hơn nữa, trận nhãn Hắc Thủy Huyền Thạch đã nằm an toàn trong balo của tôi, chiếc cọc này đối với âm mưu kích hoạt tà trận của bọn chúng đã trở thành một phế tích vô dụng!

Một mũi tên trúng ba đích: bảo vệ cọc cổ, ngăn chặn thảm họa sụt lún bờ kè, và khóa chặt cánh tay buôn lậu của Cửu Long Group mà không để lộ một chút tung tích nào về Thể Đạo của bản thân.

***

Hai mươi giờ mười lăm phút.

Từ phía đầu đường Lò Gốm, tiếng còi hụ đặc trưng của xe tuần tra cảnh sát đã bắt đầu vang lên từ xa, xé toạc màn đêm tĩnh mịch của khu phố lao động ven kênh.

Tôi đã thu dọn toàn bộ dấu vết cá nhân tại xưởng Vạn Phát. 

Thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao đã được bọc kỹ càng, nằm gọn gàng trong balo da sau lưng. 

Vận hành Quy Tức Quyết, tôi lướt nhẹ như một chiếc lá qua bức tường gạch phía sau xưởng, men theo con hẻm nhỏ ngoằn ngoèo ven mép nước để quay trở lại chỗ dựng chiếc xe máy dưới tán cây bàng cổ thụ.

Bà chủ quán nước mía lúc chiều đã dọn hàng về từ sớm, chiếc bàn nhựa và mấy cái ghế đã được xếp gọn gàng dưới mái hiên tôn.

Tôi nổ máy chiếc xe Wave Alpha. Tiếng động cơ bốn thì nổ đều đặn, giòn giã.

Đúng lúc tôi cho xe lăn bánh ra đường lớn, những hạt mưa đêm đầu tiên bắt đầu rơi lộp độp trên mặt kính chắn gió của mũ bảo hiểm.

Mưa rào tháng Mười của Sài Gòn luôn đến một cách bất ngờ và xối xả. 

Chỉ trong vòng vài phút, bầu trời đêm trên khu Chợ Lớn đã biến thành một bức màn nước trắng xóa. Những giọt mưa nặng hạt gột rửa mặt đường nhựa nóng bỏng, cuốn phai đi lớp bùn đen và mùi dầu mỡ tanh tưởi nơi bờ kênh Lò Gốm.

Tôi vít ga, cho xe hòa vào dòng người đang hối hả mặc áo mưa trên đại lộ Võ Văn Kiệt.

Hai bên bờ kênh Tàu Hủ, những ngọn đèn cao áp vàng rực nhòe đi trong làn mưa mù mịt. Nước sông cuồn cuộn dâng cao theo con nước triều rằm, nhưng nhờ luồng trọc khí tại rạch Lò Gốm đã được tôi phong tỏa kịp thời, những đợt sóng đen ngòm vỗ vào chân bờ kè bê tông đã không còn mang theo xung lực chấn động dữ dội như lúc xế chiều.

Gió sông táp vào mặt lạnh buốt, nhưng bên trong lồng ngực tôi, một dòng nhiệt lưu ấm áp từ tủy sống vẫn không ngừng luân chuyển.

Khối Hắc Thủy Huyền Thạch trong balo sau lưng dường như đang cộng hưởng với thanh Trấn Thủy Đoản Đao và chiếc trâm ngọc cổ của Lâm Tịch. Ba món cổ vật tạo thành một vòng tuần hoàn năng lượng tam giác vi diệu, liên tục gạn lọc những tạp chất còn sót lại trong khí huyết của tôi, giúp cho tầng xương cốt vốn đã vững chắc như sắt thép lại càng thêm phần dẻo dai, cô đọng.

Mười hai cọc tiêu Thủy Môn.

Bến Phú Định sẽ là chiến trường kế tiếp.

Cửu Long Group và gã phó tổng giám đốc Richard Wong chắc chắn sẽ không dừng lại sau thất bại tại xưởng Vạn Phát. Bọn chúng có tiền bạc, có công nghệ khảo sát hiện đại và có cả sự tàn nhẫn của những kẻ sẵn sàng đánh đổi sự an nguy của hàng triệu sinh mạng đô thị để mưu cầu lợi ích đen tối.

Nhưng thành phố này — dải đất nơi tôi sinh ra, lớn lên và mưu sinh mỗi ngày — không phải là nơi để bất kỳ thế lực nào muốn xới tung là có thể xới tung.

Tôi siết chặt tay ga, chiếc xe Wave lướt nhanh qua cầu Chà Và, hướng thẳng về phía Bình Thạnh trong tiếng mưa đêm gầm vang như sấm dậy."""

def run_draft():
    print(f"=== SOẠN THẢO VÀ KIỂM DUYỆT BẢN THẢO CHƯƠNG {CHAPTER_NUM} ===")
    
    # 1. Kiểm duyệt bằng CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    active_chars = ["char_minh_an", "char_lam_tich"]
    report = critique.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=active_chars,
        text=CHAPTER_PROSE
    )
    
    print("\n--- KẾT QUẢ KIỂM DUYỆT TỰ ĐỘNG (CRITIQUE ENGINE) ---")
    issues = report.get("issues", [])
    if not issues:
        print("[PASS] Không phát hiện bất kỳ vi phạm Canon, Knowledge, POV, hay Style nào!")
    else:
        print(f"[!] Phát hiện {len(issues)} vấn đề cần lưu ý:")
        has_critical = False
        for iss in issues:
            print(f"  - [{iss.get('severity')}] {iss.get('category')}: {iss.get('description')}")
            if iss.get('severity') == 'CRITICAL':
                has_critical = True
        if has_critical:
            print("[-] LỖI NGHIÊM TRỌNG! DỪNG TIẾN TRÌNH!")
            return False

    # 2. Kiểm tra từ ngữ cấm kỵ và RULE-07 (không chứa từ hậu trường sáng tác)
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing"]
    prose_lower = CHAPTER_PROSE.lower()
    found_meta = []
    for mw in meta_words:
        import re
        if re.search(rf"\b{mw}\b", prose_lower):
            found_meta.append(mw)
    if found_meta:
        print(f"[-] CẢNH BÁO RULE-07: Văn bản có chứa từ ngữ hậu trường: {found_meta}")
    else:
        print("[PASS] Đạt chuẩn RULE-07: Không phát hiện từ ngữ hậu trường sáng tác trong văn bản.")

    words = len(CHAPTER_PROSE.split())
    print(f"[+] Số từ của bản thảo: {words} từ.")

    # 3. Ghi tệp Markdown vào manuscript
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
    print(f"[+] Đã lưu bản thảo Markdown: {md_file_path}")

    # 4. Xuất bản Word .docx chuẩn in ấn
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
    print(f"[+] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 5. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 5.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Thu hồi Hắc Thủy Huyền Thạch & Giải mã Bản đồ Thập Nhị Thủy Khóa",
        CHAPTER_NUM,
        1,
        f"{DATE}T20:30:00+07:00",
        CHAPTER_NUM,
        "loc_rach_lo_gom",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An tra khảo Thầy Cảnh, thu giữ bản đồ hải đồ cổ 1898 và điện thoại chuyên dụng của Cửu Long Group. Thu hồi thành công trận nhãn Hắc Thủy Huyền Thạch, niêm phong cọc tiêu cho cơ quan chức năng tiếp quản.",
        "Xác định mục tiêu kế tiếp của Cửu Long Group là cọc tiêu số 3 tại Bến Phú Định; Minh An phối hợp kỹ sư Tuấn và Công an Quận 6 tiếp quản bảo vệ hiện trường cọc cổ an toàn."
    ))

    # 5.2 Cập nhật active thread TH-MYS-001
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An thu hồi trận nhãn Hắc Thủy Huyền Thạch tại rạch Lò Gốm, nắm giữ bản đồ Thập Nhị Thủy Khóa và xác định mục tiêu kế tiếp ở Bến Phú Định."
    ))

    conn.commit()
    conn.close()
    print("[+] Database synced: timeline_events & story_threads updated.")

    # 6. Cập nhật inventory.json (thêm Hắc Thủy Huyền Thạch)
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T21:00:00+07:00"
        
        has_item = any("Hắc Thủy Huyền Thạch" in it.get("name", "") for it in inv_data.get("core_weapons_and_artifacts", []))
        if not has_item:
            inv_data.setdefault("core_weapons_and_artifacts", []).append({
                "name": "Hắc Thủy Huyền Thạch (Trận Nhãn Thủy Môn Tiêu số 2)",
                "type": "Cổ thạch trận nhãn / Thủy linh khoáng thạch",
                "location": "Bọc túi nhung đen dưới đáy balo dã chiến",
                "condition": "Nguyên vẹn 100%, lam quang u trầm, tỏa hàn khí thanh thuần",
                "durability": "100/100",
                "function": "Trận nhãn cọc tiêu Lò Gốm; có khả năng nhiếp thủy trấn sát, tinh lọc khí huyết và phụ trợ tôi luyện tủy xương"
            })
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] state/inventory.json updated.")

    return True

if __name__ == "__main__":
    success = run_draft()
    if not success:
        sys.exit(1)

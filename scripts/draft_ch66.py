# -*- coding: utf-8 -*-
"""Full Production Pipeline for Chapter 66: Tam Giác Phong Ấn."""

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
from system.engines.knowledge_engine import KnowledgeEngine

CHAPTER_NUM = 66
CHAPTER_TITLE = "Tam Giác Phong Ấn"
LOCATION = "Viện Địa tầng Đô thị (Quận 1) & Phòng trọ Nơ Trang Long (Bình Thạnh, TP.HCM)"
DATE = "2026-10-20"

ACT1 = '''Năm giờ ba mươi phút chiều.

Cơn dông nhiệt đới quét qua bán đảo Sài Gòn đã tan biến hoàn toàn, nhường chỗ cho một buổi hoàng hôn rực rỡ hiếm thấy. Những vạt nắng chiều muộn mang sắc vàng cam ấm áp rọi xiên qua những tán cây dầu cổ thụ trên đường Lý Tự Trọng, rải những mảng sáng lung linh lên bậc thềm đá hoa cương rêu phong của Viện Địa tầng Đô thị. Sau một ngày dài căng thẳng vật lộn giữa mưa gió ngã ba sông Mũi Đèn Đỏ, không khí bên trong tòa nhà kiểu Pháp cổ kính cuối cùng cũng tìm lại được vẻ tĩnh mịch quen thuộc.

Tôi dựng chiếc xe Wave cũ vào góc sân, cởi chiếc áo khoác gió còn vương mùi nước lợ mặn mòi, bước lên cầu thang gỗ dẫn vào phòng thí nghiệm vi chấn tầng hai.

Bên trong phòng làm việc, mùi cà phê phin đậm đà quyện với mùi thơm giòn của bánh mì thịt nướng mua từ góc đường Pasteur lan tỏa khắp không gian. Viện trưởng Trịnh Hoài Nam đã cởi chiếc áo bảo hộ dã chiến lấm lem bùn đất, mặc chiếc áo sơ mi cộc tay chỉn chu, đang đích thân rót từng tách trà nóng đặt trước mặt các kỹ sư. 

Kỹ sư Tuấn ngồi tựa lưng vào chiếc ghế xoay, hai chân gác lên bục máy tính, trên tay cầm ổ bánh mì cắn dở, gương mặt lộ rõ vẻ nhẹ nhõm sau cơn bão dữ.

"Minh An vào đây ăn bánh mì uống nước đi em!" Kỹ sư Tuấn vẫy tay rối rít khi thấy tôi bước vào. "Đêm qua tới giờ quần thảo từ Bến Phú Định qua Mũi Đèn Đỏ, chắc bụng dạ em rỗng tuếch rồi!"

Tôi mỉm cười kéo ghế ngồi xuống bên cạnh anh, đón lấy ly trà ấm từ tay Viện trưởng Nam: "Cảm ơn bác, cảm ơn anh Tuấn. Tình hình bên phía Cảnh sát đường thủy và Cần Giờ thế nào rồi ạ?"

Viện trưởng Trịnh Hoài Nam nhấp một ngụm trà sen, đôi mắt sau tròng kính titan ánh lên nét nghiêm nghị pha lẫn phấn chấn:

"Đại tá Toàn bên Công an Thành phố vừa gọi điện trực tiếp thông báo cho tôi cách đây mười phút. Cuộc đột kích tại cửa biển Cần Giờ là một thắng lợi trọn vẹn. Chiếc ca nô cao tốc chở Richard Wong cùng bốn cận vệ trang bị vũ khí nóng đã bị biên đội tàu tuần tra của Hải quân và Bộ đội Biên phòng khóa chặt ngay tại phao số không luồng hàng hải Soài Rạp."

"Bắt sống được Richard Wong không bác?" Tôi hỏi, trong lòng đã biết rõ kết cục nhưng vẫn giữ đúng vai trò của một nhân viên kỹ thuật trẻ.

"Bắt sống toàn bộ, không một tên nào kịp nhảy xuống biển tẩu thoát!" Viện trưởng Nam gật đầu, giọng nói đanh thép. "Ba chiếc vali chống nước bọn chúng mang theo chứa đầy tài liệu gốc về các dự án lấn biển ma, hồ sơ chuyển tiền xuyên quốc gia trị giá hàng trăm triệu đô la, và đặc biệt là toàn bộ tập hải đồ cổ vẽ chi tiết mạng lưới thủy mạch của vùng đất Nam Bộ. Đại tá Toàn nói, Tập đoàn Cửu Long thực chất chỉ là một bức bình phong kinh tế do một tổ chức ngầm mang tên Cửu Long Thiên Hải điều hành từ nước ngoài."

"Cửu Long Thiên Hải?" Kỹ sư Tuấn tròn mắt, đặt ổ bánh mì xuống bàn.

"Đúng vậy," Viện trưởng Nam trầm ngâm giải thích. "Bọn chúng không đơn thuần chỉ muốn khai thác cát trái phép hay đầu cơ đất đai ven sông. Mục đích tối hậu của tổ chức này là tìm kiếm và kích nổ mười hai cọc tiêu phong thủy cổ xưa để làm sụp đổ toàn bộ cấu trúc địa tầng sông Sài Gòn, phục vụ cho một âm mưu trục vớt cổ vật viễn cổ dưới đáy biển Cần Giờ. Nếu hôm nay chiếc tàu `Vạn Hưng 18` khoan thủng cọc Trấn Giang Tiêu tại Mũi Đèn Đỏ, toàn bộ bờ kè Quận 7 và Nhà Bè đã bị xóa sổ trong biển nước."

Viện trưởng Trịnh Hoài Nam nhìn đồng hồ đeo tay, đặt tách trà sen xuống bàn rồi đứng dậy dặn dò:

"Bây giờ tôi phải sang Ủy ban Nhân dân Thành phố để dự cuộc họp đột xuất với Thường trực Thành ủy, báo cáo nhanh tình hình ổn định địa chất bờ kè Mũi Đèn Đỏ và phương án phối hợp rà soát toàn bộ các điểm xung yếu dọc sông Sài Gòn. Hai cậu ở lại rà soát kỹ các thông số phổ chấn từ ba trạm quan trắc tự động gửi về máy trạm, hoàn thiện báo cáo sơ bộ để sáng mai nộp cho Sở Tài nguyên và Môi trường nhé."

"Bác Nam cứ yên tâm công tác, tụi cháu kiểm tra kỹ lưỡng các đồ thị dao động rồi hoàn thành ngay trong tối nay!" Kỹ sư Tuấn quả quyết gật đầu.'''

ACT2 = '''Sau khi Viện trưởng Trịnh Hoài Nam rời phòng làm việc để tham dự cuộc họp khẩn cấp tại Ủy ban Nhân dân Thành phố, trong phòng kỹ thuật chỉ còn lại tôi và kỹ sư Tuấn.

Đồng hồ trên tường đã điểm bảy giờ tối. Phố xá trung tâm Quận 1 bên ngoài khung cửa sổ kính đã lên đèn rực rỡ, dòng người xe tấp nập ngược xuôi dưới ánh đèn vàng của những quán ăn đêm.

Kỹ sư Tuấn quay lại bàn làm việc, gõ vài dòng lệnh trên bàn phím máy trạm. Trên màn hình máy tính công suất lớn, bản đồ trắc địa số 3D của toàn bộ lưu vực sông Sài Gòn và sông Đồng Nai hiện ra với độ chi tiết đến từng mét vuông.

"Minh An, lại đây anh chỉ cho xem cái này," giọng Tuấn bỗng nhiên chùng xuống, mang vẻ kỳ bí khác thường. "Chiều nay lúc ở hiện trường Mũi Đèn Đỏ bận rộn quá, anh chưa kịp phân tích kỹ thuật toán vi sai địa chấn. Nhưng vừa rồi anh chạy thuật toán chuỗi Fourier trên số liệu thu được từ ba trạm quan trắc... thì phát hiện ra một sự thật kinh ngạc!"

Tôi bước lại gần, cúi người nhìn vào màn hình máy tính: "Sự thật gì vậy anh?"

Kỹ sư Tuấn nhấp chuột, làm nổi bật ba tọa độ địa lý trên bản đồ: điểm thứ nhất là cọc số hai rạch Lò Gốm (Quận 6), điểm thứ hai là cọc số ba ngã ba Bến Phú Định (Quận 8), và điểm thứ ba là cọc số bốn Mũi Đèn Đỏ (Quận 7).

Khi ba điểm này được nối lại bằng những đường thẳng màu lam sáng, một hình tam giác cân khổng lồ ôm trọn toàn bộ nửa phía tây nam của đô thị hiện ra rõ mồn một.

"Em nhìn xem," ngón tay Tuấn chỉ dọc theo ba cạnh của tam giác. "Sau khi ba cọc tiêu này ngừng phát xung dị thường chiều nay, toàn bộ năng lượng từ trường ngầm không hề biến mất vào hư không. Những đường sức từ ngầm dưới độ sâu ba mươi mét đang uốn cong, hội tụ chính xác về giao điểm của ba đường trung trực trong tam giác này!"

Con trỏ chuột của Tuấn rê thẳng vào tâm điểm của tam giác trên màn hình bản đồ.

Điểm hội tụ ấy nằm ngay tại một khu vực vô cùng quen thuộc ở trung tâm thành phố: **Ngã ba rạch Bến Nghé — Cầu Mống — Ba Son cổ cảng**!

"Em thấy điều quái dị chưa?" Tuấn nuốt nước bọt, hai mắt mở to nhìn tôi. "Ba cọc tiêu Lò Gốm, Phú Định và Mũi Đèn Đỏ đóng vai trò như ba chiếc kiềng ba chân vững chắc. Chúng tạo thành một thế chân vạc năng lượng để phong tỏa và khóa chặt một khối cấu trúc ngầm bí ẩn nằm ngay dưới lòng đất Quận 1 và Quận 4!"

"Khối cấu trúc ngầm ở Ba Son và Cầu Mống sao anh?" Tôi vờ kinh ngạc, nhưng trong lòng từng đợt sóng cuộn trào dữ dội.

"Chính xác!" Tuấn đập tay xuống bàn. "Theo dữ liệu quét sóng phản xạ sâu của trạm Ba Son từ năm ngoái, bên dưới độ sâu bốn mươi mét của đoạn sông Bến Nghé có một lớp đá bazan dị thường mang từ tính cực mạnh. Trước đây chúng ta cứ ngỡ đó là phế tích móng thành Gia Định xưa hoặc xưởng đóng tàu của người Pháp năm 1863. Nhưng kết hợp với đồ hình tam giác này... anh dám cá với em rằng cọc tiêu số năm và cọc tiêu số sáu chắc chắn nằm ở khu vực rạch Bến Nghé và cảng Ba Son!"

Kỹ sư Tuấn dựa lưng vào ghế, thở dài một hơi thán phục:

"Các bậc tiền nhân thời Nguyễn và những nhà phong thủy cổ xưa thật sự là những bậc thầy địa chất vĩ đại. Họ không chỉ xây dựng thành quách trên mặt đất, mà đã dùng cả mạng lưới sông ngòi tự nhiên để tạo nên một đại trận đồ trấn áp lòng đất!"

"Em nhìn kỹ vị trí Cầu Mống mà xem," Tuấn hào hứng bổ sung, ngón tay gõ nhịp trên bàn phím. "Cây cầu bằng thép đen do người Pháp xây dựng từ cuối thế kỷ mười chín bắc qua rạch Bến Nghé, thực chất lại tọa lạc ngay trên nút thắt long mạch trọng yếu cổ xưa. Sóng vi chấn phản xạ từ độ sâu bốn mươi mét dưới chân mố cầu liên tục gửi về những tín hiệu từ trường dị thường ở tần số không phẩy mười hai Hertz. Rõ ràng lòng sông Bến Nghé đang ẩn giấu một nguồn uy lực trấn áp khổng lồ chưa từng bị đánh thức."

Tôi lặng lẽ gật đầu đồng tình với anh, nhưng trong đầu tôi, những mắt xích của bức tranh toàn cảnh đang dần khép lại. 

Tập đoàn Cửu Long đã thất bại trong việc phá hủy ba cọc tiêu phương Nam. Ba trận nhãn quý giá nhất đã nằm trọn trong tay tôi. Và mục tiêu tiếp theo của cuộc hành trình Thể Đạo... chính là yết hầu trung tâm của dòng sông Bến Nghé lịch sử!'''

ACT3 = '''Tám giờ tối.

Tôi chào kỹ sư Tuấn rồi rời khỏi trụ sở Viện Địa tầng. 

Gió đêm mùa thu Sài Gòn sau cơn mưa rào mang theo hơi lạnh thanh khiết, thổi bay đi những mệt mỏi tích tụ suốt một ngày lặn lội ngoài hiện trường. Tôi nổ máy chiếc xe Wave cũ, hòa mình vào dòng xe cộ nườm nượp xuôi qua đường Nam Kỳ Khởi Nghĩa, rẽ sang đường Điện Biên Phủ rồi vượt qua cầu Thị Nghè để tiến về quận Bình Thạnh.

Đứng trên đỉnh cầu Thị Nghè trong giây lát, tôi phóng tầm mắt nhìn xuôi theo dòng kênh Nhiêu Lộc — Thị Nghè. Ánh đèn neon rực rỡ từ những tòa nhà cao tầng đôi bờ phản chiếu xuống mặt nước lăn tăn gợn sóng, tạo thành những dải lụa ngũ sắc lung linh huyền ảo. Thành phố này nơi tôi sinh ra và lớn lên, bề ngoài vẫn ồn ào, náo nhiệt và hối hả với nhịp sống mưu sinh thường nhật của hàng triệu con người. Không một ai hay biết rằng, chỉ cách đây vài giờ đồng hồ, ngay tại cửa ngõ Mũi Đèn Đỏ, một thảm họa sạt lở đê biển kinh hoàng suýt chút nữa đã nhấn chìm cả vùng đất này xuống đáy bùn lầy.

Chiếc xe máy lướt qua những con phố quen thuộc, rẽ vào con hẻm ngoằn ngoèo trên đường Nơ Trang Long.

Mùi khói than nướng thịt thơm lừng từ quán bún chả đầu ngõ quyện với mùi chè sen ấm áp của xe chè đêm ven đường. Tiếng trẻ con nô đùa ríu rít trước khoảng sân chung của khu xóm trọ, tiếng tivi phát bản tin thời sự buổi tối vọng ra từ những ô cửa sổ sáng đèn. Sự bình yên dung dị của chốn thị thành đời thường khiến tâm hồn người tu luyện Thể Đạo như tôi tìm lại được sự lắng đọng sâu xa.

Tôi dắt xe vào căn phòng trọ nhỏ chưa đầy mười lăm mét vuông, nhẹ nhàng cài then cửa sắt và vặn ngược chốt khóa đồng an toàn.

Sau khi tắm rửa bằng gáo nước mát lành để tẩy sạch lớp bùn mặn ngập mặn còn vương trên da thịt, tôi thay một bộ quần áo vải thô rộng rãi, trải tấm chiếu cói mới ra giữa nền gạch bông cũ.

Tôi cẩn thận tháo chiếc balo dã chiến chống nước, kéo khóa ngăn bí mật dưới đáy.

Dưới ánh sáng vàng nhạt của bóng đèn sợi đốt bốn mươi oát, tôi lần lượt đặt ba khối trận nhãn cùng thanh *Trấn Thủy Đoản Đao* lên mặt chiếu.

Bên trái là khối *Hắc Thủy Huyền Thạch* thu giữ từ rạch Lò Gốm, đen bóng như thiên thạch, tỏa ra làn sương mỏng lạnh ngắt trầm ổn của phù sa ngàn năm.

Bên phải là viên *Định Hải Huyền Châu* thu giữ từ Bến Phú Định, tròn trịa như quả trứng chim, bên trong cuộn trào quầng sáng xanh lam u trầm của hàn triều đáy sâu.

Và đặt trang trọng ở chính giữa... là khối *Trấn Giang Huyền Tỷ* vừa thu được chiều nay tại ngã ba Mũi Đèn Đỏ!

Khối ngọc tỷ vuông vức bằng bàn tay lấp lánh sắc hổ phách pha lam ngọc tuyệt mỹ. Hình tượng Thần Quy ngậm kiếm ngọc trên đỉnh ấn uy nghi lẫm liệt, từng đường chạm khắc sóng nước cổ kính dường như đang thở theo nhịp đập của lòng đất mẹ.

Bên cạnh ba khối bảo ngọc, thanh *Trấn Thủy Đoản Đao* bằng hắc thiết nằm trầm mặc uy nghiêm trên mặt chiếu cói. Lưỡi đao đen nhánh sắc lạnh không hề vương một vết mẻ hay rạn nứt nào sau cú va chạm sấm sét với mũi khoan hợp kim khổng lồ của chiếc tàu khai khoáng ban chiều. Khí tức trầm tĩnh của thanh đoản đao hòa cùng từ trường dịu mát của ba khối ngọc, giúp những thớ cơ bắp và kinh mạch trên toàn thân tôi nhanh chóng thư giãn, xua tan hoàn toàn cảm giác nhức mỏi sau trận kịch chiến nghẹt thở dưới đáy sâu.

Ba khối trận nhãn vừa nằm tề tựu bên cạnh nhau, không khí trong căn phòng trọ nhỏ lập tức lắng dịu lại một cách kỳ lạ. Không còn hiện tượng xung đột sát khí dữ dội như lúc chỉ có hai viên ngọc sáng nay. Ba vật phẩm tạo thành một thế chân vạc hoàn mỹ, từ trường của chúng hòa quyện vào nhau, tạo thành một quầng hào quang tam sắc mờ ảo bao phủ khắp căn phòng.'''

ACT4 = '''*"Minh An..."*

Tiếng gọi trong trẻo, êm ái như tiếng đàn cầm vang lên từ tận đáy thức hải sâu thẳm.

Trong tâm thức của tôi, đài sen ngọc bích bỗng rực sáng ngàn đạo thanh quang biếc ngọc. Lớp sương mù bao quanh đài sen tan biến hoàn toàn. Hình bóng Lâm Tịch ngồi xếp bằng trên đài sen lúc này đã ngưng tụ rõ ràng đến từng đường nét: gương mặt thanh tú không tì vết, đôi mắt phượng sâu thẳm như chứa đựng cả bầu trời sao cổ đại, tà áo trắng bồng bềnh như mây trời lướt nhẹ theo làn gió đạo. 

Sau khi hấp thu và dung hòa nguồn năng lượng thuần âm từ ba cọc tiêu đại phong ấn, thần niệm của nàng rõ ràng đã khôi phục thêm một bước dài, khí chất toát lên vẻ siêu phàm thoát tục của bậc đại năng viễn cổ.

Lâm Tịch khẽ mở mắt, ánh nhìn chăm chú hướng về ba khối trận nhãn trên mặt chiếu cói:

*"Rất tốt! Ngươi đã hoàn thành xuất sắc bước đi đầu tiên trên con đường Thể Đạo. Ba khối trận nhãn này chính là Tam Cực Trấn Thủy của phương Nam. Hãy vận chuyển kình lực Ngọc Tủy, kết nối thần thức của ngươi với ba vật phẩm theo thế Tam Tài: Thiên — Địa — Nhân!"*

Tôi không chút do dự, lập tức ngồi xếp bằng theo thế ngũ tâm triều thiên.

Tôi nhắm mắt lại, vận chuyển khẩu quyết Thức thứ bảy *Ngọc Tủy Quy Nhất*. 

Dọc theo cột sống, dòng tủy ngọc trong suốt lấp lánh như dải ngân hà bắt đầu cuộn trào mạnh mẽ. Từng tế bào xương tủy phóng thích ra luồng kình lực tinh khiết không tì vết, chia làm ba nhánh kình khí trong suốt từ các đầu ngón tay tôi bắn ra, nối liền vào ba khối bảo vật trên chiếu.

"Onggggg!"

Một tiếng ngân vang thanh thoát vang lên giữa không trung.

Ba khối bảo vật đồng thời bay bổng lên cách mặt chiếu nửa thước, xoay tròn theo chiều kim đồng hồ. Luồng hắc quang của Huyền Thạch, lam quang của Huyền Châu và hoàng kim quang của Huyền Tỷ đan xen vào nhau, phóng thẳng lên trần nhà, tạo thành một bức đồ hình tinh tú ba chiều khổng lồ trôi lơ lửng giữa căn phòng trọ nhỏ bé!

Tôi nín thở ngước nhìn lên.

Đó không phải là một bản đồ trắc địa thông thường của thời hiện đại, mà là một bức hải đồ thiên văn cổ đại tuyệt mỹ. Trên nền các vì sao lấp lánh, mười hai điểm sáng tượng trưng cho mười hai cọc Thủy Môn Tiêu đang nhấp nháy theo một trận đồ Bát Quái Cửu Cung phức tạp. Ba điểm sáng Lò Gốm, Phú Định và Mũi Đèn Đỏ đã chuyển sang màu xanh lục an toàn.

Và từ ba điểm sáng đó, ba đạo kim quang bắn thẳng về phía trung tâm, thắp sáng rực rỡ hai điểm nút tiếp theo nằm ngay giữa lòng đô thị Sài Gòn:

Điểm nút thứ năm: **Thanh Long Tả Tiêu** — tọa lạc tại ngã ba rạch Bến Nghé, dưới chân Cầu Mống lịch sử!

Điểm nút thứ sáu: **Thủy Môn Chấn Tiêu** — yết hầu phong ấn nghìn năm cắm sâu dưới đáy thủy đài cổ của xưởng đóng tàu Ba Son!

*"Minh An, ngươi có thấy cấu trúc của bức đồ hình này không?"* Giọng nói của Lâm Tịch vang lên, ngập tràn vẻ trang nghiêm cổ kính. *"Trái Đất nơi các ngươi đang sinh sống hoàn toàn không phải là một thế giới phàm trần nhỏ bé như người đời vẫn tưởng. Hàng triệu năm trước vào thời kỳ viễn cổ, nơi đây từng là **Cực Tù Lục Trọng Giới** — đại phong ấn tầng thứ sáu do chư thiên vạn giới chung tay thiết lập để giam cầm những thực thể hung hãn nhất thời hỗn mang!"*

Trái tim tôi đập mạnh dồn dập trong lồng ngực: "Giam cầm thực thể thời hỗn mang? Ý nàng là bên dưới lòng đất Sài Gòn có một bí mật cổ xưa bị phong ấn?"

*"Đúng vậy,"* Lâm Tịch khẽ gật đầu, ánh mắt xa xăm như nhìn thấu qua vạn cổ thời gian. *"Mạng lưới Thủy Môn Thập Nhị Tiêu mà tiền nhân triều Nguyễn gia cố năm 1898 thực chất chỉ là lớp then cài bên ngoài của chiếc lồng giam ấy. Khi thu thập đủ sáu cọc tiêu đầu tiên, la bàn định vị của Cực Tù sẽ hoàn toàn thức tỉnh. Và khi đó, tầng thứ tám của Đoán Cốt Thập Nhị Thức — **Hoán Huyết Hóa Cương** — mới có thể chính thức mở ra cho ngươi!"*

Bức đồ hình tinh tú trên trần nhà từ từ thu nhỏ lại rồi hóa thành một luồng ánh sáng dịu dàng, chui tọt vào sâu trong thức hải của tôi, khắc sâu từng tọa độ ngầm của Cầu Mống và Ba Son vào tâm trí.

Ba khối trận nhãn nhẹ nhàng hạ xuống mặt chiếu cói, hoàn toàn thu liễm ánh sáng, trở lại vẻ mộc mạc nguyên sơ.

Tôi mở mắt ra, thở ra một luồng trọc khí dài nửa thước giữa không trung.

Nhìn qua khe cửa sổ gỗ, ánh trăng rằm tháng Mười đã lên cao, rọi một vệt sáng bạc mát rượi xuống mặt sàn gạch bông. Tôi cẩn thận cất giữ ba khối trận nhãn vào ngăn bí mật của chiếc balo dã chiến, siết chặt quai đeo.

Một chặng đường đầy thử thách vừa khép lại trong chiến thắng oanh liệt tại Mũi Đèn Đỏ. Nhưng tôi biết rất rõ, những cơn sóng ngầm lớn hơn tại bến nước Ba Son và rạch Bến Nghé... bây giờ mới thực sự bắt đầu.'''

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

    # 3. Kiểm tra Canon Forbidden Assumptions
    ce = CanonEngine()
    canon_errors = ce.validate_text_for_forbidden_assumptions(CHAPTER_PROSE)
    if canon_errors:
        print(f"[-] Vi phạm Canon: {canon_errors}")
        return False
    print("[PASS] [2/5] Kiểm tra Canon Assumptions: Hoàn hảo 100%.")

    # 4. Thẩm định toàn diện bằng CritiqueEngine
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
    print("[PASS] [3/5] CritiqueEngine (Canon, POV, Style, Knowledge): Hoàn hảo 100%.")

    # 5. Lưu trữ bản thảo Markdown nguồn chân lý
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

    # 6. Xuất bản Word (.docx) chuẩn in ấn
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
        "Tam Giác Phong Ấn & Giải Mã Tinh Đồ Cực Tù",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:30:00+07:00",
        CHAPTER_NUM,
        "loc_no_trang_long",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_trinh_hoai_nam"]),
        "Minh An cùng kỹ sư Tuấn phân tích số liệu địa chấn tại Viện Địa tầng, phát hiện ba cọc tiêu 2-3-4 tạo thành tam giác cân khóa chặt tâm điểm Bến Nghé - Ba Son. Tối cùng ngày tại phòng trọ Nơ Trang Long, Minh An vận dụng Ngọc Tủy kích hoạt Tam Tài trận vị từ ba viên trận nhãn (Hắc Thủy Huyền Thạch, Định Hải Huyền Châu, Trấn Giang Huyền Tỷ). Lâm Tịch xuất hiện, mở ra tinh đồ cổ xưa hé lộ Trái Đất là Cực Tù Lục Trọng Giới và xác định tọa độ cọc số 5 Cầu Mống và cọc số 6 Ba Son.",
        "Giải mã thành công cấu trúc tam giác phong ấn phương Nam; kích hoạt tinh đồ định vị Cực Tù Lục Trọng Giới; xác định mục tiêu chiến lược kế tiếp tại rạch Bến Nghé và cảng cổ Ba Son."
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
        "Ba trận nhãn 2-3-4 kết hợp kích hoạt tinh đồ Cực Tù Lục Trọng Giới; mở ra tọa độ cọc tiêu số 5 Thanh Long Tả Tiêu (Cầu Mống) và cọc tiêu số 6 Thủy Môn Chấn Tiêu (Ba Son cổ cảng)."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An vận dụng Ngọc Tủy Quy Nhất kết nối Tam Tài trận vị giữa ba viên trận nhãn; Lâm Tịch hé lộ điều kiện đột phá Thức thứ 8 Hoán Huyết Hóa Cương khi mở đủ 6 cọc tiêu đầu tiên."
    ))

    conn.commit()
    conn.close()
    print("[+] Đã đồng bộ Database (timeline_events & story_threads).")

    # 8. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T22:30:00+07:00"
        inv_data["current_location"] = "Phòng trọ Nơ Trang Long (Bình Thạnh, TP.HCM)"
        
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json (vị trí phòng trọ Nơ Trang Long).")

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

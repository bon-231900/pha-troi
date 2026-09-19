# -*- coding: utf-8 -*-
"""Draft Chapter 77 for Phá Trời Novel OS with ~3,500+ words prose, zero meta-words, severe physical and tactical realism, everyday warmth, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 77
CHAPTER_TITLE = "Thạch Kiếm Chứa Chan"
DATE = "2026-10-24"
LOCATION = "Quốc Lộ 1A (Sài Gòn - Đồng Nai) & Sườn Đông Bắc Núi Chứa Chan (Xuân Lộc, Đồng Nai)"

ACT1 = '''Chín giờ sáng ngày hai mươi tư tháng mười.

Chiếc xe máy Wave Alpha màu đỏ thẫm nổ giòn giã, đưa tôi hòa vào dòng xe cộ tấp nập trên đại lộ Phạm Văn Đồng hướng về phía cửa ngõ đông bắc thành phố.

Ánh nắng ban mai của Sài Gòn đã bắt đầu gay gắt, rọi xuống mặt đường nhựa phẳng lì những vệt sáng lấp lánh như dát bạc. Tôi mặc chiếc áo khoác gió sẫm màu chống bụi, bên trong là bộ đồ rằn ri dã chiến ôm sát cơ thể rắn rỏi, chân mang đôi giày lính cao cổ có đế cao su chống trượt chuyên dụng. Chiếc ba lô dã chiến nặng gần ba mươi ký được chằng buộc chắc chắn trên yên sau bằng hai sợi dây chun bọc thép chuyên dụng.

Bên trong chiếc ba lô ấy là toàn bộ thành quả và công cụ sinh tử của tôi suốt chặng đường vừa qua: thanh Hắc Thiết Đoản Côn bọc da bò ánh chu sa, thanh Trấn Thủy Đoản Đao đồng rỉ xanh, Hắc Thủy Huyền Thạch, Định Hải Huyền Châu, Trấn Giang Huyền Tỷ và khối Tỏa Long Huyền Tỷ vừa đoạt được từ rãnh nứt Cực Tù Hải Uyên. Cùng với đó là la bàn địa chất, đèn pin tác chiến, bi-đông nước và tấm bản đồ địa hình huyện Xuân Lộc tỷ lệ một trên hai mươi lăm ngàn.

Ngồi trên xe, hai tay tôi nắm chắc ghi-đông, lưng giữ thẳng tự nhiên.

Toàn bộ ba mươi ba đốt sống lưng của tôi lúc này tựa như một trục cột bằng ngọc thạch đồng thau vững chãi. Từng ổ gà, gờ giảm tốc hay chấn động từ mặt đường truyền lên qua đôi thụt nhún giảm xóc của chiếc xe máy đều bị kình lực Luyện Cốt Hậu kỳ trong cơ thể tôi hóa giải một cách tự nhiên. Thuần Dương Cương Huyết cuộn chảy êm đềm qua từng huyết quản, mang theo luồng nhiệt ấm áp nuôi dưỡng từng thớ cơ bắp, khiến tôi không hề cảm thấy mỏi mệt dù phải giữ nguyên tư thế lái xe suốt hàng chục cây số.

Qua khỏi cầu vượt Linh Xuân, tôi rẽ vào Quốc lộ 1A, băng qua cầu Đồng Nai lộng gió để chính thức tiến vào địa phận thành phố Biên Hòa.

Dòng sông Đồng Nai cuồn cuộn phù sa đỏ đục mở ra bên dưới cầu, nối dài tầm mắt về phía hạ lưu nơi tôi vừa cùng tàu tuần tra chiến đấu đêm qua. Nhưng khi bánh xe lăn sâu hơn vào địa phận tỉnh Đồng Nai, qua khỏi ngã ba Tam Hiệp rồi tiến vào thị trấn Trảng Bom, cảnh sắc xung quanh bắt đầu thay đổi rõ rệt.

Hơi nước mặn mòi của rừng ngập mặn Cần Giờ và những con kênh rạch chằng chịt của vùng châu thổ lùi dần lại phía sau. Không khí trước mặt tôi trở nên khô ráo, thoang thoảng mùi ngai ngái nồng đượm của đất đỏ bazan và hương nhựa mủ cao su đặc trưng của miền Đông.

Hai bên Quốc lộ 1A, những cánh rừng cao su bạt ngàn thẳng tắp trải dài ngút ngàn tầm mắt. Những thân cây cao vút, vỏ xám mốc thếch, xếp thành từng hàng lối ngay ngắn như một đạo quân bất tận đứng trầm mặc dưới vòm lá xanh rì rậm rạp. Nắng trưa xuyên qua kẽ lá, rọi xuống nền đất đỏ phủ đầy lá mục những đốm sáng lung linh. Thỉnh thoảng, tôi bắt gặp những người công nhân cạo mủ cao su mặc áo xanh công nhân, đầu đội mũ có gắn đèn pin, đang thoăn thoắt đưa lưỡi dao cạo trên thân cây, hứng từng dòng nhựa trắng sữa tí tách chảy vào chiếc bát sành nhỏ.

Mười một giờ trưa.

Tôi dừng xe nghỉ chân tại một quán nước mía ven đường gần ngã ba Dầu Giây. Quán lợp mái lá đơn sơ, nép mình dưới bóng một cây xà cừ cổ thụ xum xuê cành lá.

"Cho con một ly nước mía đá nhiều tắc nhe bác!" Tôi dựng chân chống xe, tháo găng tay da rồi bước vào quán.

"Có ngay đây chú em!" Bác chủ quán trạc ngoài sáu mươi tuổi, dáng người gầy gò nhưng quắc thước, mặc chiếc áo cộc tay màu chàm đậm chất người Bắc di cư vào Nam lập nghiệp từ những năm tám mươi. Bác thoăn thoắt đưa mấy khúc mía tím bóng loáng vào máy ép, tiếng động cơ ro ro phát ra cùng mùi hương thơm ngọt ngào của nước mía quyện với vỏ tắc tươi mát lạnh bốc lên ngào ngạt.

Bác đặt ly nước mía lớn đầy ắp đá bào trước mặt tôi, nhìn chiếc ba lô dã chiến to sụ và đôi giày lính dính bụi đất đỏ của tôi, bác cười xởi lởi:

"Chú em đi phượt hay đi công trình mà đồ đạc lỉnh kỉnh thế kia? Nhìn tướng mạo rắn rỏi thế này chắc là dân trắc địa công trình hay bộ đội phục viên rồi?"

"Dạ, con làm bên khảo sát địa chất công trình bác ạ." Tôi mỉm cười nhấp một ngụm nước mía ngọt lịm mát lạnh, cảm nhận vị ngọt thanh tao xua tan cái nóng rát của chặng đường bốn mươi cây số vừa qua. "Con đang trên đường lên huyện Xuân Lộc để khảo sát mấy mỏ đá quanh khu vực núi Chứa Chan."

Nghe tôi nhắc đến núi Chứa Chan, ánh mắt bác chủ quán chợt lóe lên một nét suy tư. Bác kéo chiếc ghế nhựa ngồi xuống đối diện, hạ thấp giọng:

"Núi Chứa Chan à... Ngọn núi thiêng ấy phong cảnh hùng vĩ lắm chú em. Người ta còn gọi là núi Gia Lào, cao nhất nhì cái đất Nam Bộ này đấy. Trên núi có chùa Bửu Quang, có miếu Ba Giọt nước chảy róc rách quanh năm không bao giờ cạn, lại có cây da ba gốc một ngọn linh thiêng lắm, khách thập phương về cúng bái nườm nượp."

Bác dừng lại một chút, châm một điếu thuốc lá, nhả một làn khói mỏng vào không trung rồi nói tiếp:

"Nhưng đó là mạn sườn tây bên thị trấn Gia Ray thôi. Còn mạn sườn đông bắc thì hoang vu, hiểm trở lắm, toàn vách đá tai mèo dựng đứng với rừng le gai góc, xưa nay chẳng mấy ai dám bén mảng lên. Vậy mà dạo ba tháng gần đây, có một công ty khoáng sản tên Thiên Hải Cương gì đó trên thành phố về xin dự án cáp treo hay mở mỏ đá. Họ quây tôn, chăng dây thép gai kín mít sườn núi, thuê toàn mấy tay bặm trợn mặc áo bảo hộ đen đứng gác không cho ai lại gần."

"Họ làm rầm rộ lắm hả bác?" Tôi chăm chú hỏi, ánh mắt hơi nheo lại.

"Rầm rộ lắm!" Bác chủ quán gật đầu quả quyết. "Đêm hôm nào cũng thấy xe tải hạng nặng chở những cỗ máy cồng kềnh bọc bạt kín mít kéo lên núi. Cách đây chừng mươi bữa nửa tháng, đêm nào ở mạn Dầu Giây này cũng cảm nhận được mặt đất rung rinh khe khẽ, tiếng nổ bình bịch trầm đục như sấm rền vọng ra từ lòng núi. Dân quanh vùng đồn ầm lên là họ đang khoan nổ mìn gì đó làm động long mạch. Chú em lên khảo sát mạn đấy thì phải hết sức cẩn thận, bọn bảo vệ công trường đó dữ dằn lắm, không dễ nói chuyện đâu!"

"Dạ, con cảm ơn bác đã nhắc nhở." Tôi uống cạn ly nước mía, gửi tiền cho bác rồi mỉm cười chào từ biệt.

Bước ra khỏi quán lá, tiếng gió xào xạc thổi qua những hàng cây cao su bên đường. Giữa trưa nắng chang chang, làn gió miền Đông mang theo một cảm giác khô khốc, đanh thép khác hẳn với gió biển Cần Giờ.

*"Minh An, ngươi có nghe thấy tiếng gió không?"*

Tiếng nói của Lâm Tịch khẽ vang lên trong thức hải tôi. Nàng vẫn đang tĩnh tọa trong đài sen ngọc bích nơi sâu thẳm ý thức, nhưng luồng thần niệm thanh khiết của nàng đã lan tỏa ra thế giới bên ngoài.

"Gió rất khô, và có mùi của đá hoa cương nung dưới nắng." Tôi truyền niệm đáp lại, nổ máy chiếc xe Wave tiếp tục lăn bánh.

*"Không chỉ có thế."* Giọng Lâm Tịch mang theo một sự hoài niệm xa xăm. *"Trong ngọn gió từ hướng đông bắc thổi lại, có ẩn chứa một sợi kiếm khí sắc lạnh đến buốt tủy. Đó chính là tàn dư kiếm ý của Bạch Viên Kiếm Tôn để lại từ thời viễn cổ."*

"Kiếm ý ngàn năm mà vẫn còn tỏa ra xa đến mấy chục cây số sao?" Tôi ngạc nhiên hỏi.

*"Đó là bởi vì kiếm ý của Kiếm Tôn không phải là thứ kiếm khí hư vô do linh lực tạo thành."* Nàng giải thích tỉ mỉ. *"Bạch Viên Kiếm Tôn năm xưa là bậc kỳ tài tuyệt đỉnh theo con đường Thể Kiếm Song Tu. Ngài không dùng những chiêu thức kiếm pháp hoa mỹ xảo trá, mà lấy chính thể phách phàm nhân tôi luyện đến cực cảnh làm gốc rễ. Từng đường kiếm của ngài nặng tựa thiên cân, mượn chính sự kiên cố của đá trời để nghiền nát tà ma. Đạo kiếm ngân trên Thần Quy Thạch là kết tinh của ý chí 'Dĩ Thể Vi Kiếm'. Khi bọn tà đạo dùng máy khoan cơ giới nện vào vách núi, chúng đã vô tình đánh thức kiếm ý đang ngủ yên, khiến kiếm khí phản chấn lan tỏa khắp vùng trời non cao."*

*"Ngươi phải ghi nhớ: khi đối mặt với kiếm ý ấy, chớ có dùng bạo lực chống đối. Phải dùng sự đồng điệu của xương cốt Thể Đạo để cảm nhận và hòa nhập. Thân thể ngươi là vỏ kiếm, tâm tính ngươi là mũi kiếm. Chỉ khi nào ngươi hiểu được sự cứng cỏi của đá và sự sắc bén của kiếm, ngươi mới có thể chế ngự được cọc tiêu thứ tám."*

"Dĩ Thể Vi Kiếm... Lấy thân làm vỏ, lấy tâm làm mũi kiếm..."

Tôi lặp lại lời chỉ dạy của Lâm Tịch, ánh mắt nhìn thẳng về phía rặng núi mờ ảo đang dần hiện rõ nơi đường chân trời phía trước. Một cảm giác phấn chấn kỳ lạ dâng trào trong huyết quản, xua tan mọi mỏi mệt của chặng đường dài.'''

ACT2 = '''Một giờ mười lăm phút chiều.

Sau khi vượt qua cầu Gia Ray và trung tâm huyện Xuân Lộc, ngọn núi Chứa Chan hùng vĩ đã sừng sững hiện ra ngay trước mắt tôi.

Đó là một khối núi đơn độc khổng lồ mọc lên sừng sững giữa bình nguyên đất đỏ trù phú. Ngọn núi cao tám trăm ba mươi bảy mét, đỉnh núi hình vòng cung uốn lượn như một cánh cung khổng lồ giương lên nền trời xanh thẳm. Khác với vẻ mềm mại của những đồi chè hay rừng cao su thoai thoải bên dưới, toàn bộ sườn núi Chứa Chan được cấu tạo bởi những khối đá magma hoa cương xám tro kỷ đệ tứ khổng lồ, nhẵn bóng và trơ trọi sau hàng triệu năm phong hóa. Dưới ánh nắng gắt gỏng của buổi trưa miền Đông, những vách đá granite phản chiếu ánh sáng lấp lánh như một tấm khiên hộ thân bằng thép nguội của một vị thần khổng lồ thời tiền sử.

Theo đúng kế hoạch tác chiến, tôi không đi vào cổng khu du lịch chùa Gia Lào ở sườn tây — nơi có cáp treo và hàng ngàn bậc thang đá dành cho khách hành hương.

Tôi rẽ xe vào một con đường đất đỏ gồ ghề chạy vòng qua chân núi về phía sườn đông bắc hoang vu. Con đường mòn hẹp chỉ đủ một chiếc xe máy đi lọt, hai bên là những rẫy tiêu, rẫy điều của đồng bào dân tộc Chơro và người dân địa phương. Đất đỏ bazan bụi mù cuốn theo từng vòng bánh xe, bám đầy lên ống quần và lốc máy.

Đi chừng năm cây số, đến chân một triền dốc vắng vẻ, tôi tấp xe vào một lán trại trông rẫy điều của một hộ dân bản địa. Sau khi gửi xe và trả tiền gửi chu đáo cho chủ rẫy, tôi khoác chiếc ba lô dã chiến nặng trịch lên vai, chỉnh lại chiếc mũ lưỡi trai và chiếc kính râm trắc địa, rồi một mình rảo bước tiến sâu vào cánh rừng thưa chân núi.

Rời xa nương rẫy trần thế, không gian lập tức chìm vào sự tĩnh lặng thâm nghiêm của đại ngàn.

Khí hậu vùng núi cao lập tức phát huy sự khắc nghiệt của nó. Rừng Chứa Chan ở sườn đông bắc không phải là rừng mưa nhiệt đới rậm rạp ẩm ướt như Rừng Sác Cần Giờ, mà là kiểu rừng họ dầu lá rộng rụng theo mùa kết hợp với những trảng le gai dày đặc. Gai le nhọn hoắt như những chiếc kim thép cào sột soạt vào lớp vải rằn ri dã chiến của tôi. Dưới chân, những tảng đá hoa cương tai mèo sắc lẹm lởm chởm nhô lên giữa lớp lá khô dày cộp.

Tôi hít sâu một hơi, vận chuyển kình lực Thể Đạo Luyện Cốt Hậu kỳ xuống hai chân.

Từng khớp xương bàn chân, mắt cá và đầu gối của tôi chuyển động nhịp nhàng, êm ái tựa như những khớp lò xo hợp kim hoàn hảo. Mỗi bước chân tôi đạp lên đá tai mèo đều sử dụng tuyệt kỹ Kính Kình — triệt tiêu hoàn toàn phản lực va đập, đồng thời mượn chính độ dốc sáu mươi độ của vách đá làm điểm tựa đẩy cơ thể lao vút lên cao mà không phát ra bất kỳ một tiếng động nào.

Tốc độ leo núi của tôi nhanh đến kinh ngạc. Một phàm nhân leo núi thông thường phải mất ba đến bốn tiếng đồng hồ mới vượt qua được những vách đá tai mèo hiểm trở này, nhưng với ba mươi ba đốt sống lưng đã ngưng luyện thành khối ngọc thạch vững chãi, tôi thoăn thoắt lướt qua các khe nứt, vách đá dựng đứng chẳng khác nào một loài vượn núi cổ xưa.

Khi tôi leo lên đến độ cao bốn trăm năm mươi mét so với mực nước biển, thảm thực vật bắt đầu thưa dần, nhường chỗ cho những vách đá hoa cương sừng sững trơ trọi.

Và cũng chính tại đây, những dấu vết nhân tạo đáng ngờ bắt đầu xuất hiện.

Nấp sau một bụi cây bằng lăng cổ thụ mọc nghiêng trên vách đá, tôi rút chiếc ống nhòm trắc địa quân sự ra quan sát.

Cách vị trí tôi đứng khoảng một trăm mét về phía trên, một hàng rào thép gai razor wire sắc bén cao hơn hai mét được chăng ngang sườn núi, ngăn cách hoàn toàn khu vực sườn đông bắc hiểm trở. Cứ cách ba mươi mét lại có một camera an ninh ảnh nhiệt gắn trên thân cây rừng hoặc cột thép ngụy trang, ống kính liên tục quét qua quét lại các góc chết.

Trên những tấm biển cảnh báo bằng tôn gắn dọc hàng rào, dòng chữ màu đỏ rực đập vào mắt tôi: *KHU VỰC THI CÔNG DỰ ÁN CÁP TREO SỐ 2 — CÔNG TY TNHH THIÊN HẢI CƯƠNG — NGUY HIỂM CẤM VÀO*.

"Dự án cáp treo mà lại dùng thép gai chống xâm nhập quân sự và camera ảnh nhiệt thế này sao?" Tôi thầm cười lạnh.

Đúng lúc này, từ phía trên đỉnh dốc vẳng lại tiếng bước chân nặng nề cùng tiếng kim loại va chạm lách cách.

Hai gã bảo vệ mặc đồng phục màu xám đen của công ty Thiên Hải Cương đang chậm rãi đi tuần tra dọc hàng rào. Tôi lập tức vận chuyển Quy Tức Quyết, ghìm nhịp tim xuống mức hai mươi nhịp một phút, thu liễm toàn bộ khí huyết nóng bỏng trong cơ thể, hòa lẫn hơi thở của mình vào nhịp đập của vách đá hoa cương phía sau.

Qua lăng kính ống nhòm, tôi nhìn rõ từng chi tiết của hai kẻ tuần tra. Chúng không hề giống những nhân viên bảo vệ thông thường. Dưới lớp áo bảo hộ rộng thùng thình, cả hai đều mặc áo giáp chống đạn Kevlar quân dụng, hông đeo bao súng ngắn quân dụng và dùi cùi điện công suất cao, trên tay lăm lăm súng tiểu liên báng gấp. Bước đi của chúng vững chãi, ánh mắt đảo lia lịa đầy vẻ cảnh giác của những kẻ lính đánh thuê dạn dày sương gió.

"Mẹ kiếp, trời nắng như đổ lửa mà lão Tạ Lôi cứ bắt anh em đi tuần liên tục!" Một gã gầy còm, trên cổ có hình xăm đầu rắn hổ mang càu nhàu bằng giọng lơ lớ miền biên giới. "Bốn cỗ máy khoan khí nén nện suốt từ sáng tới giờ mà cái vách đá chết tiệt ấy vẫn không nứt ra thêm được tấc nào. Mũi khoan hợp kim vonfram thay đến bộ thứ mười rồi mà cứ chạm vào là mẻ vụn ra như đất sét!"

"Mày im mồm đi, muốn bị lão Lôi bẻ gãy xương à?" Gã to con đi bên cạnh gắt khẽ, ánh mắt lộ vẻ sợ hãi tột cùng. "Lão Lôi vừa ra lệnh rồi, nếu đến chiều nay mà máy khoan rung chấn không phá vỡ được chân móng khối Thần Quy, lão sẽ cho nổ tung cụm bộc phá C4 định hướng đã gài sẵn dưới đáy vực. Lão bảo cấp trên bên tổng bộ Cửu Long Thiên Hải đã hạ tối hậu thư, bằng mọi giá trước khi trời tối phải đánh sập cọc tiêu thứ tám để khai thông mạch ác long!"

"Nhưng nổ cả tạ thuốc nổ C4 ngay trên sườn núi dốc thế này, lỡ lở núi vùi lấp cả bọn mình thì sao?" Gã xăm cổ rụt cổ lại lo lắng.

"Lo cái gì! Hầm kỹ thuật của lão Lôi được gia cố bằng thép tấm hai mươi phân, nổ xong đoạt được bảo vật là trực thăng tới bốc đi ngay. Đi nhanh lên, kiểm tra nốt trạm cảm biến số ba rồi về báo cáo!"

Hai tên lính đánh thuê vừa nói vừa rảo bước đi khuất sau khúc quanh của hàng rào thép gai.

Tôi thu hồi ống nhòm, trong lòng cuộn trào sóng gió.

Tình thế nguy cấp hơn tôi tưởng tượng rất nhiều. Bọn chúng không chỉ dùng máy khoan rung chấn để thăm dò, mà đã chuẩn bị sẵn thuốc nổ dẻo công nghiệp C4 để sẵn sàng liều mạng đánh sập thềm đá Thần Quy!

Nếu cả tạ thuốc nổ C4 phát nổ trên sườn dốc hiểm trở này, không chỉ đạo kiếm ngân viễn cổ bị hủy hoại, mà sự sụp đổ của khối đá hoa cương hàng ngàn tấn sẽ tạo ra một trận lở đất kinh hoàng, quét sạch các bản làng dưới chân núi Chứa Chan và vùi lấp hàng vạn sinh linh vô tội.

Tôi không thể chậm trễ thêm một giây phút nào nữa.'''

ACT3 = '''Hai giờ mười lăm phút chiều.

Vận dụng tuyệt kỹ Quy Tức Quyết kết hợp với bộ pháp Thể Đạo nhẹ nhàng uyển chuyển, tôi luồn qua một góc chết của camera ảnh nhiệt nơi vách đá granite bị nứt toác, lướt qua hàng rào thép gai razor wire mà không để lại một dấu vết.

Vượt qua độ cao năm trăm năm mươi mét, tiếng ồn ào cơ giới và những nhịp rung chuyển chấn động bỗng trở nên dữ dội đến mức nghẹt thở.

*ẦM... ẦM... ẦM!*

Từng đợt sóng xung kích tần số cực thấp truyền qua lòng đá hoa cương, khiến mặt đất dưới chân tôi rung bần bật như có một đàn voi ma-mút thời tiền sử đang giẫm đạp trong lòng núi. Những mảnh đá dăm, cát bụi rào rào rơi xuống từ các vách đá dựng đứng xung quanh.

Tôi trườn người qua một khe nứt tự nhiên giữa hai khối cự thạch, leo lên một mỏm đá nhô cao quan sát toàn bộ hiện trường trung tâm ở độ cao sáu trăm mét.

Một khung cảnh ngoạn mục và bi tráng đập thẳng vào mắt tôi!

Đó chính là *Thềm Đá Cổ Thần Quy* — cọc tiêu thứ tám của Thủy Môn Thập Nhị Tiêu!

Giữa sườn vực sâu thăm thẳm của núi Chứa Chan, một phiến đá granite nguyên khối khổng lồ dài hơn bốn mươi mét, rộng gần mười lăm mét nhô hẳn ra ngoài không trung tựa như chiếc mai của một con rùa thần khổng lồ thời hồng hoang đang ngạo nghễ phục quỳ hướng về phía biển Đông. Khối đá hoa cương có màu xám bạc ánh kim loại, bề mặt phủ đầy những đường vân tự nhiên uốn lượn tựa như những phù điêu cổ xưa của trời đất.

Nhưng điều khiến tôi kinh tâm động phách nhất chính là cảnh tượng trên lưng Thần Quy Thạch:

Một vết chém sâu hoắm dài hơn ba mươi trượng, rộng chừng nửa thước, cắt ngang lưng mai rùa đá và cắm sâu vào lòng núi không thấy đáy!

Vết chém ấy phẳng lì, sắc ngọt đến mức khó tin, như thể được một bàn tay thần thánh dùng một thanh kiếm sắc bén nhất vũ trụ chém ngọt qua một tảng bơ mềm. Hàng ngàn năm mưa nắng phong hóa của kỷ đệ tứ không hề làm mòn đi nét sắc nhọn của vết chém ấy.

Đó chính là *Kiếm Ngân* viễn cổ của Bạch Viên Kiếm Tôn!

Xung quanh vết chém, không khí bị bóp méo thành những gợn sóng trong suốt mờ ảo. Đó là những luồng Vô Ngân Kiếm Khí sắc bén vô hình đang không ngừng dao động theo một quy luật huyền diệu. Bất kỳ một chiếc lá khô hay hạt cát nào bị gió cuốn rơi vào phạm vi ba thước quanh vết chém đều lập tức bị kiếm khí vô hình cắt ngọt thành từng hạt bụi mịn li ti, biến mất không dấu vết!

Lúc này, ở bốn góc chân móng của thềm đá Thần Quy, bốn cỗ máy khoan hầm khí nén bánh xích hạng nặng màu vàng cam đang gầm rú hết công suất. Những chiếc cần khoan thủy lực khổng lồ đang cố gắng đâm những mũi khoan hợp kim vonfram dài ba mét vào chân bệ đỡ của thềm đá.

Nhưng mỗi khi mũi khoan thép chạm vào lớp đá phát xuất kiếm khí, những tia lửa màu xanh lam chói lòa lập tức bùng lên kèm theo tiếng rít chói tai. Mũi khoan hợp kim vonfram siêu cứng bị kiếm khí vô hình nghiền nát, mẻ vụn ra từng mảng lớn, trong khi phiến đá hoa cương vẫn sừng sững bất động, không hề suy suyển!

"Đồ ăn hại! Một lũ vô dụng!"

Một tiếng gầm thét vang dội tựa sấm sét vang lên từ phía trước lán chỉ huy dã chiến.

Một bóng người đồ sộ bước ra mép vực.

Đó là một gã đàn ông trung niên cao gần một mét chín, thân hình vạm vỡ hộ bối lang yêu, cơ bắp cuộn tròn như những khối sắt nguội. Hắn để ngực trần, làn da toàn thân không phải màu rám nắng bình thường mà mang một sắc xám xịt ánh kim loại kỳ dị — dấu hiệu rõ ràng của kẻ tu luyện Thể Đạo biến dị theo nhánh Thiết Cốt tà môn. Từ thái dương bên trái kéo dài xuống tận quai hàm của hắn là một vết sẹo dài đỏ ửng như một con rết khổng lồ, khiến gương mặt hắn càng thêm phần hung bạo, dữ tợn.

Hắn chính là *Tạ Lôi*, biệt danh *Lôi Báo*, thủ lĩnh lính đánh thuê khét tiếng Tam Giác Vàng, kẻ chỉ huy chiến dịch phá hoại cọc tiêu thứ tám của Cửu Long Thiên Hải!

Trên tay phải của Tạ Lôi là một khẩu súng phóng lựu M79 báng cưa nòng ngắn cự ly gần, còn tay trái hắn xách một thanh đại đao bằng thép hợp kim đen nhánh nặng không dưới hai mươi ký.

Tạ Lôi sải bước tới trước cỗ máy khoan gần nhất, đạp mạnh một cú vào thân máy xích khiến cỗ máy nặng hàng chục tấn rung chuyển bần bật:

"Tắt hết mấy cái máy khoan chết tiệt này đi! Kiếm ý của lão già Bạch Viên để lại trên đá quá mạnh, công cụ cơ giới thông thường không thể phá vỡ được bệ đá!"

Tạ Lôi quay đầu lại, trừng mắt nhìn đám thuộc hạ lính đánh thuê đang run rẩy đứng xếp hàng:

"Đem toàn bộ mười sáu khối bộc phá dẻo C4 ra đây! Gài sâu vào bốn hốc nứt địa chấn dưới chân bệ đỡ thềm đá. Đấu nối kíp nổ điện vô tuyến điện tử vào máy kích nổ trên tay tao. Tao muốn xem xem, giữa kiếm ý ngàn năm của lão già chết tiệt đó với uy lực nổ định hướng của một trăm ký thuốc nổ quân dụng thời nay, cái nào cứng hơn!"

"Rõ... rõ thưa Lôi ca!" Bốn tên lính đánh thuê vội vàng khiêng hai chiếc hòm kim loại màu xanh ô-liu tiến về phía vách đá Thần Quy.

Nhìn thấy cảnh tượng đó, trong thức hải tôi, tiếng nói của Lâm Tịch bỗng vang lên dồn dập, nghiêm nghị chưa từng có:

*"Minh An! Tuyệt đối không thể để chúng kích nổ C4!"*

"Nàng hãy nói rõ đi, uy lực của kiếm ngân sẽ thế nào nếu bị kích nổ?" Tôi siết chặt nắm tay, truyền niệm hỏi dồn.

*"Kiếm Ngân trên Thần Quy Thạch là phong ấn trấn áp ác long mạch. Khi bị chấn động của chất nổ kích hoạt đến điểm bùng nổ, Vô Ngân Kiếm Khí sẽ không biến mất mà sẽ phát cuồng, bùng phát thành một cơn bão kiếm khí vô hình quét sạch toàn bộ đỉnh Chứa Chan trong bán kính ba cây số! Khi đó, chính thân thể bọn tà đạo và hàng vạn sinh linh dưới chân núi sẽ bị kiếm khí xé nát thành tro bụi, và đại ác long mạch bị giam cầm ngàn năm dưới lòng núi sẽ hoàn toàn thức tỉnh!"*

*"Cách duy nhất để cứu vãn là ngươi phải dùng Thể Đạo phàm nhân tiến vào kiếm ngân trước khi chất nổ được kích hoạt! Hãy dùng ba mươi ba đốt sống ngọc thạch đồng thau và Thuần Dương Cương Huyết của ngươi để cộng hưởng với kiếm ý viễn cổ. 'Dĩ Thể Vi Kiếm, Khí Quán Cửu Tiêu' — lấy thân ngươi làm vỏ kiếm, thu nạp và thuần phục Vô Ngân Kiếm Khí!"*

"Lấy thân làm vỏ kiếm..."

Từng lời nói của Lâm Tịch như những hồi chuông ngân vang, dội thẳng vào sâu thẳm tâm thức tôi.

Tôi cúi xuống, bàn tay nắm chặt lấy chuôi da bò của thanh Hắc Thiết Đoản Côn bên hông ba lô. Kim loại đen nhánh ánh chu sa khẽ rung lên khe khẽ, như cảm nhận được ý chí chiến đấu sục sôi của chủ nhân.

Trong lồng ngực tôi, quả tim đập mạnh mẽ, từng đợt Thuần Dương Cương Huyết sôi trào cuồn cuộn đổ dồn về ba mươi ba đốt sống lưng. Một cảm giác nóng rực và sắc bén chưa từng có bắt đầu lan tỏa khắp các khớp xương, ngón tay và từng thớ cơ bắp.

Từ phía xa trên vách đá Thần Quy, đạo kiếm ngân ngàn năm dường như cũng cảm nhận được sự hiện diện của một nguồn huyết khí Thể Đạo thuần phác đồng nguyên. Một tiếng rền rĩ trầm đục, vi vu như tiếng kiếm reo giữa trời xanh bỗng vang lên từ vết chém trên vách đá, hòa nhịp cùng nhịp tim của tôi.

Dưới vách đá, bọn lính đánh thuê đang cắm những thanh thuốc nổ dẻo C4 màu xám vào các khe nứt, dây điện kích nổ đã được đấu nối.

Tạ Lôi đứng trên mỏm đá cao, ngón tay cái đặt trên nút bấm của chiếc máy kích nổ vô tuyến, nụ cười tàn độc nở trên gương mặt đầy sẹo:

"Vĩnh biệt, ngọn núi thiêng!"

"Dừng tay lại!"

Một tiếng thét vang dội tựa sấm sét xé toạc không gian đỉnh núi!

Tôi dồn toàn bộ kình lực Luyện Cốt Hậu kỳ xuống đôi chân, búng người lao vút ra khỏi khe đá như một mũi tên xé gió. Thanh Hắc Thiết Đoản Côn vung lên, ánh chu sa đỏ sẫm quyện cùng kình lực kim thạch cuồn cuộn giáng thẳng từ trên cao xuống đầu tên tà tu Thiết Cốt Tạ Lôi!

Trận chiến sinh tử trên đỉnh non cao Chứa Chan chính thức bùng nổ!'''

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
        'char_ta_loi',
        'Tạ Lôi (Lôi Báo)',
        'character',
        json.dumps(['Lôi Báo', 'Tạ Lôi', 'Chỉ huy Thiên Hải Cương'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'role': 'Chỉ huy chi nhánh nội địa Cửu Long Thiên Hải tại Núi Chứa Chan', 'cultivation': 'Thể Đạo biến dị Thiết Cốt tà môn', 'origin': 'Cựu thủ lĩnh lính đánh thuê Tam Giác Vàng'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'loc_them_da_than_quy',
        'Thềm Đá Cổ Thần Quy',
        'location',
        json.dumps(['Thần Quy Thạch', 'Thềm Đá Thần Quy', 'Cọc Tiêu Thứ Tám'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'elevation': '600m', 'significance': 'Cọc tiêu thứ tám Thủy Môn Thập Nhị Tiêu, nơi lưu giữ Kiếm Ngân của Bạch Viên Kiếm Tôn'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'faction_thien_hai_cuong',
        'Công ty TNHH Thiên Hải Cương',
        'faction',
        json.dumps(['Thiên Hải Cương', 'Công ty Khoáng sản Thiên Hải Cương'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'role': 'Vỏ bọc nội địa của Tập đoàn Cửu Long Thiên Hải tại Đồng Nai', 'leader': 'char_ta_loi'}, ensure_ascii=False)
    ))

    conn.commit()
    conn.close()

    # 4. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich", "char_ta_loi"],
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
        "Độc Hành Đông Bắc, Thâm Nhập Núi Chứa Chan & Khởi Động Huyết Chiến Thần Quy Thạch",
        CHAPTER_NUM,
        1,
        f"{DATE}T14:15:00+07:00",
        CHAPTER_NUM,
        "loc_them_da_than_quy",
        json.dumps(["char_minh_an", "char_lam_tich", "char_ta_loi"]),
        "Minh An xuất phát từ Sài Gòn trên xe Wave Alpha theo Quốc lộ 1A tiến vào Đồng Nai, băng qua những cánh rừng cao su bạt ngàn của đất đỏ miền Đông. Nghỉ chân tại ngã ba Dầu Giây, lắng nghe bác chủ quán nước mía chia sẻ về những dị động cơ giới và rung chấn bất thường tại sườn đông bắc Núi Chứa Chan. Lâm Tịch truyền thụ về bản chất Thể Kiếm Song Tu của Bạch Viên Kiếm Tôn. Đến chân núi Chứa Chan, Minh An gửi xe và luồn rừng vượt vách đá granite hiểm trở, vượt qua hàng rào thép gai và camera ảnh nhiệt của công ty bình phong Thiên Hải Cương. Tại Thềm Đá Cổ Thần Quy độ cao 600m, Minh An chứng kiến vết Kiếm Ngân viễn cổ kháng cự máy khoan khí nén. Tạ Lôi chuẩn bị kích nổ cụm bộc phá C4 định hướng nhằm đánh sập thềm đá. Minh An vung Hắc Thiết Đoản Côn xuất kích chặn đứng âm mưu.",
        "Xâm nhập thành công sườn đông bắc Núi Chứa Chan; chứng kiến uy lực Kiếm Ngân viễn cổ; ngăn chặn kịp thời vụ nổ C4; bùng nổ chiến đấu trực diện với Tạ Lôi."
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
        "Minh An độc hành đến Núi Chứa Chan (Đồng Nai), thâm nhập Thềm Đá Cổ Thần Quy và đối đầu với toán tà tu do Tạ Lôi chỉ huy."
    ))

    # 7.3 Cập nhật story thread TH-PLT-002 (Tiến Trình Tu Luyện Khí Huyết & Thể Đạo của Minh An)
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An ứng dụng Luyện Cốt Hậu kỳ và Kính Kình leo vách đá granite Chứa Chan; bắt đầu tiếp xúc và cộng hưởng với kiếm ý Dĩ Thể Vi Kiếm của Bạch Viên Kiếm Tôn."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T14:15:00+07:00"
        inv_data["current_location"] = "Thềm Đá Cổ Thần Quy, Núi Chứa Chan, Huyện Xuân Lộc, Tỉnh Đồng Nai"
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

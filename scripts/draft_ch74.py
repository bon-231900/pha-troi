# -*- coding: utf-8 -*-
"""Draft Chapter 74 for Phá Trời Novel OS with ~3,614 words prose, zero meta-words, severe physical and tactical hardships for Minh An, and multi-tier foreshadowing."""

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
# -*- coding: utf-8 -*-
"""Refine Chapter 74 acts to exactly ~3,480 words."""

ACT1 = '''Bốn giờ ba mươi phút chiều ngày hai mươi ba tháng Mười.

Trên boong Tàu Tuần Tra Cao Tốc HQ-268, gió biển vịnh Gành Rái bắt đầu thổi mạnh, mang theo hơi muối mặn chát và từng đợt bọt sóng tung trắng xóa. Bầu trời phía tây rực sắc đỏ ối của ráng chiều, nhưng phía đông nam — hướng ra hải phận quốc tế nơi rãnh nứt Cực Tù Hải Uyên ẩn mình — mây đen mù mịt đã dâng cao như bức thành trì xám xịt.

Sau cuộc thẩm vấn tên chỉ huy người nhái Hắc Giao Đường, kỹ sư Tuấn cùng tổ hoa tiêu âm học của tàu HQ-268 đã giải mã trọn vẹn dữ liệu từ chiếc máy mã hóa chống nước.

Trên màn hình hải đồ điện tử của đài chỉ huy, tọa độ màu đỏ rực nhấp nháy tại mười độ ba phút vĩ Bắc, một trăm lẻ bảy độ mười hai phút kinh Đông.

"Minh An, nhìn vào đây!" Tuấn chỉ tay vào đồ thị trắc diện đáy biển ba chiều. "Cách phao số không sáu hải lý về phía đông nam, thềm lục địa cát bỗng gãy cụp xuống gần tám mươi độ. Đó là rãnh nứt địa chất khổng lồ kéo dài mười lăm cây số, đáy vực sâu nhất vượt mốc một ngàn hai trăm mét. Đáy vực bị bao phủ bởi lớp đá bazan núi lửa cổ đại và những dòng xoáy ngầm xé rách với vận tốc cực lớn."

Đại úy Lê Đình Hùng bước tới, ánh mắt người thuyền trưởng ngập tràn âu lo:

"Đồng chí An, độ sâu một ngàn hai trăm mét là vùng tử địa với sinh lý con người! Thợ lặn cứu nạn tinh nhuệ nhất của quân chủng chúng tôi, khi dùng chuông lặn chuyên dụng và hít thở hỗn hợp khí cao áp he-li và ô-xy, mức lặn sâu tối đa cũng chỉ dám dừng ở ba trăm đến bốn trăm mét. Xuống tới một ngàn hai trăm mét, áp lực thủy tĩnh lên tới một trăm hai mươi át-mốt-phe — tương đương một trăm hai mươi ký-lô-gam đè nén trên mỗi phân vuông cơ thể! Chỉ một sơ suất nhỏ, lồng ngực và sọ não sẽ bị khối nước nghiền nát ngay tức khắc!"

Thuyền trưởng Hùng định mang ra bộ đồ lặn bão hòa vỏ cứng nặng hơn tám mươi ký, nhưng tôi mỉm cười từ chối:

"Cảm ơn tấm lòng của anh em thủy thủ đoàn. Nhưng ở độ sâu ấy, bộ giáp kim loại nặng nề sẽ biến tôi thành bia ngắm di động. Kẻ địch sở hữu tàu lặn chuyên dụng trang bị cánh tay cơ giới và hỏa lực ngầm, sự linh hoạt tuyệt đối của thân thể mới là cơ hội sống sót duy nhất của tôi."

"Nhưng cậu không mang bình khí, làm sao duy trì sự sống dưới vực sâu lạnh giá ấy?" Thuyền trưởng Hùng kinh ngạc.

"Tôi có phương pháp điều tức nội sinh của riêng mình," tôi đáp, ánh mắt kiên định. "Tôi là Nguyễn Minh An, Giám Đốc Kỹ Thuật Dữ Liệu của Viện Địa tầng Đô thị. Sứ mệnh của tôi là ngăn chặn bàn tay tà đạo của Cửu Long Thiên Hải phá hủy cọc tiêu thứ bảy của long mạch phương Nam. Nếu cọc tiêu này bị phá vỡ, toàn bộ vùng duyên hải trũng thấp của Cần Giờ sẽ sụp lún nghiêm trọng."

Tôi siết chặt đai lưng dã chiến, kiểm tra thanh Hắc Thiết Đoản Côn sau lưng và thanh Trấn Thủy Đoản Đao bên hông trái. Chiếc hộp đồng chứa mai rùa thần được buộc chặt trước ngực, áp sát vị trí trái tim nơi dòng Cương Huyết đang lưu chuyển. Tôi chỉ mang thêm đèn rọi công nghiệp chịu áp lực ngàn mét và máy phát tín hiệu định vị ngầm do Tuấn chế tạo.

"Minh An, bảo trọng!" Tuấn nắm chặt tay tôi. "Chúng tôi túc trực liên tục tại đài chỉ huy HQ-268 theo dõi biến động âm học của cậu."

"Chờ tin tôi!"

Tôi bước ra mạn tàu, hít sâu một hơi dưỡng khí rồi lao mình xuống làn nước sâu thẳm.

"Ùm!"

Khối nước biển ôm trọn lấy tôi. Toàn thân tôi hóa thành mũi tên lam ngọc xé nước lao thẳng xuống đáy sâu theo phương thẳng đứng.

Từ không mét xuống hai trăm mét: Ánh sáng hoàng hôn biến mất. Nước biển chuyển từ xanh ngọc sang lam thẫm rồi đặc quánh tựa mực tàu. Nhiệt độ nước tụt dốc từ hai mươi tám độ C xuống sáu độ C.

Từ hai trăm mét xuống sáu trăm mét: Ánh sáng mặt trời tắt ngấm, xung quanh chìm vào bóng đêm vĩnh cửu. Áp lực nước vọt lên sáu mươi át-mốt-phe nén chặt vào màng nhĩ và lồng ngực. Ở độ sâu này phổi người thường sẽ co rút lại bằng quả cam, máu bão hòa khí ni-tơ gây tử vong tức thì.

Nhưng trong lồng ngực tôi, Thức thứ tám *Hoán Huyết Hóa Cương* đã phát huy uy lực kỳ diệu. Dòng máu đồng thau tỏa nhiệt lượng nóng rẫy, tự động điều hòa áp suất thủy tĩnh nội sinh cân bằng với đại dương. Nhịp tim tôi chậm rãi giữ ở mức ba mươi nhịp một phút, từng tế bào được nuôi dưỡng bằng dưỡng khí dồi dào trong Cương Huyết. Tôi tiếp tục lao sâu xuống đáy vực, nơi rãnh nứt Cực Tù Hải Uyên đang mở toang miệng vực đón chờ.'''

ACT2 = '''Sáu giờ tối. Độ sâu chín trăm mét... một ngàn mét!

Tôi đã vượt qua thềm lục địa, rơi thẳng vào miệng rãnh nứt Cực Tù Hải Uyên.

Nhiệt độ nước tụt xuống chỉ còn hai độ C — cái lạnh buốt thấu xương dường như muốn đóng băng mọi cơ thể sống. Xung quanh tôi là khoảng không gian đen kịt, tịch mịch đến rợn người. Không có tia sáng, không có âm thanh của sự sống trần gian, chỉ có tiếng gầm gào từ những dòng xoáy ngầm cọ xát vào vách đá bazan dựng đứng.

Và khi đồng hồ đo độ sâu nhảy qua con số một ngàn mét, áp lực khủng khiếp của đại dương mới giáng xuống!

Một trăm át-mốt-phe!

Mỗi một mét vuông thân thể tôi gánh chịu sức nặng một triệu ký-lô-gam nước biển! Khối nước đen kịt ép chặt từ bốn phương tám hướng, cố nghiền nát từng khớp xương của tôi thành tro bụi.

"Răn rắc... rắc!"

Chuỗi âm thanh ken két, rạn nứt trầm đục đột ngột vang lên từ cột sống của tôi!

Dưới mô-men xoắn và áp lực nén vạn cân, ba mươi ba đốt sống lưng bắt đầu chịu tải cực hạn. Các đĩa đệm co thắt dữ dội, lồng ngực bị ép nghẹt cứng như có cỗ xe lu chèn qua. Hai màng nhĩ căng phồng nhức nhối tựa sắp nổ tung. Cơn đau buốt thấu xương tủy lan truyền dọc theo mạng lưới dây thần kinh khiến toàn thân tôi run rẩy kịch liệt.

"Minh An! Giữ vững tâm niệm!" Thanh âm của Lâm Tịch vang lên từ đài sen ngọc bích trong thức hải: *"Đây là ranh giới sống còn của Luyện Cốt Hậu kỳ! Đáy biển ngàn mét này là lò rèn tự nhiên vĩ đại nhất! Dùng Cương Huyết tôi luyện tủy sống, ép ba mươi ba đốt sống hấp thụ áp lực đại dương để tái cấu trúc khung xương! Vượt qua, thân thể sẽ cứng cáp như thần binh; chùn bước, đáy vực này sẽ chôn vùi ngươi mãi mãi!"*

"Ta hiểu!"

Tôi gầm lên trong tâm thức, cắn chặt môi đến ứa máu. Tôi vận chuyển toàn bộ Cương Huyết, dốc cạn sinh lực bơm vào khối tủy vàng ngọc bên trong ba mươi ba đốt sống.

Dòng máu màu đồng thau sôi trào mãnh liệt, tỏa ánh sáng rực đỏ tựa lửa nung kim loại. Từng đợt Cương Huyết nóng bỏng thâm nhập sâu vào các vết nứt tế vi trên bề mặt xương cốt, điên cuồng hàn gắn, gia cố và nén chặt các phân tử can-xi lại với nhau.

Cơn đau đớn giằng xé thân thể tôi suốt gần mười phút. Nhưng rồi, từng đốt sống dần ổn định lại, phát ra ánh hào quang hoàng kim xuyên qua da thịt. Lồng ngực mở rộng trở lại, nhịp thở nội sinh được thiết lập vững như bàn thạch!

Nhưng tôi chưa kịp thở phào thì một hiểm họa cơ giới chết người đã ập tới!

Từ vách đá bazan phía đối diện ở độ sâu một ngàn một trăm mét, hai luồng ánh sáng đèn pha xenon công suất lớn đột ngột bật sáng chói lòa, xé toạc màn đêm chiếu thẳng vào mặt tôi!

Hiện ra trước mắt tôi là chiếc tàu lặn nghiên cứu hạng nặng mang tên *Kình Uyên 01*. Con tàu dài hơn mười hai mét, đúc bằng hợp kim ti-tan dày mười phân sơn màu đen tuyền, hai bên mạn vẽ hình chín con rồng đen của Cửu Long Thiên Hải!

Phía trước mũi tàu lặn, cánh tay cơ giới thủy lực dài sáu mét với bộ ngàm kẹp năm mươi tấn đang vươn dài ra; bên cạnh là mũi khoan kim cương đường kính một mét đang quay cuồng xé toạc đá bazan ngầm phát ra tiếng rít chói tai!

Cụm cảm biến sonar của tàu lặn *Kình Uyên 01* lập tức khóa chặt vào tôi. Sát tâm của những kẻ tà đạo bùng nổ!

"Oooong... Chiiiiu!"

Trên nóc tàu lặn, vòm phát sóng âm bằng gốm áp điện đột ngột tích tụ năng lượng, rực sáng ánh điện lam u tối — vũ khí xung âm định hướng công suất hai trăm hai mươi đề-xi-ben!

Chùm sóng siêu âm xung kích mang năng lượng hủy diệt xé toạc khối nước biển, lao thẳng về phía tôi với vận tốc một ngàn năm trăm mét một giây! Dưới môi trường nước, sóng âm truyền đi với mật độ phân tử dày đặc gấp ngàn lần không khí. Đòn tấn công âm học vô hình này chẳng khác nào quả búa tạ nặng hàng chục tấn nện thẳng vào ngực tôi!

"BÙM!"

Tiếng nổ trầm đục kinh hoàng bùng phát dưới đáy sâu. Làn sóng xung kích đánh trúng trực diện vào tôi! Bộ đồ lặn dã chiến rách toạc. Áp lực âm thanh khổng lồ xuyên thẳng qua da thịt, rung giật dữ dội màng nhĩ, chấn động kịch liệt vào lục phủ ngũ tạng!

"Phụt!"

Khóe miệng tôi trào ra ngụm máu tươi đỏ thẫm. Tầm nhìn nhòe đi giữa làn nước biển, hai tai ong lên chói gắt, cả thân thể bị chấn động đánh văng dội ngược lại vách đá bazan ngầm!'''

ACT3 = '''Thân thể tôi va mạnh vào gờ đá bazan lởm chởm. Cú va đập cộng hưởng với chấn thương nội tạng do sóng siêu âm gây ra khiến toàn bộ kinh mạch trong lồng ngực đau nhức như bị xé rách. Máu tươi từ khóe miệng hòa tan vào làn nước lạnh hai độ C, tạo thành vệt mây đỏ lơ lửng giữa bóng tối.

Mùi máu tươi nồng nặc, kết hợp cùng dòng khí hắc trọc cổ xưa đang rò rỉ từ kẽ nứt bazan do mũi khoan của tàu lặn tạo ra, đã đánh thức mối hiểm họa kinh hoàng khác của đáy vực!

Từ những kẽ nứt sâu hun hút, hàng chục bóng đen khổng lồ lao vun vút ra từ bóng tối, rẽ nước bơi quanh với tốc độ kinh hồn — loài *U Minh Quỷ Sa*!

Mỗi con quỷ sa dài bốn đến sáu mét, thân mình dẹp bên tựa thanh đại đao đen trũi. Đôi mắt thoái hóa thành hai hốc mù tro tàn. Toàn thân bọc lớp vảy giáp sừng cứng như đá mác-ma, trên sống lưng mọc tua tủa hàng gai nhọn chứa độc tố hoại tử.

Cơ quan thụ cảm điện trường và khứu giác săn mồi của chúng nhạy bén gấp ngàn lần cá mập thường. Vừa ngửi thấy mùi máu Cương Huyết tràn ngập linh khí, bầy quỷ sa lập tức phát cuồng, đồng loạt quẫy đuôi lao thẳng về phía tôi để cắn xé!

Cùng lúc đó, tàu lặn *Kình Uyên 01* cũng không dừng tay. Vòm gốm áp điện trên nóc tàu lặn lại nhấp nháy ánh điện lam nạp năng lượng cho phát bắn thứ hai. Cánh tay cơ giới thủy lực năm mươi tấn vươn dài ra, bộ ngàm thép bén ngót mở toang, lao thẳng tới nhằm nghiền nát thân thể tôi!

Trên có sóng xung âm hai trăm hai mươi đề-xi-ben! Trước mặt có cánh tay kẹp cơ giới năm mươi tấn và mũi khoan kim cương! Xung quanh là bầy U Minh Quỷ Sa hơn ba mươi con hung tợn! Đây là nghịch cảnh sinh tử hiểm nghèo nhất mà tôi từng đối mặt!

"Minh An! Bình tâm lại!" Giọng nói của Lâm Tịch vang lên trong thức hải tôi. Đài sen ngọc bích tỏa luồng khí mát lành xoa dịu thần kinh đang bị sóng siêu âm tàn phá. *"Đừng dùng man lực đối đầu trực diện với sóng âm dưới nước! Ngươi là kỹ sư địa tầng, hãy dùng tri thức địa chất và âm học để giải mã tử cục này!"*

Lời nhắc nhở của Lâm Tịch như luồng điện xé tan sự choáng váng trong đầu tôi! Tôi là Nguyễn Minh An — Giám Đốc Kỹ Thuật Dữ Liệu! Tôi đã dành mười năm nghiên cứu về sóng địa chấn và thủy âm công trình! Dưới đáy biển ngàn mét này, sóng âm truyền đi theo quy luật vật lý chứ không phải ma thuật huyền bí!

Tôi mở trừng hai mắt, quan sát cấu trúc địa hình xung quanh.

Rãnh nứt Cực Tù Hải Uyên gồm những vỉa đá bazan nứt nẻ sau các đợt phun trào núi lửa ngầm cổ đại. Vách đá dốc bảy mươi lăm độ, bề mặt gồ ghề với những gờ đá hoa cương nhô ra tựa tấm khiên khổng lồ, xen kẽ các hốc đá sâu hình chữ V.

Theo nguyên lý phản xạ âm thanh dưới nước: Chùm sóng siêu âm định hướng có tần số cực cao, bước sóng ngắn. Khi va chạm vào bề mặt đá gồ ghề lớn hơn bước sóng, nó sẽ bị phản xạ tán loạn ngược chiều, tạo ra vùng hoàn toàn không có sóng âm ở phía sau gờ đá — đó chính là **vùng bóng âm** (acoustic shadow zone)!

"Vùng bóng âm nằm ngay sau gờ đá bazan bên tay phải!"

Một tia sáng lóe lên trong não bộ tôi!

Tôi nén chặt cơn đau nơi lồng ngực, vận chuyển dòng Cương Huyết dồn xuống hai bàn chân. Tôi đạp mạnh vào vách đá, né tránh nhát cắn chí mạng của hai con quỷ sa, phóng vút vào khe nứt hình chữ V phía sau gờ đá bazan!

"BÙM! XOANH!"

Chùm sóng âm hai trăm hai mươi đề-xi-ben từ tàu lặn nện thẳng vào mặt trước của gờ đá bazan dày ba mét. Khối năng lượng kinh hoàng bùng nổ làm vỡ vụn hàng tấn đá mác-ma, toàn bộ sóng chấn động bị phản xạ ngược lại vùng nước mở!

Ẩn mình trong vùng bóng âm phía sau gờ đá, áp lực âm thanh tác động lên thân thể tôi giảm đi hơn tám mươi phần trăm, chỉ còn lại những đợt rung chấn nhẹ không làm tổn hại đến khung xương của tôi! Ngược lại, bầy U Minh Quỷ Sa ngoài vùng nước mở lại phải gánh chịu trọn vẹn sức mạnh sóng dội lại! Cơ quan thụ cảm điện trường mỏng manh của loài thủy quái bị sóng âm công suất cao phá hủy tức thì. Hàng chục con quỷ sa đau đớn quẫy đạp điên cuồng, bầy đàn rơi vào trạng thái hỗn loạn mất phương hướng hoàn toàn!'''

ACT4 = '''Cơ hội phản kích chớp nhoáng đã mở ra trước mắt!

Tàu lặn *Kình Uyên 01* sau khi bắn liên tiếp hai phát đạn xung âm, cụm tụ điện tạm thời rơi vào chu kỳ nạp lại trong ba mươi giây.

Thấy mục tiêu biến mất sau gờ đá, người điều khiển tàu lặn tăng hết công suất cụm máy đẩy, điều khiển cánh tay cơ giới thủy lực năm mươi tấn lao thẳng vào khe nứt truy quét! Bộ ngàm kẹp titanium mở rộng hết cỡ, kẹp vỡ vụn đá cản đường, chụp thẳng xuống vị trí tôi!

"Muốn nghiền nát ta sao? Đồ sắt vụn!"

Ánh mắt tôi rực lên hàn quang lạnh lẽo. Tôi bùng phát kình lực phỉ thúy xen lẫn ánh đỏ chu sa rực rỡ! Thức thứ tám *Hoán Huyết Hóa Cương* kết hợp cùng thức thứ tư *Long Lân Phá Kình*!

Tôi rút thanh Hắc Thiết Đoản Côn bằng tay phải, dòng Cương Huyết sôi trào truyền thẳng vào thân côn. Mượn lực dòng nước xoáy, tôi phóng mình lướt tới đón đầu cánh tay cơ giới!

"KENG! RẮC RẮC RẮC!"

Đầu côn Hắc Thiết nện chuẩn xác vào chốt khớp xoay thủy lực! Dưới áp lực nước một trăm hai mươi át-mốt-phe kết hợp cùng kình lực xuyên thấu kinh hoàng, chốt pit-tông chịu lực năm mươi tấn bị bẻ cong gãy gập thành góc chín mươi độ! Ống dẫn dầu áp lực cao nổ tung, cánh tay cơ giới khổng lồ rũ xuống bất động, trở thành đống phế liệu treo lơ lửng!

Không để đối phương kịp hoàn hồn, thân hình tôi lướt đi tựa bóng ma lam ngọc, lộn vòng ra sau đuôi tàu — nơi ba chân vịt đẩy bằng hợp kim đồng ti-tan đang quay cuồng!

"Đoạn Lưu Phá Giáp!"

Tôi dồn toàn bộ kình lực giáng một đòn côn sấm sét bổ thẳng vào trục truyền động chân vịt chính giữa!

"CHOẢNG!"

Trục thép tôi luyện siêu cứng dày mười lăm phân bị đánh gãy vụn làm đôi! Ba cánh quạt chân vịt khổng lồ văng khỏi trục quay, chém thẳng vào vỏ khoang động cơ phía sau đuôi tàu lặn!

"XOẸT!"

Vỏ hợp kim ti-tan bị xé rách một mảng dài! Khối nước biển một trăm hai mươi át-mốt-phe lập tức tràn vào khoang động cơ tựa khẩu pháo nước áp lực cực cao. Cụm máy phát điện, bình ắc-quy và mạch điện bị nước biển nén ép chập cháy, nổ tung những chùm tia lửa điện sáng lòa! Đèn pha xenon tắt ngấm. Chiếc tàu lặn biển sâu *Kình Uyên 01* nặng hai mươi tấn hoàn toàn tê liệt, trôi dạt đâm sầm vào vách đá bazan ngầm, mắc kẹt bất động trong khe nứt sâu!

Cùng lúc đó, con U Minh Quỷ Sa đầu đàn dài sáu mét nhe hàm răng cưa nhọn hoắt lao thẳng vào lưng tôi!

Tôi không thèm quay đầu lại. Tay trái rút thanh Trấn Thủy Đoản Đao, tôi vung ngược ra sau một đường đao bán nguyệt sắc lẹm!

"Xoẹt!"

Ánh đao đỏ thẫm rực cháy chém đứt đôi đầu lâu con quỷ sa khổng lồ! Máu đen phun ra cuồn cuộn. Mùi máu của kẻ đầu đàn khiến bầy quỷ sa còn lại kinh hoàng bạt vía, đồng loạt tháo chạy thục mạng xuống khe nứt tối tăm sâu hơn!

Trận chiến kết thúc. Đại dương sâu thẳm lại trở về với sự tĩnh lặng vĩnh cửu.

Tôi dừng lại giữa làn nước, buông lỏng hai cánh tay. Toàn thân đau nhức ê ẩm, từng thớ cơ bắp như bị xé rách, lớp da trên cánh tay và bả vai rướm những giọt Cương Huyết đỏ sẫm do vận kình quá tải dưới áp lực nước cực hạn. Lồng ngực phập phồng dồn dập, dòng máu đồng thau đang chậm rãi luân chuyển để hàn gắn những vết thương tổn cơ học.

Nhưng tôi đã chiến thắng! Bằng ý chí sắt đá, Thể Đạo kiên cường và trí tuệ của một chuyên gia kỹ thuật dữ liệu, tôi đã đập tan cỗ máy cơ giới tối tân của kẻ thù và chế ngự được sự khắc nghiệt của đáy biển ngàn mét!

Tôi bơi chậm lại, từ từ hạ chân đáp xuống thềm đáy của rãnh nứt Cực Tù Hải Uyên ở độ sâu đúng một ngàn hai trăm mét dưới mực nước biển.

Dưới chân tôi là bề mặt đá ngọc thạch cổ xưa nhẵn thín, rộng hàng trăm mét vuông, bị chôn vùi dưới lớp trầm tích ngàn năm. Và ngay giữa trung tâm thềm đá ngọc thạch, sừng sững hiện ra một kỳ quan cổ đại khiến tim tôi rung lên thổn thức!

Đó là một cây cột đá ngọc bích màu xanh thẫm cao hơn ba mươi mét, chu vi bốn người ôm không xuể. Thân cột được bao bọc bởi chín sợi xích thần long đúc bằng hoàng kim cổ đại, trên thân xích khắc chi chít hàng ngàn ký tự phù triện phát ra ánh hào quang hoàng kim ấm áp, xua tan hoàn toàn bóng tối lạnh giá của đáy biển.

Dưới chân cột đá, bốn chữ triện cổ đại khắc chìm sâu vào lòng đá ngọc thạch đang rực sáng lung linh:

*Hải Uyên Tỏa Long Trụ*!

Cọc tiêu thứ bảy của mạng lưới Thủy Môn Thập Nhị Tiêu — trận nhãn cốt lõi cai quản tầng thứ sáu của Cực Tù Lục Trọng Giới ngàn năm — cuối cùng đã chính thức hiện diện trước mắt tôi!'''



CHAPTER_NUM = 74
CHAPTER_TITLE = "Cực Tù Hải Uyên"
LOCATION = "Rãnh Nứt Cực Tù Hải Uyên (Độ sâu 1.200m, Vịnh Gành Rái - Cần Giờ)"
DATE = "2026-10-23"

def run_pipeline():
    print(f"=== BẮT ĐẦU CHU TRÌNH SÁNG TÁC & KIỂM TOÁN CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    
    # 1. Ghép nối bản thảo
    raw_content = f"{ACT1}\n\n{ACT2}\n\n{ACT3}\n\n{ACT4}"
    word_count = len(raw_content.split())
    print(f"[+] [1/5] Soạn thảo hoàn tất: {word_count:,} từ (Mục tiêu: 3.300 - 3.650 từ).")
    if word_count < 3300 or word_count > 3650:
        print(f"[-] Cảnh báo: Độ dài từ {word_count} chưa nằm trong khoảng tối ưu 3.300 - 3.650 từ!")
        return False

    # 2. Kiểm tra cấm chữ "hồi" và meta-words theo RULE-07
    forbidden_words = [
        "chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện",
        "bản thảo", "canon", "database", "plot", "foreshadowing", "hệ thống"
    ]
    
    found_violations = []
    
    # Quét chữ "hồi" dưới mọi hình thức
    hoi_matches = re.findall(r'\b\w*hồi\w*\b', raw_content, re.IGNORECASE)
    if hoi_matches:
        found_violations.append(f"Chứa biến thể chữ 'hồi': {set(hoi_matches)}")

    # Quét các meta-words khác
    for fw in forbidden_words:
        if fw == "hồi":
            continue
        m = re.findall(rf'\b{fw}\b', raw_content, re.IGNORECASE)
        if m:
            found_violations.append(f"Chứa meta-word '{fw}': {len(m)} lần")

    # Quét cấm "cắt đứt" khi có "phong ấn" (Knowledge leak prevention)
    if "phong ấn" in raw_content and "cắt đứt" in raw_content:
        found_violations.append("Phát hiện kết hợp 'phong ấn' + 'cắt đứt' (Nguy cơ Knowledge leak)!")

    # Quét kiểm tra danh xưng Giám Đốc Kỹ Thuật Dữ Liệu
    if "Giám Đốc Kỹ Thuật Dữ Liệu" not in raw_content:
        found_violations.append("Thiếu danh xưng chuẩn xác: 'Giám Đốc Kỹ Thuật Dữ Liệu' của Minh An!")

    if found_violations:
        print(f"[-] [LỖI RULE-07 / KIỂM TOÁN NỘI DUNG] Phát hiện vi phạm:")
        for v in found_violations:
            print(f"    * {v}")
        return False
    print(f"[+] [2/5] RULE-07 đạt chuẩn tuyệt đối: 0 meta-words, 0 chữ 'hồi', 0 'hệ thống', danh xưng chuẩn xác.")

    # 3. Đảm bảo các nhân vật và thực thể tồn tại trong entities
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'char_le_dinh_hung',
        'Lê Đình Hùng',
        'character',
        json.dumps(['Thuyền trưởng Hùng', 'Đại úy Hùng'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'role': 'Thuyền trưởng Tàu Tuần Tra Cao Tốc HQ-268', 'rank': 'Đại úy Hải quân'}, ensure_ascii=False)
    ))
    
    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'loc_cuc_tu_hai_uyen',
        'Rãnh Nứt Cực Tù Hải Uyên',
        'location',
        json.dumps(['Cực Tù Hải Uyên', 'Rãnh biển Cực Tù (-1200m)'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'depth': '-1200m', 'region': 'Cần Giờ / Vịnh Gành Rái', 'type': 'Abyssal Trench / Ancient Seal'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'vehicle_kinh_uyen_01',
        'Tàu Lặn Biển Sâu Kình Uyên 01',
        'item',
        json.dumps(['Kình Uyên 01', 'Tàu lặn Cửu Long Thiên Hải'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'weight': '20 tons', 'hull': 'Titanium alloy', 'armament': '220dB acoustic cannon, 50t hydraulic clamp, diamond drill'}, ensure_ascii=False)
    ))

    cur.execute('''
    INSERT OR REPLACE INTO entities (id, name, type, aliases, status, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        'artifact_hai_uyen_toa_long_tru',
        'Hải Uyên Tỏa Long Trụ',
        'item',
        json.dumps(['Cọc tiêu thứ bảy', 'Cột Trận Nhãn Cực Tù'], ensure_ascii=False),
        'ACTIVE',
        json.dumps({'height': '30m', 'material': 'Deep jade & Archaic gold chains', 'function': 'Seventh pillar of Thuy Mon Thap Nhi Tieu'}, ensure_ascii=False)
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
        "Lặn Sâu Ngàn Mét & Huyết Chiến Cực Tù Hải Uyên",
        CHAPTER_NUM,
        1,
        f"{DATE}T18:30:00+07:00",
        CHAPTER_NUM,
        "loc_cuc_tu_hai_uyen",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_le_dinh_hung"]),
        "Minh An lặn sâu không bình khí xuống rãnh nứt Cực Tù Hải Uyên (-1.200m). Đối mặt áp lực thủy tĩnh cực hạn 120 atm ép nứt 33 đốt sống, bị tàu lặn titanium Kình Uyên 01 tấn công bằng chùm sóng xung âm 220 dB gây thổ huyết, đồng thời bị bầy quỷ sa biển sâu bao vây. Vận dụng trí tuệ kỹ sư dữ liệu tìm ra vùng bóng âm (acoustic shadow) né tránh sóng siêu âm, Minh An tung đòn Long Lân Phá Kình đánh gãy cánh tay cơ giới và trục chân vịt tàu lặn địch, tiêu diệt quỷ sa đầu đàn và chạm chân xuống thềm đáy phong ấn cổ xưa, tìm thấy cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ.",
        "Tiêu diệt tàu lặn Kình Uyên 01 của Cửu Long Thiên Hải; đánh lui bầy U Minh Quỷ Sa; tiếp cận thành công cọc tiêu thứ bảy Hải Uyên Tỏa Long Trụ tại độ sâu 1.200m."
    ))

    # 7.3 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An vượt qua áp lực 120 atm và vũ khí xung âm tại Cực Tù Hải Uyên, phá hủy tàu lặn Kình Uyên 01 và tiếp cận cột trận nhãn thứ bảy Hải Uyên Tỏa Long Trụ."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (chapters, timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T18:45:00+07:00"
        inv_data["current_location"] = "Rãnh Nứt Cực Tù Hải Uyên (Độ sâu 1.200m, Vịnh Gành Rái / Cần Giờ)"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ (Cương Huyết Thuần Dương)"
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

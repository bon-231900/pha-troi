# -*- coding: utf-8 -*-
"""Draft Chapter 73 for Phá Trời Novel OS with ~3,400 words prose, zero meta-words, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 73
CHAPTER_TITLE = "Hải Trình Cần Giờ"
LOCATION = "Quân cảng Cát Lái & Tàu Tuần Tra HQ-268 trên Vịnh Gành Rái (Cần Giờ)"
DATE = "2026-10-23"

ACT1 = '''Tám giờ sáng ngày hai mươi ba tháng Mười.

Quân cảng Cát Lái nằm bên bờ sông Đồng Nai rực rỡ dưới ánh nắng sớm mùa thu. Mặt nước phù sa cuộn sóng lăn tăn, phản chiếu những cánh hải âu chao liệng giữa vòm trời phương Nam cao vời vợi. Tại khu vực cầu cảng quân sự số ba, không khí làm việc diễn ra hết sức khẩn trương nhưng trật tự, nghiêm cẩn. Những người lính hải quân trong bộ quân phục dã chiến xanh màu nước biển thoăn thoắt kiểm tra dây neo, tiếp nhận trang thiết bị trinh sát và tiếp tế nhiên liệu.

Sừng sững bên mép cầu cảng là chiếc Tàu Tuần Tra Cao Tốc mang số hiệu HQ-268.

Con tàu có lượng giãn nước bốn trăm tấn, thân tàu sơn màu xám ngụy trang chống bám muối, các vách cabin vát nghiêng góc cạnh theo thiết kế tán xạ sóng radar hiện đại. Trên mũi tàu, tháp pháo tự động ba mươi mi-li-mét nòng đôi vươn cao uy dũng; hai bên mạn là các bệ phóng đạn mồi bẫy và giá treo ngư lôi; trên nóc cabin, cụm radar quét biển đa búp sóng và ăng-ten liên lạc vệ tinh liên tục xoay tròn chậm rãi.

Kỹ sư Tuấn cùng hai chiến sĩ cần vụ cẩn thận khiêng hai hòm nhôm chống sốc chứa thiết bị đo vẽ phổ quang, máy quét sonar đa chùm tia và máy ghi chấn ba chiều lên boong tàu. Tôi bước theo sau, vai đeo chiếc ba-lô dã chiến quen thuộc chứa thanh Hắc Thiết Đoản Côn, thanh Trấn Thủy Đoản Đao và chiếc hộp đồng cổ vân mai rùa.

Tại chân cầu thang dẫn lên đài chỉ huy, một sĩ quan hải quân mang quân hàm Đại úy bước nhanh tới đón chúng tôi.

Người sĩ quan trạc ba mươi tám tuổi, vóc dáng cao lớn vững chãi tựa một cây đước lâu năm, làn da ngăm đen bóng màu sương gió thao trường và đôi mắt sáng quắc, tinh anh.

"Chào các đồng chí! Tôi là Đại úy Lê Đình Hùng, Thuyền trưởng tàu HQ-268," anh giơ tay chào theo điều lệnh, giọng nói sang sảng át cả tiếng sóng vỗ mạn thuyền. "Đơn vị chúng tôi đã nhận được mệnh lệnh hiệp đồng tác chiến từ Bộ Tư lệnh Vùng 2 Hải quân và Viện Địa tầng Đô thị. Rất hân hạnh được đồng hành cùng đoàn công tác đặc biệt."

Tôi giơ tay đáp lễ, bắt chặt bàn tay thô ráp đầy vết chai sần của người chỉ huy tàu biển:

"Chào Thuyền trưởng Hùng. Tôi là Nguyễn Minh An, Giám Đốc Kỹ Thuật Dữ Liệu của Viện Địa tầng Đô thị, phụ trách tổ trinh sát thực địa. Còn đây là kỹ sư Tuấn, chuyên viên cao cấp phụ trách mạng lưới viễn thám và phân tích âm học địa tầng."

Thuyền trưởng Hùng siết chặt bàn tay tôi. Khoảnh khắc hai bàn tay chạm nhau, ánh mắt anh khẽ lóe lên một tia ngạc nhiên kín đáo. Là một chỉ huy dày dạn kinh nghiệm từng trải qua nhiều năm tuần tra trên thềm lục địa nhà giàn DK1, anh lập tức cảm nhận được luồng sức mạnh ngưng tụ tựa sắt nguội toát ra từ bàn tay tôi — một bàn tay không hề có vẻ mảnh khảnh của một cán bộ bàn giấy thông thường, mà vững chãi, lạnh lùng tựa một phiến thép đúc.

"Tốt lắm! Lực lượng vũ trang và các nhà khoa học cùng chung một chiến hào," Thuyền trưởng Hùng gật đầu tán thưởng. "Tất cả các khoang máy, cụm máy động lực và trạm định vị thủy âm của HQ-268 đã sẵn sàng. Mời các đồng chí lên tàu ổn định vị trí, chúng ta sẽ rời bến ngay bây giờ."

"Rút dây neo! Chuẩn bị rời cảng!" Tiếng còi tàu vang lên dõng dạc.

Cụm động cơ đi-ê-zen công suất lớn rùng mình gầm vang trầm đục. Ba chân vịt đẩy tàu sủi bọt trắng xóa sau đuôi. Chiếc tàu tuần tra HQ-268 từ từ tách khỏi cầu cảng Cát Lái, rẽ sóng lướt nhanh vào luồng hàng hải sông Lòng Tàu, mở màn cho chuyến hải trình sinh tử tiến thẳng ra cửa biển.'''

ACT2 = '''Mười một giờ trưa cùng ngày.

Sau hơn ba tiếng hành trình xuôi theo dòng Lòng Tàu, bóng dáng những khu đô thị nhộn nhịp, những cây cầu bê tông đồ sộ của thành phố đã hoàn toàn lùi lại phía sau. Xung quanh tàu HQ-268 lúc này là một màu xanh bạt ngàn ngút ngàn tầm mắt của Rừng Sác Cần Giờ — khu bảo tồn sinh thái ngập mặn thế giới rộng hơn bảy mươi ngàn héc-ta.

Những dải rừng đước, rừng mắm nguyên sinh ken dày đặc đôi bờ sông. Bộ rễ đước chằng chịt tựa đàn trăn đá khổng lồ cắm sâu vào lớp bùn lầy phù sa, vươn những chiếc vòi thở lên khỏi mặt nước đón ngọn gió biển đầu mùa mặn mòi.

Đây không chỉ là căn cứ địa cách mạng lừng danh của các chiến sĩ đặc công Rừng Sác năm xưa, mà xét về mặt phong thủy địa tầng, vùng rừng ngập mặn này chính là cổ họng trọng yếu nơi long mạch nước ngọt phương Nam giao thoa với đại dương bao la.

Trong phòng tác chiến âm học của tàu HQ-268, Tuấn đang cắm tai nghe chống ồn, mắt chăm chú nhìn màn hình máy quét sonar quét sườn đa chùm tia. Tôi đứng cạnh anh, hai tay tựa lên mép bàn kim loại, tĩnh lặng cảm thụ từng biến chuyển vi tế của mạch nước.

Kể từ khi hoàn tất Thức thứ tám *Hoán Huyết Hóa Cương*, dòng Cương Huyết màu đồng thau trong lồng ngực tôi luân chuyển chậm rãi nhưng mang theo nguồn sinh lực dồi dào chưa từng thấy. Nhịp tim của tôi duy trì ở mức ba mươi hai nhịp một phút, đều đặn, trầm lắng tựa tiếng chuông chùa giữa đêm thanh vắng. Nhưng mỗi một nhịp đập lại khuếch tán một vòng sóng cảm ứng vô hình, giúp giác quan của tôi xuyên thấu qua lớp vỏ thép tàu, thâm nhập sâu vào làn nước đục ngầu phù sa bên dưới.

"Minh An, có tín hiệu dị thường!" Tuấn đột ngột xoay núm điều chỉnh tần số, màn hình hiển thị những dải phổ âm thanh màu đỏ thẫm đang nhấp nháy liên tục. "Bên dưới độ sâu mười lăm mét của luồng lạch, máy thu thủy âm bắt được một dải sóng hạ âm có tần số bốn mươi lăm Héc. Tín hiệu này phát ra từ hướng cửa biển, truyền ngược dòng nước đi vào rừng ngập mặn."

"Bốn mươi lăm Héc?" Tôi chau mày, nhìn kỹ biểu đồ sóng dao động. "Đây không phải sóng âm tự nhiên do dòng triều tạo ra. Dao động này có chu kỳ ngắt quãng cơ học, mang theo từ trường tà đạo cực kỳ u ám."

Dưới đáy sông, qua làn nước mờ mịt, dòng Cương Huyết trong người tôi bỗng rung động nhè nhẹ.

Nhờ thính giác và cảm ứng Thể Đạo đã đạt tới Luyện Cốt Hậu kỳ, tôi nghe thấy những tiếng quẫy nước điên cuồng, hỗn loạn từ những bãi bùn dưới chân rễ đước. Hàng đàn cá sấu hoa cà, cá trê biển và các loài rắn nước ngập mặn đang bơi lội tán loạn, mắt chúng đỏ ngầu, thân mình cọ xát vào thân cây tựa như đang phát cuồng dưới tác động của luồng sóng hạ âm.

Trong thức hải, đóa sen ngọc bích khẽ rung rinh. Lâm Tịch ngồi trên đài sen, thanh âm thanh lãnh của nàng vang lên trong tâm thức tôi:

*"Minh An, kẻ địch đang dùng trận bàn siêu âm đáy biển phát tán sóng tà sát để quấy nhiễu luồng lạch, kích động thủy thú nhằm che giấu hoạt động của tàu mẹ. Sóng hạ âm bốn mươi lăm Héc này chính là chìa khóa mở đường của Hắc Giao Đường. Phía trước ranh giới cửa biển, cạm bẫy của chúng đã giăng sẵn."*

"Ta hiểu rồi," tôi đáp lại trong tâm thức. "Dù là cạm bẫy gì, ta cũng sẽ đập tan."

Tôi quay sang Tuấn, trầm giọng căn dặn:

"Tuấn, ghi nhận toàn bộ tọa độ và bước sóng hạ âm này. Bật máy lọc nhiễu âm học của Viện Địa tầng lên mức tối đa, truyền trực tiếp dữ liệu sang màn hình chỉ huy của Thuyền trưởng Hùng. Chúng ta sắp tiến vào vùng biển mở rồi."'''

ACT3 = '''Hai giờ mười lăm phút chiều.

Chiếc tàu tuần tra HQ-268 vượt qua ngã ba sông Soài Rạp, lướt qua mũi cù lao Cần Giờ rồi chính thức tiến vào vùng biển mở của vịnh Gành Rái.

Không gian bỗng chốc mở rộng mênh mông bát ngát. Màu nước sông phù sa đục ngầu dần dần nhường chỗ cho sắc nước biển xanh thẫm, từng con sóng bạc đầu cao hơn hai mét dồn dập đập vào mũi tàu, tung bọt trắng xóa lên tận kính chắn gió buồng lái. Gió biển mặn chát thổi lồng lộng, mang theo vị mặn nồng nàn của đại dương.

Từ đài quan sát trên nóc cabin, qua ống nhòm quang học độ phóng đại cao, tôi nhìn thấy rõ phao số không — chiếc phao hoa tiêu hàng hải sơn màu đỏ rực dập dềnh giữa muôn trùng sóng nước.

Và cách phao số không khoảng năm hải lý về phía Đông Nam, ngay trên lằn ranh hải phận quốc tế, một bóng tàu khổng lồ hiện ra mờ ảo trong màn sương mù biển.

Đó chính là tàu *Thiên Hải 09*.

Con tàu dài hơn một trăm ba mươi mét, lượng giãn nước hơn năm ngàn tấn, thân tàu sơn màu xanh đen ảm đạm. Phía đuôi tàu lắp đặt một cần cẩu chữ A siêu trọng tải cao hơn ba mươi mét, trên boong ngổn ngang các cụm tời cáp thép khổng lồ và các vòm radar định vị vệ tinh hình cầu. Con tàu khổng lồ ấy buông neo sừng sững giữa sóng gió tựa như một pháo đài kim loại hắc ám, chung quanh liên tục tỏa ra những làn khói đen khét lẹt từ các máy phát điện diesel công suất lớn.

"Báo động tác chiến toàn tàu!"

Bỗng nhiên, tiếng còi báo động đỏ rực trên đài chỉ huy HQ-268 réo vang dồn dập.

Sĩ quan trực ban sonar hét lớn vào micro:

"Báo cáo Thuyền trưởng! Sonar chủ động phát hiện tám mục tiêu ngầm di chuyển tốc độ cao ở cự ly ba trăm năm mươi mét, hướng mười một giờ! Tốc độ tiếp cận mười hai hải lý một giờ, đang lặn sâu mười lăm mét hướng thẳng vào lườn tàu ta!"

Thuyền trưởng Hùng lập tức lao tới bàn hải đồ tác chiến, ánh mắt sắc lẹm:

"Nhận dạng mục tiêu là gì? Ngư lôi hay phương tiện lặn không người lái?"

"Không phải ngư lôi! Tín hiệu âm học cho thấy đó là các mô-tơ đẩy ngầm cá nhân DPV của người nhái đặc nhiệm! Bọn chúng mang theo các khối kim loại có từ tính cao — khả năng rất cao là mìn từ tính định hướng toan áp sát gắn vào chân vịt và lườn tàu!"

Mặt biển quanh tàu HQ-268 lúc này bỗng cuộn lên những vòng xoáy ngầm dị thường. Tám bóng đen mang thiết bị lặn kín khí đang lướt đi vun vút dưới làn nước biển xanh thẫm tựa như một đàn cá mập đói mồi, mang theo những quả mìn nổ phá giáp nhằm làm tê liệt tàu tuần tra của ta.

"Khẩu đội pháo ba mươi ly chuẩn bị bắn đón đầu! Thả bom chìm cảnh cáo!" Thuyền trưởng Hùng dứt khoát ra lệnh.

"Khoan đã, Thuyền trưởng!" Tuấn vội vàng lên tiếng ngăn lại, ngón tay chỉ vào bản đồ đo tầng địa chất đáy biển. "Khu vực đáy biển dưới chân chúng ta là thềm đá móng cổ Sa Huỳnh chứa các mắt xích phong ấn ngầm dẫn ra rãnh nứt Cần Giờ. Nếu kích nổ bom chìm chống ngầm ở cự ly gần thế này, sóng xung kích từ vụ nổ sẽ đánh vỡ các kết cấu đá móng cổ, làm đứt gãy mạch dẫn long khí!"

Thuyền trưởng Hùng nghiến răng, trán nổi gân xanh:

"Nhưng nếu để chúng áp sát gắn mìn vào chân vịt, tàu ta sẽ bị bất động giữa biển mở, biến thành bia tập bắn cho hỏa lực tầm xa của tàu mẹ đối phương!"

Trong khoảnh khắc ngàn cân treo sợi tóc ấy, tôi bước lên một bước, giọng nói trầm tĩnh nhưng vững vàng tựa bàn thạch:

"Thuyền trưởng Hùng, xin anh tạm hoãn lệnh nổ súng. Hãy để tôi xuống nước giải quyết toán người nhái này."'''

ACT4 = '''Ba giờ chiều.

Thuyền trưởng Hùng mở to hai mắt nhìn tôi, vẻ mặt đầy kinh ngạc:

"Cậu An, cậu đùa sao? Dưới đó là biển sâu gần ba mươi mét, dòng chảy ngầm cực mạnh, lại có đến tám tên người nhái trang bị súng phóng lao áp lực và mìn từ tính! Cậu xuống đó một mình chẳng khác nào nạp mạng!"

"Tôi không đùa," tôi mỉm cười điềm đạm, cởi bỏ chiếc áo khoác dã chiến, để lộ bộ đồ lặn cao su chuyên dụng màu đen ôm sát thân thể rắn chắc tựa tượng đồng. "Thể chất của tôi đã qua rèn luyện đặc biệt, hoàn toàn miễn nhiễm với áp lực nước biển. Nếu nổ súng hay dùng bom chìm lúc này, chúng ta sẽ trúng kế điệu hổ ly sơn của kẻ địch. Hãy tin tôi."

Nhìn vào đôi mắt rực sáng quầng quang màu đồng thau và khí thế uy nghiêm áp bức toát ra từ người tôi, Thuyền trưởng Hùng hít một hơi thật sâu, dứt khoát gật đầu:

"Được! Toàn tàu chuyển sang trạng thái cảnh giới cấp một, yểm trợ tối đa cho đồng chí An!"

Tôi rút thanh Hắc Thiết Đoản Côn gài chặt sau lưng, thanh Trấn Thủy Đoản Đao thắt bên hông trái, đeo mặt nạ lặn rồi sải bước ra mạn phải tàu.

Không cần bình dưỡng khí cồng kềnh, chỉ với một nhịp thở sâu gom đầy dưỡng khí vào lồng ngực, thân thể tôi lao vút xuống mặt biển tựa một mũi lao thép xé toạc làn sóng bạc.

"Ùm!"

Khối nước biển lạnh giá ôm trọn lấy thân thể tôi.

Áp suất nước ở độ sâu hai mươi lăm mét lập tức ép chặt từ bốn phía. Nhưng ngay khoảnh khắc ấy, dòng Cương Huyết trong tim tôi gầm vang như sấm dậy. Thức thứ tám *Hoán Huyết Hóa Cương* tự động vận hành ở mức tối đa! Áp lực thủy tĩnh nội sinh từ dòng máu đồng thau tỏa ra khắp các mao mạch, cân bằng hoàn hảo với áp lực nước biển bên ngoài. Lồng ngực tôi không hề có cảm giác nghẹt thở, màng nhĩ vững vàng như kim loại nguội, hai mắt mở to nhìn xuyên qua làn nước biển trong vắt.

Tám tên người nhái Hắc Giao Đường đang cưỡi trên bốn chiếc mô-tơ đẩy ngầm DPV hình ngư lôi, tay cầm súng phóng lao áp lực khí nén, đang lao thẳng về phía lườn tàu HQ-268.

Nhìn thấy một bóng người lao xuống biển mà không hề mang bình dưỡng khí, tên chỉ huy dẫn đầu khẽ giật mình ngơ ngác. Nhưng sự tàn bạo của một tên sát thủ chuyên nghiệp lập tức khiến gã giơ súng phóng lao lên, bóp cò!

"Phựt! Vút!"

Mũi lao thép dài tám mươi phân xé toạc làn nước bắn thẳng vào ngực tôi.

Tôi không hề né tránh. Tay phải tôi vung lên, rút thanh Hắc Thiết Đoản Côn chém ngang một đường hình cánh cung — tuyệt chiêu *Long Lân Phá Kình*!

"Keng!"

Một tiếng vang đanh gọn bùng nổ dưới đáy nước. Mũi lao thép bị kình lực vạn cân của Luyện Cốt Hậu kỳ đánh gãy đôi, bắn văng ra xa. Kình phong phỉ thúy và ánh đỏ chu sa cuộn tròn quanh đầu côn, tạo thành một làn sóng xung kích xé rách khối nước biển, đánh thẳng vào chiếc mô-tơ đẩy ngầm của tên sát thủ!

"Rắc! Choảng!"

Vỏ hợp kim của chiếc mô-tơ vỡ toác thành nhiều mảnh. Pin lithium bên trong chập điện nổ tung bọt khí trắng xóa. Tên sát thủ bị kình lực chấn động đánh bật ra sau, máu tươi phun ra ướt đẫm mặt nạ lặn.

Bảy tên người nhái còn lại kinh hãi tột độ. Bọn chúng đồng loạt buông các khối mìn từ tính, giương súng phóng lao và rút những thanh đoản đao tẩm độc xương cá đuối lao vào vây bọc lấy tôi.

Nhưng trong môi trường nước biển này, tôi mới thực sự là chúa tể!

Thân thể tôi lướt đi trong làn nước tựa một con kình ngư đạp sóng.

Thức thứ hai — *Đoạn Lưu*!

Thức thứ ba — *Phá Giáp*!

Từng đường côn rực sáng xé toạc màn nước biển. Tiếng kim loại gãy vụn, tiếng vỏ mô-tơ nứt toác liên tiếp vang lên trầm đục dưới đáy sâu. Từng tên sát thủ lần lượt bị đánh gãy vũ khí, phế bỏ kinh mạch tay chân, ngất lịm trôi lơ lửng trong nước biển.

Tên đội trưởng cầm đầu toan kích hoạt khối mìn từ tính trên tay để tự sát đồng quy vu tận.

Thân hình tôi lướt tới như một tia chớp lam ngọc. Bàn tay trái của tôi vươn ra, ngón tay cứng như kìm thép bóp chặt lấy cổ tay gã, bẻ ngoặt ra sau.

"Rắc!"

Xương cổ tay gã gãy gục, quả mìn tuột khỏi tay rơi xuống đáy biển cát mịn. Tay phải tôi vung lên, tước phăng chiếc túi chống nước đeo trước ngực gã — bên trong chứa chiếc máy giải mã âm học và bản đồ hoa tiêu dẫn đường bí mật!

Năm phút sau.

Bên mạn tàu HQ-268, mặt nước rẽ sóng sủi bọt trắng xóa.

Tôi một tay xách cổ áo tên đội trưởng người nhái đang mê man bất tỉnh, một tay bám vào thang dây kim loại, phóng mình nhảy vọt lên boong tàu một cách nhẹ nhàng, vững chãi.

Nước biển chảy ròng ròng trên bộ đồ lặn dã chiến của tôi, nhưng hơi thở tôi vẫn êm ả, nhịp tim bình thản ba mươi lăm nhịp một phút, làn da ẩn hiện ánh đồng thau rắn rỏi dưới ánh nắng chiều rực rỡ. Dưới chân tôi, tám quả mìn từ tính định hướng đã bị tháo ngòi nổ nằm trơ trọi trên boong.

Thuyền trưởng Hùng và toàn thể thủy thủ đoàn đứng sững sờ như hóa đá.

Vài giây sau, tiếng reo hò thán phục vang dội khắp boong tàu HQ-268!

"Đồng chí An... Cậu... Cậu quả thực là một Thần nhân!" Thuyền trưởng Hùng bước tới, siết chặt vai tôi bằng tất cả sự kính phục chân thành của một người lính biển.

Tuấn lập tức cầm chiếc máy giải mã âm học vừa đoạt được cắm vào bảng điều khiển máy tính. Chỉ sau vài giây xử lý, màn hình rực sáng lên một tọa độ hải trình đỏ rực:

"Minh An, Thuyền trưởng! Đã giải mã thành công! Đây chính là vị trí thả tàu lặn thám hiểm biển sâu của tàu *Thiên Hải 09* tại rãnh nứt Cực Tù Hải Uyên ở độ sâu một ngàn hai trăm mét!"

Tôi nhìn về phía chân trời xa xôi ngoài khơi vịnh Gành Rái, nơi bóng con tàu mẹ khổng lồ đang dập dềnh giữa muôn trùng sóng dữ. Ngọn gió biển mặn mòi thổi lồng lộng qua mái tóc tôi.

Hải trình Cần Giờ đã chính thức mở màn. Trận chiến quyết định vận mệnh long mạch phương Nam đang ở ngay trước mắt.'''

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

    if found_violations:
        print(f"[-] [LỖI RULE-07] Phát hiện vi phạm từ cấm:")
        for v in found_violations:
            print(f"    * {v}")
        return False
    print(f"[+] [2/5] RULE-07 đạt chuẩn tuyệt đối: 0 meta-words, 0 chữ 'hồi'.")

    # 3. Đảm bảo nhân vật Lê Đình Hùng tồn tại trong entities
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
        "Xuất Bến Cát Lái & Thủy Chiến Vịnh Gành Rái",
        CHAPTER_NUM,
        1,
        f"{DATE}T15:30:00+07:00",
        CHAPTER_NUM,
        "loc_vinh_ganh_rai",
        json.dumps(["char_minh_an", "char_lam_tich", "char_tuan", "char_le_dinh_hung"]),
        "Minh An và Tuấn lên Tàu Tuần Tra HQ-268 do Thuyền trưởng Lê Đình Hùng chỉ huy rời Quân cảng Cát Lái. Vượt qua Rừng Sác Cần Giờ, phát hiện dải sóng hạ âm 45 Hz của Hắc Giao Đường quấy nhiễu luồng lạch. Đến phao số 0 Vịnh Gành Rái, phát hiện tàu mẹ Thiên Hải 09 buông neo. Tàu HQ-268 bị 8 người nhái ôm mìn từ tính DPV phục kích. Minh An nhảy xuống biển sâu gần 30m, vận dụng Cương Huyết Luyện Cốt Hậu kỳ và Long Lân Phá Kình đánh gãy mũi lao thép, phá hủy mô-tơ đẩy DPV, tước mìn từ tính và bắt sống tên chỉ huy dẫn đường đoạt máy giải mã âm học tọa độ rãnh nứt Cực Tù Hải Uyên.",
        "Tiêu diệt mối nguy phục kích lườn tàu HQ-268; bảo vệ toàn vẹn thềm đá móng cổ Sa Huỳnh; bắt sống đội trưởng người nhái đoạt máy giải mã âm học và tọa độ thả tàu lặn biển sâu của tàu Thiên Hải 09."
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
        "Minh An mở màn hải trình Cần Giờ trên tàu HQ-268, đập tan toán người nhái phục kích mìn từ tính tại phao số 0 Vịnh Gành Rái và đoạt máy giải mã tọa độ rãnh nứt Cực Tù Hải Uyên."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T16:00:00+07:00"
        inv_data["current_location"] = "Tàu Tuần Tra Cao Tốc HQ-268 (Vịnh Gành Rái / Phao Số 0 Cần Giờ)"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ (Hoán Huyết Hóa Cương)"
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

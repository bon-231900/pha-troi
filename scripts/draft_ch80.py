# -*- coding: utf-8 -*-
"""Draft Chapter 80 for Phá Trời Novel OS with ~4,000+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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
from system.engines.emotion_dopamine_engine import EmotionDopamineEngine

CHAPTER_NUM = 80
CHAPTER_TITLE = "Sóng Vỗ Cù Lao"
DATE = "2026-10-25"
LOCATION = "Kênh Chợ Gạo & Cù Lao Ven Sông Tiền (Tiền Giang)"

ACT1 = '''Năm giờ ba mươi phút sáng ngày hai mươi lăm tháng mười.

Sương mù bảng lảng trên mặt sông Đồng Nai như những dải lụa trắng xám là đà trôi theo con nước ròng. Tiếng còi tầm từ các cảng cạn xa xa vọng lại, đánh thức một ngày mới của vùng đô thị công nghiệp giáp ranh giữa Dĩ An và Thủ Đức.

Tôi đứng dậy khỏi tấm bạt dã chiến, chỉnh đốn lại hành trang.

Sau một đêm dài vận chuyển Thuần Dương Cương Huyết tôi luyện ba mươi ba đốt sống lưng, cảm giác đau buốt do mảnh đạn M79 găm vào vai trái đã hoàn toàn biến mất. Toàn bộ khung xương của tôi đạt tới cảnh giới Luyện Cốt Hậu kỳ Cùng Cực — vững chãi, trầm đặc và kiên cố tựa ngọc thạch tôi trong lửa đỏ. Từng thớ thịt, đường gân đều tràn trề sức sống dẻo dai của một phàm nhân khổ tu Thể Đạo.

Nhưng trong thức hải, đài sen ngọc bích của Lâm Tịch vẫn hoàn toàn bất động.

Vết rạn màu xám tro trên cánh sen vẫn nằm nguyên ở đó. Nàng chìm sâu trong giấc ngủ tĩnh dưỡng, không một lời nhắc nhở, không một gợn sóng ý thức.

"Hãy yên nghỉ đi, Lâm Tịch. Chặng đường này, cứ để tôi tự bước."

Tôi thầm nhủ trong lòng, rồi dứt khoát khóa chặt chiếc ba lô dã chiến.

Tôi không thể tiếp tục chạy chiếc xe Wave Alpha quen thuộc xuôi theo Quốc lộ 1A để về Tiền Giang. Tuyến đường bộ trọng yếu nối Sài Gòn với các tỉnh miền Tây có quá nhiều trạm thu phí tự động, camera giao thông quét biển số và các nút giao trọng điểm — nơi tai mắt của Tập đoàn Cửu Long Thiên Hải có thể dễ dàng giăng lưới phục kích.

Một kỹ sư dữ liệu am tường về địa tầng và hạ tầng giao thông như tôi biết rõ: mạng lưới sông ngòi chằng chịt của miền Tây Nam Bộ mới chính là con đường an toàn và bí mật nhất.

Tôi nổ máy xe, chạy ngược về hướng bến xe miền Tây ở quận Bình Tân. Tại đây, tôi gửi chiếc Wave Alpha vào bãi giữ xe nhiều tầng ngầm dưới lòng đất của một trung tâm thương mại lớn, trả trước tiền gửi một tuần và cầm theo chiếc vé từ giữ xe không ghi danh tính.

Tôi bước vào một con hẻm nhỏ gần chợ An Lạc, mua một bộ quần áo bà ba màu xanh đen đã giặt bạc màu của người làm vườn miền Tây, một đôi dép cao su đúc và chiếc nón tai bèo cũ kỹ.

Thanh Hắc Thiết Đoản Côn và Trấn Thủy Đoản Đao được tôi bọc cẩn thận trong tấm bạt dứa rách, bên ngoài buộc thêm vài chiếc cờ-lê mỏ lết gỉ sét và một cuộn dây thừng dầu, ngụy trang hoàn hảo thành bộ đồ nghề sửa máy nổ của một anh thợ cơ khí đường sông.

Bảy giờ sáng.

Tôi bắt xe buýt sang bến Bình Đông ven dòng kênh Tàu Hủ ở Quận 8.

Nơi đây từ hàng trăm năm qua đã là bến đỗ tấp nập của những đoàn ghe gỗ chở trái cây, dừa xiêm, trấu gạo và cây giống từ các tỉnh đồng bằng sông Cửu Long cập bến Sài Gòn. Mùi bùn non ngai ngái hòa lẫn với mùi khói dầu máy nổ đuôi tôm và hương chuối chín tạo nên một bầu không khí đậm đặc phong vị sông nước phương Nam.

Tại một góc bến thuyền dưới chân cầu Chà Và, một chiếc ghe gỗ tải trọng ba mươi tấn mang biển kiểm soát Tiền Giang đang chuẩn bị nổ máy rời bến sau khi đã dỡ xong chuyến dừa sáp.

Chủ ghe là một đôi vợ chồng già ngoài sáu mươi tuổi, dáng người quắt queo, da ngăm đen vì mưa nắng sông hồ.

"Bác Hai ơi, cho con quá giang một đoạn về miệt Chợ Gạo được không bác?" Tôi bước lại gần mép cầu tàu, cất tiếng chào bằng giọng rặt miền Tây. "Con là thợ sửa máy nổ dưới quê lên trển mua đồ phụ tùng, mà lỡ kẹt tiền xe đò, xin bác cho con theo ghe, con phụ bác kéo dây neo với châm dầu máy."

Bác tài xế già ngước nhìn tôi, thấy bộ đồ bà ba sẫm màu dính vài vệt dầu luyn và bao đồ nghề cơ khí trên vai tôi, ánh mắt ông lộ vẻ hiền hậu, chất phác:

"Thôi nhảy xuống đi chú mày! Dân sông nước với nhau cả, tiện đường thì cho đi nhờ chứ tính toán chi vài đồng bạc lẻ. Xuống mui sau coi chừng trơn trợt nghen!"

"Dạ, con cảm ơn hai bác nhiều!"

Tôi nhanh nhẹn nhảy xuống sàn ghe gỗ. Chiếc ghe khẽ lắc lư theo nhịp sóng rồi rẽ nước nổ máy giòn giã: *Tạch tạch tạch tạch...*

Chiếc ghe gỗ từ từ rời bến Bình Đông, xuôi theo dòng kênh Tàu Hủ tiến vào ngã ba sông Chợ Đệm.

Dòng nước màu nâu đỏ cuộn trào dưới đáy ghe. Khi con thuyền vượt qua ngã ba sông Vàm Cỏ Đông để tiến vào dòng Kênh Chợ Gạo — con kênh đào huyền thoại nối liền hai miền Đông và Tây Nam Bộ — không gian xung quanh bỗng mở toang ra bát ngát.

Hai bên bờ kênh là những rặng dừa nước bạt ngàn ken dày tựa như những bức tường thành xanh biếc. Những vạt hoa muống biển màu tím nhạt nở rộ trên bãi bùn lầy, và những dề lục bình hoa tím trôi bồng bềnh dập dềnh theo con nước lớn.

Tôi ngồi xếp bằng trên mui sau của ghe, kéo chiếc nón tai bèo xuống ngang mày, nhắm mắt điều hòa nhịp thở.

Ở trạng thái Quy Tức Cùng Cực, nhịp tim tôi duy trì đều đặn ba mươi lăm nhịp một phút. Mỗi nhịp đập của cuống tim đều đẩy một luồng Thuần Dương Cương Huyết chảy dọc qua ba mươi ba đốt sống lưng tủy ngọc.

Khi chiếc ghe lướt qua ranh giới giữa Long An và Tiền Giang, tiến gần về phía ngã ba sông Tiền, toàn bộ cột sống lưng của tôi bỗng khẽ giật giật.

Một xung chấn vi mô với tần số cực thấp — đúng 0.12 Hz — từ sâu dưới lòng đáy sông phù sa truyền ngược lên đáy ghe, dội vào lòng bàn chân tôi!

Đó chính là dao động từ trường đặc trưng của mạng lưới phong ấn cổ xưa!

Dưới lòng dòng sông Tiền cuộn đỏ phù sa này, chắc chắn có một cọc tiêu ngầm của Thủy Môn Thập Nhị Tiêu đang âm thầm trấn giữ dòng chảy đại ngàn!'''

ACT2 = '''Một giờ bốn mươi lăm phút chiều.

Sau hơn sáu tiếng đồng hồ xuôi dòng kênh Chợ Gạo, chiếc ghe gỗ rẽ ra lòng sông Tiền mênh mông sóng nước.

Dòng sông Tiền vào mùa nước nổi cuộn đỏ một màu phù sa màu mỡ, rộng đến hơn một cây số, trải dài tít tắp đến tận đường chân trời. Những cù lao xanh mướt như những chiếc mai rùa khổng lồ nổi bồng bềnh giữa sóng nước, rợp bóng dừa xiêm, vườn sầu riêng và vườn bưởi da xanh trĩu quả.

Ghe tấp vào một bến đò ngang bằng gỗ tạm bợ dưới bóng một rặng dừa nước rậm rạp thuộc huyện cù lao.

Tôi biếu hai bác chủ ghe một gói thuốc rê và một ít tiền dầu máy mà hai bác nhất quyết từ chối, chỉ dặn tôi đi đứng cẩn thận rồi nổ máy rẽ sóng xuôi về miệt Bến Tre.

Tôi khoác bao đồ nghề lên vai, bước lên con đường đan rải đá dăm quanh co rợp bóng dừa nước.

Đây chính là quê hương tôi — mảnh đất cù lao phù sa nơi tôi đã sinh ra và lớn lên suốt mười tám năm đầu đời trước khi khăn gói lên Sài Gòn học đại học rồi làm việc tại Viện Địa tầng.

Mùi đất bùn non ngai ngái, mùi khói rơm rạ đốt đồng thoang thoảng trong gió chiều mang lại cho tôi một cảm giác thân thuộc đến nao lòng. Mỗi khúc quanh, mỗi cây cầu khỉ bắc qua con rạch nhỏ ngoằn ngoèo đều in hằn sâu đậm trong ký ức tuổi thơ nghèo khó nhưng ấm êm của tôi.

Tôi cất bước đi nhanh về phía xóm Cây Me — nơi có căn nhà lá ba gian đơn sơ của mẹ tôi nằm nép mình bên một vườn chuối ven rạch.

Tuy nhiên, càng tiến gần về phía xóm cũ, các giác quan sắc bén của một người tu Thể Đạo đạt tới Luyện Cốt Hậu kỳ Cùng Cực càng khiến tôi nâng cao cảnh giác tối đa.

Gió chiều thổi xào xạc qua tán lá dừa, mang theo tiếng chim bìm bịp kêu chiều và tiếng sóng vỗ ì oạp vào chân cầu đan.

Bỗng nhiên, từ khoảng cách hơn một trăm năm mươi mét phía trước, thính giác vượt trội của tôi bắt được một chuỗi âm thanh bất thường: tiếng động cơ của một chiếc xe máy phân khối lớn đang nổ cầm chừng rất khẽ, hòa lẫn với tiếng thì thầm của hai người đàn ông lạ mặt.

Tôi lập tức dừng bước, nép mình vào bóng râm của một gốc dừa nước cổ thụ ven đường.

Đưa mắt nhìn qua kẽ lá dừa, tôi nhìn thấy hai gã thanh niên mặc áo khoác gió màu đen, đội mũ bảo hiểm trùm kín cằm, đeo kính râm đen sì đang dừng xe bên cạnh bụi rào dâm bụt đầu ngõ dẫn vào nhà mẹ tôi. Chiếc xe máy tay ga của chúng bị tháo rời biển số, trên ghi-đông gắn một thiết bị định vị vệ tinh chuyên dụng.

Một tên cầm chiếc điện thoại thông minh chụp liên tiếp vài bức ảnh về phía chái bếp và chiếc sọt tre đựng rau của mẹ tôi đang úp ngoài hàng rào.

Tên còn lại vừa hút thuốc vừa cất giọng nói the thé qua tai nghe Bluetooth:

"Báo cáo anh Bảy, đúng là căn nhà lá này rồi. Em vừa giả vờ hỏi thăm mấy bà già trong xóm, họ xác nhận bà cụ tên Nguyễn Thị Lành, bán rau ngoài chợ huyện Chợ Gạo, sống thui thủi một mình. Thằng con trai Nguyễn Minh An làm trên Sài Gòn cả tháng nay chưa thấy về quê... Dạ, bên công an xã dạo này tuần tra gắt lắm, bọn em không dám manh động bắt giữ bà già ngay ban ngày."

Đầu dây bên kia dường như đang quát tháo chỉ thị điều gì đó rất gay gắt. Tên mặc áo đen gật đầu lia lịa:

"Dạ, em hiểu rồi anh Bảy! Chiều nay bốn giờ đội khảo sát trắc địa ngầm của tổng bộ Cửu Long Thiên Hải sẽ đi ca-nô cao tốc từ bến phà Rạch Miễu xuống thẳng Cồn Trấn Ba đúng không ạ? Nghe nói cái Cổ Miếu Trấn Ba trên cồn cát nổi giữa sông Tiền có giấu một cái cọc đá cổ ngàn năm trấn giữ long mạch thủy đạo. Tổng bộ ra lệnh bằng mọi giá trước đêm nay phải đóng cọc sắt gắn kíp nổ định vị để phá hủy phong ấn... Bọn em nắm rõ rồi, canh chừng ở đây thêm nửa tiếng nữa bọn em sẽ ra bến đò đón đội thợ lặn!"

Nghe đến đó, lồng ngực tôi cuộn trào một ngọn lửa giận dữ ngút trời!

Phán đoán của tôi hoàn toàn chính xác!

Tập đoàn Cửu Long Thiên Hải quả thực đã lần ra địa chỉ quê nhà của mẹ tôi, và mục tiêu tiếp theo của chúng tại miền Tây chính là **Cổ Miếu Trấn Ba** trên cồn cát nổi giữa sông Tiền — nơi lưu giữ **cọc tiêu thứ chín** của mạng lưới Thủy Môn Thập Nhị Tiêu!

Nếu tôi không kịp thời có mặt tại đây trong chiều nay, mẹ tôi sẽ rơi vào tay đám tà tu làm con tin, và cọc tiêu thứ chín của long mạch phương Nam sẽ bị chúng nổ tung dưới đáy sông sâu!

Bàn tay tôi siết chặt chuôi Hắc Thiết Đoản Côn giấu trong bao bạt dứa.

Tôi không để cho bất kỳ kẻ nào có cơ hội làm tổn hại đến người mẹ hiền của tôi, dù chỉ là một sợi tóc!'''

ACT3 = '''Ba giờ mười lăm phút chiều.

Hai tên thám thính của Cửu Long Thiên Hải nổ máy xe, từ từ rẽ vào con đường đất ven rạch dừa nước để hướng ra bến đò ngang.

Đoạn đường này dài hơn ba trăm mét, một bên là mương rạch sâu ngập bùn lầy rợp bóng dừa nước ken dày, một bên là vườn sầu riêng bạt ngàn không một bóng người qua lại.

Đây chính là tử địa hoàn hảo để hành động!

Tôi đạp mạnh chân vào thân cây dừa nghiêng sát mép nước, toàn thân nhẹ bẫng vút lên tầng không tựa như một cánh chim ưng săn mồi. Bộ pháp Thể Đạo kết hợp với kình lực Luyện Cốt Hậu kỳ Cùng Cực giúp tôi di chuyển trên những đọt dừa nước mà không hề phát ra một tiếng động nhỏ, nhanh hơn cả tốc độ chiếc xe máy chạy trên mặt đường bùn đất bên dưới.

Ngay tại khúc quanh khuất tầm mắt dưới chân một cây cầu khỉ gãy, tôi búng người lao thẳng xuống!

*VÚT!*

Một bóng đen từ trên trời giáng thế.

Tên ngồi sau chưa kịp nhận thức được chuyện gì xảy ra thì hai ngón tay cứng như thép nguội của tôi đã điểm chuẩn xác vào huyệt Á Môn sau gáy hắn. Kình lực Thuần Dương thấu qua da thịt khóa chặt thanh quản, khiến hắn nghẹn họng không thể thốt lên một tiếng kêu.

Đồng thời, chân phải tôi quét ngang một vòng tròn tuyệt mỹ, mũi giày cao su đập trúng tay lái chiếc xe máy.

*RẮC!*

Chiếc xe máy bị lực chấn bẻ gập ghi-đông, ngã lăn ra vệ cỏ mềm bên lề đường mà không hề phát ra tiếng va đập kim loại chói tai.

Tên cầm lái ngã dúi dụi xuống bãi bùn, hoảng hốt rút khẩu súng ngắn giảm thanh giắt trong cạp quần ra định bóp cò. Nhưng bàn tay trái của tôi đã vươn ra như một chiếc kìm thủy lực, bóp nghẹt cổ tay hắn, vặn ngược một góc chín mươi độ.

*RẮC!*

Xương cổ tay của hắn gãy lìa. Khẩu súng rơi tuột xuống mặt đất. Trước khi hắn kịp há mồm rên rỉ vì đau đớn, đầu ngón trỏ của tôi đã điểm thẳng vào huyệt Cự Khuyết trước ngực hắn, khiến toàn thân hắn co giật một hồi rồi tê liệt hoàn toàn, mềm oặt như một sợi bún thiu!

Toàn bộ quá trình phục kích và vô hiệu hóa hai tên tay sai trang bị vũ khí nóng chỉ diễn ra trong vòng chưa đầy bốn giây đồng hồ!

Tôi nhanh chóng kéo hai tên bất tỉnh cùng chiếc xe máy của chúng lủi sâu vào một căn chòi giữ vườn sầu riêng bỏ hoang cách con đường hơn năm mươi mét.

Lột bỏ áo khoác và mũ bảo hiểm của chúng, tôi tịch thu toàn bộ hai chiếc điện thoại di động, khẩu súng ngắn giảm thanh, hai con dao găm quân dụng và thiết bị định vị vệ tinh. Tôi dùng kìm bóp nát chiếc thẻ SIM cùng toàn bộ chip định vị GPS của chúng, tránh để tổng bộ Cửu Long Thiên Hải phát hiện tín hiệu bất thường.

Sau đó, tôi dùng những sợi dây dù quân dụng có sẵn trong ba lô trói chặt hai tên lại thành một khối vào cột kèo của căn chòi, nhét giẻ sạch vào mồm chúng.

Rút chiếc điện thoại thông minh bảo mật ra, tôi dùng một số ảo không thể truy vết, soạn một tin nhắn văn bản gửi trực tiếp vào đường dây nóng của Công an xã và Công an huyện Chợ Gạo:

*"Tại chòi giữ vườn hoang sau rạch dừa ấp Ba, có hai đối tượng lạ mặt tàng trữ vũ khí quân dụng trái phép và xe máy trộm cắp. Đề nghị lực lượng chức năng đến tiếp nhận xử lý."*

Giải quyết xong mối hiểm họa trực tiếp, tôi khoác bao đồ nghề lên vai, lặng lẽ bước ra khỏi căn chòi hoang.

Bốn giờ mười lăm phút chiều.

Cơn mưa rào mùa nước nổi bất chợt đổ xuống cù lao, giăng kín một màn sương trắng mờ ảo trên những ngọn dừa xanh mướt.

Tôi đứng nép mình sau rặng dừa nước rậm rạp bên bờ con rạch nhỏ, cách căn nhà lá ba gian của mẹ tôi chừng ba mươi mét qua mặt nước.

Từ phía đầu con đường đan rải đá dăm, một tiếng kêu quen thuộc vang lên giữa tiếng mưa rơi rả rích:

*Kẽo cà kẽo kẹt... kẽo cà kẽo kẹt...*

Đó là tiếng xích xe đạp cọc cạch của chiếc xe đạp Thống Nhất cũ kỹ mà ba tôi để lại từ hơn hai mươi năm trước.

Một người phụ nữ nhỏ nhắn, gầy gò trong bộ đồ bà ba màu nâu vá vai, đầu đội chiếc nón lá rách vành, đang còng lưng đẩy chiếc xe đạp chở hai chiếc sọt tre trống rỗng từ chợ huyện trở về.

Mẹ tôi!

Gương mặt mẹ sạm đen vì nắng gió sông hồ, những nếp nhăn nơi khóe mắt hằn sâu nỗi vất vả của một người mẹ đơn thân cả đời tảo tần nuôi con ăn học. Mẹ bước từng bước chậm rãi trên con đường trơn trượt vì mưa bùn, thỉnh thoảng lại dừng lại đưa bàn tay gầy guộc lên vuốt những giọt nước mưa chảy ròng ròng trên má.

Nhìn thấy dáng mẹ liêu xiêu dưới cơn mưa chiều, lồng ngực tôi nhói buốt như bị hàng ngàn mũi kim châm. Sống mũi tôi cay xè, nước mắt trào ra nơi khóe mi hòa lẫn với nước mưa lạnh buốt.

Tôi muốn lao ngay qua con rạch, muốn chạy lại đỡ lấy chiếc xe đạp cho mẹ, muốn ôm chầm lấy người mẹ già mà gọi một tiếng "Mẹ ơi!" cho thỏa nỗi nhớ nhung da diết.

Nhưng lý trí thép của một người tu Thể Đạo đã giữ chân tôi lại.

Tôi không thể bước ra!

Xung quanh tôi là chiếc bóng đen ngòm của Tập đoàn Cửu Long Thiên Hải. Nếu tôi xuất đầu lộ diện, nếu tôi để bất kỳ ai trong xóm nhìn thấy tôi trở về, ngôi nhà lá đơn sơ này sẽ không bao giờ còn có được một ngày bình yên. Kẻ thù sẽ dùng mẹ tôi để uy hiếp tôi, và ngọn lửa chiến tranh tàn khốc sẽ thiêu rụi mảnh đất cù lao hiền hòa này.

Để bảo vệ mẹ, tôi phải chấp nhận trở thành một kẻ vô hình trong bóng tối!

Chờ cho mẹ dựng chiếc xe đạp bên hiên, bước vào gian bếp sau để nhóm lửa đun ấm nước chè xanh, tôi hít sâu một hơi, vận chuyển Quy Tức Quyết lướt nhẹ qua mặt nước con rạch như một làn gió thoảng.

Tôi tiếp cận chiếc bàn gỗ tràm cũ kỹ kê ngoài hiên nhà — nơi ba tôi thuở sinh thời vẫn thường ngồi uống trà ngắm trăng.

Tôi nhẹ nhàng đặt lên mặt bàn một bọc vải dầu chống nước được buộc dây chuối cẩn thận:

Bên trong là toàn bộ số tiền tiết kiệm bốn mươi triệu đồng tôi đã rút từ trước, hai lọ cao xoa bóp thảo dược bí truyền làm dịu chứng đau khớp tuổi già, và một phong thư viết tay nắn nót với nội dung mạo danh một người học trò cũ của ba tôi ở Sài Gòn gửi biếu cô giáo cũ để an dưỡng tuổi già.

Đặt bọc đồ xuống bàn xong, tôi lùi lại ba bước, cúi đầu lạy ba lạy về phía gian bếp đang bốc lên làn khói lam chiều ấm áp.

"Mẹ ơi... tha lỗi cho con... Con đi rồi con sẽ về!"

Tôi thì thầm nghẹn ngào trong mưa, rồi xoay người, biến mất vào màn mưa rậm rạp của rặng dừa nước.

Năm giờ chiều.

Tôi đứng trên bến đò ven sông Tiền, phóng tầm mắt nhìn ra giữa lòng sông cuộn sóng.

Giữa màn mưa mù mịt, một cồn cát nổi hình đầu rùa khổng lồ hiện ra mờ ảo cách bờ hơn tám trăm mét. Trên đỉnh cồn cát, mái ngói rêu phong của Cổ Miếu Trấn Ba đứng sừng sững giữa ngàn trùng sóng gió.

Dưới đáy sông sâu thẳm, tiếng gầm gừ của mạch nước ngầm và dao động từ trường 0.12 Hz lại một lần nữa dội vang trong tủy ngọc của tôi.

Cọc tiêu thứ chín của Thủy Môn Thập Nhị Tiêu đang chờ đợi tôi!

Tôi siết chặt thanh Hắc Thiết Đoản Côn trong tay, ánh mắt rực sáng kiên định giữa cơn mưa chiều miền Tây sông nước!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3000 or word_count > 5500:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,000 - 5,000 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words)
    print(f"[*] [2/6] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường)...")
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

    # 3. Chạy EmotionDopamineEngine để đo lường cảm xúc
    print(f"[*] [3/6] Đo lường chỉ số cảm xúc độc giả qua EmotionDopamineEngine...")
    emo_eng = EmotionDopamineEngine(DB_PATH)
    emo_res = emo_eng.analyze_text(CHAPTER_NUM, raw_content, arc_id="arc_02")
    print(f"  -> Pathos Score: {emo_res['pathos_score']:.2f}/10.0")
    print(f"  -> Dopamine Score: {emo_res['dopamine_score']:.2f}/10.0")
    print(f"  -> Grounding Score: {emo_res['grounding_score']:.2f}/10.0")
    print(f"  -> Đánh giá nhịp độ: {emo_res['pacing_assessment']}")

    # 4. Chạy CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_lam_tich"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        return False
    print(f"[+] [4/6] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 5. Xuất bản Markdown với YAML Frontmatter và Heading H1
    frontmatter = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {word_count}
date: "{DATE}"
location: "{LOCATION}"
pathos_score: {emo_res['pathos_score']}
dopamine_score: {emo_res['dopamine_score']}
grounding_score: {emo_res['grounding_score']}
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

"""
    full_markdown = frontmatter + raw_content
    md_file_name = f"ch_{CHAPTER_NUM:03d}.md"
    md_file_path = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02", md_file_name)
    os.makedirs(os.path.dirname(md_file_path), exist_ok=True)
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(full_markdown)
    print(f"[+] [5/6] Đã xuất tệp Markdown chuẩn Frontmatter + H1: {md_file_path}")

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
    print(f"[+] [6/6] Đã xuất tệp Word (.docx): {docx_file_path}")

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
        "Thủy Lộ Sông Tiền, Bẻ Gãy Nanh Vuốt & Định Vị Cọc Tiêu Thứ Chín",
        CHAPTER_NUM,
        1,
        f"{DATE}T17:00:00+07:00",
        CHAPTER_NUM,
        "loc_cu_lao_song_tien",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An gửi xe máy tại Sài Gòn, ngụy trang thành thợ máy đường sông đi nhờ ghe gỗ qua kênh Chợ Gạo về Tiền Giang. Tại cù lao quê nhà, Minh An phát hiện hai tên gián điệp của Cửu Long Thiên Hải đang thám thính nhà mẹ già và chuẩn bị hỗ trợ đội trắc địa ngầm phá hủy Cổ Miếu Trấn Ba trên cồn cát sông Tiền (cọc tiêu thứ chín). Minh An bí mật phục kích điểm huyệt bắt sống cả hai tên gián điệp, bàn giao nặc danh cho công an xã xử lý. Đứng trong mưa nhìn mẹ cọc cạch đẩy xe đạp bán rau về nhà, Minh An nuốt nước mắt không lộ diện, âm thầm gửi lại tiền và thuốc dưỡng khớp trên bàn trà rồi hướng ra Cồn Trấn Ba chuẩn bị cho trận chiến bảo vệ cọc tiêu thứ chín.",
        "Tai mắt kẻ thù tại quê nhà bị triệt phá hoàn toàn; mẹ Minh An an toàn; Minh An định vị chính xác cọc tiêu thứ chín tại Cổ Miếu Trấn Ba giữa sông Tiền."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-TRG-001'
    """, (
        CHAPTER_NUM,
        "Minh An về đến cù lao Tiền Giang, bảo vệ mẹ thành công khỏi tai mắt thám thính và âm thầm gửi lại tiền tiết kiệm mà không xuất đầu lộ diện."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Định vị thành công cọc tiêu thứ chín tại Cổ Miếu Trấn Ba (Cồn cát nổi giữa sông Tiền, Tiền Giang); 8/12 cọc tiêu đã giải quyết, cọc thứ chín chuẩn bị khai chiến."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An vận hành thuần thục Luyện Cốt Hậu kỳ Cùng Cực và Quy Tức Cùng Cực, sẵn sàng nghênh chiến phân đà miền Tây của Cửu Long Thiên Hải."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T17:00:00+07:00"
        inv_data["current_location"] = "Cù Lao Ven Sông Tiền, Tỉnh Tiền Giang"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ Cùng Cực (33 Đốt Sống Ngọc Tủy Viên Mãn / Chuẩn Bị Hoán Huyết)"

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

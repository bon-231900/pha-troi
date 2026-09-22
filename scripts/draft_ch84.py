# -*- coding: utf-8 -*-
"""Draft Chapter 84 for Phá Trời Novel OS with ~3,700+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 84
CHAPTER_TITLE = "Cực Nam Phong Hải"
DATE = "2026-10-27"
LOCATION = "Rừng Đước Năm Căn & Đất Mũi Cà Mau"

ACT1 = '''Sáu giờ ba mươi phút sáng ngày hai mươi bảy tháng mười.

Chiếc xe khách liên tỉnh chở tôi vượt qua bến phà Năm Căn cũ, tiến thẳng vào dải đất cuối cùng của bán đảo Cà Mau.

Sau lưng tôi, cuộc đụng độ dữ dội trên sông Cổ Chiên đêm qua đã lùi xa hàng trăm cây số. Chuyến hành trình xuyên đêm đưa tôi lướt qua những cánh đồng muối Bạc Liêu trắng lóa dưới ánh trăng tàn, qua những ngôi cổ tự Khmer trầm mặc với mái cong vút vươn lên giữa rặng thốt nốt Sóc Trăng, rồi men theo những con kênh xáng xẻ dọc xẻ ngang vùng bán đảo Cà Mau.

Nhờ an định kịp thời cọc tiêu thứ mười một Cổ Chiên Thủy Long Quyết, toàn bộ mạng lưới thủy mạch từ sông Tiền qua sông Hậu đã được liên kết vững chắc, khôi phục lại thế phong thủy cân bằng cho khắp vùng châu thổ màu mỡ.

Nhưng lòng tôi không hề có lấy một giây phút nào để buông lỏng cảnh giác.

Trước mắt tôi, con đường thiên lý đưa tôi đến với điểm chót cùng của dải đất hình chữ S: Đất Mũi Cà Mau. Nơi đất biết nở, rừng biết đi, nơi mỗi một tấc phù sa bồi đắp hàng năm đều thấm đẫm mồ hôi, nước mắt và máu xương của bao thế hệ tiền nhân đi mở cõi.

Ngồi bên cửa sổ xe khách, tôi phóng tầm mắt ra hai bên bờ sông Cửa Lớn mênh mông sóng nước.

Rừng đước Năm Căn bạt ngàn ngút ngàn tầm mắt, xanh thẫm một màu kiên cường trước ngọn gió chướng từ biển Tây Nam thổi thốc vào bờ. Những thân đước vươn thẳng tắp kiêu hãnh lên nền trời lam biếc, chùm rễ đước ken dày đan bện chằng chịt vào nhau như hàng triệu cánh tay gân guốc cắm sâu vào lòng bùn non lầy lội.

Đó không đơn thuần là một hệ sinh thái rừng ngập mặn hoang sơ, mà là bức thành trì xanh vĩ đại của đất nước. Những chiếc rễ đước ấy giữ lại từng hạt phù sa từ thượng nguồn đổ về, kiên nhẫn bồi đắp bờ bãi, che chắn cho hàng triệu người dân khỏi sự tàn phá hung hãn của bão táp đại dương.

Tôi nhớ về mẹ tôi nơi cù lao Tiền Giang êm đềm, nhớ về căn gác trọ nhỏ che mưa che nắng ở quận Bình Thạnh giữa lòng Sài Gòn náo nhiệt. Những con người bình dị, những mảnh đời lam lũ mà tôi từng gặp trên suốt dặm dài đất nước — từ ông lão lái đò râu tóc hoa râm ở bến Gò Công, bác thợ sửa máy tàu đường sông ở kênh Chợ Gạo, cho tới những người nông dân chân lấm tay bùn — chính là linh hồn của mảnh đất này.

Bảo vệ long mạch, với tôi chưa bao giờ là một khái niệm huyền học xa vời. Đó là bảo vệ sự bình yên cho từng mái nhà tranh, từng mảnh vườn cây ăn trái, từng bữa cơm gia đình đầm ấm của đồng bào mình.

Tôi đặt hai tay lên đầu gối, nhắm mắt tĩnh tâm, lắng nghe sự biến chuyển vi mô đang cuộn trào mãnh liệt bên trong cốt tủy.

Sau khi tiếp nhận luồng địa khí thanh thuần từ mười một cọc tiêu khắp phương Nam, ba mươi ba đốt sống ngọc tủy của tôi lúc này đang rung lên những tiếng rền vang trầm hùng tựa tiếng sấm ngầm dưới đáy vực. Hiện tượng sôi tủy đã đạt đến đỉnh điểm viên mãn!

Cảm giác nóng rực bỏng rát lan tỏa từ đốt sống cùng cụt, men theo tủy sống dâng trào lên tận đỉnh đầu. Dưới sự vận hành miệt mài của quy tức cùng cực, từng giọt tạp chất sinh học li ti còn sót lại trong tủy xương bị nhiệt lượng Thuần Dương thiêu rụi hoàn toàn, bài tiết qua hàng triệu lỗ chân lông thành một làn sương mỏng manh rồi tan biến vào không khí.

Trong từng khối xương ngọc thạch sáng trong như ngọc bích, một quá trình tạo huyết kỳ diệu đang diễn ra với tốc độ phi thường.

Đó không còn là phàm huyết bình thường của người phàm tục. Từng giọt huyết tương đỏ thẫm ánh lên sắc kim quang ấm áp, mang theo mật độ năng lượng và hàm lượng dưỡng khí cao gấp hàng chục lần máu thông thường. Chúng cuộn trào chảy vào tâm thất, được trái tim dũng mãnh bơm đi khắp mười hai kinh mạch chính, nuôi dưỡng từng thớ cơ bắp, màng gân và dây chằng của tôi thêm phần dẻo dai phi thường.

Cảnh giới Hoán Huyết — đại cảnh giới tiếp theo của Thể Đạo phàm nhân sau Luyện Cốt — đã bắt đầu hé mở cánh cửa kỳ vĩ!

Tôi khẽ hướng tâm thức vào sâu trong thức hải bao la.

Đài sen ngọc bích của Lâm Tịch lúc này đang trôi bồng bềnh giữa một quầng sáng màu lam ngọc rạng rỡ. Vết rạn xám tro từng khiến nàng suýt hồn phi phách tán sau trận kịch chiến ở Hàng Xanh nay đã gần như liền miệng hoàn toàn, chỉ còn lại một vết sẹo mờ nhạt tựa sợi chỉ bạc mỏng manh.

Đột nhiên, một rung động tinh thần dịu dàng nhưng vô cùng rõ ràng truyền thẳng vào tâm trí tôi:

"Minh An... anh đã đến Cà Mau rồi sao?..."

Tiếng thì thầm yếu ớt quen thuộc của Lâm Tịch khiến lồng ngực tôi thắt lại trong niềm xúc động khôn xiết.

"Lâm Tịch! Cô đã tỉnh lại rồi?"

"Tôi mới chỉ hồi phục được một phần linh thức nhờ luồng sinh khí long mạch mà anh không ngừng thu thập từ mười một cọc tiêu... Nhưng Minh An, anh phải tuyệt đối cẩn trọng. Cọc tiêu thứ mười hai ở Mũi Cà Mau chính là Trận Nhãn Tối Cao của toàn bộ mười hai cọc Thủy Môn. Nơi đó là ngã ba hải lưu giao thoa giữa biển Đông và vịnh Thái Lan, áp lực địa từ vô cùng hỗn loạn và dữ dội. Kẻ thù chắc chắn sẽ dốc toàn bộ nguồn lực nguy hiểm nhất để ngăn cản anh..."

"Tôi hiểu. Dù kẻ thù có là ai, tôi cũng quyết không lùi bước. Cô hãy yên tâm dưỡng thần, việc còn lại cứ để tôi gánh vác."

Ý niệm của Lâm Tịch khẽ gật đầu, truyền lại một luồng hơi ấm dịu dàng rồi thu liễm vào sâu trong đài sen ngọc bích để tiếp tục bồi bổ nguyên khí.

Tôi siết chặt nắm tay, cảm nhận từng dòng máu mới đang rần rật chảy qua ba mươi ba đốt sống tủy ngọc. Cọc tiêu cuối cùng đang ở ngay trước mắt. Dù phía trước có là đầm lầy vực sâu hay thiên la địa võng, tôi nhất định sẽ san bằng!'''

ACT2 = '''Mười lăm giờ ba mươi phút chiều.

Ca-nô cao tốc đưa tôi cập bến xóm Mũi thuộc xã Đất Mũi, huyện Ngọc Hiển.

Gió biển phương Nam thổi ào ạt từ hai phía: một bên là biển Đông ngầu đục phù sa đỏ thắm, một bên là vịnh Thái Lan xanh ngắt màu ngọc bích sâu thẳm. Hai khối nước biển khổng lồ gặp nhau nơi mũi đất tận cùng tạo nên những con sóng giao thoa cuộn trào bọt trắng xóa, ngày đêm rì rào vỗ vào mỏm bùn bãi bồi quanh năm lấn biển.

Tôi khoác chiếc ba-lô dù sẫm màu, bước đi trên con đường lát bê-tông uốn lượn dưới tán rừng đước ngập mặn cổ thụ. Không gian tĩnh mịch hoang sơ, chỉ có tiếng chim hải âu chao liệng trên nền trời xanh ngắt và tiếng còng gió, ba khía lách chách bò trên bãi bùn lầy màu mỡ.

Tiến về phía mốc tọa độ quốc gia GPS 0001 — biểu tượng con tàu kiêu hãnh vươn khơi của tổ quốc — chiếc la bàn địa từ trên cổ tay tôi bắt đầu quay tít điên cuồng.

Kim địa từ dao động liên tục ở tần số 0.12 Hz, biên độ xung lực mạnh chưa từng thấy, dội ngược lên từ vùng bãi bồi ngập nước cách bờ biển chừng tám trăm mét về hướng Tây Nam!

Đó chính là nơi an vị của cọc tiêu thứ mười hai: **Cà Mau Trấn Hải Thần Sa**!

Theo các ghi chép cổ xưa mà tiền nhân Thủ Hộ Nhất Mạch lưu truyền, cọc tiêu thứ mười hai là một khối thạch anh bazan khổng lồ nguyên khối mang hình mũi tàu rẽ sóng. Cột đá thiêng này được các bậc tiền hiền phong ấn sâu dưới thềm đá mẹ kỷ đệ tứ nơi rốn biển Cà Mau từ hàng trăm năm trước, giữ vai trò then chốt nhất: làm điểm tựa quy tụ toàn bộ long mạch phương Nam, điều hòa phản lực giữa hai luồng hải lưu Thái Bình Dương và Ấn Độ Dương.

Nếu không có cọc tiêu Trấn Hải Thần Sa này neo giữ, toàn bộ mũi đất trũng thấp của Cà Mau và dải bờ biển Tây Nam đã sớm bị những cơn sóng triều đại dương xâm thực và cuốn phăng từ lâu.

Tôi men theo một lạch nước nhỏ quanh co rậm rạp rễ đước, leo lên một cọc ngắm cao nhô khỏi bãi bồi, dùng ống nhòm quang học tầm xa quan sát ra ngoài khơi.

Cảnh tượng trước mắt khiến mày tôi nhíu chặt lại.

Cách mỏm đất mũi chừng tám trăm mét, một chiếc tàu nghiên cứu đại dương cỡ lớn dài hơn bảy mươi mét mang cờ hiệu quốc tế giả mạo đang thả bốn mỏ neo cố định sừng sững giữa vùng nước nông bãi bồi. Xung quanh chiếc tàu lớn, bốn chiếc bè nổi chuyên dụng lắp ráp bằng khung thép chịu lực đang vây quanh một vùng nước sủi bọt khí sùng sục.

Trên bốn chiếc bè nổi, những máy phát xung điện từ trường công suất cực đại đang liên tục phóng những luồng sóng siêu âm hình nón cắm thẳng xuống lòng đất đáy biển!

Dưới tác động phá hoại của sóng xung kích cao tần, lớp bùn non ngàn năm bảo vệ chân móng cột đá bazan đang bị xới tung, bốc lên từng luồng khí đen kịt hôi nồng mùi lưu huỳnh tà ác.

Đặc biệt, trên sàn chiếc tàu khảo sát chính, tôi nhận ra một bóng người quen thuộc đang đứng chắp tay nhìn ra biển: Tạ Bách Xuyên — phó tổng giám đốc phụ trách an ninh đặc nhiệm của Tập đoàn Cửu Long Thiên Hải!

Lão mặc bộ đồ ký giả màu xám tro, gương mặt gầy gò nham hiểm lộ rõ vẻ sốt ruột. Bên cạnh lão là hơn chục tay lính đánh thuê thiện chiến mặc áo giáp chống mảnh văng, tay lăm lăm những khẩu súng phóng xung điện tầm nhiệt và súng bắn lao cơ giới áp lực cao.

"Các người chuẩn bị nhanh lên! Chỉ cần phá hủy khối thạch anh bazan trấn hải này trước khi con nước triều biển Tây đạt đỉnh, toàn bộ mạng lưới phong ấn phương Nam sẽ sụp đổ dây chuyền! Khi đó, không một ai có thể ngăn cản đại kế của tập đoàn!"

Tiếng quát the thé đầy vẻ hung tàn của Tạ Bách Xuyên theo gió biển lọt vào tai tôi.

Tôi hít một hơi thật sâu, ánh mắt sắc lạnh như lưỡi dao thép.

Chúng đã dồn toàn bộ nguồn lực công nghệ và tà thuật tinh vi nhất về đây hòng tung ra đòn chí mạng cuối cùng. Nếu để chúng làm nứt vỡ cột thạch anh bazan Trấn Hải Thần Sa, mười một cọc tiêu trước đó sẽ mất đi điểm tựa quy tụ, toàn bộ công sức của bao ngày qua sẽ tan thành mây khói.

Nhưng chúng đã đánh giá quá thấp ý chí kiên định của một kẻ thủ hộ phàm nhân!'''

ACT3 = '''Hai mươi giờ bốn mươi lăm phút đêm.

Màn đêm buông xuống Đất Mũi mịt mùng không một ánh sao. Thủy triều biển Tây dâng cao cuồn cuộn với vận tốc kinh hoàng, nhấn chìm toàn bộ bãi bồi dưới lớp nước mặn sâu hơn ba mét.

Gió biển gầm rít từng cơn điên đảo, sóng lớn chồm qua mạn bè nổi tạo nên những âm thanh ầm ầm vang dội như tiếng gầm của muôn ngàn dã thú.

Đó chính là thời khắc hành động hoàn hảo nhất.

Tôi cởi bỏ chiếc ba-lô và quần áo ngoài, chỉ mang chiếc quần lặn co giãn đen tuyền ôm sát cơ thể. Thanh Trấn Thủy Đoản Đao giắt chặt bên hông phải, thanh Hắc Thiết Đoản Côn nẹp chéo sau lưng bằng đai dù quân sự.

Vận chuyển quy tức cùng cực, nhịp tim tôi hạ xuống mức tối thiểu ba mươi nhịp một phút. Các lỗ chân lông toàn thân khép chặt, dòng máu mới mang kình lực cương dương ấm áp chảy tuần hoàn khép kín trong nội tạng, triệt tiêu hoàn toàn sự xâm nhập của hơi lạnh biển đêm buốt giá.

*TÕM!*

Tôi trượt mình xuống làn nước mặn cuộn sóng, không hề tạo ra một tiếng động hay bọt khí nào.

Thay vì bơi trên mặt nước nơi ánh đèn pha và camera tầm nhiệt quét qua, tôi áp dụng tuyệt kỹ Đạp Sa Vô Ngân của Thể Đạo, mượn lực đẩy của các luồng nước ngầm cuộn xoáy để lướt sát mặt đáy bùn sâu. Ba mươi ba đốt sống tủy ngọc của tôi co giãn nhịp nhàng, hấp thụ toàn bộ chấn động của sóng triều, giúp tôi tiếp cận cụm bè nổi của quân địch chỉ sau vài phút.

Tiếp cận chiếc bè nổi thứ nhất, tôi thấy rõ sợi cáp cao thế bọc thép truyền dẫn xung kích đang rung bần bật dưới làn nước đục ngầu.

Rút thanh Trấn Thủy Đoản Đao ra khỏi bao, tôi dồn kình lực hoán huyết vào lưỡi đao. Một vệt sáng đỏ thẫm ánh kim bùng lên rực rỡ xé toạc bóng tối đáy biển!

*XOẸT!*

Lưỡi đao sắc bén chém đứt ngọt xớt cụm cáp dẫn tín hiệu và ống thủy lực của cỗ máy phát sóng siêu âm. Cỗ máy lập tức nổ tung những tia lửa điện lách tách dưới nước rồi chìm vào câm lặng.

"Báo động! Cụm phát sóng số một mất tín hiệu hoàn toàn!"

Tiếng la hét hỗn loạn vang lên từ trên tàu chính. Những chùm đèn pha công suất lớn rọi xuống mặt biển quét tìm điên cuồng.

Không cho chúng cơ hội kịp thời phản ứng, tôi thoăn thoắt lướt qua ba chiếc bè còn lại dưới đáy sâu, liên tiếp vung đao chém đứt toàn bộ các đường dây truyền dẫn, vô hiệu hóa hoàn toàn cỗ máy phá hoại của Cửu Long Thiên Hải!

"Là nó! Nguyễn Minh An! Bắn! Bắn chết nó cho tao!"

Tạ Bách Xuyên gầm lên điên cuồng trên boong tàu. Hàng chục ngọn lao thép áp lực cao cùng đạn xung điện xé nước lao vun vút về phía tôi.

Tôi búng người vọt lên khỏi mặt biển như một cánh hải âu lướt sóng, đạp lên một phao thép bè nổi rồi lộn người đáp thẳng xuống sàn boong chiếc tàu nghiên cứu chính!

Bốn tên lính đánh thuê hung hãn mặc giáp chống đạn giương vũ khí lao tới bao vây tôi từ bốn góc.

Tôi vung thanh Hắc Thiết Đoản Côn ra như rồng vờn mây. Đòn Du Thân Bổng kết hợp với kình lực ngọc tủy đánh chuẩn xác vào khớp cổ tay và huyệt Đản Trung của từng tên, chấn văng vũ khí và làm tê liệt toàn bộ hệ thần kinh vận động của chúng chỉ trong ba hơi thở ngắn ngủi!

Tạ Bách Xuyên thấy toán tay sai tinh nhuệ ngã rạp trong chớp mắt thì mặt cắt không còn hạt máu. Lão nghiến răng rút ra một thanh đoản kiếm nẹp điện cao thế, dồn toàn bộ tà khí đâm thẳng vào yết hầu tôi:

"Thằng nhóc phàm nhân, chết đi cho tao!"

Tôi không hề né tránh, ánh mắt bình thản nhìn thẳng vào mũi kiếm đang lao tới.

Tay trái tôi đưa ra như một chiếc kìm thép bọc ngọc thạch, chộp chuẩn xác vào cổ tay cầm kiếm của lão. Đồng thời, ba mươi ba đốt sống lưng của tôi rền vang một tiếng giòn giã, dồn toàn bộ kình lực Thuần Dương Cương Huyết vào lòng bàn tay!

*RẮC!*

Thanh kiếm nẹp điện vỡ vụn thành nhiều mảnh vụn kim loại. Cổ tay của Tạ Bách Xuyên bị trật khớp gập ngược ra sau. Cú hích vai tiếp theo của tôi đập thẳng vào lồng ngực lão, đánh bay thân hình gầy guộc của lão đập sầm vào vách cabin thép, khiến lão ngất lịm ngay tại chỗ.

Giải quyết xong toàn bộ quân địch trên boong, tôi lao mình trở lại lòng biển sâu mênh mông.

Ở độ sâu mười lăm mét dưới thềm cát bãi bồi nơi giao thoa của hai dòng hải lưu, khối đá thạch anh bazan **Cà Mau Trấn Hải Thần Sa** cao hơn năm mét sừng sững cắm sâu vào lòng đất mẹ. Trên thân đá, hình hài mũi tàu kiêu hãnh rẽ sóng biển Đông và biển Tây hiện lên trang nghiêm, phát ra những vệt sáng lam ngọc dịu dàng dưới làn nước trong vắt.

Tôi bơi tới, áp trọn hai bàn tay ấm nóng của mình lên thân đá bazan nghìn năm.

Dòng máu mới trong cơ thể tôi — những tế bào máu Hoán Huyết mang kình lực cương dương bừng cháy — lập tức cộng hưởng mãnh liệt với mạch đá ngàn năm của tổ quốc.

*UỲNH... UỲNH... UỲNH...!*

Một chuỗi âm thanh trầm hùng như tiếng trống đồng từ thời dựng nước rung chuyển cả thềm lục địa phương Nam!

Từ khối đá Trấn Hải Thần Sa nơi Đất Mũi Cà Mau, một cột sáng vàng rực rỡ bùng lên, phóng thẳng lên vòm trời đêm rồi phân nhánh thành mười hai dải sáng lung linh tỏa đi khắp bốn phương tám hướng:

Núi Sam, Thất Sơn, Kênh Vĩnh Tế, Ngã Bảy, Sóc Trăng, Cồn Tân Phong, Núi Chứa Chan, Rãnh Cực Tù Hải Uyên, Cổ Miếu Trấn Ba, Soài Rạp Hải Giáp Trụ, Cổ Chiên Thủy Long Quyết, và Trận Nhãn Mũi Cà Mau!

Mười hai cọc tiêu Thủy Môn phương Nam đồng loạt bừng sáng, kết nối lại thành một đồ hình đại trận hoàn mỹ bảo vệ vững chắc từng tấc đất, từng dòng sông của giang sơn bờ cõi!

Cùng lúc đó, một luồng địa khí thanh khiết vô biên dội ngược từ lòng đất mẹ vào thân thể tôi.

Ba mươi ba đốt sống lưng của tôi sáng rực như ngọc thạch liên hoa thấu quang. Toàn bộ dòng máu trong cơ thể tôi được thay mới hoàn toàn, chuyển hóa thành Thuần Dương Cương Huyết viên mãn, đẩy thể phách phàm nhân của tôi chính thức bước vào cảnh giới **Hoán Huyết Sơ kỳ**!

Một cảm giác nhẹ nhõm, thanh thản và tràn đầy sinh lực dâng trào trong từng huyết quản.

Tôi trồi lên khỏi mặt biển khi vầng thái dương đỏ ối từ từ nhô lên từ phía đường chân trời biển Đông rực rỡ.

Gió sớm Đất Mũi thổi lồng lộng qua mái tóc ướt đẫm phù sa thiêng liêng. Dưới chân tôi, từng đợt sóng bạc đầu hiền hòa vỗ về mỏm đất tận cùng của tổ quốc.

Mười hai cọc tiêu Thủy Môn đã an định trọn vẹn!

Hành trình bảo vệ long mạch phương Nam đã hoàn thành sứ mệnh lịch sử rực rỡ nhất, mở ra một chương mới đầy kiêu hãnh cho con đường Thể Đạo phàm nhân!'''

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
description: "Minh An tiến về Đất Mũi Cà Mau, phá tan dàn bè nổi siêu âm và đả bại Tạ Bách Xuyên, an định cọc tiêu thứ mười hai Trấn Hải Thần Sa, đột phá Hoán Huyết Sơ kỳ."
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
        "Đến Đất Mũi Cà Mau, Phá Dàn Bè Siêu Âm, Đả Bại Tạ Bách Xuyên & Hoàn Tất An Định 12 Cọc Tiêu Thủy Môn, Đột Phá Hoán Huyết",
        CHAPTER_NUM,
        1,
        f"{DATE}T21:00:00+07:00",
        CHAPTER_NUM,
        "loc_dat_mui_ca_mau",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An tiến về cực Nam tổ quốc tại Đất Mũi Cà Mau, nơi tọa lạc cọc tiêu thứ mười hai Trấn Hải Thần Sa. Phát hiện tàu khảo sát của Tạ Bách Xuyên cùng 4 bè nổi phát xung siêu âm mưu toan làm sụp đổ thềm địa tầng rốn biển. Minh An lặn sâu cắt toàn bộ cáp tín hiệu, đột kích boong tàu đả bại toán lính đánh thuê và chấn nát kiếm điện của Tạ Bách Xuyên. Chạm tay vào cột thạch anh bazan Trấn Hải Thần Sa, kích hoạt thành công toàn bộ 12 cọc tiêu Thủy Môn phương Nam, hoàn tất đại trận phong ấn, đồng thời hấp thu địa khí đột phá cảnh giới Hoán Huyết Sơ kỳ.",
        "Cọc tiêu thứ mười hai Trấn Hải Thần Sa an định hoàn toàn; 12/12 cọc tiêu Thủy Môn phương Nam đại công cáo thành; đả bại Tạ Bách Xuyên; Minh An chính thức đột phá cảnh giới Hoán Huyết Sơ kỳ."
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
        "Toàn bộ 12 cọc tiêu Thủy Môn phương Nam đã an định 100% sau khi kích hoạt Trấn Nhãn Cực Nam tại Mũi Cà Mau; đại trận Thủy Môn hoàn thành liên kết vững chắc."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An chính thức hoàn thành giai đoạn Luyện Cốt, đột phá bước vào đại cảnh giới Hoán Huyết Sơ kỳ nhờ dòng Thuần Dương Cương Huyết mới và địa khí phương Nam."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch hồi phục một phần linh thức, giao tiếp ngắn ngủi với Minh An trước khi đại trận 12 cọc tiêu hoàn tất bồi bổ nguyên khí."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T21:00:00+07:00"
        inv_data["current_location"] = "Đất Mũi Cà Mau & Rừng Ngập Mặn Năm Căn, Cà Mau"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Thuần Dương Cương Huyết Viên Mãn / Cốt Tủy Thấu Quang)"

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

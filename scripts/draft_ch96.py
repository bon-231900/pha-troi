# -*- coding: utf-8 -*-
"""Draft Chapter 96 for Phá Trời Novel OS: Hải Yến.
Standardized pipeline matching Chapter 95 architecture.
Target length: 3,800 - 4,100 words. Zero meta-words, zero 'huyết mạch', zero bold.
"""

import os
import sys
import json
import sqlite3
import re

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine
from system.engines.emotion_dopamine_engine import EmotionDopamineEngine

CHAPTER_NUM = 96
CHAPTER_TITLE = "Hải Yến"
DATE = "2026-11-04"
LOCATION = "Cầu Tàu Dã Chiến & Trạm Khảo Sát Thủy Văn Duyên Hải, Vịnh Xuân Đài, Thị Xã Sông Cầu, Tỉnh Phú Yên"

ACT1 = '''Chiếc xe bán tải hai cầu của Viện Khảo sát Địa chất gầm rú vượt qua những khúc cua tay áo cuối cùng của đèo Phượng Hoàng.

Mùi khói củi và hương thông ngai ngái của Chư Yang Sin dần lùi lại sau lưng. Càng xuôi về phía đông, không khí trong cabin càng ẩm ướt, mang theo vị muối nồng gắt của gió biển miền Trung thốc qua khe kính hé mở.

Kỹ sư Tuấn ngồi ôm vô lăng, ngón trỏ gõ lách cách theo nhịp nổ trầm đục của động cơ dầu bốn chấm không. Gương mặt anh sạm đen sau những đêm thức trắng trên cao nguyên bazan, miệng ngậm mẩu thuốc lá sâu kèn:

— Cái đèo này nuốt dầu như voi uống nước mía! Vừa thoát lò than lưu huỳnh Chư Yang Sin chưa kịp thở thì Viện trưởng đã giục chạy thục mạng xuống biển. Cái gầm xe bám đầy bụi đỏ, giờ đâm đầu vào hơi muối mặn chát xứ Nẫu, tối nay không rửa kỹ thì rỉ sét nát hết mấy cái khớp chữ thập của tao!

Tôi ngồi ghế phụ, khẽ cười nhìn những bãi cát trắng và rặng phi lao bắt đầu hiện ra sau những mái ngói rêu phong ven quốc lộ:

— Anh Tuấn lo xa quá. Xe của Viện bọc gầm ba lớp hợp kim chịu lực, đi rừng lội suối cả tháng trời có hề hấn gì đâu. Tín hiệu hạ âm từ Sector 05 Hòn Yến không đợi mình được đâu anh.

Ở băng sau, Viện trưởng Trần Minh Nam đang cặm cụi mở máy tính bảng quân sự, soi từng lát cắt bản đồ độ sâu quét sườn của vùng biển Phú Yên. Nghe chúng tôi trò chuyện, ông ngẩng đầu lên, tháo cặp kính lão kẹp vào túi áo:

— Cậu Tuấn đừng cằn nhằn nữa. Lần này khảo sát trận nhãn rạn nứt bazan ngầm ở đảo Hòn Yến khó khăn gấp bội lần trên cạn. Vùng biển đó đáy sâu hơn sáu mươi mét, bên dưới là quần thể cột đá bazan hình lăng trụ lục giác chìm sâu trong nước, dòng hải lưu xoáy ngầm xé rách mọi thiết bị định vị. Nếu chỉ dựa vào đám thợ máy cạn của cậu thì xe với tời có mà vứt cho cá gặm.

Anh Tuấn liếc kính chiếu hậu, nhăn nhở cười lộ chiếc răng khểnh:

— Ấy, tời thủy lực năm tấn của con vừa kéo sập cửa hang dơi Chư Yang Sin kia kìa. Ra biển thì cũng chỉ thả dây xuống nước thôi chứ có gì ghê gớm đâu thầy!

— Thả dây xuống nước mà cậu tưởng như thả câu ở kênh Nhiêu Lộc hả? — Viện trưởng Nam lắc đầu: — Đáy biển Hòn Yến là địa hình rạn san hô bazan tổ ong nghìn năm tuổi, nước luồn qua các hang hốc đá ngầm tạo thành những túi chân không áp suất cực lớn. Thợ lặn thiếu kinh nghiệm xuống đó ba phút là mạch máu mũi vỡ toang vì bệnh giảm áp. Sáng nay Tổng cục đã điều động một kỹ sư trắc địa hải văn kiêm thợ lặn kỹ thuật cao tinh nhuệ nhất phân trạm duyên hải ra đón đoàn ta tại Vịnh Xuân Đài làm hoa tiêu dẫn đường.

Anh Tuấn nhướng mày, bĩu môi:

— Lại mấy đứa nhỏ tốt nghiệp đại học ra vẻ ta đây chứ gì? Cứ đợi đấy, lát nữa ra cầu tàu gặp sóng cồn cấp năm say lảo đảo thì khóc ròng, cuối cùng cũng phải đến tay anh Tuấn búa tạ này khiêng bình dưỡng khí cho coi!

Tôi không tham gia cuộc tranh luận. Đôi mắt tôi hướng ra mặt vịnh phẳng lặng như tấm gương khổng lồ đang mở rộng trước mũi xe. Dưới lòng bàn tay tôi, thanh Trấn Thủy Đoản Đao bọc trong bao da bò giắt bên hông bỗng khẽ rung lên một nhịp cực nhỏ. Đó là sự cộng hưởng kỳ lạ giữa kim loại cổ xưa và dòng nước mặn mòi của biển cả.'''

ACT2 = '''Chiếc xe bán tải đỗ xịch trước dãy nhà tôn lạnh của Trạm Khảo sát Thủy văn & Địa chất Biển Duyên hải Nam Trung Bộ, nép mình bên mép nước kín gió của Vịnh Xuân Đài.

Phía xa ngoài cửa lạch, những khối núi đá bazan sừng sững nhô lên khỏi làn nước xanh biếc. Gió biển thổi lồng lộng, mang theo mùi muối nồng và tiếng sóng vỗ ì oạp vào chân cọc gỗ chiếc cầu tàu dã chiến.

Vừa bước xuống xe, tiếng máy nổ xình xịch đinh tai đã dội thẳng vào màng nhĩ. Trên cầu tàu gỗ, một cụm máy tời cáp dã chiến đang xả từng luồng khói đen xì xì lên nền trời. Nhưng điều khiến tôi chú ý là cụm bọt khí trắng xóa đang sủi tăm cuồn cuộn dưới nước sát chân cọc.

Mặt nước xanh thẫm đột ngột rẽ đôi. Một bóng người từ đáy vịnh vút lên, hai tay bám chuẩn xác vào thanh giằng gỗ rồi đu mình trồi lên khỏi mặt nước với động tác dọn gàng, dứt khoát.

Đó là một cô gái.

Tôi khẽ chớp mắt, bước chân dừng lại trên bờ cát.

Cô gái có vóc dáng cao ráo nổi bật, chừng một mét sáu mươi tám. Thân hình thon dài, vai thẳng, eo thắt gọn và đôi chân dài dẻo dai toát lên vẻ đẹp khỏe khoắn của thợ lặn chuyên nghiệp. Nàng mặc bộ đồ lặn cao su neoprene đen tuyền ôm sát đường nét cơ thể, hai bên hông và bắp đùi chạy dọc dải viền cam phản quang. Trên lưng nàng là bình khí đôi màu vàng chanh, thắt lưng dù giắt dao lặn titan cùng cụm đồng hồ đo áp suất ba cổng.

Cô gái tháo cặp chân vịt vắt lên thành cầu tàu, đưa đôi bàn tay mang găng kéo phăng chiếc nón trùm lặn xuống cổ. 

Nàng lắc mạnh đầu. Mái tóc đen nhánh, dày và ướt sũng buông xõa xuống tận thắt lưng trong tích tắc, óng ả như dải lụa đen huyền bí giữa trời biển bao la.

Thế nhưng vẻ nữ tính dịu dàng ấy chỉ tồn tại trong đúng ba giây.

Rất thuần thục, cô gái đưa tay với chiếc kẹp cơ khí bằng thép giắt trên quai ngực, thoăn thoắt gom toàn bộ mái tóc ướt cuộn tròn rồi búi chặt thành búi củ tỏi cao vút sau gáy. Chiếc cổ thon dài trắng ngần cùng bờ vai rám nắng mật ong lộ ra hoàn toàn dưới nắng chiều. Thần thái nàng lập tức biến thành một nữ chỉ huy thực địa sắc sảo, đanh thép và đầy vẻ ngạo nghễ phong trần.

Gương mặt nàng mang nét trái xoan thanh tú nhưng quai hàm kiên định. Đôi mắt to hai mí sáng trong veo, đuôi mắt hơi xếch tự nhiên toát lên nét bướng bỉnh khó thuần phục. 

Nàng sải bước dài về phía chiếc máy tời đang xả khói trên cầu tàu, vươn ngón tay bấm phím ngắt khẩn cấp trên thân máy. 

Tiếng máy nổ gầm rú lập tức câm bặt. Làn khói tan dần, trả lại không gian tĩnh lặng cho mặt vịnh. 

Cô gái quay ngoắt lại, trừng mắt nhìn kỹ sư Tuấn:

— Mấy ông nội ở Sài Gòn ra đây làm ăn kiểu gì kỳ cục vậy hả?! Ai cho phép các người đem cái máy nổ này ra xả khói thẳng xuống nước sát chân phao tiêu vậy?! Khói muội than với bọt khí nó tạo ra túi bọt dày cả tấc dưới chân cầu tàu, sóng âm của đầu dò sonar quét sườn dội ngược lại nát bét hết dải dữ liệu trắc địa của tui rồi kìa! Có biết tui phải lặn ngâm nước suốt ba tiếng đồng hồ để cân chỉnh từng cái đế cảm biến không hả?!

Anh Tuấn đang vênh váo bỗng khựng lại, hai tay vẫn ôm cuộn cáp nặng trịch, miệng há hốc. Một gã thợ máy kỳ cựu từng lăn lộn khắp công trường Nam Bộ vậy mà lúc này bị một cô gái trẻ chỉ thẳng mặt mắng xối xả.

— Ơ... này cô em... Cái máy tời dầu này là đồ cơ khí chuẩn của Viện mang từ thành phố ra đó nghen!

— Chuẩn mà lắp ống xả chĩa thẳng xuống nước hả bác tài? — Cô gái khoanh tay trước ngực, nhướng mày sắc lẻm, khóe miệng lộ mẩu kẹo cao su bạc hà đang nhai dở: — Cơ khí đất liền thì ôm lấy cái máy mà đào đất, ra đến biển cả thì phải học lại nguyên lý thủy âm học giùm tui cái đi! Nước biển truyền âm thanh nhanh gấp bốn lần không khí, bọt khí của bác làm máy đo nhiễu trắng xóa màn hình, lát nữa sóng ngầm Hòn Yến nó dập lật úp ca-nô rồi đổ thừa tại thủy thần nghen!'''

ACT3 = '''— Thôi nào Yến! Đừng có vừa gặp mặt đã chĩa súng vào khách quý như thế chứ con gái!

Viện trưởng Trần Minh Nam thong thả bước lên cầu tàu, trên môi nở nụ cười hiền hậu:

— Cháu chào bác Nam! — Cô gái nghe tiếng Viện trưởng liền đổi giọng dịu lại, gật đầu chào cung kính: — Cháu đâu dám chĩa súng vào ai, tại bác này vừa xuống xe đã khởi động máy nổ làm kinh động hết bầy cá cơm dưới chân cọc của cháu đấy chứ!

— Đây là kỹ sư Trần Anh Tuấn, Đội trưởng Đội Cơ điện của Viện ta. — Viện trưởng Nam cười xòa, rồi trỏ sang tôi: — Còn đây là Nguyễn Minh An, Giám đốc Kỹ thuật Dữ liệu, người chịu trách nhiệm phân tích mọi mô hình địa tầng và xung chấn cho chiến dịch giải mã Sector 05 lần này.

Đôi mắt trong veo của cô gái lập tức chuyển hướng sang tôi.

Ánh mắt nàng sắc bén, thẳng thắn của người sống nơi đầu sóng ngọn gió. Nàng đánh giá tôi từ đầu đến chân: chiếc quần kaki dã chiến dính vệt bùn khô bazan, đôi bốt da lộn sờn cũ, bờ vai không quá vạm vỡ nhưng lồng ngực phẳng lặng không một tiếng thở dốc sau chặng đường dài.

Khóe môi nàng khẽ nhếch nụ cười nửa miệng phong trần:

— Chào anh Minh An. Nghe danh Giám đốc Dữ liệu của Viện đã lâu, tưởng người đứng tuổi nào đó, hóa ra lại trẻ măng thế này. Nhưng tui nói trước nghen, ngồi phòng máy lạnh đối soát số liệu nó khác xa việc ra giữa lạch Hòn Yến lặn xuống rãnh bazan sâu sáu mươi mét đấy. Sóng ngầm ở đó dập một cái là say mật xanh mật vàng, đến lúc đó đừng bám áo tui đòi vào bờ nghen!

Tôi nhìn thẳng vào đôi mắt sáng ngời của nàng, khẽ gật đầu:

— Kỹ sư Hải Yến cứ yên tâm. Tôi ra đây là để cùng cô xử lý đới đứt gãy, không phải để làm gánh nặng cho ai cả.

— Được! Nói nghe cứng cỏi đó! — Nàng nhổ mẩu kẹo cao su bọc lại bỏ vào túi rác bên hông, xoay người vỗ mạnh lên chiếc hòm hợp kim chứa máy đo phổ Sonar đa tia đặt trên sàn gỗ: — Vậy phiền anh Giám đốc phụ tui khiêng cái hòm cảm biến này xuống ca-nô dã chiến giùm cái. Nặng ngót nghét một tạ đấy, khiêng cẩn thận kẻo sụn lưng!

Chiếc hòm bằng hợp kim nhôm đúc dày cộp chứa khối đầu dò siêu âm chìm, bên trong bọc lớp chì chống nhiễu từ trường ngầm, nặng ngót nghét chín mươi lăm cân.

Hải Yến bước tới, hai tay nắm chặt quai xách bên trái, khom người dồn lực đùi nâng lên. Tôi bước tới phía đối diện, đưa một bàn tay trần nắm quai xách bên phải.

Không cần gồng người, không cần lấy đà. Bên trong ba mươi ba đốt sống lưng, luồng Thuần Dương Cương Huyết ấm áp lưu chuyển một nhịp khoan thai. Lực kình từ màng tủy ngọc thấu quang truyền thẳng xuống cánh tay, biến các bó gân cơ thành những thanh thép dẻo dai.

Tôi khẽ nâng tay lên.

Chiếc hòm hợp kim nặng gần một tạ bổng nhẹ lên không trung như chiếc va-li rỗng, thăng bằng giữa hai người.

Hải Yến bỗng thấy tay mình nhẹ bẫng đi. Nàng giật thót người, trượt chân một nhịp trên ván ướt, đôi mắt to mở trừng trừng nhìn cánh tay tôi. Cánh tay tôi buông thõng tự nhiên, cơ bắp không nổi gân, hơi thở đều đặn, một mình tôi đã chịu tới tám phần mười trọng lượng khối kim loại.

— Anh... — Nàng ngước nhìn tôi, đôi môi mỏng mấp máy, vẻ ngạo nghễ biến sạch: — Tay anh... làm bằng pít-tông thủy lực hả?!

— Tôi dân Tiền Giang quen vác lúa từ nhỏ thôi. — Tôi cười nhẹ, bước vững chãi đưa chiếc hòm đặt êm ru xuống lòng ca-nô: — Cô Yến cẩn thận bậc thang trơn.

Hải Yến bước theo sau, ánh mắt nhìn tôi chuyển hẳn sang sự kiêng dè lẫn tò mò sâu sắc. Nàng đưa tay kéo mép tay áo lặn lên để lau giọt mồ hôi vừa túa ra trên trán.

Chính khoảnh khắc ống tay áo cao su co rút lên quá nửa cổ tay nàng, ánh mắt tôi đột ngột khựng lại.

Toàn thân tôi như bị một luồng điện giật xuyên qua lồng ngực.

Trên cổ tay trái thon dài rám nắng của Hải Yến, nổi bật chiếc đồng hồ lặn cơ khí quân sự cổ của Liên Xô — dòng Vostok Amphibia vỏ thép bát giác cũ mòn theo năm tháng. Mặt kính mica chi chít vết xước dăm san hô, vòng bezel xoay viền răng cưa đã bạc màu.

Nhưng điều khiến tim tôi thắt lại chính là phần nắp lưng kim loại áp sát cổ tay nàng. Ở mép vát có đường gờ nghiêng ba mươi độ gia công thủ công bằng tay mịn như lụa. Và ngay chính giữa nắp lưng thép không gỉ, bên cạnh biểu tượng mỏ neo, có dòng chữ triện khắc chìm bằng mũi đục cơ khí sắc lẹm:

V.H. - 1996 // KHOAN ĐỊA TẦNG BIỂN SÂU

Chữ "V.H." hoa lồng trong hình tròn nhỏ, bên cạnh là hình triện vuông tí hon bằng hạt đậu xanh.

Giống hệt nét triện trên vành đai hợp kim dưới đáy vạc núi lửa Chư Yang Sin!

Dấu ấn của cha tôi — Nguyễn Văn Hùng!'''

ACT4 = '''— Chiếc đồng hồ này...

Cổ họng tôi nghẹn đắng, một thanh âm run rẩy bật ra khỏi lồng ngực. Tôi bất giác bước tới một bước, đưa bàn tay trần nắm lấy cổ tay Hải Yến. Đầu ngón tay tôi run lên khi chạm vào lớp vỏ thép lạnh buốt mang theo hơi muối mặn của chiếc đồng hồ ba mươi năm tuổi.

— Này! Anh làm cái trò gì vậy hả?!

Hải Yến giật thót người lùi phắt lại phía sau. Đôi mắt nàng lóe lên tia nhìn cảnh giác, bàn tay phải vung lên, năm ngón tay co lại thành trảo thế hiểm hóc quét thẳng vào cổ tay tôi để gạt phăng ra. Động tác của nàng cực kỳ uyển chuyển, mang theo luồng kình lực mềm mại dẻo dai của sóng biển, mượn chính phản lực của tôi để đẩy lùi tôi ra xa.

Tôi không né tránh, chỉ khẽ chùng cổ tay đón đỡ đòn gạt bằng lực đạo nhu hòa triệt tiêu xung lực. Bàn chân tôi vẫn đứng vững như bàn thạch trên sàn ca-nô, ánh mắt nhìn xoáy vào mặt kính chiếc đồng hồ:

— Kỹ sư Yến... Đừng hiểu lầm. Tôi chỉ muốn hỏi... chiếc đồng hồ này từ đâu cô có được?

Hải Yến thấy đòn Nhu Kình của mình chạm vào cổ tay tôi như chạm vào cột sắt ngâm nước biển nghìn năm không hề lay chuyển, trong mắt nàng lóe lên tia kinh ngạc. Nàng giấu cổ tay ra sau lưng, trừng mắt nhìn tôi:

— Đồng hồ của ba tui để lại cho tui! Mắc mớ gì tới anh mà anh xông vào chụp giật như ăn cướp vậy hả?!

— Ba cô... có phải tên là Trần Vũ Cương không? — Tôi cố nén từng nhịp đập thình thịch trong lồng ngực: — Người từng là hoa tiêu lặn ngầm giỏi nhất vùng biển Hòn Yến ba mươi năm trước?

Hải Yến chết sững. Đôi lông mày thanh tú nhíu chặt lại, sự giận dữ bỗng chốc đông cứng trên gương mặt:

— Sao... sao anh biết tên ba tui?! Ba tui bị liệt chân nằm ở nhà mười mấy năm nay, người trong trạm lứa mới còn chẳng mấy ai nhớ tên ông, anh là người từ thành phố mới tới lần đầu làm sao biết được?!

Gió biển lùa vào ngực áo lành lạnh. Tôi nén tiếng thở dài, rút chiếc ví da cũ kỹ trong túi áo gi-lê, mở tấm ảnh đen trắng chụp đoàn khảo sát địa chất năm 1996 mà Viện trưởng Nam trao cho tôi chìa ra trước mặt nàng.

Trong bức ảnh ố vàng vì thời gian, người đàn ông trẻ tuổi dáng vạm vỡ mặc áo thợ lặn cao su dày cộp đang đứng khoác vai cha tôi bên mạn thuyền gỗ. Trên cổ tay người thợ lặn ấy, chiếc đồng hồ Vostok Amphibia vỏ bát giác phản chiếu ánh nắng lấp lánh của vùng biển Hòn Yến ba mươi năm trước.

Ngón tay tôi run run chỉ vào người thợ cơ khí mặc áo thun bạc màu đứng bên cạnh:

— Người khắc dòng chữ V.H. - 1996 trên nắp lưng chiếc đồng hồ của ba cô... chính là cha tôi — Nguyễn Văn Hùng. Ba tôi là thợ tiện cơ khí của đoàn khảo sát năm đó. Chuyến lặn thăm dò đáy biển Hòn Yến năm ấy suýt chút nữa lấy mạng cả đoàn vì dòng xoáy ngầm nuốt chửng mũi khoan. Chính bác Trần Vũ Cương đã liều mình lặn xuống năm mươi mét, dùng tay không cắt đứt dây cáp cứu kẹt mũi khoan để cứu sống ba tôi và đoàn nghiên cứu. Trước khi rời Phú Yên, ba tôi tự tay dùng dao tiện ren vát lại nắp lưng chiếc đồng hồ này, đóng dấu triện tặng lại bác Cương làm vật kỷ niệm sinh tử.

Hải Yến trừng lớn đôi mắt. Nàng giật lấy tấm ảnh cũ, hai bàn tay khẽ run rẩy. Ánh mắt nàng đảo qua lại giữa gương mặt người đàn ông trong ảnh và gương mặt của tôi. Nét chân mày chữ điền, sống mũi thẳng và ánh mắt kiên định của tôi trùng khớp hoàn toàn với người thợ cơ khí năm xưa.

— Anh... anh là con trai của bác Hùng thợ tiện sao? — Giọng nói đanh thép bỗng nghẹn lại, chuyển thành thanh âm mềm mại ngỡ ngàng: — Trời đất ơi... Ba tui nhắc tới bác Hùng suốt hai chục năm nay! Mỗi lần trở trời cái chân đau nhức buốt xương, ba tui lại lôi chiếc đồng hồ này ra lau chùi từng cái bánh răng, rồi bảo: Thằng Hùng thợ mộc Tiền Giang tiện ren giỏi nhất nước Việt Nam này, cái đồng hồ nó tiện lại cho tao ngâm nước ba mươi năm nay chưa từng lọt một giọt nước biển...

Bao nhiêu sự phòng thủ, gai góc của cô gái miền biển bỗng chốc tan biến như bọt sóng vỗ bờ cát. Nàng ngẩng đầu nhìn tôi, ánh mắt trong veo ngập tràn sự xúc động và niềm cảm mến chân thành của những đứa con cùng chung một cội nguồn nghĩa tình sâu nặng.

Mặt trời lặn dần sau rặng núi đèo Cù Mông phía tây. Ánh hoàng hôn rải dải lụa vàng lộng lẫy lên mặt nước Vịnh Xuân Đài. 

Hải Yến đưa tay tháo chiếc kẹp cơ khí bằng thép sau gáy. Mái tóc đen dài óng ả buông xõa xuống ngang lưng, bay bồng bềnh trong làn gió biển chiều tà. Nét đanh đá của nữ thợ lặn biến mất hoàn toàn, chỉ còn lại một cô gái Phú Yên hai mươi tư tuổi mộc mạc, dịu dàng giữa non nước hữu tình.

Nàng với chiếc nón tai bèo đội tạm lên đầu, rồi cúi người xách từ khoang ca-nô ra một trái dừa xiêm đã gọt sẵn vỏ trắng tinh, cắm sẵn ống hút bằng sậy:

— Nè... uống miếng nước dừa xiêm cho lại sức đi anh An. Lúc nãy tui nói năng cộc lốc quá, anh đừng có để bụng nghen.

Tôi đón lấy trái dừa từ tay nàng. Ngón tay nàng khẽ chạm vào mu bàn tay tôi, mang lại cảm giác mát rượi, mềm mại của da thịt phàm nhân chân thật. Vị nước dừa ngọt lịm, thanh mát lan tỏa từ cuống họng xuống tận ruột gan. Lần đầu tiên sau bao tháng ngày ròng rã khổ tu trên đất đỏ bazan và rèn giũa cơ bắp trong hầm lò ngột ngạt, tôi cảm nhận được một luồng hơi ấm đời thường dịu dàng len lỏi vào tâm hồn mình.'''

ACT5 = '''Màn đêm buông xuống vịnh biển nhanh như một cái chớp mắt.

Những ngọn đèn cao áp của trạm thủy văn hắt từng vệt sáng dài loang loáng trên mặt nước biển lăn tăn. Kỹ sư Tuấn và Viện trưởng Nam đã vào trong phòng điều hành dã chiến để ráp nối các cụm dữ liệu vi chấn, tiếng lách cách gõ phím và tiếng càu nhàu của anh Tuấn về đường truyền vệ tinh thỉnh thoảng lại vọng ra ngoài hiên.

Tôi ngồi một mình trên mỏm đá bazan nhô ra sát mép nước, chiếc áo khoác gió sờn vai khẽ phần phật theo từng cơn gió biển đêm lạnh buốt. Dưới ánh trăng mười sáu vằng vặc, tôi cẩn thận dùng mảnh vải dù tẩm dầu máy lau chùi lại từng rãnh khía chu sa đỏ trên thân thanh Hắc Thiết Đoản Côn.

Đột nhiên, trong không gian tĩnh mịch của thức hải tôi, đài sen Lục Diệp Thanh Liên khẽ lay động một nhịp.

Những cánh sen ngọc bích tỏa ra từng làn khói mỏng màu lam ngọc dịu dàng. Bạch Y Thần Nữ Lâm Tịch — sau nhiều giờ trầm mặc ngắm nhìn thế giới trần gian qua đôi mắt tôi — bỗng chậm rãi ngẩng đầu lên.

Đôi mắt phượng sâu thẳm như chứa cả dải ngân hà của nàng nhìn xuyên qua tâm thức tôi, khóe môi khẽ cong lên nét cười huyền ảo, thanh âm truyền âm cất lên mang theo dư vị kỳ lạ chưa từng có:

— Minh An...

— Lâm Tịch? — Tôi khẽ giật mình trong tâm thức: — Cô thấy có điều gì bất thường dưới đáy biển Hòn Yến sao?

Nàng khẽ lắc đầu, tà áo lụa trắng phất phơ giữa không gian thức hải tĩnh lặng:

— Dưới đáy biển Hòn Yến quả thực có một trận nhãn cổ xưa đang co giật, lát nữa ta sẽ nói rõ cho anh. Nhưng điều ta muốn nói... là cô nương thợ lặn phàm trần ban nãy.

Tôi thoáng ngơ ngác:

— Kỹ sư Hải Yến sao? Cô ấy có vấn đề gì à?

Lâm Tịch khẽ thở dài, nhưng trong thanh âm lại phảng phất chút ý vị trêu chọc nửa đùa nửa thật:

— Khung xương của nha đầu đó vô cùng đặc biệt. Nàng ta sinh ra và lớn lên bên rãnh nứt của biển sâu, ngày đêm ngâm mình dưới áp lực hàng ngàn tấn nước mặn, nên toàn bộ gân mạc và kinh lạc đều mang thuộc tính Thuần Âm Nhu Thể của loài thủy tộc thời viễn cổ. Nếu anh dùng kình lực Thuần Dương Cương Huyết khai mở các huyệt đạo sau gáy cho nàng, nàng sẽ là một chiến hữu Thể Đạo hệ Thủy vô cùng đắc lực cho anh khi lặn xuống đáy sâu sáu mươi mét...

Nói đến đây, thanh âm của Thần Nữ bỗng ngập ngừng trong nửa khắc. Đôi mắt nàng nhìn thẳng vào tâm thức tôi, ánh mắt sâu thẳm dường như xuất hiện một gợn sóng lăn tăn:

— Nhưng mà... điều ta lấy làm lạ là lúc nàng ta tháo kẹp tóc, mái tóc buông xõa ngang lưng đưa trái dừa cho anh... nhịp tim của anh bỗng nhiên đập nhanh hơn bình thường ba nhịp, lại còn lỡ mất nửa nhịp thở nữa.

Mặt tôi bỗng nóng bừng lên giữa đêm biển lạnh. Tôi lúng túng gãi đầu, vội vàng thanh minh trong tâm tưởng:

— Tôi... tôi chỉ bất ngờ vì cô ấy là con gái của bác Cương, người quen cũ của cha tôi thôi mà...

— Thật là vậy sao? — Lâm Tịch khẽ mỉm cười, một nụ cười hiếm hoi mang chút vị chua nhẹ của một tri kỷ ngàn năm: — Xem ra Thể Đạo Hoán Huyết của anh rèn luyện gân cốt như sắt đá, nhưng quả tim phàm trần hai mươi lăm tuổi kia vẫn chưa thể nào đoạn tuyệt được thất tình lục dục của cõi nhân gian đâu...

Tôi chưa kịp tìm lời đáp lại nàng thì từ trong phòng điều hành của trạm thủy văn, một tiếng còi báo động điện tử dồn dập vang lên phá tan bầu không khí tĩnh mịch.

Cánh cửa lưới bật mở toang. Kỹ sư Tuấn tay cầm chiếc máy tính bảng truyền số liệu dã chiến lao bổ ra ngoài cầu tàu, hai mắt trợn trừng:

— Chú An! Bác Nam! Mau vào đây xem này!

Tôi đứng phắt dậy, cất vội thanh đoản côn vào thắt lưng rồi lao nhanh vào gian phòng điều hành.

Trên chiếc màn hình radar quét sườn Sonar đa tia đặt ở trung tâm căn phòng, một dải sóng âm ba chiều màu đỏ quạch đang nhảy múa dữ dội ở tọa độ ngoài khơi đảo Hòn Yến. Độ sâu đo được đã chạm mức âm sáu mươi hai mét.

Một luồng sóng xung chấn hạ âm có tần số đúng 0.08 Hertz đang phát ra từ tâm chấn rạn nứt bazan tổ ong dưới đáy biển, từng đợt dội ngược lên mặt nước như tiếng gầm gừ của một con quái thú ngủ vùi triệu năm vừa cựa mình thức giấc.

Hải Yến lúc này đã thay sang chiếc áo thun thể thao sẫm màu, mái tóc búi cao gọn gàng sau gáy, đôi bàn tay thoăn thoắt gõ phím khóa chặt tọa độ mục tiêu. Nàng ngẩng đầu lên nhìn tôi, ánh mắt sắc sảo và kiên định như một mũi lao thép:

— Trận nhãn Sector 05 dưới đáy rạn san hô Hòn Yến vừa phát tín hiệu cộng hưởng khẩn cấp. Lúc nửa đêm nay, thủy triều sẽ rút xuống mức thấp nhất trong tháng, để lộ ra cửa hang bazan ngầm. 

Nàng với lấy bộ đồ lặn và chiếc đồng hồ Vostok Amphibia đeo chặt vào cổ tay, cất giọng đanh gọn:

— Anh An, chuẩn bị đi. Nửa đêm nay, tui lái ca-nô đưa anh và bác Tuấn xuống đáy biển.'''

raw_content = f"""{ACT1}

{ACT2}

{ACT3}

{ACT4}

{ACT5}"""

def run_pipeline():
    print(f"=== KHỞI CHẠY PIPELINE SÁNG TÁC & KIỂM DUYỆT CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    
    # 1. Kiểm tra dung lượng từ
    word_count = len(raw_content.split())
    print(f"[+] [1/6] Độ dài văn xuôi: {word_count} từ (Chuẩn mực: 3.200 - 4.500 từ, đại chương mở rộng đến 6.000 từ).")
    if word_count < 3200 or word_count > 6000:
        print(f"[CẢNH BÁO] Độ dài nằm ngoài khoảng cho phép: {word_count} từ!")
        return False
    
    # 2. Kiểm tra từ cấm và quy tắc RULE-07
    meta_words = ["chương", "hồi", "quyển", "tác giả", "hệ thống", "bản thảo", "canon", "database", "plot", "foreshadowing"]
    for mw in meta_words:
        matches = re.findall(rf"\b{mw}\b", raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ meta '{mw}' trong thân bài! ({len(matches)} lần)")
            return False
            
    if "huyết mạch" in raw_content.lower():
        print("[-] VI PHẠM RULE 3: Phát hiện từ cấm 'huyết mạch' trong thân bài!")
        return False
    print("[+] [2/6] Kiểm tra từ cấm tối cao: 0 meta-words, 0 'huyết mạch'.")

    # Kiểm tra entity bold
    bold_matches = re.findall(r'\*\*[^*]+\*\*', raw_content)
    if bold_matches:
        print(f"[-] LỖI VI PHẠM IN ĐẬM DANH TỪ: {len(bold_matches)} trường hợp bôi đậm!")
        return False
    print("[+] 0 trường hợp bôi đậm Markdown trong thân bài (Clean Prose).")

    # 3. Đo lường cảm xúc & nhịp độ
    emo_engine = EmotionDopamineEngine(DB_PATH)
    emo_res = emo_engine.analyze_text(CHAPTER_NUM, raw_content, arc_id="arc_02")
    print(f"[+] [3/6] Chỉ số Cảm xúc & Dopamine:")
    print(f"    - Pathos Score    : {emo_res['pathos_score']:.2f}")
    print(f"    - Dopamine Score  : {emo_res['dopamine_score']:.2f}")
    print(f"    - Grounding Score : {emo_res['grounding_score']:.2f}")

    # 4. Tự phản biện bằng CritiqueEngine
    critique_engine = CritiqueEngine()
    critique_res = critique_engine.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Nguyễn Minh An",
        active_characters=["char_minh_an", "char_tuan", "char_trinh_hoai_nam", "char_hai_yen", "char_lam_tich"],
        text=raw_content
    )
    critical_issues = [i for i in critique_res.get("issues", []) if i.get("severity") in ("CRITICAL", "HIGH")]
    if critical_issues:
        print(f"[-] CritiqueEngine phát hiện lỗi nghiêm trọng: {critical_issues}")
        for ci in critical_issues:
            print("   ->", ci)
        return False
    print(f"[+] [4/6] CritiqueEngine thông qua: 0 lỗi nghiêm trọng.")

    # 5. Xuất bản Markdown
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
description: "Minh An, Viện trưởng Nam và Kỹ sư Tuấn vượt đèo Phượng Hoàng đến Vịnh Xuân Đài (Phú Yên) chuẩn bị thám hiểm Sector 05 Hòn Yến; lần đầu gặp gỡ nữ kỹ sư trắc địa hải văn kiêm thợ lặn Trần Vũ Hải Yến (1m68, tóc búi cao phong trần); phát hiện chiếc đồng hồ lặn Liên Xô cổ Vostok Amphibia có vết ren ngược V.H.-1996 của người cha Nguyễn Văn Hùng trao tặng ba của Yến; Lâm Tịch nhận ra căn cốt Thủy Mạch Nhu Thể của Yến; tín hiệu hạ âm 0.08Hz rền rĩ dưới đáy biển 60m mở màn chiến dịch nửa đêm."
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

    # 6. Xuất Word (.docx)
    word_arc_dir = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02")
    os.makedirs(word_arc_dir, exist_ok=True)
    docx_file_path = os.path.join(word_arc_dir, f"ch_{CHAPTER_NUM:03d}.docx")
    
    dp = DocxPipeline()
    dp.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=full_markdown,
        output_docx_path=docx_file_path
    )
    print(f"[+] [6/6] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 7. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Tiếp Cận Vịnh Xuân Đài & Chạm Trán Kỹ Sư Hải Văn Trần Vũ Hải Yến",
        CHAPTER_NUM,
        1,
        f"{DATE}T17:30:00+07:00",
        CHAPTER_NUM,
        "loc_vinh_xuan_dai_phu_yen",
        json.dumps(["char_minh_an", "char_tuan", "char_trinh_hoai_nam", "char_hai_yen", "char_lam_tich"]),
        "Đoàn khảo sát vượt đèo Phượng Hoàng đến Vịnh Xuân Đài; Minh An gặp gỡ Trần Vũ Hải Yến (1m68, tóc búi cao phong trần); phát hiện chiếc đồng hồ lặn Liên Xô cổ có vết ren ngược V.H.-1996 của người cha Nguyễn Văn Hùng; Lâm Tịch nhận ra căn cốt Thủy Mạch Nhu Thể của Yến; tín hiệu hạ âm 0.08Hz từ rạn san hô Hòn Yến Sector 05 thức giấc lúc nửa đêm.",
        "Thiết lập liên kết định mệnh giữa An và Hải Yến; chuẩn bị mở chiến dịch lặn biển sâu 60m khám phá Thủy Phủ Sector 05 Hòn Yến."
    ))

    # Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-WLD-001'
    """, (
        CHAPTER_NUM,
        "Chuyển chiến trường khảo sát từ cao nguyên Chư Yang Sin xuống duyên hải Nam Trung Bộ; tiếp cận Sector 05 Hòn Yến."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Thể Đạo của Minh An thể hiện sự vượt trội về lực nâng vật lý trần trụi; phát hiện căn cốt Thủy Mạch Nhu Thể của Hải Yến."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-003'
    """, (
        CHAPTER_NUM,
        "Chiếc đồng hồ Vostok Amphibia 1996 của ba Minh An tái xuất hiện trên tay Hải Yến, nối liền ân nghĩa của thế hệ tiền bối thợ lặn."
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
        inv_data["current_location"] = "Trạm Khảo Sát Thủy Văn & Địa Chất Biển Duyên Hải, Vịnh Xuân Đài, Phú Yên"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Khí Ly Thể & Nhận Biết Căn Cốt Thủy Mạch)"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] Đã cập nhật state/inventory.json.")

    # 9. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    print(f"\n===> SÁNG TÁC & KIỂM DUYỆT CHƯƠNG {CHAPTER_NUM} HOÀN TẤT THÀNH CÔNG 100%! <===")
    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

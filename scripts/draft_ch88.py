# -*- coding: utf-8 -*-
"""Draft Chapter 88 for Phá Trời Novel OS with ~3,500+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 88
CHAPTER_TITLE = "Bình Minh Sau Bão"
DATE = "2026-10-30"
LOCATION = "Bán Đảo Thanh Đa & Khu Trọ Nơ Trang Long, TP. Hồ Chí Minh"

ACT1 = '''Sáu giờ sáng ngày ba mươi tháng mười.

Sau một đêm mưa giông nhiệt đới vần vũ cuồng nộ làm rung chuyển cả khúc sông Sài Gòn, bầu trời thành phố mở ra một dải ánh sáng ban mai tinh khôi, vàng óng ả tựa như mật ong rừng vừa rót xuống mặt nước mênh mông.

Gió sớm từ phía rừng ngập mặn Cần Giờ thổi ngược theo triều cường lên bến Thanh Đa, mang theo luồng không khí thanh mát, lành lạnh hòa quyện với mùi thơm ngai ngái nồng nàn của đất phù sa mới lắng đọng sau cơn bão lớn. Từng đàn chim sẻ ríu rít gọi bầy trên những tán bần cổ thụ trổ hoa trắng xóa bên bờ kè, rũ sạch những giọt nước mưa còn đọng lại trên lông cánh đón chào một ngày mới an lành.

Khúc sông hình móng ngựa bao quanh bán đảo Thanh Đa lúc này hoàn toàn êm ả chảy trôi.

Mặt nước đỏ nặng phù sa phẳng lặng như gương, phản chiếu bóng hình những tòa nhà cao tầng bọc kính của khu Thảo Điền bên kia sông đang bừng sáng rực rỡ dưới ánh bình minh. Không còn một chút dấu vết nào của luồng âm trọc khí màu tím đen ma quái từng cuộn lên nghẹt thở đêm qua. Dưới lòng sông sâu ba mươi mét, ngọn Cổ Tháp Thần Hoang sau khi được giải trừ hiểm họa đã chìm sâu vào trạng thái tự ẩn, các đạo văn phù điêu thu liễm ánh sáng vào lòng đá huyền vũ, để lại sự tĩnh lặng vững chãi nghìn đời cho thềm lục địa Nam Bộ.

Bốn chiếc sà lan ngụy trang của Tập đoàn Cửu Long Thiên Hải vẫn neo đậu im lìm giữa khúc sông, nhưng toàn bộ cụm máy phát xung điện từ và những bệ đá huyết thạch tà thuật trên đó đã bị nghiền nát thành từng đống sắt vụn và bụi đá vô hại.

Tiếng ca-nô tuần tra chuyên dụng của lực lượng an ninh đường thủy xé nước lao tới từ hướng hạ lưu cầu Sài Gòn.

Đại úy Phan Thế Dũng — người vừa bay khẩn cấp từ Cà Mau về thành phố trong đêm để trực tiếp chỉ đạo chuyên án đặc nhiệm — bước nhanh lên boong chiếc sà lan số 4. Phía sau anh là đội cơ động mang đầy đủ thiết bị niêm phong và bảo hộ chuyên dụng.

Nhìn thấy Tạ Lôi bị trói chặt vào cột thép chịu lực bằng xích sắt, cánh tay trái đã được sơ cứu cầm máu bằng vải dù dã chiến, đôi mắt gã trùm tác chiến ngầm hoàn toàn dại đi vì kinh mạch tà công bị chấn phế, Đại úy Dũng khẽ thở phào một hơi dài nhẹ nhõm. Từng tốp chiến sĩ công binh đường thủy nhanh chóng tản ra các khoang tàu, kiểm tra từng mét cáp điện, niêm phong các thiết bị kỹ thuật ngụy trang và chuẩn bị phương án kéo lai dắt toàn bộ bốn chiếc sà lan về bến cảng quân sự an toàn.

Đại úy Dũng bước tới bên mạn tàu nơi tôi đang đứng, đưa tay vỗ mạnh lên bờ vai vững chắc của tôi, giọng nói đanh thép thường ngày bỗng chốc chùng xuống vì xúc động:

"Minh An... Cậu đã làm được một điều không tưởng. Đêm qua, nếu để khối bẫy xung chấn của chúng giật sập thềm địa tầng Thanh Đa này, hậu quả đối với toàn bộ các quận nội thành Sài Gòn sẽ khủng khiếp không thể nào lường trước được. Hàng ngàn hộ dân ven sông, các tuyến cầu trọng yếu và toàn bộ hạ tầng kỹ thuật đô thị ven bờ có thể đã bị cuốn phăng xuống lòng sông trong cơn sạt lở kinh hoàng."

Tôi đưa mắt nhìn ra dòng nước phù sa đang lững lờ trôi dưới chân mình, từng đám bèo lục bình tím ngát trôi lững lờ theo con nước ròng êm ả, khóe môi khẽ nở một nụ cười mộc mạc:

"Em không làm điều đó một mình, anh Dũng. Nếu không có sự phối hợp kịp thời của lực lượng an ninh biên phòng, việc phong tỏa hiện trường và cô lập các kênh sóng vô tuyến của chúng sẽ không thể hoàn hảo như vậy. Mảnh đất này đã che chở cho chúng ta, em chỉ làm tròn bổn phận của một người con sinh ra từ dòng sông này."

Đại úy Dũng gật đầu thật mạnh, ánh mắt nhìn tôi tràn đầy sự kính trọng và tin cậy:

"Hồ sơ mật trích xuất từ máy tính của Tạ Bách Xuyên và lời khai ban đầu của các toán bắt giữ đêm qua đã đủ để Viện Kiểm sát và cơ quan an ninh quốc gia ra lệnh phong tỏa toàn bộ tài sản, bắt giữ toàn bộ ban điều hành của Tập đoàn Cửu Long Thiên Hải. Mạng lưới ngầm tác oai tác quái suốt mười năm qua của chúng tại phương Nam đã hoàn toàn bị xóa sổ trên diện rộng. Hơn hai mươi công ty bình phong chuyên buôn lậu khoáng vật và khai thác ngầm trái phép tại các cửa sông duyên hải đều đã bị các tổ chuyên án đồng loạt khám xét trong sáng nay."

Anh dừng lại một chút, khẽ nhìn sâu vào mắt tôi, hạ thấp giọng dặn dò:

"Lãnh đạo cấp cao muốn gặp mặt và trao tặng huân chương đặc biệt cho cậu sau chiến dịch này. Cậu nghĩ sao?"

Tôi lắc đầu, ánh mắt hướng về phía những chiếc ghe chài nhỏ của người dân xóm Mũi Thanh Đa đang bắt đầu buông lưới buổi sớm:

"Em là một kỹ thuật viên địa chất, một người luyện võ phàm nhân. Em muốn giữ cuộc sống của mình thật giản dị, bình yên bên người thân và khu xóm nghèo. Được nhìn thấy thành phố bình yên đón ánh mặt trời mỗi sớm mai, được thấy người dân an tâm mưu sinh, đối với em đã là phần thưởng lớn nhất rồi."

Hiểu được tính cách trầm ổn và tấm lòng trong sáng của tôi, Đại úy Dũng mỉm cười, siết chặt tay tôi:

"Tôi hiểu rồi. Toàn bộ hồ sơ chiến dịch sẽ được lưu trữ dưới cấp độ mật vĩnh viễn, tên của cậu sẽ không xuất hiện trên bất kỳ phương tiện truyền thông đại chúng nào. Nhưng trong lòng những người lính chúng tôi, Nguyễn Minh An luôn là người thủ hộ kiên cường nhất của mảnh đất này."

Tôi trao lại chiếc ba-lô đựng các tài liệu kỹ thuật thu giữ cho đội điều tra, chỉ giữ lại chiếc ống mẫu địa tầng số 9 của Viện Địa chất, rồi nhẹ nhàng nhảy xuống chiếc xuồng nhỏ sang bờ, hòa mình vào màu xanh biếc của bán đảo Thanh Đa.'''

ACT2 = '''Bảy giờ ba mươi phút sáng.

Nắng sớm rọi qua những rặng dừa nước nghiêng mình soi bóng xuống con lạch nhỏ gần bến đò Bình Quới.

Tôi ngồi trong một quán trà nhỏ lợp mái lá dừa nước đơn sơ ven đường đất đỏ, thưởng thức tách trà lài nóng thơm lừng hòa quyện với làn gió mát lành từ lòng sông thổi vào. Xung quanh tôi, vài bác nông dân lớn tuổi trong bộ quần áo bà ba đang ngồi đàm đạo chuyện mùa vụ, chuyện con nước son mang phù sa về bồi đắp cho những liếp vườn cây ăn trái, tiếng cười nói giòn tan xua tan đi mọi âu lo đời thường.

Bên bến đò cũ, từng chuyến đò ngang chở đầy ắp rau củ, trái cây miệt vườn và những người phụ nữ gánh hàng rong chuẩn bị sang chợ bán buổi sáng. Tiếng mái chèo khua nước róc rách, tiếng máy đuôi tôm nổ giòn tan trên dòng kênh nhỏ tạo nên một bản hòa âm thanh bình, đằm thắm của vùng đất phương Nam.

Dưới làn da của tôi, sự tĩnh lặng diệu kỳ của **Hoán Huyết Sơ kỳ** đang vận hành ở trạng thái cân bằng tuyệt mỹ.

Ba mươi ba đốt sống tủy ngọc sau lưng tôi không còn phát quang rực rỡ như lúc chiến đấu, mà thấu suốt một làn ánh sáng ấm áp, nuôi dưỡng từng khớp xương và tủy sống. Dòng Thuần Dương Cương Huyết sau khi bộc phát toàn lực đêm qua nay đã lắng dịu lại, chảy trôi chậm rãi nhịp nhàng tựa như dòng phù sa màu mỡ bồi đắp cho bờ bãi sau mùa lũ lớn. Mỗi tế bào cơ bắp đều được thư giãn sâu sắc, tự động hấp thu những dưỡng chất tinh khiết nhất từ không khí trong lành để hàn gắn mọi vi tổn thương.

Trong thức hải của tôi, một làn hương thơm thanh khiết như hoa sen đầu mùa bỗng thoang thoảng lan tỏa.

Đài sen ngọc bích **Lục Diệp Thanh Liên** khẽ rung rinh. Thần ảnh của Lâm Tịch hiện ra trong bộ áo lụa trắng tinh khôi, đôi mắt trong veo như ngọc bích đang chăm chú nhìn tôi với một nụ cười thanh tao hiếm thấy.

"Chúc mừng anh, Minh An," thanh âm nàng trong trẻo như tiếng chuông ngọc ngân vang giữa hư không. "Toàn bộ mười hai then cài ngoài duyên hải phương Nam và hạch tâm phong ấn của dòng sông này đã được an định trọn vẹn. Ngọn Cổ Tháp Thần Hoang đã lấy lại được chín thành linh quang bảo hộ, sẽ không còn bất kỳ thế lực tà tu nào có thể làm tổn hại đến vùng đất này trong nhiều năm tới."

Tôi khẽ nhấp một ngụm trà nóng, cảm nhận vị chát ngọt đọng lại nơi đầu lưỡi, mỉm cười đáp lại trong tâm thức:

"Nếu đêm qua không có đạo kiếm ý băng phách của cô kịp thời đóng băng thần thức của Tạ Lôi trong một phần mười giây định mệnh, có lẽ khối bẫy tự bạo đã nổ tung rồi. Cô mới chính là người lập công lớn nhất."

Lâm Tịch khẽ lắc đầu, đôi gò má thanh tú hơi ửng lên một vệt hồng nhạt:

"Tôi chỉ đóng góp một phần nhỏ. Sức mạnh thực sự cứu sống thành phố này chính là ý chí sắt đá và lòng dũng cảm của anh. Một người phàm nhân không màng hiểm nguy, tay không lao vào tâm bão để che chở cho sinh mệnh của hàng triệu con người xa lạ... Ở thượng giới xa xôi, nơi kẻ mạnh coi sinh linh như cỏ rác, người ta tranh đoạt từng ngọn cỏ cọng rác linh dược mà sẵn sàng tàn sát cả một tinh thành, tôi chưa từng thấy một ai có được tâm niệm thuần khiết và kiên cường như anh."

Nàng ngập ngừng giây lát, ánh mắt dõi nhìn qua những chuyến đò ngang ven sông:

"Mảnh đất này thật kỳ lạ. Những người dân chân chất kia không có thần thông, không biết đến pháp thuật cao siêu, nhưng trong dòng máu của họ lại ẩn chứa một sức sống mãnh liệt đến phi thường. Suốt hàng ngàn năm qua, tổ tiên của họ đã bám trụ nơi đầu sóng ngọn gió, lập đình lập miếu, dùng lòng thành kính và đức hy sinh để bồi đắp cho địa mạch phương Nam. Chính nguồn năng lượng phàm trần thuần khiết ấy mới là phong ấn vững chắc nhất chở che cho ngọn cổ tháp."

Nàng ngước mắt nhìn quanh thức hải rộng lớn của tôi, nơi dải sáng hoàng kim của Thuần Dương Cương Huyết đang lưu chuyển tựa như dải ngân hà thu nhỏ:

"Nhờ luồng địa khí thanh khiết dội ngược từ cổ tháp đêm qua, nguyên thần của tôi đã vững vàng ở mức sáu phần mười, không còn phải lo lắng về việc tiêu tán nữa. Nhưng Minh An này, con đường phía trước của anh sẽ còn dài dằng dặc và gian nan hơn gấp bội. Muốn xây một tòa tháp cao vạn trượng, nền móng phải được đào sâu và nén chặt qua muôn ngàn năm tháng. Con đường Thể Đạo phàm nhân cũng vậy, không thể nóng vội một sớm một chiều."

"Tôi hiểu," tôi điềm tĩnh đáp. "Thế giới này rộng lớn vô cùng. Mười hai cọc Thủy Môn và cổ tháp sông Sài Gòn mới chỉ là chiếc then cài ngoài cùng. Phía trước vẫn còn những bí mật to lớn hơn của dải đất non sông này. Dù mất bao nhiêu năm tháng, tôi vẫn sẽ bước từng bước vững chắc nhất, dùng chính đôi chân của mình để đi trọn con đường."

Lâm Tịch khẽ gật đầu, ánh mắt nàng đong đầy sự tin tưởng sâu sắc:

"Đúng vậy. Dù là trăm năm hay ngàn năm, dù là ở mảnh đất này hay bước ra những chân trời bao la ngoài kia, tôi sẽ luôn đồng hành bên cạnh anh."

Lời hứa nhẹ nhàng tựa gió thoảng nhưng nặng tựa ngàn cân của nàng như một ngọn lửa sưởi ấm toàn bộ tâm trí tôi.

Tôi đặt chén trà xuống bàn, hít sâu một hơi luồng không khí trong lành của bán đảo Thanh Đa. Sự gắn kết giữa hai linh hồn, hai con người từ hai thế giới hoàn toàn khác biệt nay đã trở thành một mối tri kỷ keo sơn không gì có thể chia cắt.'''

ACT3 = '''Mười một giờ ba mươi phút trưa.

Tôi trở về con hẻm nhỏ quen thuộc trên đường Nơ Trang Long, quận Bình Thạnh.

Nắng trưa vàng rực đổ dài trên những bức tường gạch rêu phong và những mái tôn cũ kỹ. Dấu vết của bốn tay súng bắn tỉa và hai khối mìn bẫy đêm qua đã được lực lượng công binh bí mật dọn dẹp sạch sẽ từ lúc rạng sáng, không để lại bất kỳ sự xáo trộn nào cho cuộc sống của người dân nghèo.

Trên sạp báo nhỏ đầu ngõ, những tờ báo in buổi sáng đăng tin về một chiến dịch triệt phá chuyên án buôn lậu khoáng sản và lừa đảo tài chính quy mô lớn trên các tuyến đường thủy phía Nam. Người dân trong hẻm xúm xít bàn tán rôm rả, ai nấy đều tấm tắc khen ngợi sự vào cuộc quyết liệt của các chiến sĩ công an và bộ đội biên phòng, hoàn toàn không hay biết rằng bên dưới lớp vỏ chuyên án kinh tế ấy là một cuộc chiến sinh tử rúng động cõi u minh.

Tiếng rao lanh lảnh của chị bán xôi dạo, tiếng máy may lách cách từ tiệm may nhỏ của cô Năm đầu ngõ, tiếng lũ trẻ con í ới đuổi bắt nhau dưới bóng râm của cây hoa giấy nở hoa đỏ rực... Mọi thứ đều bình dị, thân thương và tràn đầy nhựa sống như bao ngày bình thường khác.

Tôi ghé vào quán hủ tiếu gõ quen thuộc của bác Ba đầu hẻm — nơi tôi vẫn thường ghé ăn mỗi buổi tối tăng ca muộn thời còn làm nhân viên kỹ thuật tập sự.

"Ủa, chú An! Đi công tác khảo sát ngoài biển mấy tuần nay mới về hả chú?" Bác Ba vừa thoăn thoắt trụng bánh hủ tiếu vào nồi nước lèo nghi ngút khói thơm, vừa tươi cười đon đả chào tôi.

"Dạ, cháu mới về tới trưa nay bác Ba. Bác cho cháu một tô hủ tiếu xương thập cẩm nhiều hành nhiều giá nghen bác!" Tôi kéo chiếc ghế nhựa ngồi xuống góc bàn quen thuộc dưới giàn mướp xanh mát.

"Có ngay, có ngay! Bữa nay nhìn chú rắn rỏi, phong trần hẳn ra nghen, da dẻ hồng hào mà cặp mắt sáng quắc hà!"

Một tô hủ tiếu nóng hổi được bưng ra, nghi ngút khói thơm phức mùi xương hầm hòa quyện với hành phi vàng ruộm và vài miếng tóp mỡ giòn tan.

Tôi cầm đôi đũa tre, thưởng thức từng sợi hủ tiếu dai ngon và húp một ngụm nước dùng đậm đà ngọt lịm. Đó là hương vị bình dị của nhân gian, hương vị của cuộc sống đời thường mà tôi đã đem cả tính mạng ra để bảo vệ đêm qua. Giữa những hiểm nguy chết người và những âm mưu tà thuật to lớn, chính những khoảnh khắc đời thường mộc mạc này mới là mỏ neo giữ chặt tâm hồn tôi lại với thế giới thực tại, nhắc nhở tôi về lý do vì sao mình phải kiên cường tiến bước.

Tôi lấy chiếc điện thoại di động cũ ra khỏi túi áo, bấm vào dãy số quen thuộc đã khắc sâu trong tâm khảm.

Chuông reo hai hồi thì đầu dây bên kia bắt máy. Tiếng mẹ tôi vang lên hiền từ giữa không gian yên bình của miệt vườn cù lao Tiền Giang:

"An hả con? Về tới thành phố an toàn chưa con? Mấy bữa nay ngoài biển nghe đài báo có giông bão, mẹ ở nhà lo cho con quá chừng..."

Lắng nghe thanh âm ấm áp của mẹ, sống mũi tôi bỗng cay cay, nhưng khóe môi lại nở một nụ cười rạng rỡ:

"Dạ con về tới phòng trọ rồi mẹ ơi. Công việc ngoài biển xong xuôi hết rồi, sóng gió ngoài đó không làm gì được con đâu mẹ. Cuối tuần này con được nghỉ phép mấy ngày, con sẽ bắt xe đò về cù lao thăm mẹ, phụ mẹ cuốc đất tỉa cành nghen mẹ."

"Thiệt hôn con? Vậy để mẹ dặn thím Bảy để dành cho con con cá lóc đồng nướng trui với mớ rau đắng đất nghe con!" Tiếng cười vui sướng của mẹ vang lên rộn rã qua điện thoại.

"Dạ, con nhớ rồi mẹ."

Tắt điện thoại, tôi ngồi ăn hết tô hủ tiếu trong sự thanh thản tuyệt đối của tâm hồn.

Tôi trả tiền nước rồi khoác ba-lô rảo bước về phía căn phòng trọ nhỏ cuối dãy. Mở cánh cửa gỗ quen thuộc, nắng trưa rọi qua khung cửa sổ nhỏ chiếu lên chiếc bàn làm việc đơn sơ với những cuốn sổ ghi chép địa chất đã ố vàng theo năm tháng.

Tôi cẩn thận đặt thanh Hắc Thiết Đoản Côn và thanh Trấn Thủy Đoản Đao lên giá gỗ sau cánh cửa.

Bão ngầm phương Nam đã hoàn toàn lắng xuống.

Mười hai cọc Thủy Môn ngoài biển lớn và Cổ Tháp Thần Hoang dưới lòng sông Sài Gòn đã an định. Mẹ già ở quê vẫn bình yên, khu xóm nghèo vẫn êm đềm rộn rã tiếng cười, và thành phố này vẫn tiếp tục vươn mình rực rỡ đón chào những ngày mới tươi sáng.

Tôi đứng bên khung cửa sổ, hít một hơi thật sâu luồng gió trưa phương Nam lồng lộng.

Một chặng đường lớn đã khép lại vẻ vang, và tôi biết, phía trước tôi là cả một tương lai rộng mở của người thủ hộ phàm nhân!'''

def run_pipeline():
    print(f"[*] Bắt đầu thực thi pipeline sáng tác Chương {CHAPTER_NUM}: {CHAPTER_TITLE}")
    
    raw_content = ACT1.strip() + "\n\n" + ACT2.strip() + "\n\n" + ACT3.strip()
    words = raw_content.split()
    word_count = len(words)
    print(f"[+] [1/6] Tổng số từ bản thảo: {word_count} từ")
    if word_count < 3000 or word_count > 5500:
        print(f"[!] Cảnh báo độ dài từ: {word_count} (Mục tiêu chuẩn: 3,000 - 5,000 từ)")

    # 2. Kiểm tra cấm kỵ RULE-07 (0 meta words, 0 forbidden words)
    print(f"[*] [2/6] Kiểm tra RULE-07 (Cấm từ ngữ meta/hậu trường & cấm 'huyết mạch')...")
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
        r"\bforeshadowing\b",
        r"\bhuyết mạch\b"
    ]
    for pat in meta_patterns:
        matches = re.findall(pat, raw_content, re.IGNORECASE)
        if matches:
            print(f"[-] VI PHẠM RULE-07: Phát hiện từ ngữ cấm '{matches}' trong văn bản bản thảo!")
            return False
    print(f"[+] Không phát hiện từ ngữ meta/cấm kỵ nào. Đạt chuẩn RULE-07 100%.")

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
description: "Bình minh trên sông Sài Gòn sau đại chiến, lực lượng an ninh tiếp quản hiện trường, Minh An trở về căn phòng trọ Nơ Trang Long và hẹn ngày về cù lao thăm mẹ."
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
        "Bình Minh Bán Đảo Thanh Đa, Bàn Giao Hiện Trường Cho Đại Úy Dũng & Minh An Trở Về Khu Trọ Nơ Trang Long",
        CHAPTER_NUM,
        1,
        f"{DATE}T12:00:00+07:00",
        CHAPTER_NUM,
        "loc_phong_tro_no_trang_long",
        json.dumps(["char_minh_an", "char_lam_tich", "char_phan_the_dung"]),
        "Bình minh rạng rỡ trên bán đảo Thanh Đa, lực lượng an ninh đặc nhiệm do Đại úy Phan Thế Dũng chỉ huy tiếp quản toàn bộ bốn chiếc sà lan và áp giải Tạ Lôi. Toàn bộ mạng lưới Cửu Long Thiên Hải tại phương Nam bị xóa sổ. Minh An từ chối huân chương công khai, chỉ mong giữ cuộc sống giản dị của người thủ hộ phàm nhân. Minh An trò chuyện tâm tình cùng Lâm Tịch tại quán trà bến đò Bình Quới, xác nhận Cổ Tháp Thần Hoang đã an định tự ẩn. Trưa cùng ngày, Minh An trở về căn gác trọ Nơ Trang Long, ăn tô hủ tiếu gõ bác Ba và gọi điện cho mẹ hẹn cuối tuần về cù lao Tiền Giang ăn cá lóc nướng trui. Khép lại trọn vẹn Hồi 2: Sóng Cuộn Phương Nam.",
        "Tiếp quản an toàn chiến trường Thanh Đa; xóa sổ hoàn toàn mạng lưới Cửu Long Thiên Hải; Cổ Tháp Thần Hoang an định; Minh An trở lại đời sống phàm nhân bình dị chuẩn bị về thăm mẹ."
    ))

    # 7.2 Cập nhật story threads
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-001'
    """, (
        CHAPTER_NUM,
        "Lâm Tịch củng cố vững chắc sáu phần nguyên thần trên Lục Diệp Thanh Liên, bày tỏ sự tin tưởng sâu sắc và cam kết đồng hành vạn dặm cùng Minh An."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An củng cố hoàn mỹ cảnh giới Hoán Huyết Sơ kỳ sau thực chiến; cương huyết lắng dịu tuần hoàn ấm áp, cốt tủy thấu quang vững chãi."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Cổ Tháp Thần Hoang chín tầng tại khúc sông Thanh Đa hoàn toàn an định, tự ẩn vào địa tầng sâu âm ba mươi mét, kết thúc trọn vẹn nguy cơ Tầng Thứ Sáu Cực Tù."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An trở về phòng trọ Nơ Trang Long, từ chối vinh danh công khai, gọi điện hẹn mẹ cuối tuần về cù lao Tiền Giang ăn cá lóc đồng nướng trui."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T12:00:00+07:00"
        inv_data["current_location"] = "Phòng Trọ Nơ Trang Long, Quận Bình Thạnh, TP. Hồ Chí Minh"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Huyết Ánh Kim / Cốt Tủy Thấu Quang / Thể Đạo Hoàn Mỹ)"

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

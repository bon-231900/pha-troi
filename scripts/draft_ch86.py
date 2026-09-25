# -*- coding: utf-8 -*-
"""Draft Chapter 86 for Phá Trời Novel OS with ~3,500+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 86
CHAPTER_TITLE = "Bão Ngầm Sài Gòn"
DATE = "2026-10-29"
LOCATION = "Bến Xe Miền Tây & Bán Đảo Thanh Đa, TP. Hồ Chí Minh"

ACT1 = '''Bốn giờ ba mươi phút sáng ngày hai mươi chín tháng mười.

Chiếc xe khách giường nằm tuyến Cà Mau – Sài Gòn khẽ rùng mình, lách qua dòng xe tải chở hàng nông sản nối đuôi nhau dài dằng dặc trên quốc lộ 1A rồi từ từ lăn bánh vào bến xe Miền Tây thuộc quận Bình Tân.

Tiếng còi hơi gầm rú chát chúa, mùi khói dầu diesel nồng nặc hòa lẫn với mùi ẩm mốc của đêm sương và hơi nóng hầm hập bốc lên từ mặt đường nhựa đặc trưng của một thành phố chưa bao giờ thực sự ngủ. Xung quanh tôi, tiếng hành khách lục đục thu dọn hành lý, tiếng gọi nhau í ới của những người phụ xe, tiếng mời chào đon đả xen lẫn sự chèo kéo quen thuộc của cánh xe ôm truyền thống và tài xế công nghệ đứng ken đặc trước cổng bến.

Tôi chỉnh lại chiếc mũ lưỡi trai sẫm màu, khoác chiếc ba-lô vải dù dã chiến cũ kỹ lên vai rồi bước xuống bậc thềm xe.

Dưới lớp vải bạt dày của chiếc ba-lô, hai món binh khí hộ thân — thanh Hắc Thiết Đoản Côn bát giác đúc từ thép nhíp Zil với những đường khía chu sa đỏ thẫm và thanh Trấn Thủy Đoản Đao bọc trong tấm da thuộc dày — vẫn nằm im lìm, không phát ra bất kỳ một rung động kim loại nào. Nhưng sự hiện diện vững chãi của chúng áp sát vào bờ vai tôi mang lại một cảm giác tự tin tuyệt đối.

Hít một hơi sâu luồng không khí đặc quánh khói bụi đô thị, tôi cảm nhận rõ sự thay đổi sâu sắc bên trong cơ thể mình.

Đây là lần đầu tiên tôi trở lại Sài Gòn kể từ khi chính thức bước chân vào cảnh giới **Hoán Huyết Sơ kỳ**.

Trước đây, khi còn ở tầng Luyện Cốt, mỗi lần hít phải khói xăng và bụi mịn của thành phố, lồng ngực tôi thường có cảm giác khô ráp, ngột ngạt. Nhưng lúc này, dòng Thuần Dương Cương Huyết mang ánh kim ấm áp đang vận hành chậm rãi nhưng bền bỉ trong từng mao mạch li ti. Mỗi phân tử khí oxy khi đi qua phổi lập tức được các tế bào máu tinh lọc triệt để, còn toàn bộ bụi bẩn và tạp chất hóa học bị một lớp màng nhầy sinh học tự nhiên giữ lại và đào thải ra ngoài mà không hề làm tổn hại đến khí quản.

Thính giác của tôi mở rộng ra một phạm vi kinh ngạc.

Giữa hàng ngàn âm thanh hỗn độn của bến xe — tiếng bước chân dồn dập, tiếng bánh xe đẩy chở hàng rít ken két trên nền xi măng, tiếng cãi vã mặc cả của một chủ sạp trái cây cách xa hơn một trăm mét — tôi vẫn có thể nghe thấy từng nhịp tim đập đều đặn của người phụ xe đứng thu vé, nghe được tiếng kim đồng hồ cơ trên cổ tay một hành khách đi lướt qua bên cạnh.

Nhưng điều khiến tôi cau mày ngay khi vừa đặt chân xuống nền đất Sài Gòn chính là địa khí.

Là một người đã tự tay an định trọn vẹn mười hai cọc tiêu Thủy Môn ngoài duyên hải phương Nam, mối liên kết vô hình giữa tôi và địa mạch sông nước Nam Bộ đã đạt tới mức độ tương thông mật thiết.

Lúc này, sâu dưới lớp bê tông dày cộm và mạng lưới cống ngầm chằng chịt của thành phố mười triệu dân, dòng địa mạch của sông Sài Gòn và sông Đồng Nai không hề êm ả chảy trôi như thường nhật. Nó đang rung lên những chấn động trầm đục, nghẹn ứ và đầy bất an. 

Có một luồng âm trọc khí màu xám chì đang âm ỉ thẩm thấu từ lòng đất, giống như một khối u ác tính đang bị ai đó cố tình chọc ngoáy, kích thích cho mưng mủ.

"Cửu Long Thiên Hải đã bắt đầu ra tay rồi," tôi thầm nhủ trong lòng, ánh mắt chợt lóe lên một tia sắc lạnh.

Tôi hòa mình vào dòng người lao động đang hối hả rời khỏi bến xe, rảo bước về phía trạm xe buýt công cộng. Tôi không bắt taxi công nghệ hay bất kỳ phương tiện nào có định vị mạng viễn thông. Sau trận đại chiến ngoài khơi Cà Mau và việc Tạ Bách Xuyên bị sa lưới, tổng bộ Cửu Long Thiên Hải chắc chắn đã đặt toàn bộ mạng lưới camera giám sát giao thông và dữ liệu viễn thông tại các cửa ngõ thành phố vào tình trạng báo động đỏ nhằm săn lùng tung tích của tôi.

Nhưng chúng không thể ngờ rằng, một võ giả Thể Đạo đã đạt tới Hoán Huyết kỳ có thể hoàn toàn khống chế thân nhiệt, nhịp thở và nhịp tim của bản thân đến mức trở thành một "bóng ma" vô hình trước mọi cảm biến hồng ngoại hiện đại nhất.'''

ACT2 = '''Sáu giờ mười lăm phút sáng.

Tôi có mặt tại đầu con hẻm nhỏ trên đường Nơ Trang Long, thuộc địa phận quận Bình Thạnh — nơi tọa lạc dãy nhà trọ cấp bốn lợp mái tôn xi măng mà tôi đã thuê ở suốt bốn năm qua kể từ ngày rời trường đại học.

Khu xóm lao động nghèo vẫn chưa hoàn toàn tỉnh giấc. Mùi hương ngầy ngậy của nồi nước lèo quán phở bò đầu hẻm, tiếng chổi tre quét rác xào xạc của bà cụ tổ trưởng dân phố và làn khói hương trầm thoang thoảng từ bàn thờ thiên trước hiên nhà tạo nên một khung cảnh bình dị, thân thương đến nao lòng.

Thế nhưng, ngay khoảnh khắc tôi vừa bước chân vào đầu con hẻm rải nhựa lem nhem những vệt dầu loang, toàn bộ ba mươi ba đốt sống tủy ngọc sau lưng tôi bỗng khẽ rung lên một nhịp cảnh báo buốt lạnh.

Cương huyết trong lồng ngực tôi lập tức chảy xiết.

Có sát khí!

Tôi dừng bước bên một chiếc xe bán bánh mì kẹp thịt vỉa hè, vờ như đang móc ví lấy tiền lẻ mua bữa sáng, nhưng mọi giác quan của Hoán Huyết Sơ kỳ đã âm thầm phóng thích ra toàn bộ không gian xung quanh.

Thính giác siêu phàm của tôi bắt được bốn nhịp thở cực kỳ đều đặn, chậm rãi và căng thẳng — nhịp thở của những tay súng chuyên nghiệp đã trải qua huấn luyện quân sự bài bản.

Hai nhịp thở phát ra từ tầng thượng của ngôi nhà ba tầng đối diện dãy phòng trọ của tôi, cách mặt đất chừng mười hai mét. Hai nhịp thở còn lại nằm trên gác xép của một xưởng mộc bỏ hoang ở cuối hẻm, tạo thành một góc bắn chéo hoàn hảo khống chế toàn bộ lối vào căn phòng trọ số 4 của tôi.

Không chỉ có vậy. Dưới sự vận hành của Tâm Nhãn kết hợp với khứu giác tinh tế, tôi ngửi thấy một mùi hăng hắc quen thuộc của thuốc nổ công nghiệp C4 pha lẫn mùi lưu huỳnh của kíp nổ kích hoạt từ xa bằng sóng vô tuyến tần số cao.

Căn phòng trọ của tôi đã bị chúng biến thành một cái bẫy tử thần!

Bên dưới bậc cửa gỗ mục và tấm nệm gấp đơn sơ trong phòng, chúng đã cài sẵn ít nhất hai khối mìn định hướng Claymore cải tiến. Chỉ cần tôi tra chìa khóa vào ổ hoặc đẩy cánh cửa bước vào, tín hiệu áp suất cơ học hoặc sóng hồng ngoại sẽ lập tức kích nổ toàn bộ căn phòng, san phẳng cả dãy trọ và cướp đi sinh mạng của hàng chục người dân vô tội xung quanh.

Một cơn giận dữ lạnh băng dâng trào trong lồng ngực tôi.

Bọn tà tu Cửu Long Thiên Hải này thực sự đã mất hết nhân tính. Vì muốn tiêu diệt tôi, chúng sẵn sàng xem mạng sống của những người lao động nghèo nơi khu trọ này như cỏ rác!

"Minh An..."

Một thanh âm trong trẻo như sương sớm bỗng khẽ vang lên trong tâm trí tôi. Lâm Tịch đã tỉnh táo quan sát tình hình từ đài sen ngọc bích trong thức hải:

"Cung vị bắn tỉa ở hướng tây bắc đang giữ chiếc điều khiển kích nổ dự phòng. Đừng dùng kình lực chấn động mạnh, sóng xung kích có thể kích hoạt ngòi nổ quán tính của khối bẫy."

"Tôi hiểu," tôi đáp lại trong tâm thức, giọng lạnh như băng tuyết. "Tôi sẽ không để một hạt thuốc nổ nào kịp bốc cháy giữa khu dân cư này."

Tôi nhận lấy ổ bánh mì nóng giòn từ tay người phụ nữ bán hàng, mỉm cười cảm ơn rồi thong thả bước vào con hẻm nhánh phía sau xưởng mộc.

Vừa bước qua góc khuất của bức tường rêu phong, thân hình tôi bỗng khẽ nhòe đi.

Áp dụng khẩu quyết **Quy Tức Cùng Cực**, toàn bộ khí tức sinh học của tôi thu liễm hoàn toàn về con số không. Trọng lượng cơ thể hơn bảy mươi ki-lô-gam dường như tan biến vào hư không, tôi áp sát lưng vào mép tường gạch, ngón chân khẽ điểm nhẹ lên gờ cửa sổ rồi bật người phóng thẳng lên mái tôn xưởng mộc.

Động tác mượt mà, tĩnh lặng như một chiếc lá rơi giữa đêm thu. Không một tiếng kim loại rỉ sét nào vang lên, không một viên sỏi nhỏ nào bị xê dịch.

Trên gác xép xưởng mộc ẩm mốc bụi bặm, hai gã lính đánh thuê mặc đồ rằn ri tác chiến đô thị đang nằm sấp trên tấm bạt dã chiến. Một tên cầm súng bắn tỉa nòng dài gắn ống giảm thanh và kính ngắm tầm nhiệt, tên còn lại đeo ống nhòm đo khoảng cách la-ze, tay lăm lăm chiếc bộ đàm mã hóa.

"Mục tiêu vẫn chưa xuất hiện tại khu vực Nơ Trang Long. Báo cáo tổng bộ, các tuyến xe Miền Tây đã kiểm soát xong nhưng không thấy biển số xe khả nghi," tên cầm bộ đàm đang thì thào bằng tiếng lóng quân sự.

"Tiếp tục quan sát. Lệnh của Tạ tổng quản: phát hiện bóng dáng là kích nổ ngay, không cần giữ lại toàn thây..." tên cầm súng bắn tỉa lạnh lùng đáp.

Hắn chưa kịp dứt câu thì một cái bóng đen đã lặng lẽ xuất hiện ngay sau lưng cả hai.

Tôi không rút côn, cũng không rút đao.

Với cảnh giới Hoán Huyết Sơ kỳ, cơ thể phàm nhân đã chính là món hung khí đáng sợ nhất.

*VÚT! VÚT!*

Hai ngón tay tôi khẽ búng ra trong không khí. Hai luồng kình lực **Cương Khí Ly Thể** cô đọng như hai viên đạn cao su vô hình xé gió bắn thẳng vào huyệt Đại Chùy sau gáy của hai gã thiện xạ.

Không có tiếng va chạm mạnh bạo, cũng không có máu me đổ ra.

Cả hai tên lính đánh thuê chỉ kịp trợn trừng mắt, toàn bộ hệ thần kinh trung ương lập tức bị tê liệt hoàn toàn. Chúng đổ gục xuống tấm bạt một cách mềm oặt, rơi vào trạng thái hôn mê sâu kéo dài ít nhất mười hai giờ mà không kịp phát ra dù chỉ một tiếng rên rỉ.

Tôi bước tới, tháo lấy chiếc bộ đàm mã hóa chuyên dụng và chiếc máy tính bảng tác chiến chiến thuật trên người tên chỉ huy, đồng thời nhanh tay ngắt toàn bộ mạch nối của chiếc điều khiển vô tuyến dự phòng.

Chưa đầy hai phút sau, tôi đã luồn sang nóc nhà ba tầng phía đối diện. Kịch bản tương tự lặp lại với hai tên bắn tỉa còn lại: trước tốc độ và kình lực cách không của một võ giả Thể Đạo, bốn tay súng tinh nhuệ được trang bị tận răng của Cửu Long Thiên Hải hoàn toàn bị vô hiệu hóa trong sự tĩnh lặng tuyệt đối.

Toàn bộ khu phố lao động vẫn êm đềm trôi qua trong buổi sớm mai, không một ai hay biết vừa có một thảm kịch kinh hoàng được ngăn chặn kịp thời.'''

ACT3 = '''Mười một giờ trưa.

Nắng vàng rực rỡ đổ xuống những khúc sông quanh co bao bọc lấy bán đảo Thanh Đa — một ốc đảo xanh kỳ lạ nằm lọt thỏm giữa lòng thành phố Hồ Chí Minh sầm uất.

Trái ngược với vẻ hoa lệ của những tòa tháp chọc trời bọc kính phản quang hiện đại ở bờ Thảo Điền bên kia sông, bán đảo Thanh Đa vẫn giữ nguyên vẻ hoang sơ, tịch mịch với những rặng dừa nước nghiêng mình soi bóng xuống dòng sông đỏ nặng phù sa, những đầm sen bát ngát và các khu đất giải tỏa dở dang phủ đầy cỏ dại.

Tôi ngồi trên bờ kè bê tông cũ kỹ sát mép sông, dưới bóng râm của một rặng bần cổ thụ đang trổ hoa trắng muốt.

Trên màn hình chiếc máy tính bảng tác chiến thu giữ từ toán lính đánh thuê, những tấm bản đồ vệ tinh độ phân giải cực cao hiển thị dày đặc các tọa độ đo đạc địa chấn ngầm dọc theo khúc uốn móng ngựa của sông Sài Gòn.

Tập đoàn Cửu Long Thiên Hải không hề từ bỏ dã tâm. Thất bại thảm hại ở duyên hải miền Tây và việc mất đi mười hai cọc tiêu Thủy Môn chỉ khiến chúng trở nên điên cuồng và liều lĩnh hơn bao giờ hết.

Dưới sự chỉ đạo trực tiếp của Tạ Lôi — kẻ đứng đầu bộ phận tác chiến đặc biệt tại tổng bộ Sài Gòn — chúng đã điều động bốn chiếc sà lan hút cát cỡ lớn, ngụy trang dưới danh nghĩa dự án nạo vét luồng hàng hải nội địa, neo đậu cố định tại khúc sông Ba Son và Thanh Đa. Nhưng sâu dưới khoang đáy của những chiếc sà lan đó không phải là máy hút cát thông thường, mà là các máy phát xung chấn điện từ tần số cực thấp kết hợp với những khối trận bàn tà thuật bằng huyết thạch.

Mục tiêu của chúng: dùng xung chấn nhân tạo để xé toạc lớp bùn sét địa tầng cổ sâu ba mươi mét dưới đáy sông Sài Gòn, cưỡng bức kích hoạt ngọn **Cổ Tháp Thần Hoang** viễn cổ trồi lên mặt nước!

"Minh An, hãy mở Tâm Nhãn nhìn xuống lòng sông xem," giọng nói của Lâm Tịch vang lên, mang theo vẻ nghiêm cẩn sâu sắc.

Tôi khẽ gật đầu, hít sâu một hơi rồi nhắm mắt lại.

Dưới sự dẫn dắt của Thuần Dương Cương Huyết bừng sáng trong kinh mạch, ba mươi ba đốt sống tủy ngọc của tôi phát ra ánh sáng thấu quang. Năng lực Tâm Nhãn từng giúp tôi lặn sâu xuống vực Cực Tù âm một nghìn hai trăm mét nay một lần nữa được phóng thích ra ngoài.

Tầm nhìn của tôi xuyên qua lớp nước sông đục ngầu phù sa, xuyên qua đáy sông lầy lội, cắm sâu xuống tầng địa chất bazan nằm ở độ sâu âm ba mươi mét.

Và rồi, một cảnh tượng hùng vĩ đến nghẹt thở hiện ra trước mắt tôi!

Chìm sâu dưới lòng phù sa sông Sài Gòn suốt hai phẩy năm triệu năm qua, một ngọn cổ tháp phong ấn chín tầng bằng đá huyền vũ đen nhánh sừng sững ngự trị. Toàn bộ ngọn tháp được chạm khắc vô số đồ án thần long và triện văn thái cổ phức tạp, tỏa ra những luồng linh quang màu hoàng kim và lam ngọc đan xen vào nhau như một mạng lưới tinh hà rực rỡ.

Chín sợi xích huyền thiết khổng lồ, mỗi mắt xích to bằng cả thân cây cổ thụ, neo chặt chín góc của cổ tháp vào nền đá gốc sâu thẳm của thềm lục địa.

Đó chính là ngọn tháp phong ấn trung tâm của **Tầng Thứ Sáu Cực Tù Lục Trọng Giới**!

Mười hai cọc Thủy Môn ngoài duyên hải phương Nam chính là mười hai đường kinh mạch dẫn địa khí từ biển lớn về nuôi dưỡng ngọn tháp này. Khi tôi an định mười hai cọc tiêu, dòng địa khí thanh khiết dội ngược về đã đánh thức phong ấn cổ xưa, khiến ngọn tháp bắt đầu tỏa ra ánh sáng hộ trì đất trời.

Nhưng lúc này, xung quanh ngọn cổ tháp thần thánh ấy, bốn luồng hắc khí màu tím đen bốc lên từ đáy của bốn chiếc sà lan ngụy trang đang như bốn con độc xà hung hãn, không ngừng gặm nhấm và làm xói mòn các mắt xích huyền thiết!

"Nếu bốn mắt xích ở hướng đông nam bị chúng phá vỡ hoàn toàn," Lâm Tịch ngưng tụ thần ảnh trên đài sen, sắc mặt nghiêm trọng, "ngọn cổ tháp sẽ mất thăng bằng địa tầng. Áp suất nén hàng triệu năm dưới lòng đất sẽ bùng nổ, gây ra một trận sụt lún địa chất khủng khiếp nuốt chửng toàn bộ bán đảo Thanh Đa và các quận lân cận xuống lòng sông, đồng thời mở toang cánh cổng giải phóng toàn bộ âm trọc tà ma của Tầng Thứ Sáu ra nhân gian!"

Bàn tay tôi siết chặt lại, khớp xương kêu lên những tiếng tanh tách giòn giã.

Tôi sinh ra và lớn lên trên mảnh đất Nam Bộ này. Từng khúc sông, từng con rạch, từng mái nhà của thành phố này đều gắn liền với mồ hôi, nước mắt và ký ức của biết bao thế hệ người dân hiền lành. Tôi tuyệt đối không cho phép bất kỳ kẻ nào biến nơi đây thành địa ngục trần gian!

Đúng lúc đó, chiếc bộ đàm mã hóa tác chiến thu giữ từ tên chỉ huy bắn tỉa bỗng phát ra một tràng rè rè của sóng ngắn.

Một giọng cười khàn đục, ngạo mạn và tràn đầy ác hiểm vang lên từ đầu loa bên kia:

"Số 1, số 2... Các người đã xong việc ở khu trọ Nơ Trang Long chưa? Thằng ranh Nguyễn Minh An đã về thành phố rồi. Lệnh của Tạ tổng quản: không cần chờ hắn xuất hiện nữa. Chúng ta vừa nhận được tin hắn từng để lại toàn bộ hồ sơ mẫu lõi địa chất tại Viện Khảo sát Địa chất trên đường Hoàng Hoa Thám. Cho nổ tung khu trọ để nghi binh cảnh sát, đồng thời cho toán 3 đột nhập san phẳng Viện Địa chất, thu hồi toàn bộ tài liệu nghiên cứu của hắn!"

Nghe thấy những lời đó, ánh mắt tôi bỗng lạnh buốt như băng hàn vạn trượng.

Viện Khảo sát Địa chất — nơi những người thầy, những người đồng nghiệp cũ tận tụy của tôi vẫn đang ngày đêm miệt mài nghiên cứu đất đá quê hương. Chúng muốn dùng máu của những người vô tội để ép tôi phải lộ diện!

Tôi nhấc chiếc bộ đàm lên, ngón tay ấn chặt vào nút phát sóng. Giọng nói của tôi trầm thấp, vững chãi tựa như tiếng sấm rền từ lòng đất vọng lên:

"Tạ Lôi... Ngươi không cần phải nhọc công tìm kiếm ở Nơ Trang Long hay Viện Địa chất nữa."

Đầu dây bên kia bỗng im bặt. Tiếng cười ngạo mạn đột ngột tắt ngấm, chỉ còn lại tiếng thở dồn dập kinh hãi:

"Mày... Nguyễn Minh An?! Làm sao mày có được kênh sóng này?! Lũ bắn tỉa đâu hết rồi?!"

Tôi nhìn ra dòng sông Sài Gòn đang cuộn sóng phù sa dưới ánh nắng trưa rực rỡ, khóe môi khẽ nhếch lên một nụ cười ngạo nghễ của người thủ hộ phàm nhân:

"Bốn con chó săn của ngươi đã ngủ say rồi. Mười hai cọc Thủy Môn ngoài biển lớn ta đã bẻ gãy âm mưu của các ngươi. Giờ đây đến lượt dòng sông Sài Gòn này. Hãy gom hết tà binh và những chiếc sà lan bẩn thỉu của các ngươi lại... Ta đang đợi các ngươi ở ngã ba sông Thanh Đa!"

*RẮC!*

Kình lực Hoán Huyết bộc phát từ lòng bàn tay tôi, nghiền nát chiếc bộ đàm quân sự bằng hợp kim thành một đống vụn sắt méo mó.

Gió từ mặt sông Sài Gòn bỗng nổi lên lồng lộng, thổi bay tà áo dã chiến của tôi.

Dưới đáy sâu ba mươi mét, ngọn Cổ Tháp Thần Hoang dường như cảm ứng được lời thề son sắt của người thủ hộ, khẽ rung lên một đạo linh quang hoàng kim rực rỡ.

Bão ngầm Sài Gòn đã chính thức bắt đầu, và tôi sẽ là người dập tắt nó bằng chính đôi bàn tay trần của một phàm nhân!'''

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
description: "Minh An trở lại Sài Gòn ở cảnh giới Hoán Huyết Sơ kỳ, vô hiệu hóa bẫy mìn phục kích tại khu trọ Nơ Trang Long, đối đầu Tạ Lôi tại ngã ba sông bán đảo Thanh Đa."
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
        "Minh An Trở Lại Sài Gòn, Phá Bẫy Phục Kích Nơ Trang Long & Khóa Chặt Chiến Địa Bán Đảo Thanh Đa",
        CHAPTER_NUM,
        1,
        f"{DATE}T12:00:00+07:00",
        CHAPTER_NUM,
        "loc_ban_dao_thanh_da",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An về đến bến xe Miền Tây trong cảnh giới Hoán Huyết Sơ kỳ, cảm ứng địa khí bất an của sông Sài Gòn. Di chuyển về phòng trọ cũ Nơ Trang Long, phát hiện bẫy mìn định hướng và 4 tay súng bắn tỉa của Cửu Long Thiên Hải. Dùng Quy Tức Cùng Cực và Cương Khí Ly Thể vô hiệu hóa êm thắm toàn bộ toán mai phục. Di chuyển ra bán đảo Thanh Đa, dùng Tâm Nhãn nhìn sâu -30m dưới lòng sông phát hiện Cổ Tháp Thần Hoang 9 tầng bị 4 sà lan tà thuật công kích mắt xích. Chặn sóng bộ đàm thách chiến trực diện Tạ Lôi, mở màn đại chiến bảo vệ Sài Gòn.",
        "Vô hiệu hóa toàn bộ bẫy mai phục đô thị; phát hiện vị trí chính xác Cổ Tháp Thần Hoang tại bán đảo Thanh Đa; tuyên chiến trực diện Tạ Lôi và tổng bộ Cửu Long Thiên Hải."
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
        "Lâm Tịch chỉ điểm thần niệm từ đài sen, giúp Minh An nhận diện ngòi nổ quán tính và bố cục Cổ Tháp Thần Hoang 9 tầng dưới đáy sông Sài Gòn."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An thể hiện uy lực Hoán Huyết Sơ kỳ giữa đô thị: lọc sạch khói độc bằng dòng cương huyết, Cương Khí Ly Thể điểm huyệt cách không, Tâm Nhãn xuyên thấu -30m đáy sông."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Bí mật Tầng Thứ Sáu Cực Tù Lục Trọng Giới hiển lộ: Cổ Tháp Thần Hoang 9 tầng bị 9 sợi xích huyền thiết trói dưới đáy sông Sài Gòn khúc Thanh Đa đang bị 4 sà lan tà thuật tấn công."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-CHR-001'
    """, (
        CHAPTER_NUM,
        "Minh An bóp nát bộ đàm tuyên chiến Tạ Lôi, bảo vệ an toàn cho khu dân cư Nơ Trang Long và Viện Khảo sát Địa chất."
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
        inv_data["current_location"] = "Bán Đảo Thanh Đa, Quận Bình Thạnh, TP. Hồ Chí Minh"
        inv_data["cultivation_realm"] = "Hoán Huyết Sơ kỳ (Cương Huyết Ánh Kim / Cốt Tủy Thấu Quang / Cương Khí Ly Thể)"

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

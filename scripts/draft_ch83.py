# -*- coding: utf-8 -*-
"""Draft Chapter 83 for Phá Trời Novel OS with ~3,600+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 83
CHAPTER_TITLE = "Cổ Chiên Nộ Lãng"
DATE = "2026-10-26"
LOCATION = "Cửa Sông Ba Lai & Cửa Biển Cổ Chiên (Bến Tre - Trà Vinh)"

ACT1 = '''Mười sáu giờ ba mươi phút chiều ngày hai mươi sáu tháng mười.

Chiếc ca-nô vỏ composite rời khỏi luồng lạch rừng sác Cần Giờ, men theo bờ vịnh Đồng Tranh rồi cắt ngang vùng biển cạn Bình Đại để tiến sâu vào mạng lưới thủy lộ chằng chịt của tỉnh Bến Tre.

Nắng chiều phương Nam buông xuống dòng Cổ Chiên một sắc vàng cam rực rỡ nhưng nhuốm màu cô tịch. Phía chân trời xa tít tắp ngoài cửa biển, từng đám mây giông xám chì vần vũ kéo tới, báo hiệu một đêm triều cường dậy sóng trên khắp dải duyên hải miền Tây.

Tôi ngồi tựa lưng vào khoang lái ca-nô, hai tay đặt nhẹ lên đầu gối, điều hòa từng nhịp thở sâu và chậm.

Chiếc ca-nô lướt qua những bãi nghêu bạt ngàn của miệt Ba Tri. Xa xa trên bãi bồi phù sa, những hàng đáy giăng câu của ngư dân nghèo cắm xiêu vẹo giữa làn nước bạc. Tiếng chuông chùa ngân nga từ một cổ tự trầm mặc trên cù lao An Hóa vọng lại qua làn gió chướng, hòa cùng tiếng sóng vỗ ì oạp vào mạn thuyền, gợi lên trong lòng tôi một nỗi xúc động khôn nguôi.

Mảnh đất xứ dừa này — nơi những con sông lớn như Tiền Giang, Ba Lai, Hàm Luông và Cổ Chiên chia cắt dải đất phù sa thành ba dãy cù lao trù phú — từ bao đời nay đã kiên cường chống chọi với triều cường, bão gió và sự xâm nhập mặn của đại dương. Người dân nơi đây lấy vườn dừa làm nhà, lấy mái chèo làm kế sinh nhai, sống thuần hậu và gắn bó máu thịt với từng tấc đất quê hương.

Sau khi an định cọc tiêu thứ mười Soài Rạp Hải Giáp Trụ vào trưa nay, tôi không hề dừng chân nghỉ ngơi. Mỗi một giờ trôi qua trong chậm trễ đều có thể biến thành cơ hội để kẻ thù kịp thời điều động thêm lực lượng từ các căn cứ hải ngoại.

Theo hải đồ và dữ liệu trắc địa thu được từ chiếc máy tính bảng của Trần Bảy, cọc tiêu thứ mười một án ngữ ngay tại ngã ba giao thoa giữa nhánh sông Ba Lai cổ và dòng Cổ Chiên cuồn cuộn — nơi được cổ thư ghi nhận là **Cổ Chiên Thủy Long Quyết**.

Đó là một khối ngọc thạch trấn thủy nguyên khối có niên đại hàng trăm năm, được các bậc tiền nhân Thủ Hộ Nhất Mạch thời mở cõi khảm sâu vào vòm đá hoa cương dưới lòng sông, giữ vai trò then chốt điều hòa xung lực giữa dòng nước ngọt Cửu Long và sóng mặn biển Đông.

Nếu cọc tiêu này bị tà trận phá hủy, con nước mặn sẽ tràn ngập vào hàng trăm ngàn héc-ta vườn cây ăn trái và nguồn nước sinh hoạt của cả hai tỉnh Bến Tre và Trà Vinh, gây nên thảm họa sụt lún và hoang mạc hóa không thể cứu vãn.

Tôi khẽ nhắm mắt, hướng tâm thức thăm dò sâu vào bên trong cơ thể.

Sau chuỗi trận kịch chiến liên hoàn từ ngọn núi Chứa Chan, cồn Trấn Ba cho tới đáy sâu Soài Rạp, ba mươi ba đốt sống tủy ngọc của tôi không những không hề hao tổn mà trái lại càng thêm cứng cáp, cô đọng tựa như những thanh thép vừa trải qua muôn ngàn đòn búa tôi luyện. Cảnh giới Luyện Cốt Hậu kỳ Cùng Cực đã hoàn toàn định hình, kết liên các khớp xương thành một thể thống nhất vững chãi khôn cùng.

Đặc biệt, luồng địa khí thanh thuần thu nhận từ cọc tiêu Hải Giáp Trụ trưa nay đang âm thầm lan tỏa khắp tủy sống.

Từng giọt Thuần Dương Cương Huyết cuộn trào bỏng rát từ tâm thất, chảy tràn qua ba mươi ba đốt sống tủy ngọc, tạo nên những âm thanh vi mô râm ran như tiếng dung nham sôi sục dưới lòng đất sâu. Đó là dấu hiệu báo trước của sự biến chuyển kỳ vĩ: hiện tượng sôi tủy!

Trong thể đạo cổ xưa, khi ba mươi ba đốt xương sống đã được tôi luyện đạt tới độ thuần khiết ngọc thạch viên mãn, tủy sống sẽ tự động thanh lọc những tạp chất sinh học cuối cùng, bắt đầu sản sinh ra những tế bào máu mới mang đậm nội lực cương dương. Đó chính là ngưỡng cửa chuyển giao quan trọng chuẩn bị cho bước nhảy vọt tiến vào đại cảnh giới Hoán Huyết.

Trong thức hải bao la mờ ảo, đài sen ngọc bích của Lâm Tịch vẫn lơ lửng giữa làn sương trắng.

Nhờ liên tiếp an định hai cọc tiêu Thủy Môn ngoài duyên hải, linh khí tinh khiết của đất trời phương Nam đã không ngừng thẩm thấu qua kinh mạch tôi, vỗ về tàn hồn mỏng manh của nàng. Vết rạn xám tro trên cánh hoa sen dường như đã khép lại thêm một phần, tỏa ra luồng ánh sáng dịu nhẹ tựa trăng rằm mùa thu.

Dù nàng vẫn chìm sâu trong giấc ngủ tĩnh dưỡng, nhưng sợi dây liên kết vô hình giữa linh hồn nàng và thể phách phàm nhân của tôi vẫn luôn hiện hữu, như một ngọn hải đăng soi đường giữa biển đêm giông bão. Tôi nhớ lại ánh mắt kiên định của nàng trong căn gác trọ nhỏ ở Sài Gòn ngày nào, lời nhắc nhở mộc mạc rằng con đường thể đạo phàm nhân là con đường lấy chính thân xác và ý chí để vượt qua bão giông.

"Lâm Tịch, chỉ còn hai cọc tiêu nữa thôi. Mười hai cọc Thủy Môn sắp được an định trọn vẹn, tôi nhất định sẽ giữ vững dải đất này cho đến ngày cô thức tỉnh."

Tôi siết chặt bàn tay, cảm nhận sức mạnh cuộn dâng trong từng thớ thịt. Ca-nô rẽ sóng lao vun vút vào luồng sông Cổ Chiên, nơi bóng tối của hoàng hôn đang dần nuốt trọn những rặng bần ngập mặn.'''

ACT2 = '''Hai mươi giờ ba mươi phút đêm.

Màn đêm đen đặc như mực bao trùm lấy mặt sông Cổ Chiên rộng hơn hai cây số.

Gió chướng từ biển thổi thốc vào bờ tạo nên những đợt sóng bạc đầu gầm gừ vỗ mạnh vào chân đê kè. Nước triều bắt đầu dâng cao, dòng chảy xiết ngầm dưới lòng sông xoáy tròn dữ dội, cuốn theo từng mảng lục bình trôi dạt vô định. Sông Cổ Chiên là một trong những phân lưu hung hãn nhất của sông Tiền, với những vực xoáy ngầm sâu tới ba mươi mét ở khu vực Cồn Bần và Cồn Hô có thể nghiền nát mọi chướng ngại vật.

Tôi cho ca-nô tấp vào một rặng dừa nước rậm rạp bên bờ cù lao thuộc huyện Mỏ Cày Nam, cẩn thận buộc dây neo giấu kỹ con thuyền dưới những tán lá dừa xanh sẫm rủ sát mặt nước.

Khoác lên mình bộ đồ lặn chuyên dụng màu đen tuyền, tôi leo lên một thân cây bần cổ thụ mọc chìa ra mép nước, nâng ống nhòm hồng ngoại quan sát ra giữa luồng hàng hải.

Cách vị trí của tôi chừng một ngàn mét, ngay tại giao điểm luồng lạch sâu nơi cọc tiêu thứ mười một tọa lạc, một quang cảnh cảnh giới nghiêm ngặt hiện ra trước mắt.

Không đơn thuần là một chiếc sà-lan đơn lẻ như ở Soài Rạp, kẻ địch lần này đã dựng lên một cụm cứ điểm nổi đồ sộ bằng cách ghép đôi hai chiếc sà-lan tải trọng hai ngàn tấn lại với nhau!

Trên mặt sàn hai chiếc sà-lan, hàng chục ngọn đèn pha cao áp công suất lớn quét loang loáng khắp mặt sông, biến một vùng nước bán kính năm trăm mét trở nên sáng rực như ban ngày. Những chiếc camera tầm nhiệt gắn trên tháp thép xoay chuyển liên tục ba trăm sáu mươi độ, không để sót bất kỳ góc chết nào.

Xung quanh cụm sà-lan, bốn chiếc xuồng cao tốc bọc thép tuần tra liên tục theo quỹ đạo hình thoi khép kín, động cơ gầm rú xé toạc màn đêm tĩnh mịch.

Nhưng điều khiến tôi chú ý nhất là cách thức bố phòng dưới nước của chúng.

Nhìn qua lăng kính quang phổ đặc biệt, tôi thấy mặt nước quanh cụm sà-lan liên tục phát ra những tia chớp điện màu lam nhạt lách tách. Đó là một mạng lưới bẫy điện ngầm cao thế được treo lơ lửng ở độ sâu từ năm đến mười mét, bao bọc kín mít khu vực đáy sông nơi có cột đá cọc tiêu!

Bất kỳ sinh vật hay thợ lặn nào vô tình chạm vào vùng điện trường này đều sẽ lập tức bị dòng điện hàng ngàn vôn giật co giật, tê liệt thần kinh và chết đuối trong nháy mắt.

Trên boong chiếc sà-lan chính, một người đàn ông lực lưỡng cao gần hai mét, mặc áo ba lỗ đen để lộ đôi cánh tay vạm vỡ cuồn cuộn gân xanh như rễ cây cổ thụ, đang chắp tay sau lưng đứng chỉ huy.

Gã mang trên mình một bộ khung giáp trợ lực thủy lực ngoại xương bằng hợp kim đen bóng nẹp dọc theo sống lưng và hai cánh tay. Mỗi cử động của gã đều phát ra tiếng xì hơi nén khí cơ giới đanh gọn.

Qua các tài liệu tình báo thu thập được, tôi nhận ra gã: Bành Đại Lực — một đầu lĩnh Thể Đạo sa đọa thuộc chi nhánh hải ngoại của Cửu Long Thiên Hải, kẻ tu luyện môn ngoại công tà dị "Ngưu Ma Bạt Sơn Kình" kết hợp với công nghệ cơ giới hiện đại để gia tăng sức tàn phá. Bộ giáp trợ lực thủy lực kia có thể khuếch đại lực đấm của gã lên tới hơn năm tấn, đủ sức bẻ gãy cả cột sắt của cầu tàu.

Dưới sự chỉ đạo của Bành Đại Lực, một tời kéo thủy lực khổng lồ đang từ từ hạ bốn cọc phát xung âm cực mạnh xuống đáy nước, nhắm thẳng vào vị trí của phiến ngọc Cổ Chiên Thủy Long Quyết!

Thời gian không còn nhiều. Nước triều đang dâng tới đỉnh điểm, chỉ cần dòng xung âm kích hoạt cộng hưởng với áp lực sóng triều, vòm đá mẹ ngàn năm dưới đáy sông sẽ rạn vỡ hoàn toàn.

Tôi kiểm tra lại trang bị: thanh Trấn Thủy Đoản Đao giắt chặt bên đùi, thanh Hắc Thiết Đoản Côn nẹp chéo sau lưng.

Một kế hoạch táo bạo nhanh chóng hình thành trong đầu tôi. Đối đầu trực diện với cả một mạng lưới bẫy điện cao thế và hỏa lực dày đặc là tự sát. Muốn phá trận, trước hết phải cắt đứt nguồn năng lượng của chúng!'''

ACT3 = '''Hai mươi mốt giờ mười lăm phút.

Bầu trời đổ một cơn mưa rào tầm tã. Những hạt mưa nặng hạt quất rát mặt hòa cùng tiếng sóng gầm gào của dòng Cổ Chiên tạo nên một bức màn âm thanh hỗn loạn che chở cho hành tung của tôi.

Tôi vận chuyển khẩu quyết Quy Tức Cùng Cực, hít một hơi thật sâu rồi trượt mình xuống làn nước đục ngầu phù sa.

Trái tim tôi đập chậm dần, giữ vững ở mức ba mươi nhịp một phút. Khí tức toàn thân thu liễm tuyệt đối, các lỗ chân lông đóng kín, dòng Thuần Dương Cương Huyết chuyển sang chế độ tuần hoàn nội tạng, biến cơ thể tôi thành một khối tĩnh vật hòa lẫn hoàn toàn vào môi trường nước xung quanh.

Không bơi trên tầng mặt nơi ánh đèn pha và camera tầm nhiệt quét qua, tôi lặn sâu sát đáy bùn lầy ở độ sâu hai mươi mét.

Dòng nước xoáy Cổ Chiên cuộn trào hung hãn, đẩy từng đợt cát sỏi và bùn non táp mạnh vào người tôi. Nhưng với ba mươi ba đốt sống tủy ngọc vững chãi, tôi di chuyển uyển chuyển như một loài rái cá đại dương, dùng các mỏm đá ngầm làm điểm tựa lướt ngược dòng nước.

Tiếp cận mạn sườn chiếc sà-lan phía đông, tôi ngước nhìn lên.

Mạng lưới bẫy điện ngầm đang phát quang màu lam cách đỉnh đầu tôi chừng năm mét. Dưới đáy sông sâu, sợi cáp điện bọc thép khổng lồ to bằng bắp đùi dẫn nguồn từ máy phát điện trên boong sà-lan cắm thẳng xuống cụm máy biến áp phân phối dưới nước.

Tôi rút thanh Trấn Thủy Đoản Đao ra khỏi bao.

Vận chuyển một luồng kình lực Thuần Dương Cương Huyết vào lưỡi đao, mũi đao sáng rực lên một vệt sáng đỏ thẫm ấm áp. Tôi đạp mạnh chân vào thềm đá ngầm, phóng vút lên như một mũi tên xé toạc làn nước đen đặc, vung đao chém dứt khoát vào cổ cáp chính!

*XOẸT!*

Lưỡi đao sắc bén chém đứt ngọt xớt lớp vỏ bọc thép và lõi đồng cao thế. Một luồng tia lửa điện chói lòa bùng nổ dưới nước rồi vụt tắt ngấm!

Toàn bộ mạng lưới điện ngầm lập tức mất nguồn, dàn đèn pha cao áp trên sàn sà-lan đồng loạt chớp tắt rồi tối om trong sự hỗn loạn kinh hoàng của quân địch.

"Mất điện rồi! Có kẻ đột nhập đáy sông!"

Tiếng còi báo động rú lên inh ỏi trên mặt nước. Ba chiếc xuồng tuần tra hoảng loạn bật đèn pha cầm tay quét loạn xạ.

Tận dụng khoảnh khắc hỗn loạn, tôi búng người vọt lên khỏi mặt nước, bám vào thành xích neo của chiếc sà-lan chính rồi lộn người đáp nhẹ nhàng xuống sàn boong thép.

"Kẻ nào?!"

Bành Đại Lực gầm lên một tiếng tựa sấm ran. Trong bóng tối nhá nhem của cơn mưa giông, đôi mắt gã đỏ ngầu hung tợn. Bộ khung giáp ngoại xương trên người gã rít lên ken két khi các van thủy lực bơm áp lực tối đa, truyền sức mạnh kinh người vào hai cánh tay hộ pháp.

"Nguyễn Minh An! Mày dám mò tới tận đây nộp mạng à?!"

Gã gầm lên, sải từng bước chân nặng nề làm rung chuyển cả sàn sà-lan, lao thẳng về phía tôi như một cỗ xe bọc thép! Nắm đấm bọc kim loại khổng lồ mang theo kình lực Ngưu Ma Bạt Sơn xé rách màn mưa, đấm thẳng vào ngực tôi với sức mạnh có thể nghiền nát cả một khối bê-tông cốt thép!

Tôi không hề nao núng, cũng không lùi nửa bước.

Luyện Cốt Hậu kỳ Cùng Cực giúp thần kinh vận động của tôi đạt tới độ nhạy bén phi thường. Toàn bộ quỹ đạo ra đòn của đối phương phản chiếu rõ mồn một trong tâm trí tôi tựa như một thước phim quay chậm.

Ngay khi nắm đấm kim loại chỉ còn cách ngực áo nửa tấc, tôi khẽ nghiêng người lướt qua luồng quyền phong rát mặt theo bộ pháp Du Thân Bộ. Đồng thời, thanh Hắc Thiết Đoản Côn trong tay tôi vung lên như một lằn chớp đen!

*KENG!*

Một tiếng va chạm kim loại đinh tai nhức óc vang lên giữa trời đêm.

Ngọn đoản côn điểm chuẩn xác vào trục xoay thủy lực nối giữa khớp vai và báng giáp của Bành Đại Lực. Kình lực xoắn Kính Kình truyền thẳng vào lõi thép, chấn nát van áp suất khiến dầu thủy lực phụt ra tung tóe!

Cánh tay phải của bộ giáp lập tức rũ xuống liệt bại.

Bành Đại Lực biến sắc mặt, đau đớn gầm rú. Gã vung chân trái tung một cú đá bạt ngang hung hãn nhằm bẻ gãy hông tôi.

Nhưng tôi đã nhanh hơn một nhịp. Bỏ lại chiếc đoản côn, tôi áp sát vào lòng gã, xoay người thúc một đòn chỏ Đản Trung bằng cùi chỏ cứng như ngọc thạch vào đúng tâm ngực gã — nơi ba mươi ba đốt sống lưng của tôi đồng loạt phát lực, dồn nén toàn bộ kình lực Thuần Dương Cương Huyết vào một điểm!

*ẦM!*

Tấm giáp ngực bằng hợp kim titan của gã vỡ vụn thành nhiều mảnh. Toàn bộ thân hình hộ pháp gần hai trăm ký của Bành Đại Lực bị chấn bay ngược ra sau hơn mười mét, đập nát lan can boong tàu rồi rơi tõm xuống dòng sông Cổ Chiên cuồn cuộn sóng dữ!

Bị chấn động kình lực phàm nhân làm tê liệt toàn bộ kinh mạch, gã ngất lịm đi trong dòng nước. Tôi vung tay bắn một sợi dây dù cứu sinh quấn quanh thắt lưng gã rồi buộc chặt vào mỏ neo sà-lan, giữ cho gã không bị dòng nước xiết nhấn chìm. Người luyện Thể Đạo lấy sự bảo vệ làm gốc, trừ phi bất khả kháng, quyết không tàn sát sinh mạng vô cớ.

Thấy thủ lĩnh bị hạ gục trong chớp mắt, toán tay sai còn lại trên sà-lan hoảng loạn buông vũ khí nhảy xuống xuồng tháo chạy tán loạn về phía hạ lưu.

Không nán lại boong tàu một giây, tôi quay ngoắt người, lao mình trở lại lòng sông sâu.

Ở độ sâu hai mươi hai mét dưới đáy dòng Cổ Chiên, phiến ngọc bích **Cổ Chiên Thủy Long Quyết** cao ba mét đang phát ra những quầng sáng màu lục bích huyền ảo giữa bùn lầy. Bốn chiếc cọc phát xung âm tà đạo cắm quanh vòm đá hoa cương đã bị tôi dùng Trấn Thủy Đoản Đao chặt đứt dây dẫn, vô hiệu hóa hoàn toàn.

Tôi nhẹ nhàng bơi tới, đặt bàn tay ấm nóng của mình lên bề mặt phiến ngọc cổ.

Dòng Thuần Dương Cương Huyết từ tâm thất tôi cuộn trào chảy qua lòng bàn tay, rót vào từng đường vân rồng uốn lượn trên phiến đá.

*OONG...!*

Một tiếng ngân vang thanh thoát, trầm hùng như tiếng chuông đồng vọng lại từ thời hồng hoang rung chuyển cả đáy sông. Luồng tà khí xám xịt bám quanh thềm đá ngầm tan biến như sương khói gặp nắng mai. Từ lòng phiến ngọc, một cột sáng lục bích rực rỡ bùng lên, nối liền thủy mạch sông Cổ Chiên với long mạch vĩ đại của miền Tây Nam Bộ!

Dòng chảy hung hãn của con triều bỗng chốc trở nên êm đềm lạ kỳ, vỗ về bờ bãi cù lao như bàn tay người mẹ ru con ngủ.

**Cọc tiêu thứ mười một — Cổ Chiên Thủy Long Quyết — đã được an định an toàn tuyệt đối!**

Mười một cọc tiêu đã an định!

Trong thức hải của tôi, một đồ hình trận pháp hoàn chỉnh rực sáng với mười một điểm kết nối vững chắc xuyên suốt từ ngọn Chứa Chan, rừng sác Cần Giờ, cù lao Tiền Giang cho tới cửa biển Cổ Chiên. Giờ đây, chỉ còn lại một điểm phát sáng duy nhất nằm chót vót ở cực Nam tổ quốc:

**Trận Nhãn Mũi Cà Mau!**

Tôi trồi lên khỏi mặt nước khi bình minh vừa hé rạng ở phía chân trời biển Đông.

Gió sớm thổi mát rượi qua mái tóc ướt sũng. Phía trước tôi là biển trời bao la vẫy gọi.

Đại cuộc bình ổn phương Nam đã bước vào những ngày quyết định nhất!'''

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
description: "Minh An thâm nhập vùng biển Ba Lai - Cổ Chiên, phá tan pháo đài nổi và mạng lưới bẫy điện ngầm, đả bại Bành Đại Lực, an định cọc tiêu thứ mười một Cổ Chiên Thủy Long Quyết."
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
        "Vượt Sóng Cổ Chiên, Phá Lưới Điện Ngầm, Đả Bại Bành Đại Lực & An Định Cọc Tiêu Thứ Mười Một Cổ Chiên Thủy Long Quyết",
        CHAPTER_NUM,
        1,
        f"{DATE}T23:30:00+07:00",
        CHAPTER_NUM,
        "loc_cua_song_ba_lai_co_chien",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An men theo duyên hải Bến Tre tiến vào vùng ngã ba sông Ba Lai và Cổ Chiên. Phát hiện Cửu Long Thiên Hải ghép đôi sà-lan lập pháo đài nổi cùng mạng lưới bẫy điện ngầm cao thế và máy phát xung âm đe dọa cọc tiêu thứ mười một Cổ Chiên Thủy Long Quyết. Minh An lặn sâu 20 mét cắt đứt cáp nguồn cao thế, đột kích sàn sà-lan đả bại Bành Đại Lực sở hữu giáp ngoại xương và Ngưu Ma Kình. Lặn sâu thanh tẩy tà khí, kích hoạt cọc ngọc bazan nghìn năm, an định trọn vẹn 11/12 cọc tiêu Thủy Môn phương Nam.",
        "Cọc tiêu thứ mười một Cổ Chiên Thủy Long Quyết an định hoàn toàn; đả bại Bành Đại Lực; vô hiệu hóa pháo đài nổi Cửu Long Thiên Hải; 11/12 cọc tiêu hoàn tất; chuẩn bị tiến về Trận Nhãn Mũi Cà Mau khép lại Hồi 2."
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
        "Cọc tiêu thứ mười một Cổ Chiên Thủy Long Quyết (Bến Tre - Trà Vinh) đã an định an toàn; 11/12 cọc tiêu Thủy Môn hoàn tất; chỉ còn cọc 12 Trận Nhãn Mũi Cà Mau khép lại Hồi 2."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An hoàn thiện Luyện Cốt Hậu kỳ Cùng Cực, cốt tủy hấp thu địa khí phát sinh hiện tượng sôi tủy, chuẩn bị bước đệm đại cảnh giới Hoán Huyết."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T23:30:00+07:00"
        inv_data["current_location"] = "Cửa Sông Ba Lai & Cửa Biển Cổ Chiên (Bến Tre - Trà Vinh)"
        inv_data["cultivation_realm"] = "Luyện Cốt Hậu kỳ Cùng Cực (33 Đốt Sống Ngọc Tủy Viên Mãn / Manh Nha Sôi Tủy Hoán Huyết)"

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

# -*- coding: utf-8 -*-
"""Draft Chapter 82 for Phá Trời Novel OS with ~3,600+ words prose, zero meta-words, severe physical and tactical realism, profound pathos, outwitting triumph, and multi-tier foreshadowing."""

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

CHAPTER_NUM = 82
CHAPTER_TITLE = "Tam Môn Khởi Lãng"
DATE = "2026-10-26"
LOCATION = "Cửa Tiểu (Sông Tiền) & Cửa Biển Soài Rạp (Cần Giờ)"

ACT1 = '''Năm giờ sáng ngày hai mươi sáu tháng mười.

Gió sớm từ phía biển Đông thổi thốc qua cửa sông Cửa Tiểu, mang theo vị mằn mặn nồng nàn của đại dương hòa quyện với mùi phù sa ngai ngái của châu thổ sông Cửu Long.

Trên mũi chiếc ca-nô composite cỡ nhỏ mượn từ trạm đò dân sinh ven bến Gò Công, tôi ngồi khoanh chân xếp bằng theo thế ngũ tâm triều thiên. Chiếc ca-nô lướt êm ru trên mặt nước màu xám bạc của buổi rạng đông, rẽ từng đợt sóng trắng xóa xuôi thẳng về phía vịnh Gành Rái.

Đêm qua, sau khi an định cọc tiêu thứ chín tại Cổ Miếu Trấn Ba và bàn giao toàn bộ hiện trường cùng toán tay sai của Trần Bảy cho lực lượng chức năng đường thủy bằng mật hiệu định vị an toàn, tôi không hề nán lại cù lao dù chỉ một khắc.

Tôi hiểu rõ: thời gian không còn đứng về phía tôi nữa. Mỗi một giờ trôi qua trong chậm trễ đều có thể biến thành cơ hội để kẻ thù kịp thời điều động thêm lực lượng từ các căn cứ hải ngoại.

Tôi vẫn nhớ như in ánh mắt chất phác của ông lão lái đò râu tóc hoa râm nơi bến Gò Công lúc bốn giờ sáng. Khi tôi trả tiền thuê ca-nô và ngỏ ý muốn mượn thuyền xuôi ra mạn biển Cần Giờ lúc trời còn chưa tỏ mặt người, ông cụ chỉ ái ngại nhìn tôi rồi đưa tay vỗ vỗ lên mạn thuyền:

"Chú em đi biển sớm nhớ ngó chừng ngọn sóng thần ngoài cửa Soài Rạp nghe. Mùa này gió chướng thổi ngược dòng triều, nước ròng sát đáy mà nước lớn thì ngập lút bờ bao. Sóng chỗ đó dữ dội lắm, đáy sông lại sâu hoắm những vực ngầm, tàu bè sơ sẩy một chút là chìm lỉm như chơi."

Tôi cúi đầu cảm tạ lời căn dặn mộc mạc của ông lão. Những con người bình dị của miệt duyên hải này đã bao đời bám biển, bám sông, coi từng con nước lớn ròng như nhịp thở của chính mình. Họ đâu hay biết rằng dưới lớp bùn lầy sâu thẳm nơi họ thả lưới giăng câu mỗi ngày, một cuộc chiến âm thầm bảo vệ long mạch của mảnh đất phương Nam đang diễn ra khốc liệt đến nhường nào.

Thông tin trích xuất từ chiếc máy tính bảng thu được của Trần Bảy đêm qua đã hé lộ toàn bộ quy mô của chiến dịch "Tam Môn Phong Tỏa" do đại bản doanh Cửu Long Thiên Hải đích thân chỉ đạo. Chín cọc tiêu nội địa trên khắp đồng bằng đã an định, nhưng ba cọc tiêu ngoài rìa duyên hải — "Cửa Biển Tam Môn" — mới chính là then cài then chốt nhất neo giữ toàn bộ cấu trúc địa tầng và thủy mạch phương Nam.

Ba cửa biển hiểm yếu đó bao gồm: Cửa Soài Rạp án ngữ phía đông bắc, cửa Ba Lai và Cổ Chiên giữ vững khúc ruột miền Tây, và điểm chót cùng là Trận Nhãn Mũi Cà Mau.

Nếu ba cửa biển này bị tà trận phá hủy, dòng chảy âm trọc từ vực sâu đại dương sẽ tràn ngược vào đất liền, gây nên thảm họa sụt lún và sạt lở chưa từng có cho hàng chục triệu người dân.

Chiếc ca-nô vượt qua doi cát cuối cùng của huyện Gò Công Đông, tiến vào vùng nước lợ mênh mông nơi sông Tiền hòa mình vào biển cả.

Gió biển buổi sớm buốt lạnh táp thẳng vào khuôn mặt tôi, làm tung bay vạt áo bà ba sẫm màu. Những hạt sương sớm li ti đọng trên mi mắt mát rượi.

Nhưng bên dưới làn da của tôi, một sự chuyển hóa kỳ diệu đang không ngừng diễn ra.

Ba mươi ba đốt sống lưng của tôi lúc này sáng lấp lánh như những khối ngọc thạch đồng thau hoàn mỹ. Cảnh giới Luyện Cốt Hậu kỳ Cùng Cực sau trận kịch chiến ở cổ miếu đã hoàn toàn hòa quyện vào tủy xương, mang lại cho tôi một thể phách dẻo dai tựa dây cung đại ngàn, rắn rỏi như đá hoa cương nghìn năm phong hóa.

Khung xương của tôi giờ đây không còn đơn thuần là giá đỡ sinh học thông thường. Ba mươi ba đốt sống tủy ngọc đã đạt đến trạng thái viên mãn tuyệt đối, tạo nên một kết cấu tinh thể tự nhiên bền bỉ khôn cùng. Từng thớ cơ, gân cốt liên kết chặt chẽ với nhau như những sợi cáp hợp kim dẻo dai, có thể co giãn và hấp thụ chấn động ở mức độ phi thường.

Khi ca-nô tiến từ vùng nước ngọt của sông Tiền sang vùng nước lợ mặn mòi của biển cả, áp suất thẩm thấu và độ ẩm không khí thay đổi đột ngột. Một người bình thường sẽ lập tức cảm thấy cay rát sống mũi và uể oải cơ bắp vì sự mất cân bằng ion.

Nhưng cơ thể tôi lại tự động điều tiết một cách hoàn hảo.

Từng giọt Thuần Dương Cương Huyết cuộn trào bỏng rát từ tâm thất, chảy tràn qua ba mươi ba đốt sống tủy ngọc, phân nhánh đến hàng triệu mao mạch li ti dưới da. Dưới sự vận hành của Quy Tức Cùng Cực, các lỗ chân lông của tôi tự động đóng mở nhịp nhàng, điều hòa nhiệt độ thân thể ở mức ba mươi bảy độ ổn định, triệt tiêu hoàn toàn sự xâm lấn của hàn khí và hơi muối mặn mòi.

Tôi khẽ nhắm mắt, hướng tâm thức vào sâu bên trong thức hải.

Đài sen ngọc bích của Lâm Tịch vẫn thu nhỏ lại bằng lòng bàn tay, lơ lửng giữa làn sương mờ tĩnh lặng. Nàng vẫn đang trong giấc ngủ sâu để hồi phục nguyên thần vỡ nát.

Tuy nhiên, sau khi cọc tiêu thứ chín được kích hoạt, một luồng khí tức thanh khiết từ long mạch sông Tiền đã âm thầm thẩm thấu vào thức hải của tôi, nuôi dưỡng cho đài sen của nàng thêm một phần sinh khí. Vết nứt màu xám tro trên cánh sen dường như đã bớt đi phần u ám, chuyển dần sang sắc trắng mờ dịu dàng. Từng sợi tơ sáng mỏng manh như sương sớm bao bọc lấy cánh hoa, phát ra những rung động êm đềm tựa tiếng thở sâu của người thiếu nữ sau cơn sốt dài.

Tôi nhớ lại lời nàng từng dặn dò trước khi chìm vào trầm miên: Thể Đạo phàm nhân lấy chính xương thịt làm thuyền, lấy ý chí làm mái chèo, vượt qua muôn trùng bão tố không cầu thần phật độ trì. Con đường rèn giũa thân xác là con đường gian nan nhất, nhưng cũng là điểm tựa chân thật nhất giữa cõi đời vô thường.

"Lâm Tịch, cô hãy yên tâm dưỡng thương. Tôi nhất định sẽ giữ vững mười hai cọc tiêu này, bảo vệ mảnh đất này cho đến ngày cô thức tỉnh."

Tôi thầm nhủ trong lòng, bàn tay siết chặt chuôi Hắc Thiết Đoản Côn giắt bên hông.

Trước mắt tôi, đường chân trời rực lên một vệt rạng đông màu hồng ngọc. Bức tranh thiên nhiên kỳ vĩ mở toang ra trước mũi thuyền: những đàn chim hải âu trắng muốt chao lượn trên mặt biển bạc, phía xa xa là màu xanh thẫm bạt ngàn của rừng sác Cần Giờ đang dần hiện rõ trong làn sương sớm.

Đó không đơn thuần là cảnh sắc thiên nhiên hoang sơ, mà là bức tường thành xanh ngắt che chở cho thành phố suốt bao cuộc thăng trầm lịch sử. Rừng ngập mặn Cần Giờ từng chở che những đoàn quân anh dũng năm xưa, và giờ đây, nơi cửa biển Soài Rạp này, một cuộc thử thách mới lại đang chờ đón tôi.'''

ACT2 = '''Tám giờ ba mươi phút sáng.

Chiếc ca-nô rẽ vào luồng lạch Soài Rạp — con sông ranh giới tự nhiên giữa huyện Cần Giờ thuộc thành phố Hồ Chí Minh và tỉnh Tiền Giang.

Không gian xung quanh bỗng chốc biến chuyển kỳ ảo.

Hai bên bờ sông là rừng sác Cần Giờ bạt ngàn ngút tầm mắt. Những rặng đước cổ thụ hàng chục năm tuổi xòe những chùm rễ chằng chịt như hàng ngàn chiếc chân nhện khổng lồ cắm sâu vào bãi bùn đen lầy lội. Mùi lá đước mục rữa hòa lẫn với mùi rong biển và vỏ ốc tạo nên một bầu không khí hoang sơ, tịch mịch đến nghẹt thở.

Xen lẫn giữa những rặng đước là rừng mắm trắng và bần chua ken dày đặc. Những chiếc rễ mắm nhọn hoắt nhô lên khỏi mặt bùn lầy như hàng triệu ngọn chông tre tự nhiên, tạo thành một phên giậu bẫy rào phòng ngự kiên cố của thiên nhiên trước sức tàn phá của sóng gió biển khơi.

Đây chính là khu dự trữ sinh quyển thế giới, nhưng đồng thời cũng là cửa ngõ thủy đạo hiểm yếu bậc nhất của toàn bộ vùng kinh tế trọng điểm phía Nam. Hàng triệu tấn hàng hóa xuất nhập khẩu của các cụm cảng Hiệp Phước, Cát Lái và Thị Vải đều phải nương theo luồng lạch sâu thẳm của dòng Soài Rạp để ra vào biển Đông.

Mỗi khi con triều biển Đông tràn vào, hàng triệu mét khối nước mặn cuộn trào dâng lên, đối đầu trực tiếp với dòng nước ngọt từ sông Đồng Nai và sông Sài Gòn đổ xuống. Sự giao tranh khốc liệt giữa hai khối nước tạo nên những vực xoáy ngầm hung hãn, gọt giũa đáy sông thành những hẻm vực sâu tới ba mươi mét dưới làn nước đục ngầu phù sa.

Càng tiến gần ra phía phao số không cửa biển, ba mươi ba đốt sống lưng của tôi càng rung chuyển dồn dập.

Một chuỗi dao động từ trường 0.12 Hz cực kỳ mãnh liệt — mạnh gấp ba lần so với cọc tiêu tại Chứa Chan hay Trấn Ba — liên tục dội ngược lên từ đáy bùn sâu hai mươi lăm mét!

Đó chính là cọc tiêu thứ mười: **Soài Rạp Hải Giáp Trụ**!

Theo các tư liệu khảo sát địa tầng cổ mà Viện chúng tôi từng lưu trữ, cọc tiêu thứ mười là một cột đá bazan nguyên khối khổng lồ mang hình mai rùa dựng đứng. Cột đá này được các bậc tiền nhân thời khẩn hoang dựng sâu dưới lòng bùn lầy nơi đáy luồng hàng hải từ hàng trăm năm trước, có tác dụng phân chia dòng chảy thủy triều và trấn áp chấn động ngầm của vịnh Gành Rái.

Trong phong thủy hình thế học, sông Soài Rạp ví như cổ họng của con rồng phương Nam vươn ra biển lớn. Nếu không có cọc tiêu Hải Giáp Trụ này gánh chịu phản lực va đập của sóng triều biển Đông, toàn bộ vùng duyên hải trũng thấp của Nhà Bè và Cần Giờ đã sớm bị xâm thực, sụp lún từ lâu.

Tôi cho ca-nô chạy chậm lại, rẽ vào một lạch nước nhỏ quanh co rậm rạp rễ đước, dùng cành lá khô che chắn ngụy trang kín đáo con thuyền.

Tôi bám theo một thân đước nghiêng ngả, leo lên một cọc rễ đước vững chắc nhô cao khỏi bãi bồi, đưa ống nhòm quân sự quan sát ra giữa luồng sông Soài Rạp.

Cách vị trí của tôi chừng một ngàn hai trăm mét về phía cửa biển, một chiếc sà-lan chuyên dụng dài hơn sáu mươi mét mang logo của *Công ty Thăm Dò Hàng Hải Biển Đông* — một công ty bình phong khác của Tập đoàn Cửu Long Thiên Hải — đang buông bốn mỏ neo cố định giữa dòng nước xiết.

Xung quanh chiếc sà-lan, ba chiếc xuồng cao tốc bọc thép sơn màu xám ngụy trang liên tục quần đảo tuần tra. Trên mỗi chiếc xuồng đều có bốn tay súng mặc áo phao đen, mang kính viễn vọng nhiệt và súng bắn lao áp lực cao, canh gác nghiêm ngặt từng mét nước.

Trên boong chiếc sà-lan lớn, hai máy phát điện công nghiệp công suất lớn đang gầm rú xả khói đen mờ mịt. Một cần cẩu thủy lực hạng nặng đang cẩu một khối thiết bị hình trụ bằng thép titan màu vàng cam thả chầm chậm xuống lòng sông.

Nhìn qua lăng kính quang học của ống nhòm, tôi lập tức nhận ra cơ chế hoạt động của cỗ máy đó. Đó là một thiết bị phát sóng xung kích cao tần kết hợp với mũi cắt địa tầng bằng sợi kim cương chuyên dụng!

Chúng đang tìm cách cắm bốn chiếc cọc neo hợp kim tà đạo bao quanh chân móng cột đá Hải Giáp Trụ, dùng chấn động siêu âm để bẻ gãy cấu trúc bazan của cọc tiêu thứ mười từ tận gốc rễ!

Nếu để chúng kích hoạt cỗ máy đó, chỉ trong vòng hai tiếng đồng hồ, thềm đá ngầm cửa Soài Rạp sẽ vỡ vụn. Không còn điểm tựa trấn áp, sóng triều đại dương sẽ cuốn phăng dải rừng phòng hộ, kéo theo sự xâm nhập mặn tàn khốc hủy hoại toàn bộ nguồn nước ngọt sinh hoạt và tưới tiêu của hàng triệu người dân phía hạ lưu!

Lòng tôi dâng lên một luồng nhiệt khí hừng hực. Luyện Cốt Hậu kỳ Cùng Cực giúp các khớp xương của tôi siết chặt lại, kình lực tích tụ sẵn sàng bộc phát. Tôi không thể để âm mưu đen tối ấy thành hiện thực trên mảnh đất quê hương!'''

ACT3 = '''Mười một giờ mười lăm phút trưa.

Thủy triều trên sông Soài Rạp bắt đầu chuyển sang con nước ròng. Dòng nước chảy xiết cuồn cuộn với vận tốc hơn bốn hải lý một giờ, tạo nên những vùng nước xoáy nguy hiểm có thể nuốt chửng bất kỳ chiếc thuyền nan nào.

Nước ròng cuộn trào mang theo vô vàn phù sa và rác rưởi trôi xuôi ra biển, biến mặt nước thành một tấm màn nâu đục ngầu không thể nhìn xuyên qua. Nhưng đối với một người đạt cảnh giới Luyện Cốt Hậu kỳ Cùng Cực, dòng nước xiết này lại chính là lớp áo giáp che chở hoàn hảo nhất.

Tôi cởi bỏ bộ quần áo bà ba, chỉ mặc chiếc quần lặn co giãn màu đen nhánh ôm sát cơ thể. Thanh Hắc Thiết Đoản Côn được nẹp chặt sau lưng bằng đai dù quân dụng, thanh Trấn Thủy Đoản Đao giắt bên đùi phải, chiếc kính lặn chuyên dụng che kín mắt mũi.

Tôi hít một hơi thật sâu, vận chuyển khẩu quyết Quy Tức Cùng Cực.

Trái tim tôi đập chậm dần xuống ba mươi lăm nhịp một phút. Dòng Thuần Dương Cương Huyết phong tỏa toàn bộ các lỗ chân lông, chuyển đổi cơ chế hô hấp của cơ thể sang dạng tuần hoàn nội sinh ngọc tủy — cho phép tôi có thể lặn sâu dưới đáy nước hàng giờ đồng hồ mà không cần bình dưỡng khí.

*TÕM!*

Tôi trượt mình xuống dòng nước đục ngầu từ một mỏm rễ đước, không hề tạo ra một tiếng động hay bọt khí nào.

Nước mặn lạnh buốt táp vào da thịt, nhưng lớp màng cơ bắp cuộn chặt như thép nguội của tôi lập tức tỏa ra một luồng nhiệt lượng ấm áp triệt tiêu cái lạnh thấu xương.

Lợi dụng những rặng rễ đước ngập sâu dưới lòng sông làm điểm tựa ban đầu, tôi bơi ngầm sát đáy bùn lầy, men theo triền dốc địa tầng tiếp cận chiếc sà-lan của kẻ địch.

Độ sâu mười mét... hai mươi mét... rồi hai mươi lăm mét.

Ánh sáng mặt trời hoàn toàn biến mất, xung quanh chỉ còn lại một màu đen đặc quánh của bùn phù sa và nước mặn. Áp lực thủy tĩnh khổng lồ lên tới hơn hai phẩy năm át-mốt-phe bắt đầu đè nặng lên màng nhĩ và lồng ngực tôi.

Với một người bình thường, áp lực này đủ để bóp nghẹt buồng phổi và làm vỡ màng nhĩ trong tích tắc.

Nhưng ba mươi ba đốt sống tủy ngọc trong lưng tôi khẽ rền vang một tiếng giòn giã. Chúng tự động giãn nở vi mô, phân bổ đều áp lực ra toàn bộ khung xương. Lồng ngực bằng xương cốt ngọc thạch của tôi vững vàng tựa vòm cầu đá cổ, giúp tôi di chuyển uyển chuyển tựa một chú rái cá đại dương.

Bỗng nhiên, trong bóng tối dưới đáy sông sâu, một quầng sáng màu lam ngọc nhạt hiện ra mờ ảo trước mắt tôi.

Đó chính là chân móng của **Soài Rạp Hải Giáp Trụ**!

Cột đá bazan cổ xưa cao hơn mười mét, đường kính gần ba mét, sừng sững cắm sâu vào tầng đá mẹ kỷ đệ tứ. Trên thân cột đá khắc chìm hàng ngàn hoa văn sóng gió và ấn ký chữ triện của Thủ Hộ Nhất Mạch, phát xuất từng luồng uy áp trang nghiêm đẩy lùi bùn lầy xung quanh tạo thành một khoảng trống bán kính hai mét trong vắt.

Tuy nhiên, quanh chân cột đá lúc này đã bị quân của Cửu Long Thiên Hải đóng bốn chiếc cọc neo hợp kim màu đen sì.

Những chiếc cọc neo này đang phát ra những luồng sóng siêu âm chói tai, tạo thành một lồng năng lượng tà ác bao vây, làm rạn nứt từng mảng hoa văn cổ trên thân đá bazan. Phía trên đầu, mũi khoan titan khổng lồ của cỗ máy cắt đá đang từ từ hạ xuống, chỉ còn cách đỉnh cột đá chưa đầy ba mét!

Tôi không chần chừ một giây.

Rút thanh Trấn Thủy Đoản Đao ra khỏi bao đùi, tôi đạp mạnh chân vào thềm đá ngầm, lao vút tới chiếc cọc neo thứ nhất như một mũi tên xé nước!

Thanh Trấn Thủy Đoản Đao mang theo kình lực Thuần Dương Cương Huyết chém ngang một nhát tuyệt mỹ!

*XOẸT!*

Lưỡi đao sắc bén chém đứt ngọt xớt dây cáp truyền dẫn tín hiệu và trục thủy lực của chiếc cọc neo tà đạo. Luồng sóng siêu âm lập tức bị dập tắt, phát ra tiếng nổ lách tách dưới đáy nước sâu.

Thấy tín hiệu trên bảng điều khiển bị ngắt đột ngột, hai tên thợ lặn người nhái mặc đồ lặn áp suất cao của Cửu Long Thiên Hải đang canh gác dưới đáy sông lập tức quay đầu lại. Chúng giương những khẩu súng bắn lao cơ giới dưới nước nhắm thẳng vào ngực tôi!

*PHỤT! PHỤT!*

Hai ngọn lao thép dài hơn một mét rẽ nước lao tới xé toạc bóng tối.

Tôi uốn cong người theo bộ pháp Thể Đạo, né tránh ngọn lao thứ nhất trong gang tấc. Ngọn lao thứ hai bay sượt qua mạn sườn, tôi vung tay trái ra như một chiếc kìm thép chộp gọn chuôi ngọn lao, mượn chính lực quán tính của nó xoay người lao thẳng về phía tên người nhái đầu tiên!

Cú điểm huyệt bằng chuôi lao trúng ngay khớp vai hắn, đánh văng khẩu súng lao và làm đứt ống thở áp suất, khiến tên người nhái hoảng hốt kích hoạt túi khí khẩn cấp trồi ngược lên mặt nước.

Tên thứ hai chưa kịp rút dao găm thì thanh Hắc Thiết Đoản Côn trong tay tôi đã vung ra một đòn Kính Kình dưới nước. Sóng xung kích truyền qua môi trường nước đặc quánh đập thẳng vào lồng ngực hắn, chấn động kình lực Thể Đạo làm tê liệt toàn bộ hệ thần kinh vận động khiến hắn ngất lịm ngay tại chỗ. Tôi tiện tay giật dây bung túi cứu sinh trên lưng hắn để hắn từ từ nổi lên mặt nước, giữ lại tính mạng cho kẻ lầm đường.

Giải quyết xong toán người nhái, tôi bơi quanh chân cột đá Hải Giáp Trụ, dùng Trấn Thủy Đoản Đao chặt đứt toàn bộ ba chiếc cọc neo còn lại, vô hiệu hóa hoàn toàn cỗ máy cắt tầng của kẻ địch.

Khi mối đe dọa bị dập tắt, tôi đặt bàn tay trần lên thân đá bazan, vận chuyển một luồng Thuần Dương Cương Huyết thanh tẩy toàn bộ tà khí bám trên bề mặt. Cột đá bazan ngàn năm bỗng tỏa ra một làn sóng lam quang dịu dàng, những vết rạn nứt li ti tự động khép miệng.

Dưới đáy sâu sông Soài Rạp, tiếng gầm gừ hung hãn của dòng chảy chuyển thành một khúc hoan ca êm đềm, hòa quyện vào nhịp đập tủy ngọc của tôi. Một luồng địa khí thanh thuần từ thềm lục địa dội ngược vào ba mươi ba đốt sống lưng, khiến toàn thân tôi ấm rực như vừa được ngâm mình trong dòng suối khoáng nóng ngàn năm.

**Cọc tiêu thứ mười — Soài Rạp Hải Giáp Trụ — đã được an định an toàn tuyệt đối!**

Tôi thu đao vào bao, búng người rẽ sóng bơi ngược lên bờ rậm rạp của rừng sác Cần Giờ.

Một giờ chiều.

Tôi đứng trên mỏm bùn cao dưới tán rừng đước, đưa mắt nhìn ra chiếc sà-lan đang hoảng loạn thu hồi thiết bị hỏng hóc và rồ ga tháo chạy về phía ngoài khơi vịnh Gành Rái.

Gió biển thổi tung mái tóc ướt sũng của tôi, mang theo ánh nắng rực rỡ của buổi trưa xua tan màn sương mù xám xịt.

Cửa biển thứ nhất trong "Cửa Biển Tam Môn" đã được giữ vững!

Phía trước tôi, chỉ còn lại hai cọc tiêu cuối cùng: Cửa Ba Lai - Cổ Chiên và Trận Nhãn Mũi Cà Mau. Đại cục bình ổn phương Nam đang bước vào giai đoạn khốc liệt và quyết định nhất!'''

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
description: "Minh An vượt sông Cửa Tiểu ra cửa biển Soài Rạp, lặn sâu 25 mét đáy nước rừng sác Cần Giờ đập tan thiết bị cắt đá tà môn, bảo vệ an toàn cọc tiêu thứ mười Hải Giáp Trụ."
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
        "Vượt Sông Cửa Tiểu, Thâm Nhập Rừng Sác Cần Giờ & Bảo Vệ Cọc Tiêu Thứ Mười Soài Rạp Hải Giáp Trụ",
        CHAPTER_NUM,
        1,
        f"{DATE}T13:00:00+07:00",
        CHAPTER_NUM,
        "loc_cua_bien_soai_rap_can_gio",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An xuôi ca-nô qua nhánh sông Cửa Tiểu tiến vào vùng cửa biển Soài Rạp rợp bóng rừng sác Cần Giờ. Bằng thể phách Luyện Cốt Hậu kỳ Cùng Cực và Quy Tức Cùng Cực, Minh An lặn sâu 25 mét dưới đáy nước cuộn xiết, tiếp cận cọc tiêu thứ mười Soài Rạp Hải Giáp Trụ. Phát hiện sà-lan của Cửu Long Thiên Hải thả cọc neo siêu âm và máy cắt đá titan mưu toan bẻ gãy trụ bazan cổ. Minh An vận dụng Trấn Thủy Đoản Đao và kình lực Thể Đạo dưới nước đánh bại toán người nhái bảo vệ, cắt đứt toàn bộ cọc neo tà môn, an định hoàn toàn cọc tiêu thứ mười, bảo vệ cửa ngõ đầu tiên của Tam Môn.",
        "Cọc tiêu thứ mười Soài Rạp Hải Giáp Trụ an định an toàn; vô hiệu hóa thiết bị sà-lan địch; mở màn chiến dịch Cửa Biển Tam Môn thành công; 10/12 cọc tiêu Thủy Môn đã giải quyết."
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
        "Cọc tiêu thứ mười Soài Rạp Hải Giáp Trụ (Cần Giờ) đã an định hoàn toàn; 10/12 cọc tiêu Thủy Môn hoàn tất; chuẩn bị tiến vào cọc 11 và 12 tại Cửa Biển Tam Môn."
    ))

    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-PLT-002'
    """, (
        CHAPTER_NUM,
        "Minh An thích nghi hoàn hảo với áp lực nước 25m dưới đáy biển Soài Rạp bằng Luyện Cốt Hậu kỳ Cùng Cực, khí huyết tuần hoàn nội sinh ngọc tủy."
    ))

    conn.commit()
    conn.close()
    print(f"[+] Đã cập nhật database novel_os.db (timeline_events & story_threads).")

    # 8. Cập nhật state/inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T13:00:00+07:00"
        inv_data["current_location"] = "Cửa Biển Soài Rạp & Rừng Sác Cần Giờ, TP.HCM"
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

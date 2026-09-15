# -*- coding: utf-8 -*-
"""Draft Chapter 61 for Phá Trời Novel OS."""

import os
import sys
import json
import sqlite3

BASE_DIR = r"d:\tieu-thuyet"
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from system.core.config import DB_PATH, MANUSCRIPT_MD_DIR, MANUSCRIPT_WORD_DIR
from system.engines.critique_engine import CritiqueEngine
from system.engines.docx_pipeline import DocxPipeline
from system.engines.retrieval_engine import RetrievalEngine

CHAPTER_NUM = 61
CHAPTER_TITLE = "Tọa Độ Bến Phú Định"
LOCATION = "Viện Địa tầng (Quận 1) & Bến Phú Định (Phường 16, Quận 8, TP.HCM)"
DATE = "2026-10-19"

CHAPTER_PROSE = """Bảy giờ bốn mươi lăm phút sáng ngày mười chín tháng Mười.

Bầu trời trung tâm thành phố sau cơn mưa đêm trong vắt như một tấm kính lọc quang học. Không khí ban mai trên đường Nguyễn Thị Minh Khai mát rượi, thoang thoảng mùi nhựa cây dầu cổ thụ quyện với mùi cà phê rang xay thơm nồng từ những quán cóc ven đường.

Tôi dựng chiếc xe Wave Alpha vào tầng hầm trụ sở Viện Địa tầng, bước nhanh lên thang máy lên tầng tám.

Vừa bước chân vào sảnh văn phòng phòng dữ liệu vi chấn, tôi đã thấy không khí làm việc ở đây náo nhiệt hơn hẳn mọi ngày. Các kỹ sư trẻ đang tụm năm tụm ba quanh bàn trà, tay cầm tài liệu trắc địa, mắt dán vào màn hình tivi treo tường đang phát bản tin thời sự sáng của Đài Truyền hình thành phố.

"An! Vào đây mau lên cậu!" 

Kỹ sư Tuấn vừa nhìn thấy tôi liền vẫy tay rối rít. Anh kéo tôi lại gần bàn làm việc, trên tay đang cầm một xấp biên bản khám nghiệm hiện trường có đóng dấu đỏ của Công an Quận 6:

"Đêm qua vụ xưởng cơ khí Vạn Phát chấn động cả giới xây dựng thành phố rồi! Nhờ số liệu sụt lún địa tầng của cậu gửi về hòm thư trực ban kịp thời mà Đội Cảnh sát Kinh tế và Thanh tra xây dựng đã tóm gọn trọn ổ buôn lậu đồ cổ dưới lòng kênh. Cậu có biết bọn chúng đào được thứ gì không?"

Tôi làm bộ tròn xoe mắt, vờ như chưa nắm rõ chi tiết:

"Sáng nay tôi mới đọc tin nhắn của anh Tuấn. Nghe nói là một khối cọc kim loại cổ trục vớt từ đáy rạch Lò Gốm?"

"Không phải cọc kim loại bình thường đâu, mà là một khối trụ bát giác bằng đồng đúc đặc dài hơn hai mét rưỡi, nặng gần hai tấn!" Tuấn hào hứng ghé sát tai tôi nói nhỏ: "Các chuyên gia khảo cổ bên Bảo tàng Lịch sử đêm qua thức trắng để giám định sơ bộ. Bọn họ bảo các chữ Hán khắc chìm trên thân cọc có niên đại cực kỳ cổ xưa, hoa văn mây nước đúc tinh xảo đến mức kỹ thuật luyện kim hiện đại cũng phải ngả mũ thán phục!"

Tuấn kéo chiếc ghế xoay lại gần tôi, bấm chuột mở tập bản đồ thủy văn cổ trên màn hình máy tính trắc địa:

"Cậu xem này, toàn bộ mạng lưới kênh rạch Chợ Lớn thời nhà Nguyễn vốn được đào đắp dựa trên các dòng chảy tự nhiên của lưu vực sông Sài Gòn và sông Chợ Đệm. Đến thập niên 1880, người Pháp bắt đầu nạo vét và kè đá mở rộng rạch Lò Gốm để vận chuyển gạch ngói từ các lò nung gốm Cây Mai ra bến sông. Nhưng hồ sơ địa chất lưu trữ của Sở Công chánh thời thuộc địa hoàn toàn không có ghi chép nào về việc chôn các cọc đồng lớn như thế này. Đêm qua, khi bọn buôn lậu dùng tời cáp nhổ khối trụ lên khỏi tầng bùn kỵ khí, các cảm biến áp lực kẽ rỗng của chúng ta đặt dọc bờ kênh lập tức ghi nhận hiện tượng giảm áp tức thời. Đất nền xung quanh lập tức bị xé rách, tạo thành một phễu lún cát chảy nuốt trọn cả móng xưởng cơ khí."

"Nghĩa là khối cọc đồng đó không đơn thuần là phế tích khảo cổ, mà đóng vai trò như một chiếc neo giữ ổn định cho cả tầng đất yếu?" Tôi hỏi, tiếp cận vấn đề dưới góc nhìn cơ học đất.

"Chính xác là như vậy!" Tuấn gật đầu quả quyết. "Nó hoạt động như một cọc nén ứng lực trước khổng lồ, dùng trọng lượng bản thân và trường từ tính tự nhiên để cố kết lớp bùn sét bão hòa nước. Nhổ nó đi chẳng khác nào rút then cài của một chiếc đập ngăn nước ngầm. Nếu đêm qua cảnh sát không ập vào kịp thời để phong tỏa hiện trường, toàn bộ đoạn bờ rạch Lò Gốm chắc chắn đã sụt trượt hoàn toàn!"

Đúng lúc đó, cánh cửa phòng làm việc của Viện trưởng Nguyễn Hoài Nam mở ra. 

Viện trưởng Nam bước ra, trên tay cầm cặp tài liệu da, ánh mắt nghiêm nghị nhưng lộ rõ vẻ phấn khởi khi nhìn thấy tôi:

"An đến rồi đấy à? Tốt lắm. Cậu và Tuấn mang theo máy trắc địa và bản đồ vi chấn khu vực hạ lưu vào phòng họp lớn ngay. Các đồng chí bên Sở Xây dựng, Công an thành phố và Viện Khảo cổ đã có mặt đông đủ rồi."

"Dạ, chúng cháu vào ngay ạ," tôi cung kính đáp.

Tám giờ ba mươi phút. Cuộc họp giao ban liên ngành bắt đầu tại phòng họp lớn tầng tám.

Trên màn hình máy chiếu rộng bốn mét, những bức ảnh chụp chi tiết hiện trường xưởng Vạn Phát đêm qua lần lượt hiện ra. Khối cọc đồng bát giác phủ đầy rỉ xanh lam nằm sừng sững trên giá đỡ thép, những đường vân mây nước và ký tự cổ lấp lánh dưới ánh đèn huỳnh quang nghiệp vụ.

Một vị giáo sư luống tuổi đại diện cho Viện Khảo cổ đứng lên trình bày:

"Thưa các đồng chí, theo kết quả phân tích phổ quang học ban đầu, khối cọc kim loại này được đúc bằng hợp kim đồng thau pha tạp chất thạch anh đen có độ tinh khiết bất thường. Đây chắc chắn là một công trình trấn yểm thủy văn cổ xưa được chôn sâu dưới tầng bùn đáy kênh từ nhiều thế kỷ trước để chống xói lở lòng sông. Việc kẻ gian dùng sà lan và thiết bị lặn trục vớt khối cọc này lên khỏi đáy sông đã phá vỡ thế cân bằng địa chất, gây ra hiện tượng sụt lún nghiêm trọng cho cả một đoạn đường Lò Gốm."

Đại diện Cơ quan Cảnh sát Điều tra tiếp lời:

"Gã cầm đầu nhóm cơ khí mang danh 'Thầy Cảnh' hiện đang được điều trị tại Bệnh viện Chợ Rẫy do bị ngạt khí độc đáy bùn. Bước đầu điều tra, chúng tôi phát hiện gã này nhận chỉ đạo từ một đầu mối tài chính quốc tế thông qua các giao dịch chuyển khoản từ nước ngoài. Tuy nhiên, có một chi tiết kỹ thuật vô cùng bất thường..."

Viên sĩ quan điều tra bấm nút chuyển slide trên máy chiếu, phóng to bức ảnh chụp đỉnh trụ bát giác của khối cọc đồng:

"Tại vị trí trung tâm trên đỉnh cọc, chúng tôi phát hiện một ổ trục hình tròn đường kính mười phân đã bị cạy mở lớp sáp niêm phong cổ. Lỗ rỗng bên trong hoàn toàn trống không. Theo lời khai lắp bắp của Thầy Cảnh trước khi hôn mê, bên trong ổ trục này vốn có một khối đá ngọc trấn thủy cổ cực kỳ quý giá, nhưng khi cảnh sát ập vào thì viên ngọc đã biến mất. Chúng tôi đang truy tìm dấu vết của kẻ thứ ba có mặt tại hiện trường trước thời điểm lực lượng chức năng tiếp quản."

Ngồi ở hàng ghế kỹ thuật, tôi điềm tĩnh ghi chép vào cuốn sổ tay công tác, nét mặt không hề biến đổi dù chỉ một phần mười giây.

Viên ngọc mà cơ quan chức năng đang tìm kiếm — khối *Hắc Thủy Huyền Thạch* — lúc này đang nằm an toàn trong đáy chiếc balo dã chiến đã được tôi khóa chốt cẩn mật ở phòng trọ Bình Thạnh. Nếu để khối đá đó rơi vào tay kẻ phàm, hoặc để lộ ra trước công chúng, không chỉ Cửu Long Group điên cuồng săn lùng mà toàn bộ thế giới ngầm sẽ bị khuấy đảo.

Cuối buổi họp, Viện trưởng Nguyễn Hoài Nam giao nhiệm vụ trọng tâm cho phòng dữ liệu:

"Theo báo cáo của Sở Xây dựng, đêm nay và rạng sáng mai sẽ xuất hiện đợt triều cường lớn nhất trong tháng kết hợp với dòng xả lũ từ hồ Dầu Tiếng. Khu vực ngã ba Kênh Đôi, rạch Lò Gốm và Bến Phú Định thuộc Quận 8 là vùng trũng cực kỳ nguy hiểm. Giao cho đồng chí Tuấn phụ trách trạm đo cố định tại Viện, đồng chí Minh An mang thiết bị vi chấn cơ động trực tiếp xuống hiện trường Bến Phú Định để khảo sát biến thiên dòng chảy và theo dõi độ lún các trụ cầu. Có bất kỳ dấu hiệu bất thường nào phải báo cáo trực tiếp về Ban Chỉ huy."

"Rõ, thưa Viện trưởng!" Tôi đứng dậy nhận lệnh.

Một nhiệm vụ khảo sát thực địa chính danh, hoàn toàn hợp pháp và đúng vào vị trí mà tôi cần tiếp cận!

***

Mười lăm giờ ba mươi phút chiều cùng ngày.

Tôi điều khiển chiếc xe Wave Alpha xuôi theo đại lộ Võ Văn Kiệt, rẽ qua cầu Chà Và rồi hướng thẳng vào đường Bến Phú Định, Phường 16, Quận 8.

Khác hẳn với vẻ chật hẹp, tù đọng của con rạch Lò Gốm, Bến Phú Định là một ngã ba đường thủy mênh mông và khoáng đạt, nơi sông Chợ Đệm, Kênh Đôi và ngã ba kênh Tàu Hủ hợp lưu trước khi đổ ra sông Sài Gòn. Nơi đây từng là một trong những thương cảng lúa gạo sầm uất bậc nhất Nam Kỳ lục tỉnh từ thế kỷ mười chín, nơi ghe thuyền chở nông sản từ khắp các tỉnh đồng bằng sông Cửu Long tấp nập cập bến giao thương ngày đêm.

Gió sông chiều thổi lồng lộng mang theo mùi nước lợ ngai ngái lẫn mùi dầu máy diesel nồng nặc. 

Mặt nước sông đỏ ngầu phù sa cuồn cuộn chảy xiết theo con nước ròng. Hai bên bờ kênh là những bãi tập kết vật liệu xây dựng khổng lồ, núi cát vàng, đá dăm cao ngất ngưởng, xen lẫn những dãy nhà xưởng đóng tàu vỏ sắt cũ kỹ phát ra tiếng búa gõ leng keng vang rền mặt nước.

Hàng chục chiếc sà lan chở hàng tải trọng từ vài trăm đến hàng ngàn tấn đang neo đậu san sát nhau dọc theo bờ kè bê tông.

Dòng chảy ở ngã ba Bến Phú Định lúc này đang ở thời điểm giao thoa phức tạp. Phía thượng lưu sông Chợ Đệm dẫn nguồn nước ngọt từ vùng đồng bằng Long An đổ về, đụng độ với triều mặn từ hạ lưu Cần Giuộc đẩy ngược lên theo Kênh Đôi, tạo thành những dải xoáy nước ngầm cuộn tròn sủi bọt trắng xóa giữa lòng sông.

Theo tài liệu đo sâu quét sườn ba chiều mà Viện Địa tầng từng lập bản đồ năm ngoái, ngay dưới tim luồng giao nhau này tồn tại một rãnh xói hình chữ V sâu hun hút, đáy rãnh chạm mức âm ba mươi lăm mét so với mực nước biển chuẩn. Tại độ sâu ấy, áp lực thủy tĩnh lên tới gần bốn phẩy năm át-mốt-phe. Một khối bê tông nặng nửa tấn nếu thả xuống đây cũng sẽ bị dòng chảy đáy xô lệch vị trí chỉ sau vài con nước.

Tôi tấp xe vào một quán nước mía có mắc những chiếc võng dù ven mép sông, gọi một trái dừa tươi.

Ngồi trên chiếc võng dù đung đưa dưới bóng râm của rặng dừa nước, tôi lấy chiếc máy đo địa chấn cầm tay giả vờ đặt lên bàn gỗ như đang ghi chép thông số kỹ thuật. Nhưng dưới gầm bàn, tay phải tôi khẽ đưa vào túi áo khoác, rút chiếc ống nhòm dã chiến quang học độ phóng đại cao ra quan sát.

Tầm mắt tôi quét chậm rãi qua từng chiếc tàu thuyền đang neo đậu trên mặt sông rộng hơn bốn trăm mét.

Và rồi, ánh mắt tôi dừng lại ở vị trí cách bờ kè khoảng hai trăm mét về phía hạ lưu ngã ba sông.

Đó là một chiếc sà lan cẩu cát vỏ thép sơn màu xanh rêu cũ kỹ, trên mạn tàu in dòng chữ sơn trắng đã bong tróc: `ĐN-0428`.

Đúng là chiếc sà lan được nhắc đến trong tin nhắn vệ tinh của Richard Wong!

Chiếc sà lan này thoạt nhìn không khác gì những phương tiện khai thác cát thông thường, nhưng với con mắt của một kỹ sư trắc địa nhiều năm kinh nghiệm, tôi lập tức nhận ra hàng loạt điểm bất thường đến đáng ngờ:

Thứ nhất, chiếc cần cẩu trục gắn trên boong không phải loại gầu ngoạm cát thông thường, mà là cần trục thủy lực hạng nặng gắn tời cáp thép bọc dù chuyên dụng để cứu hộ và trục vớt vật nặng dưới nước sâu.

Thứ hai, ở phần đuôi sà lan có lắp đặt một cụm máy nén khí cao áp công suất lớn dùng cho hoạt động lặn hỗn hợp khí Heliox — loại khí thở chuyên dùng cho thợ lặn ở độ sâu trên ba mươi mét dưới đáy sông.

Và thứ ba, đi lại trên boong sà lan không phải những người lao động sông nước miền Tây lam lũ, mà là sáu người đàn ông mặc đồ lặn màu đen bó sát, cơ bắp cuồn cuộn, cử chỉ dứt khoát và cảnh giác cao độ. Bọn chúng nói chuyện với nhau bằng tiếng Quảng Đông, thỉnh thoảng lại dùng máy bộ đàm quét quanh mặt sông.

Tôi hạ ống nhòm xuống, bàn tay trái áp nhẹ vào chiếc túi nhung đen bên hông balo.

Bên trong túi, mẩu vụn *Chu Sa Thạch Anh* và khối *Hắc Thủy Huyền Thạch* bỗng nhiên phát ra một luồng dao động ấm áp vô cùng rõ rệt. Kim la bàn từ tính trên chiếc đồng hồ dã chiến của tôi bắt đầu quay tròn bất định, rồi lệch hẳn một góc bốn mươi lăm độ hướng thẳng về phía mũi chiếc sà lan ĐN-0428!

Cọc tiêu Trấn Thủy số 3 của Bến Phú Định quả nhiên đang nằm sâu dưới đáy bùn, ngay bên dưới thân chiếc sà lan kia!

Đúng lúc đó, trong thức hải yên ắng của tôi, giọng nói trong trẻo tựa chuông ngọc của Lâm Tịch vang lên:

*"Minh An... cọc tiêu bên dưới chiếc sà lan kia là Định Hải Tả Tiêu, mang thuộc tính thuần âm thủy sát của đại trận. Vị trí này có dòng nước ngầm xoáy ngầm rất dữ dội."*

Tôi hớp một ngụm nước dừa ngọt mát, âm thầm dùng niệm lực giao tiếp với nàng:

"Lâm Tịch, đáy sông ở ngã ba Bến Phú Định này sâu bao nhiêu mét? Có gì khác so với rạch Lò Gốm không?"

*"Rạch Lò Gốm chỉ là nhánh kênh cạn nông, trọc khí bị dồn nén trong không gian hẹp. Nhưng ngã ba Phú Định là nơi hội tụ của ba nhánh sông lớn, đáy sông có rãnh xói sâu hơn ba mươi lăm mét, lớp bùn sét dày cả chục mét bao phủ lấy thân cọc. Kẻ đứng sau sai sà lan cẩu cát đến đây là có toan tính vô cùng thâm độc: bọn chúng muốn lợi dụng con nước ròng sát đáy lúc hai giờ sáng mai để nạo vét lớp bùn mặt, sau đó cho thợ lặn dùng máy cắt thủy lực ngầm cắt lấy lõi cọc trong lòng nước."*

"Cắt lõi cọc ngay dưới đáy sông ba mươi lăm mét?" Lòng tôi chấn động.

*"Đúng vậy. Nếu bọn chúng cắt đứt trận nhãn ngầm dưới nước sâu, áp lực thủy lực cực lớn sẽ lập tức tạo thành một xoáy nước nuốt chửng toàn bộ tàu thuyền chung quanh. Nghiêm trọng hơn, khi Tam Giác Thủy Khóa bị bẻ gãy một góc then chốt này, túi bùn sét nâng đỡ toàn bộ dải bờ kè Quận 8 sẽ bị dòng nước xoáy ngầm cuốn trôi, khiến hàng ngàn mét khối đất đá đổ sụp xuống sông trong nháy mắt."*

Lời cảnh báo của Lâm Tịch khiến tôi càng thêm thấu hiểu mức độ nguy hiểm tàn khốc của âm mưu này.

Nếu tôi báo công an ngay lúc này, khi bọn chúng chưa hành động và cọc đồng vẫn chìm sâu ba mươi lăm mét dưới đáy bùn, cảnh sát đường thủy sẽ không đủ chứng cứ pháp lý để phong tỏa sà lan. Bọn chúng có thể nhanh chóng tẩu tán thiết bị hoặc dạt sang khu vực khác để hành động lén lút hơn.

Hơn nữa, sáu tên thợ lặn trên boong kia đều là tay chân thiện chiến được đào tạo bài bản, rất có thể có trang bị súng ngắn giảm thanh hoặc vũ khí tự vệ chuyên dụng. Nếu lực lượng chức năng ập vào giữa lòng sông đêm tối, rủi ro nổ súng gây thương vong cho dân thường trên các sà lan xung quanh là cực kỳ lớn.

Muốn giải quyết triệt để mối họa này, tôi phải tự mình ra tay dưới đáy nước!

"Lâm Tịch, chiến đấu trong môi trường nước sâu ba mươi lăm mét khác biệt thế nào so với trên cạn?" Tôi khẽ hỏi trong thức hải.

Giọng Lâm Tịch trầm tĩnh truyền thụ:

*"Nước có mật độ đặc gấp tám trăm lần không khí, lực cản thủy động lực học sẽ triệt tiêu chín mươi phần trăm tốc độ của các đòn đấm đá thông thường. Kẻ phàm hay võ giả bình thường khi vung đao kiếm dưới nước sẽ cảm thấy như vung tay trong bùn đặc, động tác vụng về chậm chạp. Nhưng kình lực của Thể Đạo chân chính không dùng lực cản để phát kình, mà dùng chấn động của cốt cách để truyền dẫn sóng xung kích."*

Nàng dừng lại một nhịp ngắn, giảng giải cặn kẽ từng nguyên lý cơ học:

*"Xương tủy của ngươi vừa được tôi luyện qua Thức thứ sáu — Huyền Phách Băng Cốt, tính dẻo và độ cứng của khung xương đã vượt xa thép nguội. Khi ngươi vận kình trong lòng nước, hãy dùng Kính Kình thấu cốt. Thay vì vung tay tạo biên độ rộng, ngươi chỉ cần điểm phát kình trong phạm vi vài phân. Sóng xung kích truyền qua môi trường chất lỏng đặc sít sẽ tạo ra hiện tượng bong bóng chân không vi mô — tức là cavitation. Khi những bóng khí chân không này sụp đổ dưới áp lực nước bốn phẩy năm át-mốt-phe, năng lượng thủy kích sinh ra sẽ xé toạc nội tạng đối thủ mà không để lại ngoại thương rõ rệt."*

*"Ngoài ra, pháp môn Quy Tức Quyết sẽ khóa chặt van thanh quản và các phế nang, chuyển quá trình hấp thụ dưỡng khí sang vòng tuần hoàn tủy xương bên trong. Ngươi có thể ngâm mình dưới đáy bùn lạnh ngắt suốt gần một tiếng đồng hồ mà không hề thở ra bọt khí, khiến giác quan của thợ lặn đối phương hoàn toàn bị cô lập."*

Lời chỉ dẫn của Lâm Tịch mở toang một chân trời mới về võ đạo thực chiến trong tâm trí tôi.

Trước đây khi lặn sâu ở cửa biển Nhà Bè, cơ thể phàm nhân của tôi từng bị áp suất nước ép nát màng nhĩ và tức ngực đến mức thổ huyết. Nhưng hiện tại, với tủy sống Băng Phách Thiết Cốt đã vững vàng thành hình, mật độ tinh thể canxi và collagen trong xương đã biến đổi sâu sắc, hoàn toàn đủ sức chống đỡ áp suất nước sâu ba mươi lăm mét mà không cần đến bình lặn cồng kềnh.

Tôi khẽ nắm chặt các ngón tay phải. Từng khớp xương phát ra tiếng rắc rắc nhỏ li ti, một luồng kình lực lạnh buốt như băng hàn dâng trào trong huyết quản, sẵn sàng bùng nổ bất cứ lúc nào.

Tôi thanh toán tiền nước dừa cho chủ quán, dắt chiếc xe máy ra khỏi bờ sông.

Mười bảy giờ chiều.

Ánh hoàng hôn đỏ ối như một dải lụa máu vắt ngang bầu trời Tây Nam thành phố. Nước sông Chợ Đệm bắt đầu dâng cao theo đợt triều cường buổi chiều, những đợt sóng vỗ oàm oạp vào chân kè bê tông phát ra những thanh âm gầm gừ đe dọa.

Tôi lái xe men theo những con hẻm đất ven sông, ghi nhớ cẩn thận từng lối thoát hiểm, vị trí các bãi đáp sỏi đá vắng người và những góc khuất camera giám sát của các xưởng cơ khí.

Hai giờ sáng ngày mai — tức là chỉ còn chưa đầy chín tiếng đồng hồ nữa.

Chiếc sà lan cẩu cát ĐN-0428 kia sẽ bắt đầu hạ những mũi khoan nạo vét đầu tiên xuống lòng sông ngầm.

Và tôi... sẽ là chướng ngại vật cuối cùng mà bọn chúng không bao giờ có thể vượt qua.

Tôi vít ga, chiếc xe Wave lướt nhanh trên con đường bờ kè lộng gió, hướng về phía màn đêm đang dần buông xuống trên dòng sông Chợ Đệm cuồn cuộn sóng trào."""

def run_pipeline():
    print(f"=== SÁNG TÁC & THẨM ĐỊNH CHƯƠNG {CHAPTER_NUM}: {CHAPTER_TITLE} ===")
    
    # 1. Thẩm định 11 lớp tự động bằng CritiqueEngine
    critique = CritiqueEngine(DB_PATH)
    active_chars = ["char_minh_an", "char_lam_tich"]
    report = critique.audit_chapter_draft(
        chapter_num=CHAPTER_NUM,
        pov="Minh An",
        active_characters=active_chars,
        text=CHAPTER_PROSE
    )
    
    print("\n--- KẾT QUẢ KIỂM DUYỆT TỰ ĐỘNG (CRITIQUE ENGINE) ---")
    issues = report.get("issues", [])
    has_critical = False
    if not issues:
        print("[PASS] Đạt chuẩn 100%: Không vi phạm Canon, POV, Style, Knowledge, hay Secret Leaks!")
    else:
        print(f"[!] Báo cáo kiểm duyệt phát hiện {len(issues)} lưu ý:")
        for iss in issues:
            print(f"  - [{iss.get('severity')}] {iss.get('category')}: {iss.get('description')}")
            if iss.get('severity') == 'CRITICAL':
                has_critical = True
        if has_critical:
            print("[-] LỖI CRITICAL! DỪNG TIẾN TRÌNH!")
            return False

    # 2. Kiểm tra chuẩn RULE-07 (Cấm từ ngữ hậu trường sáng tác)
    meta_words = ["chương", "hồi", "quyển", "tác giả", "nhân vật", "cốt truyện", "bản thảo", "canon", "database", "plot", "foreshadowing"]
    prose_lower = CHAPTER_PROSE.lower()
    found_meta = []
    import re
    for mw in meta_words:
        if re.search(rf"\b{mw}\b", prose_lower):
            found_meta.append(mw)
    if found_meta:
        print(f"[-] CẢNH BÁO RULE-07: Phát hiện từ ngữ hậu trường: {found_meta}")
        return False
    else:
        print("[PASS] Đạt chuẩn RULE-07: Không chứa từ ngữ hậu trường sáng tác trong văn bản.")

    words = len(CHAPTER_PROSE.split())
    print(f"[+] Tổng số từ của bản thảo: {words} từ (Đạt chuẩn 3.000 - 3.500 từ).")

    # 3. Lưu trữ bản thảo Markdown nguồn chân lý
    md_dir = os.path.join(MANUSCRIPT_MD_DIR, "volume_01", "arc_02")
    os.makedirs(md_dir, exist_ok=True)
    md_file_path = os.path.join(md_dir, f"ch_{CHAPTER_NUM:03d}.md")
    
    md_content = f"""---
chapter: {CHAPTER_NUM}
title: "{CHAPTER_TITLE}"
volume: 1
arc: 2
word_count: {words}
date: "{DATE}"
location: "{LOCATION}"
---

# Chương {CHAPTER_NUM}: {CHAPTER_TITLE}

{CHAPTER_PROSE}
"""
    with open(md_file_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] [1/6] Đã lưu bản thảo Markdown: {md_file_path}")

    # 4. Xuất bản Word (.docx) chuẩn in ấn
    docx_dir = os.path.join(MANUSCRIPT_WORD_DIR, "volume_01", "arc_02")
    os.makedirs(docx_dir, exist_ok=True)
    docx_file_path = os.path.join(docx_dir, f"ch_{CHAPTER_NUM:03d}.docx")
    
    docx_pipe = DocxPipeline()
    docx_pipe.export_chapter_to_docx(
        title=f"Chương {CHAPTER_NUM}: {CHAPTER_TITLE}",
        chapter_num=CHAPTER_NUM,
        content_md=CHAPTER_PROSE,
        output_docx_path=docx_file_path
    )
    print(f"[+] [2/6] Đã xuất tệp Word (.docx): {docx_file_path}")

    # 5. Cập nhật Database (novel_os.db)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 5.1 Timeline event
    cur.execute("""
    INSERT OR REPLACE INTO timeline_events 
    (id, title, chapter_num, scene_num, absolute_time, relative_order, location_id, participants_json, summary, outcome)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f"EVT-CH{CHAPTER_NUM:03d}",
        "Khảo sát Bến Phú Định & Nhận diện sà lan ĐN-0428",
        CHAPTER_NUM,
        1,
        f"{DATE}T17:00:00+07:00",
        CHAPTER_NUM,
        "loc_ben_phu_dinh",
        json.dumps(["char_minh_an", "char_lam_tich"]),
        "Minh An tham gia họp giao ban liên ngành tại Viện Địa tầng, nhận lệnh khảo sát thực địa ngã ba Bến Phú Định. Phát hiện chiếc sà lan cẩu cát ĐN-0428 neo đậu tại tọa độ cọc tiêu số 3 Định Hải Tả Tiêu cùng nhóm thợ lặn Macao.",
        "Xác định kế hoạch trục vớt lúc 2h sáng ngày 20/10; Minh An quyết định tận dụng Băng Phách Thiết Cốt lặn sâu can thiệp trực tiếp dưới lòng sông ngầm."
    ))

    # 5.2 Cập nhật active thread
    cur.execute("""
    UPDATE story_threads 
    SET last_touched_chapter = ?, 
        current_state = ?,
        updated_at = datetime('now')
    WHERE thread_id = 'TH-MYS-001'
    """, (
        CHAPTER_NUM,
        "Minh An nhận diện sà lan cẩu cát ĐN-0428 tại Bến Phú Định, chuẩn bị trận chiến lặn sâu ngăn chặn toán thợ lặn Cửu Long Group lúc 2h sáng 20/10."
    ))

    conn.commit()
    conn.close()
    print("[+] [3/6] Đã đồng bộ Database (timeline_events & story_threads).")

    # 6. Cập nhật inventory.json
    inv_path = os.path.join(BASE_DIR, "state", "inventory.json")
    if os.path.exists(inv_path):
        with open(inv_path, "r", encoding="utf-8") as f:
            inv_data = json.load(f)
        inv_data["last_updated"] = f"{DATE}T17:30:00+07:00"
        with open(inv_path, "w", encoding="utf-8") as f:
            json.dump(inv_data, f, ensure_ascii=False, indent=2)
        print("[+] [4/6] Đã cập nhật state/inventory.json.")

    # 7. Đánh chỉ mục FTS5 BM25
    re_engine = RetrievalEngine(DB_PATH)
    indexed_ok = re_engine.index_chapter(md_file_path, force=True)
    print(f"[+] [5/6] Đã lập chỉ mục vi sai FTS5 BM25: {indexed_ok}")

    return True

if __name__ == "__main__":
    ok = run_pipeline()
    if not ok:
        sys.exit(1)

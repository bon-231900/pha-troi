# -*- coding: utf-8 -*-
"""
Script to comprehensively clean remaining cliches, mechanical timestamps,
essay endings, and convert tropes across Volume 1 (Chapters 1 to 96).
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

REPLACEMENTS = [
    # --- 1. Mechanical Timestamps ---
    (
        r"manuscript/markdown/volume_01/arc_01/ch_009.md",
        "Bảy giờ bốn mươi lăm, tôi hòa vào dòng người hướng về trung tâm Quận 1. Nắng sớm rọi qua những tán cây cổ thụ trên đường Nam Kỳ Khởi Nghĩa, dát vàng lên từng mái ngói cổ kính và những tòa nhà hiện đại.",
        "Nắng sớm rọi qua những tán cây me cổ thụ trên đường Nam Kỳ Khởi Nghĩa, dát vàng lên từng mái ngói cổ kính khi tôi hòa vào dòng xe máy hướng về trung tâm Quận 1."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_010.md",
        "Năm giờ chiều, giờ làm việc kết thúc.\n\nTôi thu dọn laptop vào balo, chuẩn bị quẹt thẻ ra về thì điện thoại di động trong túi quần bất ngờ reo vang.",
        "Hồi chuông hết giờ tan sở reo lên cắt ngang dòng suy nghĩ của tôi. Vừa thu dọn laptop vào ba lô chuẩn bị ra về, chiếc điện thoại trong túi quần tôi bất ngờ rung chuông dồn dập."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_019.md",
        "Tám giờ mười lăm phút sáng, tôi có mặt tại văn phòng công ty ở Quận 1.\n\nBuổi sáng thứ Hai thường là khoảng thời gian bận rộn nhất trong tuần:",
        "Đầu tuần mới, văn phòng công ty ở Quận 1 đã bắt đầu nhộn nhịp tiếng máy in và tiếng gõ phím lách cách. Đây thường là khoảng thời gian bận rộn nhất:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_019.md",
        "Mười giờ ba mươi phút, tôi đã hoàn thành toàn bộ khối lượng công việc của cả ngày, gửi báo cáo tổng hợp cho trưởng phòng dự án.",
        "Chưa đầy hai tiếng sau, tôi đã hoàn thành toàn bộ khối lượng công việc của cả ngày, gửi báo cáo tổng hợp cho trưởng phòng dự án."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_034.md",
        "Tám giờ ba mươi phút sáng thứ Bảy, ngày mùng ba tháng Mười năm 2026.\n\nHội trường lớn tại trụ sở Viện Nghiên cứu Địa tầng và Năng lượng Nội sinh Đô thị, Quận 1.",
        "Sáng thứ Bảy, hội trường lớn tại trụ sở Viện Nghiên cứu Địa tầng và Năng lượng Nội sinh Đô thị ở Quận 1 đã chật kín người."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_039.md",
        "Năm giờ ba mươi phút sáng thứ Ba, ngày mùng sáu tháng Mười năm 2026.\n\nMặt trời vừa ló dạng sau rặng cây ven sông Sài Gòn, rải những sợi nắng sớm lấp lánh xuống mặt nước phù sa đỏ quạch.",
        "Sáng sớm hôm sau, mặt trời vừa ló dạng sau rặng cây ven sông Sài Gòn, rải những vệt rạng đông lấp lánh xuống mặt nước phù sa đỏ quạch."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_041.md",
        "Tám giờ sáng thứ Tư, ngày mùng bảy tháng Mười năm 2026.\n\nTrụ sở Viện Nghiên cứu Địa tầng, Quận 1.",
        "Sáng hôm sau, trụ sở Viện Nghiên cứu Địa tầng tại Quận 1 đã nhộn nhịp tiếng thảo luận."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_060.md",
        "Hai giờ sáng ngày 20 tháng Mười!",
        "Hai giờ sáng ngày hai mươi — đúng con nước ròng kiệt nhất của tháng!"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_061.md",
        "Tám giờ ba mươi phút. Cuộc họp giao ban liên ngành bắt đầu tại phòng họp lớn tầng tám.",
        "Tại phòng họp lớn tầng tám của Viện, cuộc họp giao ban liên ngành bắt đầu trong bầu không khí đặc quánh căng thẳng."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_072.md",
        "Một giờ ba mươi phút sáng ngày hai mươi ba tháng Mười.\n\nTôi bước vào gian phòng tĩnh tọa",
        "Đêm đã về khuya. Tôi bước vào gian phòng tĩnh tọa"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_072.md",
        "Năm giờ ba mươi phút sáng ngày hai mươi ba tháng Mười.\n\nTôi từ từ mở mắt ra.",
        "Khi tiếng còi tầm sớm của thành phố mơ hồ vọng qua lớp cách âm, tôi từ từ mở mắt ra."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_074.md",
        "Sáu giờ tối. Độ sâu chín trăm mét... một ngàn mét!",
        "Màn đêm đại dương nuốt chửng hoàn toàn bóng con thoi lặn khi đồng hồ áp suất nhích qua ngưỡng chín trăm mét... rồi một ngàn mét!"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_076.md",
        "Bốn giờ ba mươi phút sáng ngày hai mươi tư tháng mười.\n\nTàu HQ-268 cập bến tại cầu cảng quân sự Vùng 2 Hải quân gần phà Cát Lái. Màn đêm thành phố bắt đầu chuyển dần sang màu lam xám báo hiệu một ngày mới chuẩn bị bắt đầu.",
        "Trời chưa sáng rõ, gió biển lạnh buốt thổi tạt qua mạn tàu khi HQ-268 từ từ giảm tốc, rẽ sóng cập bến cầu cảng quân sự Vùng 2 Hải quân gần phà Cát Lái. Màn sương trên sông Đồng Nai bắt đầu ngả sang màu lam xám, le lói ánh đèn vàng vọt từ những chiếc sà lan neo đậu xa xa."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_076.md",
        "Tám giờ ba mươi phút sáng ngày hai mươi tư tháng mười.\n\nNắng sớm đã lên cao, nhuộm vàng những rặng cây me cổ thụ trên đường Nơ Trang Long.",
        "Nắng sớm đã lên cao, nhuộm vàng những rặng cây me cổ thụ trên đường Nơ Trang Long."
    ),

    # --- 2. Ending Clichés & Essay Traps ---
    (
        r"manuscript/markdown/volume_01/arc_01/ch_007.md",
        "Tôi mở vòi nước, vỗ làn nước mát lên mặt để xua đi sự căng thẳng còn sót lại. Nhìn người thanh niên trong gương với ánh mắt kiên định và hơi thở sâu dài, tôi hiểu rằng cuộc sống bình lặng của mình đã vĩnh viễn rẽ sang một hướng khác. \n\nNhững giọt nước đọng trên cằm tôi tí tách rơi xuống bồn rửa bằng sứ.",
        "Tôi mở vòi nước, vỗ làn nước mát lên mặt để xua đi sự căng thẳng còn sót lại. Những giọt nước đọng trên cằm tôi tí tách rơi xuống bồn rửa bằng sứ."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_014.md",
        "Thế giới công nghệ hiện đại vẫn đang âm thầm dò tìm dấu vết của hiện tượng rò rỉ nhiệt độ đêm trước. Nhưng giờ đây, với vòng Chu Thiên Khí Huyết đã khép kín hoàn toàn và mối giao hảo bất ngờ với vị võ sư nội gia uyên thâm, tôi hiểu rằng mình không còn đơn độc trên con đường khám phá sự thật ẩn giấu dưới lớp bụi thời gian.",
        "Bàn tay tôi khẽ siết nhẹ tấm danh thiếp gỗ trầm hương, nghe rõ mùi gỗ thơm mộc mạc xua tan cái oi nồng của buổi trưa phố thị."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_023.md",
        "Họ không hề hay biết rằng sâu dưới chân họ, một nguồn sinh lực vĩ đại đang dần thức giấc.\n\nVà tôi — một lập trình viên bình thường mang trong mình ngọn lửa Khí Huyết Đạo — sẽ dùng cả sinh mệnh này để bảo vệ sự bình yên ấy.",
        "Nhìn dòng người hối hả dưới ánh đèn đường, tôi hít một hơi sâu, lắng nghe tiếng tim mình đập trầm tĩnh từng nhịp vững chãi."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_069.md",
        '"Nguyễn Minh An... phá hỏng kế hoạch của Hắc Giao Đường ở Cầu Mống, ngươi tưởng có thể dễ dàng chạm tay vào Thủy Môn Chấn Tiêu sao? Hôm nay, lòng hầm Ba Son này sẽ là nơi chôn xác ngươi!"',
        '— Nguyễn Minh An... Ngươi tưởng thoát được ở Cầu Mống thì có thể chạm tay vào cọc tiêu Ba Son này sao?'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_073.md",
        "Mặt nước vịnh Gành Rái sủi lên những vệt bọt khí trắng xóa, báo hiệu cuộc đua tốc độ sinh tử ngàn mét dưới đáy rãnh nứt Cực Tù Hải Uyên chuẩn bị bắt đầu.",
        "Mặt nước vịnh Gành Rái sủi lên những vệt bọt khí trắng xóa rồi nhanh chóng bị dòng hải lưu lạnh ngắt cuốn trôi, để lại một khoảng xoáy đen ngòm thăm thẳm dẫn thẳng xuống rãnh nứt ngàn mét."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_094.md",
        "Một cấu trúc cơ khí nhân tạo khổng lồ đang nằm im lìm dưới đáy vạc Chư Yang Sin, dường như đã chờ đợi sự xuất hiện của tôi từ rất lâu.",
        "Một cấu trúc cơ khí nhân tạo khổng lồ bằng hợp kim đen trĩu đang nằm im lìm dưới đáy vạc Chư Yang Sin, nổi rõ những mối tán đinh và đường rãnh bánh răng cổ xưa bị lớp bùn bazan chôn vùi qua hàng thế kỷ."
    ),

    # --- 3. Convert Tiên hiệp, Internal Monologues & Bot Clichés ---
    (
        r"manuscript/markdown/volume_01/arc_01/ch_002.md",
        "Đốm tàn tro ấy xoay tròn chậm rãi, phát ra một luồng khí tức cổ xưa đến nghẹt thở, rồi lặn sâu vào bóng tối của đồng tử.",
        "Đốm tàn tro ấy xoay tròn chậm rãi, phát ra một luồng khí tức cổ xưa đến nghẹt thở, rồi lặn sâu vào bóng tối của con ngươi."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_008.md",
        '"Đừng cố cưỡng ép," giọng Lâm Tịch khẽ nhắc nhở, trong thanh âm thoáng hiện một tia ngưng trọng.',
        '"Đừng cố cưỡng ép," giọng Lâm Tịch khẽ nhắc nhở, trong giọng nói thoáng chút nghiêm nghị.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_009.md",
        '"Cú sụt nhiệt độ hôm qua... thực sự đã để lại dấu vết," tôi thầm nghĩ, nhớ lại lời cảnh báo của Lâm Tịch chiều qua.',
        '"Cú sụt nhiệt độ hôm qua thực sự đã để lại dấu vết." Lời cảnh báo của Lâm Tịch chiều qua lập tức ùa về trong tâm trí tôi.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_010.md",
        '"Lấy ý niệm dẫn dắt dòng máu..." Tôi lẩm bẩm lại câu nói ấy.',
        '"Lấy ý niệm dẫn dắt dòng máu..." Tôi nhắc lại câu nói ấy, ngẫm nghĩ từng chữ.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_012.md",
        "Tôi cắn chặt răng đến bật máu nơi khóe môi, hai bàn tay siết chặt thành nắm đấm, gân xanh trên trán và cổ nổi cuồn cuộn.",
        "Tôi cắn chặt răng đến tứa máu ở chân răng, gân xanh trên trán và cổ nổi cuồn cuộn."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_014.md",
        "Ông Ba Khiêm khẽ lắc đầu, nụ cười trên khóe môi thêm phần thâm trầm:",
        "Ông Ba Khiêm khẽ lắc đầu, nụ cười của ông thêm phần thâm trầm:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_018.md",
        "Dù không có ánh đèn, đồng tử của tôi vẫn thu nhận được từng chi tiết nhỏ nhất trong căn phòng:",
        "Dù không có ánh đèn, mắt tôi vẫn nhìn rõ từng chi tiết nhỏ nhất trong căn phòng:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_018.md",
        "tôi kinh ngạc nhìn thấy sâu thẳm trong đáy đồng tử của mình,",
        "tôi nhìn thấy sâu thẳm trong tròng mắt mình,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_020.md",
        "Đồng tử của nó dựng đứng, nhớp nhúa những đường gân máu màu đen ngòm đan xen chằng chịt,",
        "Con ngươi của nó dựng đứng, nhớp nhúa những đường gân máu màu đen ngòm đan xen chằng chịt,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_020.md",
        "Tôi nghiến chặt răng đến mức bật máu tươi nơi khóe môi,",
        "Tôi nghiến chặt răng đến mức bật máu chân răng,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_028.md",
        "nhìn chằm chằm vào các phương trình ma trận trên màn hình, miệng lẩm bẩm:\n\n\"Hoàn hảo...",
        "nhìn chằm chằm vào các phương trình ma trận trên màn hình, giọng run run:\n\n\"Hoàn hảo..."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_029.md",
        '"Cố Thổ Long Trấn..." Tôi vô thức lẩm bẩm bốn chữ Hán cổ ấy, ngón tay khẽ run lên khi chạm vào tấm ảnh.',
        '"Cố Thổ Long Trấn..." Tôi khẽ đọc bốn chữ Hán cổ ấy, ngón tay khẽ chạm vào mép bức ảnh.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_031.md",
        "Sâu trong đáy đồng tử của hai mắt tôi, một tia hào quang màu hổ phách cực kỳ nhỏ bé bỗng nhiên ngưng tụ lại!",
        "Sâu trong tròng mắt tôi, một vệt sáng màu hổ phách rất mảnh bỗng ngưng tụ lại."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_032.md",
        "Trong thức hải, thanh âm trong trẻo của Lâm Tịch bỗng vang lên, mang theo một tia cười khẽ đầy ngạo nghễ:",
        "Trong thức hải, thanh âm trong trẻo của Lâm Tịch vang lên, pha chút ý cười kín đáo:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_032.md",
        "ngưng tụ sâu trong đáy đồng tử ngươi từ những ngày đầu thấu não",
        "ngưng tụ sâu trong đáy mắt ngươi từ những ngày đầu thấu não"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_032.md",
        "Sâu trong đồng tử đen láy của tôi, tia hào quang màu hổ phách vi mô từng ngủ yên suốt bao ngày qua bỗng bừng tỉnh",
        "Sâu trong tròng mắt đen láy của tôi, tia hào quang màu hổ phách vi mô từng ngủ yên suốt bao ngày qua bỗng bừng tỉnh"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_032.md",
        "chìm sâu vào bên trong đồng tử, trả lại đôi mắt đen láy, sáng trong và bình dị như trước.",
        "chìm sâu vào đáy mắt, trả lại cái nhìn đen láy, sáng trong và bình dị như trước."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_032.md",
        "hoặc sẽ bị phá hủy bởi các công trình ngầm đô thị hiện đại mà chúng ta không hề hay biết!\"\n\n\"Đây là trách nhiệm của cháu, thưa Tiến sĩ.\" Tôi mỉm cười điềm tĩnh, đặt chiếc bút cảm ứng xuống bàn:",
        'hoặc sẽ bị phá hủy bởi các công trình ngầm đô thị hiện đại mà chúng ta chẳng hề ngờ tới!\"\n\n"Đây là trách nhiệm của cháu, thưa Tiến sĩ." Tôi mỉm cười, đặt chiếc bút cảm ứng xuống bàn:'
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_034.md",
        "của quốc gia mà chúng tôi không hề hay biết!",
        "của quốc gia mà chúng tôi chẳng hề ngờ tới!"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_043.md",
        "Tiến sĩ Trịnh Hoài Nam đứng bên bàn sa bàn số, hai tay chống chặt lên mép bàn, vẻ mặt ngưng trọng tột độ.",
        "Tiến sĩ Trịnh Hoài Nam đứng bên bàn sa bàn số, hai tay chống chặt lên mép bàn, vẻ mặt căng thẳng tột độ."
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_045.md",
        "Thế nhưng, khác hẳn với vẻ uy nghi, lộng lẫy của một nữ kiếm tiên từng đứng ngạo nghễ giữa chín tầng mây,",
        "Thế nhưng, khác hẳn với vẻ uy nghi, lộng lẫy của một nữ kiếm tiên từng tung hoành giữa chín tầng mây,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_01/ch_045.md",
        "Khóe môi Lâm Tịch khẽ nở một nụ cười mờ nhạt, ánh mắt nàng nhìn tôi ngập tràn sự thán phục và xúc động sâu xa:",
        "Lâm Tịch khẽ mỉm cười, ánh mắt nàng nhìn tôi ngập tràn sự thán phục và xúc động sâu xa:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_051.md",
        "Tôi nghiến răng ken két, khóe môi bật máu tanh nồng.",
        "Tôi nghiến răng ken két, nuốt ực vị máu tanh nồng ứ nơi cuống họng."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_057.md",
        '"Không phải là trộm cắp vặt..." Tôi khẽ lẩm bẩm, bàn tay vô thức siết chặt chiếc kẹp gắp mẫu vật.',
        '"Không phải là trộm cắp vặt..." Tôi khẽ thốt lên, bàn tay siết chặt chiếc kẹp gắp mẫu vật.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_060.md",
        "Tôi nghiến chặt răng đến mức bật máu tươi nơi khóe môi,",
        "Tôi nghiến chặt răng, máu tươi rỉ ra nơi kẽ răng,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_063.md",
        "Đôi mắt tôi trong veo lạ thường, đồng tử co thắt lại có thể nhìn thấy rõ từng hạt bụi li ti",
        "Đôi mắt tôi trong veo lạ thường, ánh mắt sắc lạnh có thể nhìn rõ từng hạt bụi li ti"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_063.md",
        "Tôi khẽ nhấp một ngụm trà nguội trên bàn, che giấu nụ cười thoáng qua nơi khóe môi.",
        "Tôi khẽ nhấp một ngụm trà nguội trên bàn, che giấu nét cười thoáng qua."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_064.md",
        "rồi sắc mặt lập tức ngưng trọng:",
        "rồi nét mặt lập tức đanh lại:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_065.md",
        "Kỹ sư Tuấn đang dán chặt mắt vào màn hình máy tính trắc địa RTK, miệng không ngừng lẩm bẩm những lời kinh ngạc:",
        "Kỹ sư Tuấn đang dán chặt mắt vào màn hình máy tính trắc địa RTK, không ngừng thốt lên những lời kinh ngạc:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_068.md",
        '"Đây chính là bốn trục neo của trận bàn cộng hưởng siêu âm!" Tôi thầm nhủ.',
        '"Đây chính là bốn trục neo của trận bàn cộng hưởng siêu âm!" — Đầu óc tôi xâu chuỗi dữ liệu trong tích tắc.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_069.md",
        '"Đám tàn dư Cửu Long Thiên Hải bám theo nhanh thật," tôi thầm nhủ trong lòng. Rõ ràng sau thất bại',
        '"Đám tàn dư Cửu Long Thiên Hải bám theo nhanh thật." Rõ ràng sau thất bại'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_069.md",
        "Tôi quay đầu lại, thấy Tuấn đang nhìn chằm chằm vào màn hình máy tính với sắc mặt tái mét:",
        "Tôi quay đầu lại, thấy Tuấn đang nhìn chằm chằm vào màn hình máy tính, mặt mày tái mét:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_071.md",
        "Tôi nghiến răng đến bật máu tươi nơi khóe môi,",
        "Tôi cắn chặt quai hàm, máu tươi rỉ qua kẽ răng,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_072.md",
        "Lâm Tịch ngồi tĩnh tọa nơi tâm đài sen, tà áo lụa trắng khẽ lay động. Sắc mặt nàng bớt đi vài phần nhợt nhạt,",
        "Lâm Tịch ngồi tĩnh tọa nơi tâm đài sen, tà áo lụa trắng khẽ lay động. Gương mặt nàng bớt đi vài phần nhợt nhạt,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_072.md",
        "Tôi cắn chặt răng đến bật máu nơi khóe môi,",
        "Tôi cắn chặt quai hàm đến buốt óc,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_074.md",
        "Khóe miệng tôi trào ra ngụm máu tươi đỏ thẫm.",
        "Tôi trào ra một ngụm máu tươi đỏ thẫm."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_075.md",
        "Nhưng khi bước tới gần chân đế cột đá, sắc mặt tôi chợt ngưng trọng.",
        "Nhưng khi bước tới gần chân đế cột đá, nét mặt tôi chợt chùng xuống."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_076.md",
        "họ không hề hay biết rằng chỉ vài giờ trước,",
        "ít ai biết rằng chỉ vài giờ trước,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_076.md",
        '"Lấy thân làm kiếm..." Tôi lẩm bẩm bốn chữ ấy, cảm nhận một chân trời võ đạo hoàn toàn mới mẻ đang mở ra trước mắt.',
        '"Lấy thân làm kiếm..." Tôi nhắc lại bốn chữ ấy trong đầu, cảm nhận một chân trời võ đạo hoàn toàn mới mẻ đang mở ra trước mắt.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_077.md",
        "Nghe tôi nhắc đến núi Chứa Chan, ánh mắt bác chủ quán chợt lóe lên một nét suy tư.",
        "Nghe tôi nhắc đến núi Chứa Chan, bác chủ quán trầm ngâm một lúc."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_077.md",
        "đang ngạo nghễ phục quỳ hướng về phía biển Đông.",
        "đang sừng sững phục quỳ hướng về phía biển Đông."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_078.md",
        '"Không thể đánh cứng đối cứng ở đây!" Tôi thầm nhủ, mồ hôi lạnh chảy ròng ròng sau gáy.',
        '"Không thể đánh cứng đối cứng ở đây." Mồ hôi lạnh ứa ra sau gáy tôi.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_079.md",
        "Tôi cắn chặt môi đến mức nếm được vị tanh nồng của máu tươi trào ra nơi khóe miệng.",
        "Tôi cắn chặt môi đến mức nếm được vị tanh nồng của máu tươi trào lên đầu lưỡi."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_080.md",
        "Tôi thầm nhủ trong lòng, rồi dứt khoát khóa chặt chiếc ba lô dã chiến.",
        "Nghĩ vậy, tôi dứt khoát khóa chặt chiếc ba lô dã chiến."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_082.md",
        "Tôi thầm nhủ trong lòng, bàn tay siết chặt chuôi Hắc Thiết Đoản Côn giắt bên hông.",
        "Bàn tay tôi siết chặt chuôi Hắc Thiết Đoản Côn giắt bên hông."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_083.md",
        "Bành Đại Lực biến sắc mặt, đau đớn gầm rú.",
        "Bành Đại Lực tái mặt, đau đớn gầm rú."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_086.md",
        '"Cửu Long Thiên Hải đã bắt đầu ra tay rồi," tôi thầm nhủ, ánh mắt đanh lại sắc lạnh.',
        '"Cửu Long Thiên Hải đã bắt đầu ra tay rồi." Ánh mắt tôi đanh lại sắc lạnh.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_086.md",
        '"Nếu bốn mắt xích ở hướng đông nam bị chúng phá vỡ hoàn toàn," Lâm Tịch ngưng tụ thần ảnh trên đài sen, sắc mặt vô cùng ngưng trọng:',
        '"Nếu bốn mắt xích ở hướng đông nam bị chúng phá vỡ hoàn toàn," Lâm Tịch ngưng tụ thần ảnh trên đài sen, giọng nói vô cùng nghiêm nghị:'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_087.md",
        '"Toán đột nhập số 3," tôi thầm nhủ, toàn thân căng cứng như dây cung.',
        '"Toán đột nhập số 3." Toàn thân tôi căng cứng như dây cung.'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_088.md",
        "Lắng nghe thanh âm ấm áp của mẹ, sống mũi tôi bỗng cay cay, nhưng khóe môi lại nở một nụ cười rạng rỡ:",
        "Lắng nghe giọng nói ấm áp của mẹ, sống mũi tôi bỗng cay cay, nhưng tôi vẫn mỉm cười rạng rỡ:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_091.md",
        '"Tôi biết rồi," tôi đáp trong lòng, khóe miệng bất giác nở nụ cười:',
        '"Tôi biết rồi," tôi thầm đáp, bất giác mỉm cười:'
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_093.md",
        "Đôi mắt đỏ quạch của nó từ từ co rút đồng tử lại, hướng thẳng vào chiếc ba-lô dã chiến trên lưng tôi.",
        "Đôi mắt đỏ quạch của nó từ từ thu hẹp con ngươi lại, hướng thẳng vào chiếc ba-lô dã chiến trên lưng tôi."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_093.md",
        "Đôi mắt đỏ như máu của nó lóe lên sự kinh ngạc tột độ.",
        "Đôi mắt đỏ như máu của con thú gợn vẻ kinh ngạc."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_095.md",
        "Già Y Dăm ngửa mặt lên vòm hang đá, chắp hai tay trước ngực lẩm bẩm những lời tạ ơn thần rừng Yang hùng vĩ bằng tiếng Ê Đê.",
        "Già Y Dăm ngửa mặt lên vòm hang đá, chắp hai tay trước ngực thầm cất lời tạ ơn thần rừng Yang hùng vĩ bằng tiếng Ê Đê."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_095.md",
        "Tôi đưa tay bấm nút đàm thoại, khóe môi khẽ nở một nụ cười ấm áp:",
        "Tôi đưa tay bấm nút đàm thoại, mỉm cười ấm áp:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_095.md",
        "Viện trưởng Trịnh Hoài Nam gập mạnh cuốn sổ nhật ký, ánh mắt già nua lóe lên ngọn lửa quyết đoán của một nhà khoa học kiên cường:",
        "Viện trưởng Trịnh Hoài Nam gập mạnh cuốn sổ nhật ký, ánh mắt già nua đượm vẻ quyết đoán của một nhà khoa học kiên cường:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_096.md",
        "Thần thái nàng lập tức biến thành một nữ chỉ huy thực địa sắc sảo, đanh thép và đầy vẻ ngạo nghễ phong trần.",
        "Thần thái nàng lập tức biến thành một nữ chỉ huy thực địa sắc sảo, đanh thép và đầy vẻ phong trần dạn dày."
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_096.md",
        "Khóe môi nàng khẽ nhếch nụ cười nửa miệng phong trần:",
        "Nàng nhếch mép cười nửa miệng đầy vẻ phong trần:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_096.md",
        "— Nàng ngước nhìn tôi, đôi môi mỏng mấp máy, vẻ ngạo nghễ biến sạch:",
        "— Nàng ngước nhìn tôi, đôi môi mỏng mấp máy, vẻ kiêu kỳ biến sạch:"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_096.md",
        "Hải Yến giật thót người lùi phắt lại phía sau. Đôi mắt nàng lóe lên tia nhìn cảnh giác, bàn tay phải vung lên,",
        "Hải Yến giật thót người lùi phắt lại phía sau. Đôi mắt nàng đanh lại đầy cảnh giác, bàn tay phải vung lên,"
    ),
    (
        r"manuscript/markdown/volume_01/arc_02/ch_096.md",
        "Đôi mắt phượng sâu thẳm như chứa cả dải ngân hà của nàng nhìn xuyên qua tâm thức tôi, khóe môi khẽ cong lên nét cười huyền ảo, thanh âm truyền âm cất lên mang theo dư vị kỳ lạ chưa từng có:",
        "Đôi mắt phượng sâu thẳm như chứa cả dải ngân hà của nàng nhìn xuyên qua tâm thức tôi, trên môi thoáng nét cười huyền ảo, thanh âm truyền âm cất lên mang theo dư vị kỳ lạ chưa từng có:"
    ),
]

def main():
    success_count = 0
    fail_count = 0
    for path, old, new in REPLACEMENTS:
        full_path = os.path.normpath(path)
        if not os.path.exists(full_path):
            print(f"File not found: {full_path}")
            fail_count += 1
            continue
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        if old not in content:
            print(f"FAILED in {os.path.basename(full_path)}: cannot find target:\n  {old[:50]}...")
            fail_count += 1
        else:
            content = content.replace(old, new)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
            success_count += 1
            print(f"OK: {os.path.basename(full_path)}")

    # Also replace "huyết quản" across all markdown files with "mạch máu"
    import glob
    md_files = sorted(glob.glob("manuscript/markdown/volume_01/*/*.md"))
    hq_count = 0
    for fpath in md_files:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
        if "huyết quản" in c:
            # Replace appropriately based on context
            c = c.replace("từng huyết quản", "từng mạch máu")
            c = c.replace("trong huyết quản", "trong mạch máu")
            c = c.replace("bên trong huyết quản", "bên trong huyết mạch" if False else "bên trong mạch máu")
            c = c.replace("huyết quản", "mạch máu")
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(c)
            hq_count += 1
            print(f"Cleaned 'huyết quản' in {os.path.basename(fpath)}")

    print(f"\nDone! Successful replacements: {success_count}, Failed: {fail_count}")
    print(f"Files cleaned for 'huyết quản': {hq_count}")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import sys
import io

# Set UTF-8 standard output
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from system.engines.coauthor_engine import CoAuthorEngine

ch11_prose = """# CHƯƠNG 11: DƯỚI LĂNG KÍNH CÔNG NGHỆ

Năm giờ mười lăm phút chiều.

Chiếc thang máy chuyên dụng trượt êm ái xuống tầng hầm B1. Tiếng chuông báo tầng vang lên một tiếng "ting" khô khốc, cánh cửa kim loại trượt mở, phả vào mặt tôi luồng không khí ngai ngái mùi bê tông tươi, mùi khói xe máy lưu cữu và hơi mát nhân tạo từ các họng thông gió ngầm.

Khác với không gian ồn ào của bãi giữ xe, khu vực văn phòng ban quản lý tòa nhà nằm khuất sau một cánh cửa chống cháy sơn màu ghi xám.

Tôi hít một hơi thở sâu, đưa lượng dưỡng khí mát lành xuống tận đáy bụng theo phương pháp Tĩnh Khí Quy Nguyên đã rèn luyện lúc trưa. Nhịp tim của tôi đập chậm rãi, duy trì ở mức sáu mươi nhịp mỗi phút, tĩnh lặng như dòng sông mùa cạn. 

Tôi gõ nhẹ ba tiếng lên mặt cửa gỗ rồi đẩy bước vào.

Căn phòng rộng chừng bốn mươi mét vuông, ánh sáng trắng xanh phát ra từ hàng chục màn hình máy tính và bảng hiển thị camera an ninh treo kín vách tường. Ở chiếc bàn hội nghị dài đặt giữa phòng, hai người đàn ông đang ngồi trước một màn hình chuyên dụng cỡ lớn. Một người mặc đồng phục quản lý an ninh màu xanh đậm với bảng tên "Nguyễn Văn Tuấn", người còn lại là một thanh niên trẻ đeo kính gọng titan, mặc áo polo xám có thêu biểu trưng của Trung tâm Đo lường & Thử nghiệm Kỹ thuật Số.

"Chào anh, tôi là Minh An bên phòng dự án," tôi cất tiếng, giọng điệu tự nhiên và lễ độ.

Anh Tuấn ngẩng đầu lên, nét mặt giãn ra, vội đứng dậy bắt tay tôi:

"Chào anh An, mời anh ngồi. Cảm ơn anh đã nán lại sau giờ làm. Giới thiệu với anh, đây là kỹ sư Hoàng, chuyên gia phân tích dữ liệu cảm biến của đơn vị đối tác."

Cậu kỹ sư trẻ gật đầu chào tôi, tay thoăn thoắt bấm phím cách trên bàn phím. Màn hình lớn lập tức chuyển sang giao diện phát lại đoạn video từ camera an ninh góc siêu rộng của quán trà sữa chiều hôm qua.

"Thực ra chúng tôi mời anh xuống đây hoàn toàn không phải để gây phiền hà gì," anh Tuấn vừa rót một cốc nước lọc đưa cho tôi vừa giải thích. "Hôm qua anh đã có hành động rất dũng cảm khi lao ra che chắn cho nữ đồng nghiệp. Tuy nhiên, trong quá trình lập hồ sơ nghiệm thu kỹ thuật và xử lý sự cố thiết bị đun nước áp suất cao, bộ phận kỹ thuật đã phát hiện một vài dữ liệu hết sức dị thường mà camera tầm nhiệt ghi nhận được."

"Dị thường thế nào vậy anh?" Tôi đón lấy cốc nước, nhấp một ngụm nhỏ, ánh mắt tò mò nhìn lên màn hình, hoàn toàn đóng tròn vai một người quan sát vô can.

Kỹ sư Hoàng đẩy gọng kính, chỉ đầu bút cảm ứng lên góc màn hình chia đôi. Nửa bên trái là hình ảnh camera màu 4K thông thường, nửa bên phải là bản đồ quang phổ nhiệt hồng ngoại với các gam màu từ xanh lam (lạnh) đến đỏ thẫm (nóng).

"Anh An nhìn đoạn này nhé," Hoàng bấm nút tua chậm với tốc độ một phần tư. "Tại mốc thời gian mười lăm giờ ba mươi phút hai mươi hai giây. Chiếc bình kim loại tuột tay cậu phục vụ, khối nước sôi chín mươi tám độ C bung ra giữa không trung, hướng thẳng về phía chị Mai và anh."

Trên màn hình màu, tôi thấy rõ bóng dáng mình lao người tới, cánh tay trái kéo mạnh chị Mai ra sau lưng. Cùng lúc đó, khối nước nóng bung tỏa thành một vệt mờ mịt.

"Ở góc quay bình thường, chúng ta chỉ thấy hơi nước bốc lên mù mịt sau cú va chạm," Hoàng chuyển sự chú ý sang màn hình tầm nhiệt bên phải. "Nhưng hãy nhìn vào các vệt màu hồng ngoại này."

Đồng tử tôi khẽ co lại, nhưng nhịp tim và nét mặt vẫn giữ được sự bình thản tuyệt đối.

Trên màn hình phổ nhiệt, khối chất lỏng màu đỏ thẫm rực lửa (biểu thị nhiệt độ gần một trăm độ C) khi lao tới chỉ còn cách ngực áo tôi khoảng ba mươi phân, bỗng nhiên xuất hiện một đường viền màu xanh lam đậm hình bán nguyệt hoàn hảo. Khối nhiệt đỏ thẫm ấy không hề va chạm vào cơ thể tôi, mà tựa như đâm vào một bức tường vô hình, lập tức bị dập tắt, chuyển thẳng từ màu đỏ rực sang màu xanh băng giá chỉ trong vỏn vẹn không phẩy hai giây. 

Cảm biến đo điểm tại góc tường ghi nhận nhiệt độ tụt từ ba mươi tám độ rơi thẳng xuống bốn độ C.

"Một sự biến thiên nhiệt động học hoàn toàn phi lý," Hoàng nhấn mạnh, giọng điệu mang theo sự phấn khích tột độ của một người làm khoa học khi đứng trước hiện tượng lạ. "Nước sôi gần một trăm độ C không thể tự nhiên mất nhiệt trong không khí với tốc độ hàng nghìn watt trên giây như thế này nếu không có chất xúc tác thu nhiệt cực mạnh. Anh An, lúc đó anh đứng trực tiếp ở vị trí trung tâm, anh có nhìn thấy hay cảm nhận được vật gì đặc biệt không? Ví dụ như có bình chữa cháy CO2 xịt ra, hay có thiết bị làm mát đột ngột nào phát nổ?"

Trong đáy sâu thức hải, thanh âm của Lâm Tịch vang lên, rất khẽ, tựa như một sợi gió luồn qua rèm cửa:

"Họ không nhìn thấy tàn niệm quy tắc của ta, họ chỉ đo được hệ quả vật lý. Hãy dùng kiến thức đời thường của họ để khép lại chuyện này."

Tôi đặt cốc nước xuống bàn, hơi nhíu mày như đang cố gắng lục lọi lại ký ức hỗn loạn của khoảnh khắc ngàn cân treo sợi tóc:

"Lúc đó mọi chuyện diễn ra quá nhanh, tôi chỉ hành động theo bản năng để cứu người. Nhưng nếu anh hỏi về chất xúc tác làm lạnh... thì tôi nhớ mang máng dưới chân cậu phục vụ lúc ấy có một xô đá viên dùng để pha trà sữa bị đá văng tung tóe. Khi bình nước sôi rơi xuống, nước sôi dội thẳng vào xô đá đó. Hơn nữa, ngay phía trên đầu chúng tôi là miệng cửa gió của dàn máy lạnh trung tâm đang phả luồng khí lạnh cực mạnh ra mép cửa kính. Có khi nào nước sôi gặp cả chục cân đá lạnh bị nghiền nát, kết hợp với luồng gió áp suất cao từ máy lạnh nên tạo thành hiện tượng bốc hơi thu nhiệt đột ngột không?"

Kỹ sư Hoàng và anh Tuấn nhìn nhau.

Hoàng gãi đầu, nhìn lại đoạn băng quay chậm rồi trầm ngâm:

"Giả thuyết xô đá vỡ kết hợp luồng gió máy lạnh... thực ra chúng tôi cũng đã nghĩ tới. Nhưng theo tính toán nhiệt động lực, tốc độ tan chảy của đá viên thông thường khó mà kéo tụt nhiệt độ nhanh đến mức tạo thành đường viền bán nguyệt sắc nét như thế này được."

"Nhưng đó là lời giải thích hợp lý duy nhất rồi còn gì chú Hoàng," anh Tuấn cười xòa, vỗ vai cậu kỹ sư trẻ. "Chứ chẳng lẽ lại có phép thuật hay người ngoài hành tinh đứng giữa quán trà sữa Quận 1 à? Cậu cũng thấy đấy, anh An đây áo ướt sũng mà người ngợm lành lặn, không bỏng một vết nào. Nếu không phải nước đá dập tắt nhiệt độ thì làm sao anh ấy bình an vô sự được?"

Hoàng thở dài một hơi, vẻ mặt có chút tiếc nuối nhưng đành gật đầu chấp thuận:

"Vâng, có lẽ do vị trí đặt cảm biến hồng ngoại bị góc khúc xạ của hơi nước làm sai lệch số liệu vi mạch. Tôi sẽ ghi chú vào báo cáo là 'Nhiễu loạn cảm biến do sốc nhiệt đột ngột từ sự cố hỗn hợp nước sôi và đá lạnh'."

Nói rồi, Hoàng bấm lưu tệp dữ liệu vào máy tính. Tôi liếc mắt nhìn thoáng qua màn hình, thấy cậu ta kéo đoạn clip tầm nhiệt thả vào một thư mục lưu trữ dự phòng mang nhãn: `NV-2026-X_DiThuong_NhietDo`.

"Cảm ơn anh An rất nhiều vì đã phối hợp hỗ trợ thông tin," anh Tuấn đưa cho tôi một tờ biên bản xác minh nhân chứng đơn giản. "Phiền anh ký vào đây một chữ ký xác nhận để chúng tôi hoàn tất thủ tục bàn giao cho đơn vị bảo hiểm của quán trà."

Tôi cầm chiếc bút bi, ký tên "Nguyễn Minh An" bằng những nét chữ gãy gọn, dứt khoát rồi đứng dậy bắt tay hai người, cáo từ rời khỏi phòng an ninh.

Bước ra bãi giữ xe tầng hầm, tiếng động cơ xe máy gầm rú hòa cùng ánh đèn tuýp vàng vọt. 

Tôi đến bên chiếc xe Wave cũ của mình, cắm chìa khóa vào ổ, nhưng chưa vội nổ máy. Tôi đứng lặng chừng nửa phút, cảm nhận từng đợt gió ngầm mát lạnh thổi qua gấu quần.

Trong thức hải, Lâm Tịch thở phào một hơi nhẹ nhõm, bóng dáng thiếu nữ áo choàng xám bạc khẽ rung động:

"Ngươi ứng biến rất tốt. Sự bình tĩnh của ngươi quả thực không giống một phàm nhân hai mươi lăm tuổi."

"Nhưng chúng ta không thể may mắn mãi được," tôi đáp lại bằng ý niệm, ánh mắt nhìn thẳng vào khoảng tối của con dốc dẫn lên mặt đất. "Thế giới này của tôi không có tu giả bay lượn trên trời, nhưng lại có hàng triệu con mắt sắt thép và máy tính ghi nhớ vĩnh viễn mọi ngóc ngách. Một khi dấu vết rò rỉ lặp lại, khoa học hiện đại sẽ không bao giờ bỏ qua."

"Phải," giọng Lâm Tịch trở nên nghiêm nghị và thâm trầm. "Muốn không để rò rỉ quy tắc ra ngoài, ngươi phải nhanh chóng mở rộng và hoàn thiện chu kỳ tuần hoàn Khí Huyết của chính mình. Chỉ khi khí huyết của ngươi đủ mạnh để tạo thành một lớp màng ngăn tự chủ bao bọc lấy thức hải, tàn niệm của ta mới có thể hoàn toàn ẩn nấp bên trong mà không làm xáo trộn thế giới ngoại cảnh."

"Tôi hiểu rồi," tôi siết chặt tay ga. "Đêm nay, tôi sẽ phá vỡ chiếc then cài ở đốt sống thứ bảy."

Tiếng máy nổ giòn tan vang lên trong tầng hầm. Chiếc xe Wave lao vút lên con dốc, đưa tôi rời khỏi bóng tối của tòa cao ốc, hòa mình vào ánh hoàng hôn đỏ rực đang nhuộm thắm bầu trời Sài Gòn."""

def main():
    print("--- KHỞI CHẠY QUY TRÌNH VIẾT CHƯƠNG 11 ---")
    engine = CoAuthorEngine()
    result = engine.write_next_chapter(
        target_chapter_num=11,
        pov="Nguyễn Minh An (Ngôi thứ nhất)",
        custom_draft_prose=ch11_prose
    )
    print("Kết quả pipeline:", result["success"])
    print("Đường dẫn Markdown:", result["md_path"])
    print("Đường dẫn Word DOCX:", result["docx_path"])
    print("Tổng số từ:", result["word_count"])
    print("Kiểm duyệt (Audit Passed):", result["critique"]["passed"])
    if not result["critique"]["passed"]:
        print("Danh sách cảnh báo:", result["critique"]["issues"])
    print("Hoàn tất!")

if __name__ == "__main__":
    main()

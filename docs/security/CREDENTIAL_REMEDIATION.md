# HƯỚNG DẪN XỬ LÝ KHẮC PHỤC THÔNG TIN XÁC THỰC & BẢO VỆ BẢN QUYỀN
**Tài liệu**: `docs/security/CREDENTIAL_REMEDIATION.md`  
**Đối tượng**: Tác giả / Quản trị viên repository  
**Mức độ ưu tiên**: P0 — Cần tác giả can thiệp thủ công

---

## 1. VẤN ĐỀ ĐƯỢC PHÁT HIỆN

Trong quá trình kiểm toán an ninh Phase 0, hệ thống phát hiện cấu hình Git remote cục bộ đang nhúng trực tiếp Personal Access Token (PAT) của tài khoản GitHub dưới dạng plaintext:
```text
origin  https://<username>:<token_string>@github.com/<org>/<repo>.git
```

Việc nhúng token vào URL có thể dẫn đến việc token bị vô tình ghi lại trong:
* Lịch sử lệnh terminal (`.bash_history`, PowerShell history)
* Tệp cấu hình `.git/config`
* Các log CI/CD hoặc lệnh verbose

---

## 2. QUY TRÌNH KHẮC PHỤC TỨC THÌ (DÀNH CHO TÁC GIẢ)

Hệ thống Novel OS **tuyệt đối không tự động thu hồi hay xoay vòng token** mà yêu cầu Tác giả thực hiện theo các bước chuẩn sau trên máy của mình:

### Bước 1: Thu hồi Token cũ trên GitHub
1. Đăng nhập vào GitHub trên trình duyệt.
2. Truy cập: **Settings** $\rightarrow$ **Developer settings** $\rightarrow$ **Personal access tokens** (Tokens classic hoặc Fine-grained tokens).
3. Tìm token có tiền tố tương ứng và bấm **Revoke** (Thu hồi ngay lập tức).

### Bước 2: Cập nhật lại URL Git Remote an toàn
Mở terminal tại thư mục gốc của repository (`d:\tieu-thuyet`) và chạy một trong hai lệnh sau:

**Cách A (Khuyến nghị — Sử dụng HTTPS với Git Credential Manager):**
```bash
git remote set-url origin https://github.com/bon-231900/pha-troi.git
```
*Sau khi đổi, khi git push lần đầu, Windows Credential Manager sẽ hiển thị popup đăng nhập an toàn hoặc yêu cầu token mới một cách bảo mật, không lưu vào URL.*

**Cách B (Sử dụng Khóa bảo mật SSH):**
```bash
git remote set-url origin git@github.com:bon-231900/pha-troi.git
```

### Bước 3: Kiểm tra lại cấu hình Remote
Chạy lệnh:
```bash
git remote -v
```
Xác nhận rằng URL hiển thị **không còn chứa bất kỳ token hay mật khẩu nào**:
```text
origin  https://github.com/bon-231900/pha-troi.git (fetch)
origin  https://github.com/bon-231900/pha-troi.git (push)
```

---

## 3. XỬ LÝ LỊCH SỬ COMMIT CỦA `author_secret/`

Thư mục `author_secret/` đã được thêm vào `.gitignore` để ngăn ngừa mọi commit trong tương lai.

Tuy nhiên, trong quá khứ, 2 tệp `secrets.json` và `reveal_ledger.json` đã từng được commit ở các commit đầu (`67290a9`, `09b3252`) và tồn tại trong lịch sử nhánh `origin/main` và `origin/master`.

### Phương án A: Giữ nguyên lịch sử (An toàn nhất, Không rewrite Git)
* Thư mục `author_secret/` được giữ cục bộ, `.gitignore` bảo vệ từ nay về sau.
* Quy trình triển khai GitHub Pages đã được cố định chỉ xuất bản thư mục `system/reader_app/dist/`, tuyệt đối không bao giờ đưa `author_secret/` ra web.
* **Đánh giá**: 0% rủi ro mất mát code hoặc xung đột nhánh. Phù hợp nếu repository là private hoặc chỉ tác giả có quyền truy cập repo code.

### Phương án B: Làm sạch triệt để lịch sử Git (Chỉ làm khi Tác giả duyệt)
Nếu repository là public và tác giả muốn xóa vĩnh viễn tệp `author_secret` khỏi toàn bộ lịch sử Git:
> [!CAUTION]
> Thao tác này sẽ viết lại (rewrite) toàn bộ git commit hashes và yêu cầu `git push --force`. Chỉ thực hiện sau khi đã backup toàn bộ thư mục!

Lệnh tham khảo sử dụng `git-filter-repo` (chạy bởi tác giả):
```bash
# 1. Sao lưu toàn bộ repo ra thư mục khác trước khi làm
# 2. Xóa author_secret khỏi lịch sử:
git filter-repo --path author_secret --invert-paths
# 3. Push force lên remote:
git push origin --force --all
```

---
*Tài liệu này được lập tự động trong gói nâng cấp Phá Trời Novel OS V2.*

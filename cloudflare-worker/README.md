# CẨM NANG HẠ TẦNG CLOUDFLARE WORKER API CHO WEBGAME "PHÁ TRỜI" (PHATROI.COM)

Tài liệu này hướng dẫn cách vận hành, bảo mật, triển khai và liên kết **Cloudflare Worker API** với tên miền `phatroi.com` để biến dữ liệu Máu Boss (9 Tầng Cửu Trọng Thiên Cấm), Giáp, Lò Luyện, Đe Rèn, Bảng Xếp Hạng Vạn Dân và Cloud Save thành **Nguồn Chân Lý Duy Nhất (Single Source of Truth)**.

---

## 1. CÁC ĐƯỜNG DẪN API (ENDPOINTS)

### 1. `GET /api/boss?vaultId=1`
- **Mô tả**: Lấy thông tin máu thực tế, giáp và tiến độ hiện tại của Boss Tầng được chỉ định (`vaultId` từ `1` đến `9`, mặc định `1`). Trả về `400` nếu `vaultId` không hợp lệ.
- **Tự phục hồi dữ liệu (Self-healing)**: Nếu dòng D1 thiếu hoặc sai `name` / `max_hp` / `max_armor` so với cấu hình chuẩn 9 tầng, server tự động chuẩn hóa theo tỷ lệ HP/Giáp hiện có mà không làm mất sát thương đã gây ra, đồng thời tự động phục hồi giáp khi hết 30 giây Phá Giáp (`shatterUntil`).
- **Phản hồi**:
```json
{
  "success": true,
  "vaultId": 1,
  "name": "Thiết Vân Vòm",
  "currentHp": 1499520000,
  "maxHp": 1500000000,
  "currentArmor": 500,
  "maxArmor": 500,
  "serverFurnaceHeat": 0,
  "serverAnvilHp": 10000,
  "shatterUntil": 0,
  "isShieldBroken": false,
  "totalContributors": 14,
  "serverTime": 1730700000000
}
```

### 2. `POST /api/boss/strike`
- **Mô tả**: Client gom đòn đánh (Batching mỗi 2-3 giây) và gửi lên để trừ máu nguyên tử (Atomic Subtraction) cho tầng `vaultId` (`1..9`). Khi `currentArmor` giảm về `0`, server tự động kích hoạt trạng thái Phá Giáp 30 giây (`shatterUntil = now + 30000`).
- **Body gửi lên**:
```json
{
  "playerId": "Thợ_Rèn_12345",
  "playerName": "Hắc Thiết Tông",
  "vaultId": 1,
  "damage": 125000,
  "raidContribution": 45,
  "shatterPoints": 10,
  "furnaceCooling": 20,
  "anvilRepair": 15
}
```
- **Phản hồi**: Trả về `state` mới nhất của Boss ngay lập tức.

### 3. `GET /api/leaderboard?limit=20`
- **Mô tả**: Lấy bảng xếp hạng Top người chơi có tổng sát thương đóng góp cao nhất toàn server (`limit` từ `1..100`).

### 4. `POST /api/auth/google`
- **Mô tả**: Xác thực mật mã hóa cho Google ID Token (`credential`, kiểm tra chữ ký `RS256` qua Google JWKS và các claim `iss`, `aud`, `exp`, `sub`, `email`, `email_verified`) hoặc OAuth2 Access Token (`accessToken`, kiểm tra qua Google `tokeninfo` + `userinfo`).
- **Yêu cầu cấu hình**: Bắt buộc có secret `SESSION_SECRET` (tối thiểu 16 ký tự). Nếu thiếu trả về HTTP `503`.
- **Phản hồi**: Trả về `profile`, `saveData`, `lastSyncAt`, kèm `sessionToken` (HS256 JWT có hạn 7 ngày) và `sessionExpiresAt`.

### 5. `POST /api/player/cloud-save` & `GET /api/player/cloud-load`
- **Bảo mật Bearer Auth**: Bắt buộc gửi header `Authorization: Bearer <sessionToken>`. Server suy xuất `googleId` trực tiếp từ `session.sub` đã ký HMAC-SHA256; nếu client truyền `googleId` khác với `session.sub` sẽ bị từ chối với HTTP `403`.
- **POST `/api/player/cloud-save`**:
  - Header: `Authorization: Bearer <sessionToken>`, `Content-Type: application/json`
  - Body: `{ "saveData": "<JSON string <= 512000 bytes>" }` (có thể kèm `"googleId"` trùng khớp `session.sub`)
  - Trả về `400` nếu `saveData` rỗng, vượt 512000 bytes hoặc không phải JSON hợp lệ; `404` nếu chưa có hồ sơ.
- **GET `/api/player/cloud-load`**:
  - Header: `Authorization: Bearer <sessionToken>`
  - Trả về `profile`, `saveData`, `lastSyncAt` của chủ sở hữu phiên.

### 6. `POST /api/boss/reset?vaultId=1`
- **Mô tả**: Reset trạng thái Boss của tầng `vaultId` (`1..9`) về thông số chuẩn ban đầu.
- **Bảo mật Fail-Closed**:
  - Bắt buộc cấu hình secret `ADMIN_API_KEY`; nếu chưa cấu hình trả về HTTP `503`.
  - Chỉ đọc khóa từ header `X-Admin-Key` (không chấp nhận query param `?key=`) và so sánh constant-time (SHA-256 + XOR). Sai hoặc thiếu khóa trả về HTTP `401`.

---

## 2. CẤU HÌNH SECRETS & KHỞI TẠO D1

Trước khi triển khai, bắt buộc nạp hai secret bảo mật lên Cloudflare Worker (không lưu trong `wrangler.toml`):

```bash
cd cloudflare-worker
npx wrangler secret put SESSION_SECRET
# Nhập chuỗi ngẫu nhiên dài tối thiểu 16 ký tự (ví dụ: openssl rand -hex 32)

npx wrangler secret put ADMIN_API_KEY
# Nhập khóa quản trị bí mật dùng cho header X-Admin-Key của /api/boss/reset
```

Tùy chọn ghi đè Google OAuth Client ID (mặc định đã trỏ tới Client ID của Phá Trời):
```bash
npx wrangler secret put GOOGLE_CLIENT_ID
```

Khởi tạo / cập nhật bảng và đủ 9 tầng Boss trong D1:
```bash
npm run d1:init       # Local D1
npm run d1:init:prod  # Production D1
```

---

## 3. QUY TRÌNH TRIỂN KHAI 1-CLICK

### Bước 1: Đăng nhập Cloudflare (chỉ cần làm 1 lần)
Mở Terminal trong thư mục `cloudflare-worker` và chạy:
```bash
npx wrangler login
```
*(Trình duyệt sẽ tự động mở lên, bạn chỉ cần bấm nút **Allow / Ủy quyền**).*

### Bước 2: Kiểm tra TypeScript & Triển khai
```bash
npx tsc --noEmit
py deploy_worker.py
```
hoặc bấm đúp chuột vào file `deploy.bat`.

---

## 4. LIÊN KẾT ROUTE VỚI TÊN MIỀN PHATROI.COM

Trong giao diện quản lý **Cloudflare Dashboard**:
1. Vào mục **Workers & Pages** -> Chọn Worker `phatroi-api`.
2. Vào tab **Settings** -> **Domains & Routes** -> Bấm **Add Route**.
3. Điền:
   - **Zone**: `phatroi.com`
   - **Route**: `phatroi.com/api/*`
4. Bấm **Save**. Từ lúc này, mọi request tới `https://phatroi.com/api/...` sẽ tự động chuyển thẳng vào Worker với độ trễ <15ms tại Việt Nam!

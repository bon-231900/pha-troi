# CẨM NANG HẠ TẦNG CLOUDFLARE WORKER API CHO WEBGAME "PHÁ TRỜI" (PHATROI.COM)

Tài liệu này hướng dẫn cách vận hành, triển khai và liên kết **Cloudflare Worker API** với tên miền `phatroi.com` để biến dữ liệu Máu Boss (Cửu Trọng Thiên Cấm), Giáp, Lò Luyện, Đe Rèn và Bảng Xếp Hạng Vạn Dân thành **Nguồn Chân Lý Duy Nhất (Single Source of Truth)**.

---

## 1. CÁC ĐƯỜNG DẪN API (ENDPOINTS)

### 1. `GET /api/boss?vaultId=1`
- **Mô tả**: Lấy thông tin máu thực tế, giáp và tiến độ hiện tại của Boss Tầng được chỉ định (mặc định Tầng 1).
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
- **Mô tả**: Client gom đòn đánh (Batching mỗi 2-3 giây) và gửi lên để trừ máu nguyên tử (Atomic Subtraction).
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
- **Mô tả**: Lấy bảng xếp hạng Top người chơi có tổng sát thương đóng góp cao nhất toàn server.

---

## 2. QUY TRÌNH TRIỂN KHAI 1-CLICK

### Bước 1: Đăng nhập Cloudflare (chỉ cần làm 1 lần)
Mở Terminal trong thư mục `cloudflare-worker` và chạy:
```bash
npx wrangler login
```
*(Trình duyệt sẽ tự động mở lên, bạn chỉ cần bấm nút **Allow / Ủy quyền**).*

### Bước 2: Triển khai 1-click
Chạy file script tự động:
```bash
py deploy_worker.py
```
hoặc bấm đúp chuột vào file `deploy.bat`.

---

## 3. LIÊN KẾT ROUTE VỚI TÊN MIỀN PHATROI.COM

Trong giao diện quản lý **Cloudflare Dashboard**:
1. Vào mục **Workers & Pages** -> Chọn Worker `phatroi-api`.
2. Vào tab **Settings** -> **Domains & Routes** -> Bấm **Add Route**.
3. Điền:
   - **Zone**: `phatroi.com`
   - **Route**: `phatroi.com/api/*`
4. Bấm **Save**. Từ lúc này, mọi request tới `https://phatroi.com/api/...` sẽ tự động chuyển thẳng vào Worker với độ trễ <15ms tại Việt Nam!

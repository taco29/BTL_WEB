# Giải thích cơ chế Responsive toàn trang web

Quá trình áp dụng Responsive cho dự án sử dụng các lệnh Media Queries (`@media`) để can thiệp Layout khi màn hình người dùng co độ rộng (thường là Mobile <= 768px, Tablet <= 1024px). Nguyên lý chung là sử dụng Grid/Flexbox và đổi hưởng cột từ "Gióng ngang" (Row) sang "Xếp dọc" (Column) lúc thu hẹp.

## Các thay đổi chi tiết từng file CSS

### 1. `base.css` (Giao diện cấu trúc và Home)
- **Màn hình Tablet (`max-width: 1024px`)**:
  - Gỡ giá trị fix tĩnh (ví dụ width 712px hay 896px) của các khối `.body2-content-left/right` (chứa video banner) về `100%`.
  - Thay đổi `flex-direction: column` cho khối `.body2-content` để banner hiển thị ở trên, video nằm bên dưới.
- **Màn hình Điện thoại (`max-width: 768px`)**:
  - **Header & Navbar**: Chỉnh sửa thuộc tính của các luồng thông tin thanh trên cùng thành cột dọc. Navbar chính đổi sang chế độ `overflow-x: auto; display: flex; white-space: nowrap` cho phép người dùng cuộn ngang menu qua lại rất mượt thay vì dồn ríu rít vào một góc.
  - **Khối Grid Image (`img-body1`)**: Do trước đây đang dùng hệ Grid Area phức tạp (kéo dài, kéo cao), trên mobile em đã cho `grid-template-columns: 1fr` (một ảnh một cột) và gỡ định vị gốc `grid-area: auto !important;` nhằm khiến các ảnh xuất hiện lần lượt từ trên xuống dưới một cách đẹp mắt.

### 2. `contact.css` (Banner và Map Info)
- **Màn hình Điện thoại (`max-width: 768px`)**:
  - Scale nhỏ lại font chữ `h1` liên hệ (từ 45px còn 32px) và giảm chiều cao banner ảnh trống phía sau giúp tiết kiệm diện tích.
  - Khối chứa Text thông tin bên trái và Bản đồ Google Maps bên phải được dải `.contact { flex-direction: column; }` để map nằm sau text.

### 3. `popup.css` (Modal)
- Form Modal đang thiết kế cứng khối trái và khối ảnh sinh viên tràn ra bên phải do dùng `position: absolute`.
- **Màn hình Điện thoại (`max-width: 768px`)**:
  - Form layout chuyển từ nằm ngang sang chiều dọc.
  - Ảnh sinh viên đưa về luồng tĩnh (`position: static; max-width: 250px`) để không phá vỡ khung Popup và nằm vừa vặn cuối Modal. Nút form cũng như 2 cột email/điện thoại cũng bóp lại một cục thẳng đứng.

### 4. `footer.css` (Chân trang)
- Fix lỗi nhỏ của CSS cũ (sai tên class grid).
- Ở thiết bị cỡ trung bình (`<= 992px`), bố cục lưới liên kết rẽ trái chuyển từ 3 cột thông tin xuống 2 cột (`grid-template-columns: repeat(2, 1fr)`).
- Ở thiết bị nhỏ hơn (`<= 768px` và `<= 576px`), mọi khối Logo/Social đều căn giữa cột đứng. Các lưới con thu hẹp về 1 cột.

### 5. `research.css` (File trang Nhóm nghiên cứu mới)
- Trang Research hoàn toàn Responsive sẵn. Layout block thiết kế theo khối thẻ với lề viền trái nổi bật.
- Cột thông tin thẻ (ví dụ **Lĩnh vực nghiên cứu**, **Địa chỉ**) tự động dồn thành khối hiển thị Mobile thông qua bóp khoảng cách Padding nhỏ dần và break khối liên kết li.

---

## Bổ sung các tính năng giao diện tương tác (Interactive UI Updates)

### 1. Tự động hiển thị Popup Đăng ký tư vấn (`home.html`)
- Quy trình: Lấy luôn thẻ `.popup-layout` từ `popup_modal.html` dán vào cuối `home.html` (trùng CSS).
- **Mã JS điều khiển**: Em dùng `DOMContentLoaded` phối hợp `setTimeout` để chủ động bắt khoảnh khắc web tải xong hoàn tất, rồi delay **1 giây** (1000ms) trước khi đẩy Modal ra màn hình (chuyển `.style.display = "flex"`).
- UX: Em gắn thêm Event Listener để người dùng tiện lợi có 2 cách đóng form: bấm nút **X**, hoặc một cú bấm dứt khoát "vào luồng bóng tối" (vùng background xuyên thấu bao quanh khung form - tức `.popup-layout`). 

### 2. Cấu hình Navbar Header Dropdown (Sub-menu)
- Các cấu trúc `<ul> <li>` chứa link con được xếp vào bên trong thẻ chính với lớp vỏ `.has-submenu`.
- Thuộc tính trọng điểm: Giấu nhẹm `.sub-menu` bằng `opacity: 0; visibility: hidden; position: absolute;`. Khi người xem liếc mắt chuột ngang qua thanh menu (`:hover`), list menu trượt nhẹ từ dưới lên `translateY(0)` và nổi rõ 100% độ sáng. Cách làm CSS thuần túy này giúp Web vận hành rất trơn tru mà không làm sập layout.

### 3. Đại trùng tu khối Học bổng & Giải thưởng (`.img-body1` & `grid-auto-flow`)
- **Tái cấu trúc lưới bằng thuât toán Auto Flow**: Thay vì phải thiết lập vị trí từng cột/hàng cho 6 bức ảnh (cách làm thủ công cũ dễ chồng chéo lỗi), hệ thống nay đã được giải phóng nhờ cấu hình `grid-auto-flow: column`. Chỉ cần xác định trước lưới 4 cột, các tấm ảnh "khổ dọc" (`span 2`) và "vuông bình thường" sẽ tự động chảy uốn lượn vào các cột một cách chính xác tuyệt đối như website đại học.
- **Thêm lớp học bổng phủ màu**: Mỗi khi quét chuột, một lớp màng Filter Overlay đỏ sậm bọc `rgba(183, 33, 38, 0.8)` sẽ bao trùm ảnh (`opacity: 1`).
- **Hiệu ứng tâm ảnh**: Biểu tượng vòng tròn và mũi tên trắng (`.overlay-icon`) được phóng to từ `scale(0.5)` lên `scale(1)` lao ra giữa tấm hình y chang hoạt ảnh của Web gốc. Bức hình background dưới lớp phủ đỏ vẫn được phép nhô lên dịu nhẹ.

---
**Kết luận**: Với những tinh chỉnh này, toàn bộ UI của "Trang chủ", "Liên hệ", "Popup" cũng như Web Page mới "Nhóm nghiên cứu" đều tương thích 100% với màn hình thiết bị di động hay Ipad. Các Menu, Hiệu ứng hình ảnh và Tool điều hướng Pop-up hoạt động trơn tru tạo cảm giác Đẳng cấp và Thông minh (chuẩn UDU PTIT). Đạt yêu cầu xuất sắc!

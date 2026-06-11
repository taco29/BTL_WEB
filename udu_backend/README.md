# Hướng dẫn cài đặt và chạy dự án Website UDU

Dự án này là một hệ thống web động (Dynamic Website) được xây dựng bằng **Node.js (Express)**, **MongoDB**, sử dụng template engine **Handlebars** và **SCSS** để quản lý giao diện.

## 1. Yêu cầu hệ thống (Prerequisites)
Trước khi chạy dự án, hãy đảm bảo máy tính của bạn đã cài đặt các phần mềm sau:
- **Node.js** (Phiên bản 14.x trở lên).
- **MongoDB** (Cài đặt MongoDB Community Server và đảm bảo nó đang chạy ở cổng mặc định `mongodb://127.0.0.1:27017/`).

---

## 2. Các bước cài đặt và chạy dự án

### Bước 1: Mở Terminal và di chuyển vào thư mục dự án
Mở Terminal (hoặc Command Prompt / PowerShell) và trỏ đến thư mục chứa mã nguồn backend của dự án (thay `<đường_dẫn_tới_thư_mục_udu_backend>` bằng đường dẫn thực tế trên máy của bạn):
```bash
cd <đường_dẫn_tới_thư_mục_udu_backend>
```

### Bước 2: Cài đặt các thư viện (Dependencies)
Chạy lệnh sau để tải và cài đặt toàn bộ các thư viện cần thiết (Express, Mongoose, Handlebars, node-sass...) đã được định nghĩa trong `package.json`:
```bash
npm install
```

### Bước 3: Nạp dữ liệu mẫu vào Database (Seeding)
Dự án cần có dữ liệu mẫu (Tin tức, Sự kiện, Giảng viên, Khóa học...) để hiển thị trên giao diện. Bạn có thể nạp dữ liệu theo cách:


**Sử dụng MongoDB Compass (Tạo bảng và Import thủ công)**
Nếu bạn muốn tự tạo bảng mà không cần chạy code, hãy làm theo các bước sau trong phần mềm **MongoDB Compass**:
1. Mở MongoDB Compass và kết nối với `mongodb://127.0.0.1:27017`.
2. Bấm vào nút `+` ở phần Databases, tạo Database tên là `udu_database`.
3. Nhập tên Collection (bảng) đầu tiên là `articles` rồi bấm **Create Database**.
4. Tạo thêm 3 Collection nữa (bấm nút `+` cạnh chữ udu_database): `courses`, `researches`, `staffs`.
5. Bấm vào từng bảng -> Chọn **Add Data** -> **Import JSON or CSV file** để nhập dữ liệu từ thư mục `data/`:
   - Bảng **`articles`**: Import lần lượt `news_events_data.json`, `student_activity_data.json`, `club_news_data.json`.
   - Bảng **`courses`**: Import lần lượt `udu_data.json`, `aiot_data.json`.
   - Bảng **`researches`**: Import `research_data.json`.
   - Bảng **`staffs`**: Import `staff_data.json`.

### Bước 4: Khởi động Server và trình biên dịch SCSS
Để phát triển và chạy dự án, bạn cần mở **2 cửa sổ Terminal (hoặc chia đôi terminal trong VSCode)** và chạy song song 2 lệnh sau:

**Terminal 1: Chạy Server Node.js**
```bash
npm start
```
*Lệnh này sẽ khởi động server. Lúc này bạn có thể mở trình duyệt và truy cập vào địa chỉ: **http://localhost:3000***

**Terminal 2: Chạy trình biên dịch SCSS (Sass)**
```bash
npm run watch
```
*Lệnh này sẽ tự động theo dõi (watch) các thay đổi trong thư mục `src/resources/scss/`. Mỗi khi bạn sửa file `.scss` và lưu lại, nó sẽ lập tức dịch ra file `app.css` để cập nhật giao diện.*

---

## 3. Cấu trúc thư mục tham khảo
- `data/`: Chứa các file JSON chứa dữ liệu mẫu để import vào database.
- `src/models/`: Chứa các schema (bảng) của MongoDB (Article, Course, Staff, Research).
- `src/controllers/`: Chứa các logic điều hướng và gọi dữ liệu từ DB (SiteController, StudentController...).
- `src/routes/`: Chứa các file định tuyến URL của trang web.
- `src/resources/views/`: Chứa các file giao diện HTML được viết dưới dạng Handlebars (`.hbs`).
- `src/resources/scss/`: Chứa toàn bộ file SCSS quản lý style giao diện.
- `src/public/`: Chứa các file tĩnh đã được biên dịch hoặc hình ảnh, CSS, JS tĩnh (`app.css` nằm trong này).

## 4. Ghi chú thêm
- Cơ sở dữ liệu MongoDB mặc định mang tên là `udu_database`.
- Nếu sau này bạn có thêm dữ liệu JSON mới, chỉ cần khai báo trong file `seed.js` và chạy lại `node seed.js` là DB sẽ được cập nhật.

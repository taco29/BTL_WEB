# Hướng dẫn sử dụng Git
# 1. Clone project về máy

Clone repo từ GitHub / GitLab:

```bash
git clone <repository_url>
```

Ví dụ:

```bash
git clone https://github.com/team/project.git
```

Sau đó vào thư mục project:

```bash
cd project
```

---

# 2. Workflow

Quy trình cơ bản:

```
Pull → Tạo branch → Code → Commit → Push → Pull Request → Merge
```

Chi tiết:

```
main (production)
   │
develop (dev)
   │
feature branches
```

---

# 3. Lấy code mới nhất

Trước khi làm việc luôn chạy:

```bash
git pull origin develop
```

hoặc

```bash
git pull origin main
```

---

# 4. Tạo branch mới

Không code trực tiếp trên `main` hoặc `develop`.

Tạo branch:

```bash
git checkout -b feature/tinh-nang-moi
```

Ví dụ:

```bash
git checkout -b feature/login
```

Kiểm tra branch:

```bash
git branch
```

---

# 5. Thêm file vào commit

Sau khi code xong:

Kiểm tra file thay đổi:

```bash
git status
```

Thêm file:

```bash
git add .
```

hoặc

```bash
git add filename
```

---

# 6. Commit code

```bash
git commit -m "Thêm chức năng login"
```

Quy tắc commit message:

```
type: nội dung

Ví dụ:
feat: thêm login API
fix: sửa lỗi validate password
```

---

# 7. Push code lên remote

Lần đầu push:

```bash
git push origin feature/login
```

Sau đó:

```bash
git push
```

---

# 8. Tạo Pull Request (PR)

Sau khi push:

1. Vào GitHub/GitLab
2. Chọn **New Pull Request**
3. So sánh:

```
feature/login → develop
```

4. Tạo Pull Request
5. Chờ review

---

# 9. Review Code

Team member sẽ:

* đọc code
* comment
* yêu cầu sửa

Sau khi sửa:

```bash
git add .
git commit -m "fix review comment"
git push
```

PR sẽ tự cập nhật.

---

# 10. Merge branch

Sau khi PR được approve:

Merge vào `develop`.

Có 3 kiểu merge:

### 1. Merge commit

Giữ toàn bộ lịch sử.

### 2. Squash merge

Gộp tất cả commit thành 1 commit.

### 3. Rebase merge

Giữ lịch sử linear.

Team nên dùng:

```
Squash merge
```

---

# 11. Xóa branch sau khi merge

Sau khi merge:

```bash
git branch -d feature/login
```

Xóa branch trên remote:

```bash
git push origin --delete feature/login
```

---

# 12. Cập nhật branch với code mới

Nếu develop đã update:

```bash
git checkout feature/login
git pull origin develop
```

hoặc

```bash
git merge develop
```

---

# 13. Giải quyết Conflict

Conflict xảy ra khi:

2 người sửa cùng 1 đoạn code.

Git sẽ hiển thị:

```
<<<<<<< HEAD
code của bạn
=======
code của người khác
>>>>>>> develop
```

Cách xử lý:

1. sửa code
2. xóa dấu conflict
3. commit lại

```bash
git add .
git commit -m "resolve conflict"
```

---

# 14. Các lệnh Git quan trọng

### Kiểm tra trạng thái

```bash
git status
```

### Xem lịch sử commit

```bash
git log
```

### Xem branch

```bash
git branch
```

### Chuyển branch

```bash
git checkout branch_name
```

---

# 15. Quy tắc Git

1. Không push trực tiếp vào `main`
2. Luôn tạo branch mới cho mỗi feature
3. Pull code trước khi bắt đầu
4. Commit message rõ ràng
5. Tạo Pull Request trước khi merge
6. Code phải được review

---

# 16. Quy trình

```
1. git pull develop
2. git checkout -b feature/new-feature
3. code
4. git add .
5. git commit
6. git push
7. tạo Pull Request
8. review
9. merge
```

---

# 17. Cấu trúc branch đề xuất

```
main
develop
feature/*
bugfix/*
hotfix/*
```

Ví dụ:

```
feature/login
feature/payment
bugfix/login-error
hotfix/security
```

---

# 18. Một số lỗi thường gặp

### Push bị reject

Chạy:

```bash
git pull origin develop
```

Sau đó push lại.

---

### Commit nhầm file

Reset:

```bash
git reset HEAD filename
```

---

### Quay lại commit cũ

```bash
git checkout commit_id
```

---



---

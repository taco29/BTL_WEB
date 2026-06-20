document.addEventListener("DOMContentLoaded", function () {
    const popup = document.getElementById("homePopup");
    const closeBtn = document.getElementById("closePopupBtn");

    // Hiện popup sau khoảng 1 giây
    setTimeout(() => {
        if(popup) popup.style.display = "flex";
    }, 1000);

    // Tắt popup khi bấm X
    if(closeBtn) {
        closeBtn.addEventListener("click", function () {
            popup.style.display = "none";
        });
    }

    // Tắt popup khi bấm ra bên ngoài form
    if(popup) {
        popup.addEventListener("click", function (e) {
            if (e.target === popup) {
                popup.style.display = "none";
            }
        });
    }

    // Xử lý gửi form đăng ký qua AJAX
    function handleRegister(formId) {
        const form = document.getElementById(formId);
        if (!form) return;
        
        form.addEventListener('submit', async function (e) {
            e.preventDefault();
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                const result = await response.json();
                
                if (result.success) {
                    alert('Đăng ký thành công!');
                    form.reset();
                    if (formId === 'popupRegisterForm') {
                        popup.style.display = 'none';
                    }
                } else {
                    alert('Lỗi: ' + result.message);
                }
            } catch (error) {
                alert('Đã xảy ra lỗi hệ thống, vui lòng thử lại!');
                console.error(error);
            }
        });
    }

    handleRegister('inlineRegisterForm');
    handleRegister('popupRegisterForm');
});

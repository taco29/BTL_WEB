module.exports = {
    formatDate: (date) => {
        if (!date) return '';
        const d = new Date(date);
        return `${String(d.getDate()).padStart(2, '0')}/${String(d.getMonth() + 1).padStart(2, '0')}/${d.getFullYear()}`;
    },
    getDay: (dateString) => dateString ? dateString.split(' ')[0] : '',
    getMonth: (dateString) => dateString ? dateString.split(' ').slice(1).join(' ') : '',
    isEven: (index) => index % 2 === 0,
    pagination: (currentPage, totalPages) => {
        if (!totalPages || totalPages <= 1) return '';
        let html = '';
        
        if (currentPage > 1) {
            html += `<a href="?page=${currentPage - 1}" class="page-btn"><i class="fa-solid fa-angle-left"></i></a>`;
        }

        for (let i = 1; i <= totalPages; i++) {
            if (i === currentPage) {
                html += `<span class="page-btn active">${i}</span>`;
            } else {
                html += `<a href="?page=${i}" class="page-btn">${i}</a>`;
            }
        }

        if (currentPage < totalPages) {
            html += `<a href="?page=${currentPage + 1}" class="page-btn"><i class="fa-solid fa-angle-right"></i></a>`;
        }
        
        return html;
    }
};

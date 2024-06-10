// 插入navbar,footer的html
fetch("/static/base.html")
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.text();
    })
    .then(data => {
        // 創建一個臨時的 div 元素來容納 base.html 的內容
        let tempDiv = document.createElement("div");
        tempDiv.innerHTML = data;

        // 尋找並插入 navbar
        let navbarInsert = tempDiv.querySelector(".navbar");
        if (navbarInsert) {
            document.querySelector(".navbar_insert").appendChild(navbarInsert);
        } else {
            console.error('Error: Element with class "navbar" not found in base.html.');
        }

        // 尋找並插入 footer
        let footerInsert = tempDiv.querySelector(".footer");
        if (footerInsert) {
            document.querySelector(".footer_insert").appendChild(footerInsert);
        } else {
            console.error('Error: Element with class "footer" not found in base.html.');
        }
    })
    .catch(error => console.error('Error loading base HTML:', error));

// 點擊導覽列的標題文字導向homepage
document.addEventListener("click", function(event) {
    let pageTitle = event.target.closest('.navbar__text');
    if(pageTitle) {
        window.location.href = '/';
    }
});

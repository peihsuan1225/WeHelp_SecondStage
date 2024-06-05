// 捷運站載入、按鈕滾動列表、點擊捷運站會代入搜索框
document.addEventListener("DOMContentLoaded", () =>{
    const listbarMRT = document.querySelector(".listbar_text");
    const btnLeft = document.querySelector(".listbar__btn--left");
    const btnRight = document.querySelector(".listbar__btn--right");
    const searchInput = document.querySelector(".heroSection__input");

    fetch('/api/mrts')
        .then(response =>{
            if (!response.ok){
                throw new Error("連線回應不成功"+response.statusText);
            }
            return response.json();
        })
        .then(data =>{
            if(data.data){
                data.data.forEach(element => {
                    const mrtDiv = document.createElement("div");
                    mrtDiv.className = "listbar__text--mrt";
                    mrtDiv.textContent = element;
                    listbarMRT.appendChild(mrtDiv);

                    mrtDiv.addEventListener("click", ()=>{
                        searchInput.value = element;
                    });
                });
            }
        })
        .catch(error =>{
            console.error("fetch有問題",error);
            listbarMRT.textContent = "載入捷運站錯誤"
        }); 
    btnLeft.addEventListener("click", () =>{
        listbarMRT.scrollBy({
            left: -750,
            behavior: "smooth"
        });
    });
    btnRight.addEventListener("click", ()=>{
        listbarMRT.scrollBy({
            left: 750,
            behavior: "smooth"
        });
    });
});

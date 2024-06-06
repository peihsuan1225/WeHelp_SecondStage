// 捷運站載入、按鈕滾動列表、點擊捷運站會代入搜索框
document.addEventListener("DOMContentLoaded", () =>{
    const listbarMRT = document.querySelector(".listbar_text");
    const btnLeft = document.querySelector(".listbar__btn--left");
    const btnRight = document.querySelector(".listbar__btn--right");
    const searchInput = document.querySelector(".heroSection__input");

    fetch("/api/mrts")
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

// 顯示景點窗格
document.addEventListener("DOMContentLoaded", () =>{
    const attractionArea = document.querySelector(".attractionDisplayArea");
    
    fetch("/api/attractions")
        .then(response =>{
            if(!response.ok){
                throw new Error("連線回應不成功"+response.statusText); 
            }
            return response.json();
        })
        .then(data =>{
            if(data.data && Array.isArray(data.data)){
                data.data.forEach(attraction => {
                    const attractionDiv = document.createElement("div");
                    attractionDiv.className = "attraction";

                    const attractionNameDiv = document.createElement("div");
                    attractionNameDiv.className = "attraction__text--nameDiv";
                    const attractionNametextDiv = document.createElement("div");
                    attractionNametextDiv.className = "attraction__text--name";
                    attractionNametextDiv.textContent = attraction.name;

                    const attractionInfoDiv = document.createElement("div");
                    attractionInfoDiv.className = "attraction__text--info";
                    
                    const attractionMrtDiv = document.createElement("div");
                    attractionMrtDiv.className ="attraction__text--mrt";
                    attractionMrtDiv.textContent = attraction.mrt;

                    const attractionCatDiv = document.createElement("div");
                    attractionCatDiv.className = "attraction__text--cat";
                    attractionCatDiv.textContent = attraction.category;

                    attractionDiv.appendChild(attractionNameDiv);
                    attractionNameDiv.appendChild(attractionNametextDiv);
                    attractionDiv.appendChild(attractionInfoDiv);
                    attractionInfoDiv.appendChild(attractionMrtDiv);
                    attractionInfoDiv.appendChild(attractionCatDiv);

                    if(attraction.images && attraction.images.length >0){
                        attractionDiv.style.backgroundImage = `url(${attraction.images[0]})`;
                    }
                    attractionArea.appendChild(attractionDiv);
                });       
            }
        })
        .catch(error => {
            console.error("獲取景點數據時出錯:", error);
        });    
});
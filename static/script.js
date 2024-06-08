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
    let nextPage = 0;
    let loading = false;

    const loadAttractions = (page) => {
        if (loading) return;
        loading = true;

        fetch("/api/attractions?page="+page)
            .then(response =>{
                if(!response.ok){
                    throw new Error("連線回應不成功" + response.statusText); 
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
                    
                    nextPage = data.nextPage;
                    if(nextPage !== null){
                        observeLastAttraction();
                        console.log("naxepage =" + nextPage);
                    }
                }
                loading = false;
            })
            .catch(error => {
                console.error("獲取景點數據時出錯:", error);
                loading = false;
            });   
    };
    const observeLastAttraction = () =>{
        const attractions =document.querySelectorAll(".attraction");
        const lastAttraction = attractions[attractions.length - 1];
        if(lastAttraction){
            const observer = new IntersectionObserver(entries =>{
                if (entries[0].isIntersecting){
                    observer.disconnect();
                    if (nextPage !== null){
                        loadAttractions(nextPage);
                    }
                }
            });
            observer.observe(lastAttraction);
        }
    };
    loadAttractions(nextPage);
});

function searchKeyword(){
    const attractionArea = document.querySelector(".attractionDisplayArea");
    let nextPage = 0;
    let loading = false;
    let noResultsMessageShown = false;

    const loadAttractions = (page) => {
        if (loading) return;
        loading = true;
        
        let input = document.querySelector("#input_keyword").value.trim();
        fetch("/api/attractions?keyword=" + input + "&page=" + page)
            // console.log("/api/attractions?keyword=" + input + "&page=" + page)
            .then(response =>{
                if(!response.ok){
                    const noResultsMessage = document.createElement("div");
                    noResultsMessage.className = "attraction__noResults";
                    noResultsMessage.textContent ="查無對應景點";
                    attractionArea.innerHTML = "";
                    attractionArea.appendChild(noResultsMessage);
                    noResultsMessageShown = true;
                    throw new Error("連線回應不成功" + response.statusText);
                }
                
                return response.json();
                
            })
            .then(data =>{
                if(data.data && Array.isArray(data.data)){
                    if(page === 0){
                        attractionArea.innerHTML = "";
                    }
                    
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
                    
                    nextPage = data.nextPage;
                    if(nextPage !== null){
                        observeLastAttraction();
                        console.log("naxepage =" + nextPage);
                    }
                }
                else{
                    
                }
                loading = false;
            })
            .catch(error => {
                console.error("獲取景點數據時出錯:", error);
                loading = false;
            });   
    };

    const observeLastAttraction = () =>{
        const attractions =document.querySelectorAll(".attraction");
        const lastAttraction = attractions[attractions.length - 1];
        if(lastAttraction){
            const observer = new IntersectionObserver(entries =>{
                if (entries[0].isIntersecting){
                    observer.disconnect();
                    if (nextPage !== null){
                        loadAttractions(nextPage);
                    }
                }
            });
            observer.observe(lastAttraction);
        }
    };

    let input = document.querySelector("#input_keyword").value.trim();
    if (input ===""){
        alert("查詢內容不能為空");
    }
    else{
        loadAttractions(nextPage);
    }
}

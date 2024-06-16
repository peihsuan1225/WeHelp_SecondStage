// 捷運站載入、按鈕滾動列表、點擊捷運站會代入搜索框
document.addEventListener("DOMContentLoaded", () =>{
    const listbarMRT = document.querySelector(".listbar__text");
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
                    let mrtDiv = document.createElement("div");
                    mrtDiv.className = "listbar__text--mrt";
                    mrtDiv.textContent = element;
                    listbarMRT.appendChild(mrtDiv);

                    mrtDiv.addEventListener("click", ()=>{
                        searchInput.value = element;
                        searchKeyword();
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
    const attractionArea = document.querySelector(".attractionDisplayArea");
    let nextPage = 0;
    let loading = false;

    const fetchAttractions = (url) => {
        return fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error("連線回應不成功" + response.statusText);
                }
                return response.json();
            });
    };

    const displayAttractions = (data, clearArea = false) => {
        if (clearArea) {
            attractionArea.innerHTML = "";
        }
        if (data.data && Array.isArray(data.data)) {
            data.data.forEach(attraction => {
                const attractionDiv = document.createElement("div");
                attractionDiv.className = "attraction";
                attractionDiv.id = attraction.id

                const attractionNameDiv = document.createElement("div");
                attractionNameDiv.className = "attraction__text--nameDiv";
                const attractionNametextDiv = document.createElement("div");
                attractionNametextDiv.className = "attraction__text--name";
                attractionNametextDiv.textContent = attraction.name;

                const attractionInfoDiv = document.createElement("div");
                attractionInfoDiv.className = "attraction__text--info";

                const attractionMrtDiv = document.createElement("div");
                attractionMrtDiv.className = "attraction__text--mrt";
                attractionMrtDiv.textContent = attraction.mrt;

                const attractionCatDiv = document.createElement("div");
                attractionCatDiv.className = "attraction__text--cat";
                attractionCatDiv.textContent = attraction.category;

                attractionDiv.appendChild(attractionNameDiv);
                attractionNameDiv.appendChild(attractionNametextDiv);
                attractionDiv.appendChild(attractionInfoDiv);
                attractionInfoDiv.appendChild(attractionMrtDiv);
                attractionInfoDiv.appendChild(attractionCatDiv);

                if (attraction.images && attraction.images.length > 0) {
                    attractionDiv.style.backgroundImage = `url(${attraction.images[0]})`;
                }

                attractionDiv.addEventListener("click", () =>{
                    let id = attractionDiv.id;
                    window.location.href = "/attraction/"+ id ;
                });
                attractionArea.appendChild(attractionDiv);
            });

            nextPage = data.nextPage;
            if (nextPage !== null) {
                observeLastAttraction();
                console.log("naxepage =" + nextPage);
            }
        }
    };

    const loadAttractions = (page) => {
        if (loading) return;
        loading = true;

        fetchAttractions("/api/attractions?page=" + page)
            .then(data => {
                displayAttractions(data);
                loading = false;
            })
            .catch(error => {
                console.error("獲取景點數據時出錯:", error);
                loading = false;
            });
    };

    const searchAttractions = (page) => {
        if (loading) return;
        loading = true;

        const input = document.querySelector(".heroSection__input").value.trim();
        fetchAttractions("/api/attractions?keyword=" + input + "&page=" + page)
            .then(data => {
                displayAttractions(data, true);
                loading = false;
            })
            .catch(error => {
                console.error("獲取景點數據時出錯:", error);
                displayNoResultsMessage("獲取景點數據時出錯");
                loading = false;
            });
    };

    const displayNoResultsMessage = (message) =>{
        const noResultsMessage = document.createElement("div");
        noResultsMessage.className = "attraction__noResults";
        noResultsMessage.textContent = message;
        attractionArea.innerHTML = "";
        attractionArea.appendChild(noResultsMessage);
    };

    const observeLastAttraction = () => {
        const attractions = document.querySelectorAll(".attraction");
        const lastAttraction = attractions[attractions.length - 1];
        if (lastAttraction) {
            const observer = new IntersectionObserver(entries => {
                if (entries[0].isIntersecting) {
                    observer.disconnect();
                    if (nextPage !== null) {
                        loadAttractions(nextPage);
                    }
                }
            });
            observer.observe(lastAttraction);
        }
    };

    const searchKeyword = () => {
        const input = document.querySelector(".heroSection__input").value.trim();
        if (input === "") {
            alert("查詢內容不能為空");
        } else {
            searchAttractions(0);
        }
    };

    loadAttractions(nextPage);

    
    document.querySelector(".heroSection__btn").addEventListener("click", searchKeyword);
});



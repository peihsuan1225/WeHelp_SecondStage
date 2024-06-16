document.addEventListener("DOMContentLoaded", () =>{
    // 取得當前景點id並獲取資訊
    const pathname = window.location.pathname;
    const parts = pathname.split("/");
    const id = parts[parts.length-1];
    let images = [];
    
    fetch("/api/attraction/"+id)
        .then(response =>{
            if(!response.ok){
                throw new Error("連線回應不成功"+response.statusText);
            }
            return response.json();
        })
        .then(data =>{
            if(data.data){
                const info = data.data;
                images = info.images;
                pictureDisplay(images);

                const nameDiv = document.querySelector(".sectionProfile__text--name");
                nameDiv.textContent = info.name;

                const introDiv = document.querySelector(".sectionProfile__text--intro");
                introDiv.textContent = info.category + " at " +info.mrt;

                const descriptionDiv = document.querySelector(".infos__text--description");
                descriptionDiv.textContent = info.description;

                const addressDiv = document.querySelector(".infos__text--address");
                addressDiv.textContent = info.address;

                const transportDiav = document.querySelector(".infos__text--transport");
                transportDiav.textContent = info.transport;
            }
        })
        .catch(error =>{
            console.log("fetch有問題",error);
        });

    // 圖片輪撥 fuction
    let currentIndex = 0;
    let autoPlay;

    const pictureDisplay = (images) =>{
        const dotsblock = document.querySelector(".sectionPicture__dotsBlock");
        dotsblock.innerHTML = "";
        
        if(images){
            const showImgDiv = document.querySelector(".sectionPicture");

            images.forEach((image,index) =>{
                const dot = document.createElement("div");
                dot.className = "sectionPicture__dot";
                dotsblock.appendChild(dot);

                if (index === currentIndex){
                    dot.classList.add("black");
                }

                dot.addEventListener("click", () =>{
                    currentIndex = index;
                    pictureDisplay(images);
                    clearInterval(autoPlay);
                });
            });
            showImgDiv.classList.remove("fade-in");
            showImgDiv.classList.add("fade-out");

            setTimeout(() =>{
                showImgDiv.style.backgroundImage = `url(${images[currentIndex]})`;
                showImgDiv.classList.remove("fade-out");
            }, 1500);
            setTimeout(() =>{
                showImgDiv.style.backgroundImage = `url(${images[currentIndex]})`;
                showImgDiv.classList.add("fade-in");
            }, 300);
        }
    };

    autoPlay = setInterval(nextImage, 4000);

    function nextImage() {
        currentIndex = (currentIndex + 1) % images.length;
        pictureDisplay(images);
    }

    function previousImage() {
        currentIndex = (currentIndex -1 +images.length) %images.length;
        pictureDisplay(images);
    }

    const next = document.querySelector(".sectionPicture__btn--right");
    next.addEventListener("click", () =>{
        nextImage();
        clearInterval(autoPlay);
    });
    const back = document.querySelector(".sectionPicture__btn--left");
    back.addEventListener("click", () =>{
        previousImage();
        clearInterval(autoPlay);
    });

    // 選擇時間顯示對應價格
    const booktimeInput = document.querySelectorAll(".sectionProfile__input--bookTime");
    const priceDiv = document.querySelector(".sectionProfile__text--bookPrice");

    booktimeInput.forEach(input =>{
        input.addEventListener("click", () =>{
            if(input.id === "morning"){
                priceDiv.textContent = "新台幣 2000 元";
            }
            else if(input.id === "afternoon"){
                priceDiv.textContent = "新台幣 2500 元";
            }
        })
    })
});
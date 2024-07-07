document.addEventListener("DOMContentLoaded", () =>{
    const orderAttrImgDisplay = document.querySelector(".orderInfo__img");
    const orderNumDisplay = document.querySelector("#order_num");
    const orderAttrNameDisplay = document.querySelector("#order_attr");
    const orderDateDisplay = document.querySelector("#order_date");
    const orderTimeDisplay = document.querySelector("#order_time");

    let id = ""
    
    const token = localStorage.getItem("token");
    
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }
    const order_number = getQueryParam('number');
    const getOrderFun = async function (){
        try{
            const response = await fetch("/api/order/"+order_number, {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                },
            });
            if(!response.ok){
                throw new Error("連線回應不成功" + response.statusText);
            }
            else{
                const data = await response.json();
                if(data == null){
                    window.location.href = "/booking"
                }
                else{
                    id = data.data.trip.attraction.id;
                    img = data.data.trip.attraction.image;
                    orderNum = data.data.number;
                    orderAttrName = data.data.trip.attraction.name;
                    orderDate = data.data.trip.date;
                    orderTime = data.data.trip.time;
                    let orderTimeWord = ""
                    if(orderTime === "morning"){
                        orderTimeWord = "早上 9 點到下午 4 點";
                    }
                    else if(orderTime === "afternoon"){
                        orderTimeWord = "下午 2 點到晚上 9 點" 
                    }
                    
                    orderAttrImgDisplay.style.backgroundImage = `url(${img})`;
                    orderNumDisplay.textContent = orderNum;
                    orderAttrNameDisplay.textContent = orderAttrName;
                    orderDateDisplay.textContent = orderDate;
                    orderTimeDisplay.textContent = orderTimeWord;
                }
            }
        }catch (error) {
            console.error("Error", error);
        }   
    };
    if(!token){
        window.location.href = '/';
    }
    else{
        getOrderFun();
    }
    
    orderAttrImgDisplay.addEventListener("click", () =>{
        let attrurl = `/attraction/${id}`
        window.location.href = attrurl;
    })
})
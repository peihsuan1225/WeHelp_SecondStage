document.addEventListener("DOMContentLoaded", () =>{
    const userNameDisplay = document.querySelector("#user_name");
    const deleteIcon = document.querySelector(".bookingInfos__icon")
    const attrImgDisplay = document.querySelector(".bookingInfos__pic");
    const attrNameDisplay = document.querySelector("#attraction_name");
    const dateDisplay = document.querySelector("#date");
    const timeDisplay = document.querySelector("#time");
    const priceDisplay = document.querySelector("#price");
    const attrAddressDisplay = document.querySelector("#location");
    const totalPraiceDisplay = document.querySelector("#total_price")

    const contactNameInput = document.querySelector("#contact_name");
    const contactEmailInput = document.querySelector("#contact_email");

    const main = document.querySelector(".main");
    const emptyBlock = document.querySelector(".empty__block");
    const token = localStorage.getItem("token");
    
    // 獲取user資訊，帶入對應欄位
    fetch("/api/user/auth", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        if(!response.ok){
            throw new Error("Token 已到期或無效");
        }
        return response.json();
    })
    .then(res =>{
        if(res.data == null){
            window.location.href = '/';
        }
        else{
            getBookingFun();
            const userInfo = res.data;
            const userName = userInfo.name;
            const userEmail = userInfo.email;

            userNameDisplay.textContent = userName;
            contactNameInput.value = userName;
            contactEmailInput.value = userEmail;
        }
    })

    // 獲取尚未下單的預定行程，帶入對應欄位
    const getBookingFun = async function (){
        try{
            const token = localStorage.getItem("token");
            const response = await fetch("/api/booking", {
                method: "GET",
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            });
            if(!response.ok){
                throw new Error("連線回應不成功" + response.statusText);
            }
            else{
                const data = await response.json();
                if(data == null){
                    main.style.display = "none";
                    emptyBlock.style.display = "block";
                }
                else{
                    const bookingInfo = data.data;
                    const attrImg = bookingInfo.attraction.image;
                    const attrName = bookingInfo.attraction.name;
                    const attrAddress = bookingInfo.attraction.address;
                    const bookingDate = bookingInfo.date;
                    const bookingTime = bookingInfo.time;
                    let bookingTimeWord = ""
                    if(bookingTime === "morning"){
                        bookingTimeWord = "早上 9 點到下午 4 點";
                    }
                    else if(bookingTime === "afternoon"){
                        bookingTimeWord = "下午 2 點到晚上 9 點" 
                    }
                    const bookingPrice = ("新台幣 " + bookingInfo.price + " 元");
            
                    attrImgDisplay.style.backgroundImage = `url(${attrImg})`;
                    attrNameDisplay.textContent = attrName;
                    dateDisplay.textContent = bookingDate;
                       
                    timeDisplay.textContent = bookingTimeWord;
                    priceDisplay.textContent = bookingPrice;
                    attrAddressDisplay.textContent = attrAddress;
                    totalPraiceDisplay.textContent = bookingPrice;
                }
            }     
        }catch (error) {
            console.error("Error", error);
        }
    };    

    const deleteFun = async function () {
        const token = localStorage.getItem("token");
        try{
            const response = await fetch("/api/booking" ,{
                method: "DELETE",
                headers:{
                    "Authorization": `Bearer ${token}`
                },
            });

            if(!response.ok){
                alert("移除行程錯誤");
            }
            else if(response.ok){
                main.style.display = "none";
                emptyBlock.style.display = "block";
            }
        }
        catch(error){
            console.error("Error", error);
        }
    }

    deleteIcon.addEventListener("click", () =>{
        deleteFun();
    });  
});

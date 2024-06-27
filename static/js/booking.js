document.addEventListener("DOMContentLoaded", () =>{
    const userNameDisplay = document.querySelector("#user_name");
    const deleteIcon = document.querySelector(".bookingInfos__icon")
    const attrImgDisplay = document.querySelector(".bookingInfos__pic");
    const attrNameDisplay = document.querySelector("#attraction_name");
    const dateDisplay = document.querySelector("#date");
    const timeDisplay = document.querySelector("#time");
    const priceDisplay = document.querySelector("#price");
    const attrAddressDisplay = document.querySelector("#location");

    const contactNameInput = document.querySelector("#contact_name");
    const contactEmailInput = document.querySelector("#contact_email");

    const main = document.querySelector(".main");
    const emptyBlock = document.querySelector(".empty_block");

    fetch("/api/user/auth")
        .then(data =>{
            if(data.data){
                const userInfo = data.data;
                const userName = userInfo.name;
                const userEmail = userInfo.email;

                userNameDisplay.textContent = userName;
                contactNameInput.textContent = userName;
                contactEmailInput.textContent = userEmail;
            }else{
                window.location.href = "/"
            }
        })
    fetch("/api/booking")
        .then(response =>{
            if(!response.ok){
                throw new Error("連線回應不成功"+response.statusText);
            }
            return response.json();
        })
        .then(data =>{
            if(data.data){
                const bookingInfo = data.data;
                const attrImg = bookingInfo.attraction.image;
                const attrName = bookingInfo.attraction.name;
                const attrAddress = bookingInfo.attraction.address;
                const bookingDate = bookingInfo.date;
                const bookingTime = bookingInfo.time;       
                const bookingPrice = bookingInfo.price;

                attrImgDisplay.style.backgroundImage = url(attrImg);
                attrNameDisplay.textContent = attrName;
                dateDisplay.textContent = bookingDate;
                timeDisplay.textContent = bookingTime;
                priceDisplay.textContent = bookingPrice;
                attrAddressDisplay.textContent = attrAddress;
            }
            else{
                main.style.display = none;
                emptyBlock.style.display = block;
            }
        })
    

    const deleteFun = async function () {
        try{
            const response = await fetch("/api/booking" ,{
                method: "DELETE",
                headers:{
                    "Content-Type": "application/json"
                },
            });
        

            if(!response.ok){
                const errorData = await response.json();
            }
            else if(data.ok){
                main.style.display = none;
                emptyBlock.style.display = block;
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
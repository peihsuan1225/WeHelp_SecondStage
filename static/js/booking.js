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
    
    let bookingInfo = null;
    let attrImg = null;
    let attrName = null;
    let attrAddress =null;
    let bookingDate =null;
    let bookingTime =null;
    
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
                    bookingInfo = data.data;
                    attrImg = bookingInfo.attraction.image;
                    attrName = bookingInfo.attraction.name;
                    attrAddress = bookingInfo.attraction.address;
                    bookingDate = bookingInfo.date;
                    bookingTime = bookingInfo.time;
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
    
    // 判斷登入狀態，獲取user資訊，帶入對應欄位
    if(!token){
        window.location.href = '/';
    }
    else{
        getBookingFun();
        const userInfo = JSON.parse(localStorage.getItem("userInfo"));
        const userName = userInfo.name;
        const userEmail = userInfo.email;

        userNameDisplay.textContent = userName;
        contactNameInput.value = userName;
        contactEmailInput.value = userEmail;
    }
    
    // 移除行程
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

    // 金流串接
    TPDirect.card.setup({
        // Display ccv field
        fields: {
            number: {
                // css selector
                element: '#card-number',
                placeholder: '**** **** **** ****'
            },
            expirationDate: {
                // DOM object
                element: document.getElementById('card-expiration-date'),
                placeholder: 'MM / YY'
            },
            ccv: {
                element: '#card-ccv',
                placeholder: 'ccv'
            }
        },  
        styles: {
            // Style all elements
            'input': {
                'color': 'gray'
            },
            // Styling ccv field
            'input.ccv': {
                // 'font-size': '16px'
            },
            // Styling expiration-date field
            'input.expiration-date': {
                // 'font-size': '16px'
            },
            // Styling card-number field
            'input.card-number': {
                // 'font-size': '16px'
            },
            // style focus state
            ':focus': {
                // 'color': 'black'
            },
            // style valid state
            '.valid': {
                'color': 'green'
            },
            // style invalid state
            '.invalid': {
                'color': 'red'
            },
            // Media queries
            // Note that these apply to the iframe, not the root window.
            '@media screen and (max-width: 400px)': {
                'input': {
                    'color': 'orange'
                }
            }
        },
        // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
        isMaskCreditCardNumber: true,
        maskCreditCardNumberRange: {
            beginIndex: 6,
            endIndex: 11
        }
    });

    const submitPaymentBtn = document.querySelector(".confirm__btn");
    submitPaymentBtn.addEventListener("click", () =>{
        TPDirect.card.getPrime(function (result) {
            if (result.status !== 0) {
                alert('Get prime error ' + result.msg);
                return;
            }

            alert('Get prime 成功，prime: ' + result.card.prime);

            // 在這裡將 prime 發送到你的伺服器
            const token = localStorage.getItem("token");
            const userName = document.querySelector("#contact_name").value;
            const userEmail = document.querySelector("#contact_email").value;
            const userPhone = document.querySelector("#contact_phone").value;
            // console.log(bookingInfo);
            const request = {
                prime: result.card.prime,
                order: {
                    price:bookingInfo.price,
                    trip: {
                        attraction:{
                            id:bookingInfo.attraction.id,
                            name:attrName,
                            address:attrAddress,
                            image:`url(${attrImg})`
                        },
                        date:bookingDate,
                        time:bookingTime
                    },
                    contact: {
                        name: userName,
                        email: userEmail,
                        phone: userPhone
                    }
                }
            }

            fetch("/api/orders", {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify(request)
            })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });        
        });
    });
});

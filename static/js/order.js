TPDirect.setupSDK(127028, 'app_bmavEzZj7YOni06F6bg6jZV8egKKxArq9Sh9X3xhzk9uZj11Av5O4STtS3CG', 'sandbox')

var fields = {
    number: {
        // css selector
        element: "#card-number",
        placeholder: "**** **** **** ****"
    },
    expirationDate: {
        // DOM object
        element: "#card-expiration-date",
        placeholder: "MM / YY"
    },
    ccv: {
        element: "#card-ccv",
        placeholder: "CVV"
    }
}


TPDirect.card.setup({
    fields: fields,
    styles: {
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
})

// 按下確認訂購並付款的按鈕
const payingButton = document.querySelector(".payingbutton")
payingButton.addEventListener("click", (event)=>{
    event.preventDefault()
    console.log("clickpayingbutton")
    let contactName = encodeURIComponent(document.querySelector("#name").value)

    // Get prim
    TPDirect.card.getPrime((result) =>{
        if (result.status !== 0){
            return result
        }else{
            fetch("/api/orders", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    "prime": result.card.prime,
                    "order": {
                        "price": document.querySelector("#orderprice").textContent,
                        "trip": trip,
                        "contact": {
                            "name": contactName,
                            "email": document.querySelector("#email").value,
                            "phone": document.querySelector("#phone").value,
                        }
                    }
                })
            }).then((response)=>{
                return response.json()
            }).then((result) =>{
                if (result["data"]["payment"]["status"] == 0){
                    let orderNumber = result.data.number;
                    window.location.href="/thankyou?number="+orderNumber;
                }else{
                    alert("訊息輸入錯誤!")
                }  
            })
        }
    })

    // 刪除已預定行程
    // fetch("/api/booking",{
    //     method: "DELETE",
    // }).then((response)=>{
    //     return response.json()
    // }).then((result)=>{
    //     if (result["ok"]){
    //         document.querySelector(".welcomeblock").style.display = "block";
    //         document.querySelector(".bookcontainor").style.display = "none";
    //         document.querySelector(".nobooking").style.display = "block";
    //     }
    // })
})
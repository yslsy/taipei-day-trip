const searchParams = new URLSearchParams(window.location.search);
let thankyouOrderumber = searchParams.get("number");

// 載入頁面
window.addEventListener("load", ()=>{
    fetch("/api/user/auth",{
        method: "GET",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        document.querySelector(".booking").style.display = "block";
        document.getElementById("login").style.display = "none";
        document.getElementById("logout").style.display = "block";
    })

    // 訂單編號資料
    fetch("/api/order/"+thankyouOrderumber , {
        method: "GET",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        console.log(result);
        console.log(document.querySelectorAll(".thankyoucontact"));
        document.querySelector(".thankyounumber").textContent = result["data"]["number"];
        // 訂購人資料
        document.querySelectorAll(".thankyoucontact")[0].textContent = decodeURI(result["data"]["contact"]["name"]);
        document.querySelectorAll(".thankyoucontact")[1].textContent = result["data"]["contact"]["phone"];
        document.querySelectorAll(".thankyoucontact")[2].textContent = result["data"]["contact"]["email"];
        // 訂單內容
        document.querySelectorAll(".thankyoucontact")[3].textContent = result["data"]["trip"]["date"];
        document.querySelectorAll(".thankyoucontact")[4].textContent = result["data"]["trip"]["attraction"]["name"];
        document.querySelectorAll(".thankyoucontact")[5].textContent = result["data"]["trip"]["attraction"]["address"];
        document.querySelectorAll(".thankyoucontact")[6].textContent = result["data"]["price"];
    })
})

// 點選預定行程
document.querySelector(".booking").addEventListener("click", ()=>{
    fetch("/api/user/auth", {
        method:"GET",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["data"]!=null){
            window.location.href="/booking"
        }else{
            loginModal.style.display = "block"
        }
    })
})
// 載入頁面
window.addEventListener("load", ()=>{
    fetch("/api/user/auth").then((response)=>{
        return response.json()
    }).then((result)=>{
        document.querySelector(".membername").textContent = result["data"]["name"]
    })

    fetch("/api/booking")
    .then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["data"] == null){
            document.querySelector(".welcomeblock").style.display = "block";
            document.querySelector(".bookcontainor").style.display = "none";
            document.querySelector(".nobooking").style.display = "block";
            document.querySelector(".booking").style.display = "block";
            document.getElementById("login").style.display = "none";
            document.getElementById("logout").style.display = "block";
        }else{
            document.querySelector(".welcomeblock").style.display = "block";
            document.querySelector(".bookcontainor").style.display = "block";
            document.querySelector(".booking").style.display = "block";
            document.getElementById("login").style.display = "none";
            document.getElementById("logout").style.display = "block";
            // 景點圖片
            const imageContainer = document.querySelector(".tourimage")
            const tourImage = document.createElement("img");
            tourImage.src = result["data"]["attraction"]["image"][0]
            tourImage.classList.add("tourImage");
            imageContainer.appendChild(tourImage)
            // 預定時間
            let tourtime = ""
            if (result["data"]["time"] === "morning"){
                tourtime = "早上九點到中午十二點"
            }else{
                tourtime = "下午一點到下午四點"
            }
            document.querySelector(".tourname").textContent = result["data"]["attraction"]["name"];
            document.querySelectorAll(".tourdata")[0].textContent = result["data"]["date"];
            document.querySelectorAll(".tourdata")[1].textContent = tourtime;
            document.querySelectorAll(".tourdata")[2].textContent = result["data"]["price"];
            document.querySelectorAll(".tourdata")[3].textContent = result["data"]["attraction"]["address"];
            document.querySelectorAll(".tourdata")[4].textContent = result["data"]["price"];
            
        }
    })
})

// 刪除預定行程
document.querySelector(".deleteicon").addEventListener("click", ()=>{
    fetch("/api/booking",{
        method: "DELETE",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["ok"]){
            location.reload()
        }
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

// 登出帳戶
document.getElementById("logout").addEventListener("click", ()=>{
    fetch("/api/user/auth", {
        method: "DELETE",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["ok"]){
            window.location.href="/"
        }
    })
})
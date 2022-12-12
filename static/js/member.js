const loginForm = document.querySelector(".loginform")
const signupform =document.querySelector(".signupform")

const booking = document.querySelector(".booking")
const login = document.getElementById("login")
const logout = document.getElementById("logout")
const close = document.querySelectorAll(".close")

const loginModal = document.querySelector(".loginmodal")
const loginEmail = document.querySelector(".loginemail")
const loginPassword = document.querySelector(".loginpw")
const loginText = document.querySelector(".logintext")

const signupModal = document.querySelector(".signupmodal")
const signupUser = document.querySelector(".signupuser")
const signupEmail = document.querySelector(".signupemail")
const signupPassword = document.querySelector(".signuppw")
const signupText = document.querySelector(".signuptext")

// 點擊叉關掉登入/註冊視窗
for (let i=0; i<close.length; i++){
    close[i].addEventListener("click", ()=>{
        loginModal.style.display = "none";
        signupModal.style.display = "none";
    })
}

// 點擊背景關掉登入/註冊視窗
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
    if (event.target == signupModal) {
        signupModal.style.display = "none";
    }
}

// 點擊登入
login.addEventListener('click',()=>{
    loginModal.style.display = "block"
})

// 登入切換至註冊
const logintosignup = document.querySelector(".logintosignup")
logintosignup.addEventListener("click",()=>{
    loginModal.style.display = "none";
    signupModal.style.display = "block";
})

// 註冊切換至登入
const signuptologin = document.querySelector(".signuptologin")
signuptologin.addEventListener("click",()=>{
    loginModal.style.display = "block";
    signupModal.style.display = "none";
})

// 登入帳戶
loginForm.addEventListener("submit", (e)=>{
    e.preventDefault()
    if (loginEmail.value === "" && loginPassword.value === ""){
        loginText.textContent = "請輸入郵箱及密碼"
    }
    else{
        fetch("/api/user/auth",{
            method:"PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                email: loginEmail.value,
                password: loginPassword.value
            })
        }).then((response)=>{
            return response.json()
        }).then((result)=>{
            if (result["ok"]){
                location.reload()
            }
            else if(result["error"]){
                loginText.textContent = result["message"]
            }
        })
    }
})

// 驗證是否登入
window.addEventListener("load",()=>{
    fetch("/api/user/auth",{method:"GET"}).then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["data"]!=null){
            booking.style.display = "block";
            login.style.display = "none";
            logout.style.display = "block";
        }else{
            booking.style.display = "block";
            login.style.display = "block";
            logout.style.display = "none";
        }
    })
})

// 註冊新帳戶
signupform.addEventListener("submit",(e)=>{
    e.preventDefault()
    if (signupUser.value === "" && signupEmail.value === "" && signupPassword.value === ""){
        signupText.textContent = "請輸入註冊資訊"
    }
    else{
        fetch("/api/user",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                user: signupUser.value,
                email: signupEmail.value,
                password: signupPassword.value
            })
        }).then((response)=>{
            return response.json()
        }).then((result)=>{
            if (result["ok"]){
                signupText.textContent = "註冊成功"
            }
            else if(result["error"]){
                signupText.textContent = result["message"]
            }
        })
    }
})

// 登出帳戶
logout.addEventListener("click", ()=>{
    fetch("/api/user/auth", {
        method: "DELETE",
    }).then((response)=>{
        return response.json()
    }).then((result)=>{
        if (result["ok"]){
            location.reload()
        }
    })
})

let pathId = location.pathname.split("/")[2];

function toindex(){
    window.location.href="/";
}

function load(){
    fetch("/api/attraction/"+pathId)
    .then((response) =>{
        return response.json();
    })
    .then((result) =>{
        render(result);
        imageRender(result);
    })
}
load();

// 景點圖片輪播
function imageRender(result) {
    for (let i=0; i<result.data.images.length; i++){
        const imgContainer = document.querySelector(".imgcontainer");
        //圖片
        const imgSlides = document.createElement("div");
        imgSlides.classList.add("imgSlides");
        const attrImage = document.createElement("img");
        attrImage.src = result.data.images[i];
        attrImage.classList.add("attrImage");
        //dot
        const outsideDot = document.querySelector(".outsideDot");
        const dot = document.createElement("div");
        dot.classList.add("dot");
        outsideDot.appendChild(dot);

        imgSlides.appendChild(attrImage);
        imgContainer.appendChild(imgSlides);        
    }
    var slideIndex = 1;
    showSlides(slideIndex);
}
var slideIndex = 1;

// 切換下一張或上一張景點圖片
function plusSlides(n) {
    showSlides(slideIndex += n);
};

function showSlides(n) {
    var i;
    let slides = Array.apply(null,document.querySelectorAll(".imgSlides"));
    let dots = Array.apply(null,document.querySelectorAll(".dot"));
    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace("active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";

}

// 景點文字
function render(result) {
    const attrName = document.querySelector(".attrname");
    let name = result.data.name;
    attrName.textContent = name; 

    const attrCategoryandMrt = document.querySelector(".attrcategoryandmrt");
    let category = result.data.category;    
    let mrt = result.data.mrt;
    attrCategoryandMrt.textContent = category +"  at  "+ mrt;

    const attrDescription = document.querySelector(".attrintroduce");
    let description = result.data.description;
    attrDescription.textContent = description;

    const addrAddress = document.querySelector(".attraddress");
    let address = result.data.address;
    addrAddress.textContent = address;

    const attrTransport = document.querySelector(".attrtraffic");
    let transport = result.data.transport;
    attrTransport.textContent = transport;
}

// 選擇時間和對應價格
let iuputList = document.querySelectorAll('[name="time"]');
let inputlistArray = Array.apply(null,iuputList);
inputlistArray[0].addEventListener("change",(e)=>{
    if(e.target.checked){
        document.querySelector(".price").textContent=2000;
    }
})
inputlistArray[1].addEventListener("change",(e)=>{
    if(e.target.checked){
        document.querySelector(".price").textContent=2500;
    }
})
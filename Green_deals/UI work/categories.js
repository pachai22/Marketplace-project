const urlParams = new URLSearchParams(window.location.search);
const user_id =urlParams.get('user_id')
if (user_id == null){
alert("Please Login!")
window.location.replace("E:/Frontend/Project/login.html")
}

var slideIndex = 0;
showSlides();

function showSlides() {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 2000); // Change image every 2 seconds
}

function navigate(ids){ 
  window.location.assign(`E:/Frontend/Project/product.html?id=${ids}&user_id=${user_id}`)
}

function home(){
  window.location.assign(`E:/Frontend/Project/categories.html?user_id=${user_id}`)
}

function cart(){
  window.location.assign(`E:/Frontend/Project/cart.html?user_id=${user_id}`)

}

function logout(){
  window.location.replace("E:/Frontend/Project/login.html")
}



function createElement(element){

  console.log("hi")

  const card = document.createElement('div')
  const h4 = document.createElement('h4')
  const a = document.createElement('a')
  const img = document.createElement('img')
  const title = document.createElement('div')

  card.setAttribute('class','card')
  title.setAttribute('class','title')
  img.setAttribute('src',element['image'])
  h4.innerHTML=element['category_type']
  title.setAttribute('id',element['category_id'])
  title.setAttribute('onclick','navigate(id)')

  const body = document.getElementsByClassName('category')[0];
  body.append(card)
  card.append(a)
  a.append(img)
  a.append(title)
  title.append(h4)

 
}


todos=fetch("http://127.0.0.1:5000/categories");
todos
.then((res)=>{
    res.json().then((data) => {
      console.log(data)
        data.forEach(function(element){
          createElement(element);         
        });
          
        
    }).catch((jErr) => {
        console.log('catch', jErr)
    })
})
.catch((err)=>{
    console.log("err",err)
})
const urlParams = new URLSearchParams(window.location.search);
const id =urlParams.get('id')
const user_id =urlParams.get('user_id')
if (user_id == null){
alert("Please Login!")
window.location.replace("E:/Frontend/Project/login.html")
}
console.log(id)
console.log(user_id)

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

function home(){
  window.location.assign(`E:/Frontend/Project/categories.html?user_id=${user_id}`)
}

function cart(){
  window.location.assign(`E:/Frontend/Project/cart.html?user_id=${user_id}`)

}

function logout(){
  window.location.replace("E:/Frontend/Project/login.html")
}

function addcart(item){
  console.log("hello")
  const item_id =item
  console.log(item_id)

  var cred={
    'item_id':item_id
}
console.log(cred)
console.log(user_id)
var todos = fetch(`http://127.0.0.1:5000/cart/${user_id}`,{
    method:'POST',
    headers: {
        'Content-Type': 'application/json;charset=utf-8'
      },
    body:JSON.stringify(cred)
});
todos.then((res)=>{
    res.json()
    .then((data)=>{
      alert(data['status'])
        console.log(data)
    })
})


}

function createElement(element){
  console.log(element)

  console.log("hi")

  const card = document.createElement('div')
  const h4title = document.createElement('h4')
  const a = document.createElement('a')
  const img = document.createElement('img')
  const title = document.createElement('div')
  const price= document.createElement('div')
  const add = document.createElement('input')
  const h4price = document.createElement('h4')

  card.setAttribute('class','card')
  title.setAttribute('class','title')
  img.setAttribute('src',element['image'])
  h4title.innerHTML=element['item_name']
  price.setAttribute('class','price')
  h4price.innerHTML="Rs :"+element['item-price']
  add.setAttribute('id','add')
  add.setAttribute('type','submit')
  add.setAttribute('value','Add-to-cart')
  add.setAttribute('id',element['item_id'])
  add.setAttribute('onclick','addcart(id)')

  const body = document.getElementsByClassName('content')[0];
  body.append(card)
  card.append(a)
  a.append(img)
  card.append(title)
  title.append(h4title)
  card.append(price)
  price.append(h4price)
  card.append(add)
 
}


todos=fetch(`http://127.0.0.1:5000/categories/${id}`);
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
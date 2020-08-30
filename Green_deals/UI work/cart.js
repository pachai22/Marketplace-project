const urlParams = new URLSearchParams(window.location.search);
const user_id =urlParams.get('user_id')
if (user_id == null){
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


function cart(){
    window.location.assign(`E:/Frontend/Project/cart.html?user_id=${user_id}`)
  
  }


function home(){
  window.location.assign(`E:/Frontend/Project/categories.html?user_id=${user_id}`)
}

function logout(){
    window.location.replace("E:/Frontend/Project/login.html")
}

function update(ids){

    const qid = ids
   
    console.log(qid)
    const val = document.getElementsByClassName(qid)[0].value
    console.log("hello")
    const item_id = ids
    console.log(item_id)
  
    var cred={
      'item_id':item_id,
      'desired_quantity':val
  }
  console.log(cred)
  console.log(user_id)
  var todos = fetch(`http://127.0.0.1:5000/cart/${user_id}`,{
      method:'PUT',
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



function remove(ids){
    console.log("hello")
    const item_id = ids
    console.log(item_id)
  
    var cred={
      'item_id':item_id
  }
  console.log(cred)
  console.log(user_id)
  var todos = fetch(`http://127.0.0.1:5000/cart/${user_id}`,{
      method:'DELETE',
      headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
      body:JSON.stringify(cred)
  });
  todos.then((res)=>{
      res.json()
      .then((data)=>{
        alert(data['status'])
        window.location.assign(`E:/Frontend/Project/cart.html?user_id=${user_id}`)
          console.log(data)
      })
  })  


}


function createElement(element){

  console.log("hi")

  const card = document.createElement('div')
  const img = document.createElement('img')
  const name = document.createElement('div')
  const h4name = document.createElement('h4')
  const tprice = document.createElement('div')
  const h4price = document.createElement('h4')
  const quantity = document.createElement('div')
  const quan = document.createElement('input')
  const update = document.createElement('input')
  const remove = document.createElement('input')

  card.setAttribute('class','card')
  name.setAttribute('class','title')
  h4name.innerHTML = element['Product-name']
  img.setAttribute('src',element['image'])
  tprice.setAttribute('class','price')
  h4price.innerHTML = "Total-Price: Rs "+element['Product-price']
  quantity.setAttribute('class','quantity')
  quan.setAttribute('class',element['Product-id'])
  quan.setAttribute('value',element['Quantity'])
  quan.setAttribute('type','number')
  quan.setAttribute('min','1')
  quan.style.color="black"
  quan.setAttribute('maxlength','2')
  remove.setAttribute('class','remove')
  update.setAttribute('class','update')
  update.setAttribute('type','submit')
  update.setAttribute('value','Update')
  update.setAttribute('id',element['Product-id'])
  update.setAttribute('onclick','update(id)')
  remove.setAttribute('id',element['Product-id'])
  remove.setAttribute('value','Remove')
  remove.setAttribute('type','submit')
  remove.setAttribute('onclick','remove(id)')
  
  
  const body = document.getElementsByClassName('category')[0];
  body.append(card)
  card.append(img)
  card.append(name)
  name.append(h4name)
  card.append(tprice)
  tprice.append(h4price)
  card.append(quantity)
  
  quantity.append(quan)
  
  quantity.append(update)
  card.append(remove)
 
}


todos=fetch(`http://127.0.0.1:5000/cart/${user_id}`);
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
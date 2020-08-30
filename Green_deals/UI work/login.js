
function validate(username,password){
    const user_name = username
    const passwrd = password

    var cred={
        'username':user_name,
        'password':passwrd
    }
    console.log(cred)

var todos = fetch("http://127.0.0.1:5000/login",{
        method:'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
          },
        body:JSON.stringify(cred)
    });
    todos.then((res)=>{
        res.json()
        .then((data)=>{
            console.log(data)
            if (data['status'] == "200")
             window.location.replace(`E:/Frontend/Project/categories.html?user_id=${data['user_id']}`)
             else{
                 alert('Incorrect username/password')
                //window.location.reload("E:/Frontend/Project/login.html")
             }
        })
    })

}

function redirect(){
    console.log("hi")
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    console.log(username)
    console.log(password)
    if (username==""||password=="")
        alert("please fill out required field")
    else{
        validate(username,password)
    }
    
    
}
//var button = document.getElementById("btn")
//button.addEventListener("click", redirect())

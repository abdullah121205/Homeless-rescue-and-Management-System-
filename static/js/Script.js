document.getElementById("registerForm").addEventListener("submit",function(e){

e.preventDefault();

let name=document.getElementById("name").value;

let email=document.getElementById("email").value;

let phone=document.getElementById("phone").value;

let password=document.getElementById("password").value;

let confirm=document.getElementById("confirmPassword").value;

if(name===""||email===""||phone===""||password===""){

alert("Please fill all fields");

return;

}

if(password.length<8){

alert("Password must be at least 8 characters");

return;

}

if(password!==confirm){

alert("Passwords do not match");

return;

}

alert("Registration Successful");

window.location.href="login.html";

});

function togglePassword(){

const pass=document.getElementById("password");

pass.type=pass.type==="password"?"text":"password";

}

document.getElementById("loginForm").addEventListener("submit",function(e){

e.preventDefault();

let email=document.getElementById("email").value;

let password=document.getElementById("password").value;

if(email===""||password===""){

alert("Please fill all fields");

return;

}

localStorage.setItem("user",email);

alert("Login Successful");

window.location.href="dashboard.html";

});
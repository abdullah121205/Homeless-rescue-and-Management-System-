document.getElementById("registerForm").addEventListener("submit", function(e){

let fullname=document.getElementById("fullname").value.trim();

let email=document.getElementById("email").value.trim();

let username=document.getElementById("username").value.trim();

let password=document.getElementById("password").value;

let confirm=document.getElementById("confirm_password").value;

let message=document.getElementById("message");

if(fullname=="" || email=="" || username==""){

e.preventDefault();

message.innerHTML="Please fill all fields.";

message.style.color="red";

return;

}

if(password.length<6){

e.preventDefault();

message.innerHTML="Password should contain at least 6 characters.";

message.style.color="red";

return;

}

if(password!=confirm){

e.preventDefault();

message.innerHTML="Passwords do not match.";

message.style.color="red";

return;

}

});

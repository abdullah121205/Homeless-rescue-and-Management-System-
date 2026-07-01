function logout() {
    localStorage.removeItem("user");
    alert("Logged out successfully");
    window.location.href = "/";
}

function logoutConfirm(){

    let answer = confirm("Are you sure you want to logout?");

    if(answer){
        alert("Logged out successfully.");
    }

}
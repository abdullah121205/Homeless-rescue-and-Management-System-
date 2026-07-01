function logout() {
    localStorage.removeItem("user");
    alert("Logged out successfully");
    window.location.href = "/";
}

function logoutConfirm() {
    if (confirm("Are you sure you want to logout?")) {
        logout();
    }
}
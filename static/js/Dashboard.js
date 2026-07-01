function logout() {
    localStorage.removeItem("user");
    alert("Logged out successfully");
    window.location.href = "/";
}
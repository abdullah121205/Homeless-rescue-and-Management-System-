function logout() {
    window.location.href = "/logout";
}

function logoutConfirm() {
    if (confirm("Are you sure you want to logout?")) {
        logout();
    }
}

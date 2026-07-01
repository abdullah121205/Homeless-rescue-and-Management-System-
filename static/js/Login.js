const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();

        let email = document.getElementById("email").value;
        let password = document.getElementById("password").value;

        if (email === "" || password === "") {
            alert("Please fill all fields");
            return;
        }

        alert("Login Successful");
        window.location.href = "/dashboard";
    });
}

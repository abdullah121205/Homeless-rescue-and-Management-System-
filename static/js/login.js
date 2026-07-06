const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", function (e) {

        const username = document.getElementById("username").value.trim();
        const password = document.getElementById("password").value.trim();
        const errorMessage = document.getElementById("error-message");

        errorMessage.textContent = "";

        if (username === "") {
            e.preventDefault();
            errorMessage.textContent = "Please enter your username.";
            return;
        }

        if (password === "") {
            e.preventDefault();
            errorMessage.textContent = "Please enter your password.";
            return;
        }

        if (password.length < 6) {
            e.preventDefault();
            errorMessage.textContent = "Password must be at least 6 characters.";
            return;
        }

        // If validation passes, the form is submitted to Flask.
    });

}

function logout() {
    window.location.href = "/logout";
}
/* Welcome Message */

window.onload = function () {
    console.log("Sabarmati NGO Dashboard Loaded Successfully");
};
function logoutConfirm() {
    if (confirm("Are you sure you want to logout?")) {
        logout();
    }
}
/* Highlight Active Navigation Button */

const navLinks = document.querySelectorAll(".buttons a");

navLinks.forEach(link => {
    if (link.href === window.location.href) {
        link.querySelector("button").style.backgroundColor = "#2e7d32";
    }
});
/* Card Animation */

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("mouseenter", function () {
        this.style.transform = "scale(1.03)";
        this.style.transition = "0.3s";
    });

    card.addEventListener("mouseleave", function () {
        this.style.transform = "scale(1)";
    });

});
/* Greeting */

const hour = new Date().getHours();

if (hour < 12) {
    console.log("Good Morning!");
}
else if (hour < 18) {
    console.log("Good Afternoon!");
}
else {
    console.log("Good Evening!");
}

const addPersonForm = document.getElementById("addPersonForm");

if (addPersonForm) {
    addPersonForm.addEventListener("submit", function (e) {

        e.preventDefault();

        let name = document.getElementById("name").value;
        let age = document.getElementById("age").value;
        let gender = document.getElementById("gender").value;
        let location = document.getElementById("location").value;

        if (name === "" || age === "" || gender === "" || location === "") {
            alert("Please fill all fields");
            return;
        }

        alert("Person added successfully!");
    });
}

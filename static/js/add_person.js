document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("addPersonForm");

    form.addEventListener("submit", function (e) {

        e.preventDefault();

        const fullName = document.querySelector('input[name="full_name"]').value.trim();
        const age = document.querySelector('input[name="age"]').value;
        const gender = document.querySelector('select[name="gender"]').value;
        const location = document.querySelector('input[name="location"]').value.trim();
        const photo = document.querySelector('input[name="photo"]').files[0];

        if (fullName === "") {
            alert("Please enter Full Name.");
            return;
        }

        if (age === "" || age < 1 || age > 120) {
            alert("Please enter a valid Age.");
            return;
        }

        if (gender === "") {
            alert("Please select Gender.");
            return;
        }

        if (location === "") {
            alert("Please enter Rescue Location.");
            return;
        }

        if (photo) {
            const allowedTypes = [
                "image/jpeg",
                "image/png",
                "image/jpg"
            ];

            if (!allowedTypes.includes(photo.type)) {
                alert("Please upload only JPG or PNG images.");
                return;
            }
        }

        alert("✅ Homeless person record saved successfully!");

        form.reset();

    });

});

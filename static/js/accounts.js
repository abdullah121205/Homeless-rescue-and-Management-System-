// Search volunteers in the table
document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("searchInput");

    searchInput.addEventListener("keyup", function () {

        const filter = searchInput.value.toLowerCase();
        const rows = document.querySelectorAll("#accountsTable tbody tr");

        rows.forEach(function (row) {

            const text = row.innerText.toLowerCase();

            if (text.includes(filter)) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

});


// Edit button
function editVolunteer(id) {
    alert("Edit Volunteer ID: " + id);
}


// Delete button
function deleteVolunteer(id) {

    if (confirm("Are you sure you want to delete this volunteer?")) {

        window.location.href = "/delete_volunteer/" + id;

    }

}

// Search Project Table

const searchInput = document.getElementById("search");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {

        let filter = searchInput.value.toLowerCase();

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            let text = row.textContent.toLowerCase();

            row.style.display = text.includes(filter) ? "" : "none";

        });

    });
}

// Delete Confirmation

function confirmDelete() {
    return confirm("Are you sure you want to delete this project?");
}

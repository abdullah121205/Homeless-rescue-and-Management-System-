// Search Beneficiaries

const searchBox = document.getElementById("search");

if (searchBox) {

    searchBox.addEventListener("keyup", function () {

        let filter = searchBox.value.toLowerCase();

        let rows = document.querySelectorAll("tbody tr");

        rows.forEach(function (row) {

            let text = row.textContent.toLowerCase();

            row.style.display = text.includes(filter) ? "" : "none";

        });

    });

}

// Delete Confirmation

function confirmDelete() {
    return confirm("Are you sure you want to delete this beneficiary?");
}

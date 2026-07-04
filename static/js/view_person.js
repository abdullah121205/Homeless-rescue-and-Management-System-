// ==============================
// Search Function
// ==============================

const searchInput = document.getElementById("searchInput");

if (searchInput) {
    searchInput.addEventListener("keyup", function () {

        let filter = searchInput.value.toUpperCase();

        let table = document.getElementById("personsTable");

        let tr = table.getElementsByTagName("tr");

        for (let i = 1; i < tr.length; i++) {

            let td = tr[i].getElementsByTagName("td")[0];

            if (td) {

                let txtValue = td.textContent || td.innerText;

                if (txtValue.toUpperCase().indexOf(filter) > -1) {
                    tr[i].style.display = "";
                }
                else {
                    tr[i].style.display = "none";
                }

            }

        }

    });
}

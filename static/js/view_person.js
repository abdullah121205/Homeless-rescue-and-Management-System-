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


// ==============================
// Edit Button
// ==============================

const editButtons = document.querySelectorAll(".edit-btn");

editButtons.forEach(function(button){

    button.addEventListener("click", function(){

        alert("Edit feature will be connected to the database later.");

    });

});


// ==============================
// Delete Button
// ==============================

const deleteButtons = document.querySelectorAll(".delete-btn");

deleteButtons.forEach(function(button){

    button.addEventListener("click", function(){

        let confirmDelete = confirm("Are you sure you want to delete this record?");

        if(confirmDelete){

            alert("Record deleted successfully. (Demo)");

        }

    });

});

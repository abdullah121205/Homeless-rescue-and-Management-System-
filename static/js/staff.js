// Staff Search Function

const searchInput = document.getElementById("search");

searchInput.addEventListener("keyup", function(){

    let value = searchInput.value.toLowerCase();

    let rows = document.querySelectorAll("tbody tr");


    rows.forEach(function(row){

        let text = row.innerText.toLowerCase();

        if(text.includes(value)){
            row.style.display = "";
        }
        else{
            row.style.display = "none";
        }

    });

});


// Add Staff Button

const addButton = document.querySelector(".add-btn");

addButton.addEventListener("click", function(){

    alert("Add Staff feature will be connected soon.");

});


// Edit Button

const editButtons = document.querySelectorAll(".edit-btn");

editButtons.forEach(function(button){

    button.addEventListener("click", function(){

        alert("Edit Staff feature will be connected soon.");

    });

});


// Delete Button

const deleteButtons = document.querySelectorAll(".delete-btn");

deleteButtons.forEach(function(button){

    button.addEventListener("click", function(){

        let confirmDelete = confirm(
            "Are you sure you want to delete this staff member?"
        );


        if(confirmDelete){

            alert("Delete feature will be connected with database soon.");

        }

    });

});
function searchPerson() {

    let input = document.getElementById("searchInput").value.toLowerCase();

    let rows = document.querySelectorAll("#personTable tbody tr");

    rows.forEach(function(row){

        let text = row.innerText.toLowerCase();

        if(text.includes(input)){
            row.style.display="";
        }
        else{
            row.style.display="none";
        }

    });

}
function filterStatus() {

    let filter = document.getElementById("statusFilter").value;

    let rows = document.querySelectorAll("#personTable tbody tr");

    rows.forEach(function(row){

        let status = row.cells[3].innerText;

        if(filter === "All" || status === filter){
            row.style.display = "";
        }
        else{
            row.style.display = "none";
        }

    });

}

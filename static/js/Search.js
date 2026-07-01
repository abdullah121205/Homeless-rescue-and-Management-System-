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

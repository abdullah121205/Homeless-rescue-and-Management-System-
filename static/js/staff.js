// Staff Search Function

const searchInput = document.getElementById("search");

if(searchInput){

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

}
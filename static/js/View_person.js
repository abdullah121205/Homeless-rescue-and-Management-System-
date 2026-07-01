function viewPerson(id) {
    alert("Viewing details of Person ID: " + id);
}

function deletePerson(id) {
    if (confirm("Are you sure you want to delete this record?")) {
        alert("Person deleted successfully.");
    }
}

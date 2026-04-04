function switchTable(tableID) {
    const sections = document.querySelectorAll(".table-container");
    sections.forEach(section => {
        section.classList.add("hidden")
    });

    const selected = document.getElementById("table-" + tableID);
    if (selected) {
        selected.classList.remove("hidden");
    }
}
function switchVisible(containerClass, elementId) {
    document.querySelectorAll(containerClass)
        .forEach(e => e.classList.add("hidden"));

    const selected = document.getElementById(elementId);
    if (selected)
        selected.classList.remove("hidden");
}

function switchGraph(graphId) {
    switchVisible(".graph-container", "plot-" + graphId);
    window.dispatchEvent(new Event("resize"));
}

function switchTable(tableId) {
    switchVisible(".table-container", "table-" + tableId);
}
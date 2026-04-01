function switchGraph(graphID) {
    const sections = document.querySelectorAll(".graph-container");
    sections.forEach(section => {
        section.classList.add("hidden")
    });

    const selected = document.getElementById("section-" + graphID);
    if (selected) {
        selected.classList.remove("hidden");
    }

    window.dispatchEvent(new Event('resize')); // Resizes graphs to full width (which is less when hidden)
}
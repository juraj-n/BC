document.addEventListener("DOMContentLoaded", function () {
    const graphDiv = document.getElementById("graph");

    const x = JSON.parse(graphDiv.dataset.x);
    const y = JSON.parse(graphDiv.dataset.y);

    const trace = {
        x: x,
        y: y,
        mode: "lines",
        type: "scatter"
    };

    const layout = {
        title: "Spectrum Graph"
    };

    Plotly.newPlot(graphDiv, [trace], layout);
});
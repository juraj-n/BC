document.addEventListener("DOMContentLoaded", function() {
    function createPlot(elementId, spectraData, plotTitle) {
        const traces = [];

        for (const [filename, data] of Object.entries(spectraData)) {
            traces.push({
                x: data.x,
                y: data.y,
                mode: "lines",
                name: filename
            });
        }

        const layout = {
            title: plotTitle,
            xaxis: { title: "Vlnová dĺžka" },
            yaxis: { title: "Intenzita" },
            hovermode: "closest"
        };

        const config = {
            scrollZoom: true,
            responsive: true,
            displaylogo: false,
            modeBarButtonsToRemove: ["select2d", "lasso2d"]
        };

        Plotly.newPlot(elementId, traces, layout, config);
    }

    if (typeof rawSpectraData !== "undefined") {
        createPlot("graph-raw", rawSpectraData, "Pôvodné dáta");
    }
    if (typeof zScoreData !== "undefined") {
        createPlot("graph-zscore", zScoreData, "Normalizované dáta (Podľa smerodajnej odchýlky / Z-Score)");
    }
    if (typeof normSpectraData !== "undefined") {
        createPlot("graph-min-max", normSpectraData, "Normalizované dáta (Min-Max)");
    }
});
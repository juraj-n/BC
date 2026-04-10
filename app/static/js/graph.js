const zones = [
    { name: "Z1", x0: 250, x1: 300 },
    { name: "Z2", x0: 300, x1: 325 },
    { name: "Z3", x0: 325, x1: 345 },
    { name: "Z4", x0: 345, x1: 380 },
    { name: "Z5", x0: 380, x1: 410 },
    { name: "Z6", x0: 410, x1: 450 },
    { name: "Z7", x0: 450, x1: 500 },
    { name: "Z8", x0: 500, x1: 550 },
];

function createZoneShapes() {
    return zones.map((zone, i) => ({
        type: "rect",
        xref: "x",
        yref: "paper",
        x0: zone.x0,
        x1: zone.x1,
        y0: 0,
        y1: 1,
        fillcolor: i % 2 === 0 ? "rgba(255,255,255,0.04)" : "rgba(50, 50, 50, 0.1)",
        line: { width: 0 }
    }));
}

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
        xaxis: { title: "Vlnová dĺžka", showgrid: false },
        yaxis: { title: "Intenzita" },
        hovermode: "closest",
        margin: {
            l: 60,
            r: 20,
            t: 40,
            b: 60
        },
        shapes: createZoneShapes()
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
if (typeof minMaxData !== "undefined") {
    createPlot("graph-min-max", minMaxData, "Normalizované dáta (Min-Max)");
}
if (typeof l1Data !== "undefined") {
    createPlot("graph-l1", l1Data, "Normalizované dáta (L1 / Area)");
}
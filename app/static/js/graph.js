document.addEventListener('DOMContentLoaded', function() {
    function createPlot(elementId, spectraData, plotTitle) {
        const traces = [];

        for (const [filename, data] of Object.entries(spectraData)) {
            traces.push({
                x: data.x,
                y: data.y,
                mode: 'lines',
                name: filename
            });
        }

        const layout = {
            title: plotTitle,
            xaxis: { title: 'Vlnová dĺžka (nm)' },
            yaxis: { title: plotTitle.includes('Normalizované') ? 'Intenzita (norm)' : 'Intenzita (a.u.)' },
            hovermode: 'closest'
        };

        const config = {
            scrollZoom: true,
            responsive: true,
            displaylogo: false,
            modeBarButtonsToRemove: ['select2d', 'lasso2d']
        };

        Plotly.newPlot(elementId, traces, layout, config);
    }

    if (typeof rawSpectraData !== 'undefined') {
        createPlot('graph-raw', rawSpectraData, 'Nenormalizované dáta');
    }
    if (typeof zScoreData !== 'undefined') {
        createPlot('graph-zscore', zScoreData, 'Z-Score Normalizované dáta (Standard Deviation)');
    }
    if (typeof normSpectraData !== 'undefined') {
        createPlot('graph-min-max', normSpectraData, 'Min-Max Normalizované dáta');
    }
});
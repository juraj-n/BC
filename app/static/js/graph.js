document.addEventListener('DOMContentLoaded', function() {
    
    // Function to create a plot
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

    // Initialize Graph 1: Raw Data
    if (typeof rawSpectraData !== 'undefined') {
        createPlot('graph-raw', rawSpectraData, 'Nenormalizované dáta');
    }

    // Initialize Graph 2: Normalized Data
    if (typeof normSpectraData !== 'undefined') {
        createPlot('graph-norm', normSpectraData, 'Min-Max Normalizované dáta');
    }
});
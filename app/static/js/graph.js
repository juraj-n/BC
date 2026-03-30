document.addEventListener('DOMContentLoaded', function() {
    const traces = [];

    for (const [filename, data] of Object.entries(allSpectra)) {
        const trace = {
            x: data.x,
            y: data.y,
            mode: 'lines',
            name: filename
        };

        traces.push(trace);
    }

    const layout = {
        title: 'Nenormalizované dáta',
        xaxis: { title: 'Vlnová dĺžka' },
        yaxis: { title: 'Intenzita' },
        hovermode: 'closest'
    };

    const config = {
        scrollZoom: true,
        responsive: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['select2d', 'lasso2d']
    };

    Plotly.newPlot('graph', traces, layout, config);
});
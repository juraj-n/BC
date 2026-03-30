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

    // 4. Render the plot
    if (traces.length > 0) {
        Plotly.newPlot('graph', traces, layout);
    } else {
        console.log("No data available to plot.");
        document.getElementById('graph').innerHTML = "No data uploaded yet.";
    }
});
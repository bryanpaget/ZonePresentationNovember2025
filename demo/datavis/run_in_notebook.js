// Run this in a JavaScript cell in Jupyter
%%javascript

// Simple D3 example in Jupyter
require.config({
    paths: {
        d3: 'https://d3js.org/d3.v7.min'
    }
});

require(['d3'], function(d3) {
    // Create a div for our chart
    element.append(`
        <div id="jupyter-chart" style="width: 100%; height: 300px;"></div>
    `);
    
    const data = [25, 50, 75, 100, 125];
    
    const svg = d3.select("#jupyter-chart")
        .append("svg")
        .attr("width", 400)
        .attr("height", 200);
    
    svg.selectAll("circle")
        .data(data)
        .enter()
        .append("circle")
        .attr("cx", (d, i) => i * 80 + 50)
        .attr("cy", 100)
        .attr("r", d => d / 10)
        .style("fill", "steelblue")
        .style("opacity", 0.7);
});


(function(d3) {
    var container = d3.select("#content");
    var height = container.node().clientHeight;
    var width = container.node().clientWidth;
    var margin = {top: 40, right: 40, bottom: 40, left: 40}

    var svg = d3.select("#content").append("svg")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width).attr("height", height);

    d3.json("/cpu_load").then(function(data) {
        var loads = data.loads.map(function (d) { return [new Date(1000 * d[0]), d[1]] });
        var series = data.series;

        var x = d3.scaleTime()
            .domain(d3.extent(loads, function(d) {return d[0];}))
            .range([margin.left, width - margin.right]);
        svg.append("g")
            .attr("class", "axis xaxis")
            .attr("transform", "translate(0," + (height - margin.bottom) + ")")
            .call(d3.axisBottom(x));

        var y = d3.scaleLinear()
            .domain([0, d3.max(loads, function(d) { return d3.max(d[1]); })])
            .range([height - margin.bottom, margin.top]);
        svg.append("g")
            .attr("class", "axis yaxis")
            .attr("transform", "translate(" + margin.left + ",0)")
            .call(d3.axisLeft(y));

        function drawLine(index, stroke) {
            svg.append("path")
                .datum(loads)
                .attr("fill", "none")
                .attr("stroke", stroke)
                .attr("stroke-width", 1.5)
                .attr("d", d3.line()
                    .x(function(d) { return x(d[0]) })
                    .y(function(d) { return y(d[1][index]) })
                )
        }
        drawLine(0, d3.schemeCategory10[0])
        drawLine(1, d3.schemeCategory10[1])
        drawLine(2, d3.schemeCategory10[2])
    });

})(d3);

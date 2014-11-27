var genReviewScore = function(name) {
    var width = 500;
    var height = 330;
    var marginLeft = 50;
    var marginTop = 20;

    d3.select('#product')
        .select('svg')
        .data([])
        .exit()
        .remove();

    var svg = d3.select('#product').append('svg')
        .attr('width', width + marginLeft)
        .attr('height', height + marginTop)
        .style('display', 'block')
        .style('margin', '0px auto');

    var main = svg.append('g')
        .attr('transform', 'translate(' + marginLeft + ',' + marginTop + ')');

    //svg.append('text')
        //.attr('x', 5)
        //.attr('y', marginTop + height - 10)
        //.attr('dy', '.32em')
        //.style('text-anchor', 'start')
        //.text('Product: ' + name);

    svg.append('text')
        .attr('x', 5)
        .attr('y', marginTop + height / 2)
        .attr('dy', '.32em')
        .style('text-anchor', 'start')
        .text('Score');

    svg.append('text')
        .attr('x', 5)
        .attr('y', marginTop + height / 4 + 10)
        .attr('dy', '.32em')
        .style('text-anchor', 'start')
        .text('Reviews');

    svg.append('text')
        .attr('x', 5)
        .attr('y', marginTop + height / 4 + 23)
        .attr('dy', '.32em')
        .style('text-anchor', 'start')
        .text('Sentiment');

    svg.append('text')
        .attr('x', 5)
        .attr('y', marginTop + height - 30)
        .attr('dy', '.32em')
        .style('text-anchor', 'start')
        .text('Features');

    main.append('line')
        .attr('x1', 0)
        .attr('y1', height / 2)
        .attr('x2', width)
        .attr('y2', height / 2)
        .style('stroke', '#EEEEEE')
        .style('stroke-width', '2px');

    //main.append('line')
        //.attr('x1', 0)
        //.attr('y1', height / 4 + 10)
        //.attr('x2', width)
        //.attr('y2', height / 4 + 10)
        //.style('stroke', '#EEEEEE')
        //.style('stroke-width', '2px');

    main.append('line')
        .attr('x1', 0)
        .attr('y1', height - 30)
        .attr('x2', width)
        .attr('y2', height - 30)
        .style('stroke', '#EEEEEE')
        .style('stroke-width', '2px');

    genScore2Feature(main, product2Scores[name], width, height);
    genReview2Score(main, reviews2Scores[name], width, height);
    genFeatureCircle(main, width, height);
    genScoreCircle(main, width, height);
};

var genReview2Score = function(svg, dict, width, height) {
    var reviewList = [];
    var maxNum = 1;
    for (var key in dict) {
        if (dict.hasOwnProperty(key)) {
            dict[key]['sentiment'] = +key;
            reviewList.push(dict[key]);
            for (var i = 1; i <= 5; i++) {
                if ((dict[key][i + '.0'] != undefined) && (dict[key][i + '.0'] > maxNum)) {
                    maxNum = dict[key][i + '.0'];
                }
            }
        }
    }
    reviewList.sort(function(a, b) {
        return a['sentiment'] - b['sentiment'];
    });
    d3.selectAll('.review2Score')
        .data([])
        .exit()
        .remove();
    var xScale = d3.scale.ordinal().rangeRoundBands([0, width], .1);
    var yScale = d3.scale.linear().range([height / 4 + 10, 0]);
    var widthScale = d3.scale.linear().domain([1, maxNum]).range([1, 8]);
    var minMax = d3.extent(reviewList, function(d) {return d['sentiment'];});
    xScale.domain(d3.range(minMax[1] - minMax[0] + 1).map(function(d) {return minMax[0] + d;}));
    yScale.domain([0, d3.max(reviewList, function(d) {return d['count'];})]);

    var xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom');

    svg.append('g')
        .attr('class', 'x axis')
        .attr('transform', 'translate(0,' + (height / 4 + 10) + ')')
        .call(xAxis);

    svg.selectAll('.bar')
        .data(reviewList)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', function(d) {
            return xScale(d['sentiment']);
        })
        .attr('width', xScale.rangeBand())
        .attr('y', function(d) {
            return yScale(d['count']);
        })
        .attr('height', function(d) {
            return height / 4 + 10 - yScale(d['count']);
        })
        .style('cursor', 'pointer')
        .on('click', function(d) {
            var tList = [];
            for (var key in d) {
                if ((+key <= 5) && (+key >= 1)) {
                    tList.push({'key': key, 'value': d[key], 'sentiment': d['sentiment']});
                }
            }
            d3.selectAll('.bar')
                .style('fill', '#EEEEEE');

            d3.select(this)
                .style('fill', 'grey');
            svg.selectAll('.review2Score')
                .data([])
                .exit()
                .remove();

            svg.selectAll('.review2Score')
                .data(tList)
                .enter()
                .append('line')
                .attr('class', 'review2Score')
                .attr('x1', function(d) {
                    return xScale(d['sentiment']);
                })
                .attr('y1', height / 4 + 30)
                .attr('x2', function(d) {
                    return (width - 3) / 4 * ((+d['key']) - 1);
                })
                .attr('y2', height / 2)
                .style('stroke', 'grey')
                .style('stroke-opacity', 0.6)
                .style('stroke-width', function(d) {
                    return widthScale(d['value']);
                });


        })
        .on('mouseover', function(d) {
            d3.select(this)
                .style('stroke', 'grey')
                .style('stroke-width', '1');
        })
        .on('mouseout', function(d) {
            d3.select(this)
                .style('stroke', 'none');
        });
};

var genScore2Feature = function(svg, dict, width, height) {
    var score2Feature = svg.selectAll('.score2Feature')
        .data([1, 2, 3, 4, 5])
        .enter()
        .append('g')
        .attr('class', 'score2Feature')
        .each(function(d, i) {
            genScore2FeatureEdge(dict[d + '.0'], d, this, width, height);
        });

    function genScore2FeatureEdge(dict, score, _this, width, height) {
        var min = 0;
        var max = 0;
        var featuresList = [];
        for (var key in dict) {
            if (dict.hasOwnProperty(key)) {
                if (features2Index[key] != undefined) {
                    var tElement = {};
                    tElement['feature'] = key;
                    tElement['sentiment'] = dict[key];
                    if (dict[key] > max)
                        max = dict[key];
                    if (dict[key] < min)
                        min = dict[key];
                    featuresList.push(tElement);
                }
            }
        }

    var edgeColor = d3.scale.ordinal().domain([min, max])
    .range(['#2166ac', '#4393c3', '#92c5de', '#d1e5f0', 'grey', '#fddbc7', '#f4a582', '#d6604d', '#b2182b']);

        var edges = d3.select(_this)
            .selectAll('.score2FeatureEdge')
            .data(featuresList)
            .enter()
            .append('line')
            .attr('class', 'score2FeatureEdge')
            .attr('x1', (width - 3) / 4 * (score - 1))
            .attr('y1', height / 2)
            .attr('x2', function(d) {
                return (width - 3) / (features.length - 1) * features2Index[d['feature']];
            })
            .attr('y2', height - 30)
            .style('stroke-opacity', 0.5)
            .style('stroke-width', 1)
            .style('stroke', function(d) {
                var sentiment = d['sentiment'];
                return edgeColor(sentiment);
            });
    }
};

var genScoreCircle = function(svg, width, height) {
     svg.selectAll('.scoreCircle')
        .data([1, 2, 3, 4, 5])
        .enter()
        .append('circle')
        .attr('class', 'scoreCircle')
        .attr('cx', function(d, i) {
            return (width - 3) / 4 * i;
        })
        .attr('cy', height / 2)
        .attr('r', 4)
        .style('fill', 'grey')
        .style('fill-opacity', 0.8)
        .on('mouseover', function(d, i) {
            var xPos = (width - 3) / 4 * i;
            d3.select(this)
                .style('fill', 'black');

            d3.selectAll('.score2FeatureEdge')
                .style('stroke-opacity', function(d) {
                    var x1 = d3.select(this).attr('x1');
                    console.log(xPos);
                    console.log(x1);
                    if (x1 == xPos)
                        return 0.8;
                    else
                        return 0.05;
                });
            svg.append('text')
                .attr('class', 'scoreText')
                .attr('x', (width - 3) / 4 * i)
                .attr('y', height / 2)
                .attr('dx', -2)
                .attr('dy', 25)
                .attr('fill', 'black')
                .style('text-anchor', 'start')
                .text(d);

        })
        .on('mouseout', function(d, i) {
            d3.select(this)
                .style('fill', 'grey');
            d3.selectAll('.score2FeatureEdge')
                .style('stroke-opacity', 0.8);
            d3.selectAll('.scoreText')
                .data([])
                .exit()
                .remove();

        });
};

var genFeatureCircle = function(svg, width, height) {
    svg.selectAll('.featureCircle')
        .data(features)
        .enter()
        .append('circle')
        .attr('class', 'featureCircle')
        .attr('cx', function(d, i) {
            return (width - 3) / (features.length - 1) * i;
        })
        .attr('cy', height - 30)
        .attr('r', 4)
        .style('fill', 'grey')
        .style('fill-opacity', 0.8)
        .on('mouseover', function(d, i) {
            var xPos = (width - 3) / (features.length - 1) * i;
            d3.select(this)
                .style('fill', 'black');

            d3.selectAll('.score2FeatureEdge')
                .style('stroke-opacity', function(d) {
                    var x2 = d3.select(this).attr('x2');
                    if (x2 == xPos)
                        return 0.8;
                    else
                        return 0.05;
                });
            svg.append('text')
                .attr('class', 'featureText')
                .attr('x', (width - 3) / (features.length - 1) * i)
                .attr('y', height - 20)
                .attr('dx', -10)
                .attr('dy', 15)
                .attr('fill', 'black')
                .style('text-anchor', 'start')
                .text(d);
        })
        .on('mouseout', function(d, i) {
            d3.select(this)
                .style('fill', 'grey');
            d3.selectAll('.score2FeatureEdge')
                .style('stroke-opacity', 0.8);
            svg.selectAll('.featureText')
                .data([])
                .exit()
                .remove();
        });

    var featureTextG = svg.selectAll('featureTextG')
        .data(features)
        .enter()
        .append('g')
        .attr('class', 'featureTextG')
        .attr('transform', function(d, i) {
            return 'translate(' + ((width - 3) / (features.length - 1) * i )+ ',' + (height - 20) + ')rotate(-90)';
        });


};

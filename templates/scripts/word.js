var genWordCloud = function(name, feature, sentiment) {
    var fill = d3.scale.category20();
    var originalList = undefined;
    if (sentiment == 'positive') {
        originalList = product2Features[name][feature.join(' ')]['posAdj'];
    } else {
        originalList = product2Features[name][feature.join(' ')]['negAdj'];
    }
    var reduceDict = {};
    originalList.forEach(function(word, i) {
        if (reduceDict[word] == undefined) {
            reduceDict[word] = 0;
        }
        reduceDict[word] += 1;
    });
    var wordList = [];
    for (var key in reduceDict) {
        if (reduceDict.hasOwnProperty(key)) {
            var tElement = {};
            tElement['text'] = key;
            tElement['size'] = reduceDict[key];
            wordList.push(tElement);
        }
    }
    d3.layout.cloud().size([450, 350])
        .words(wordList)
        .padding(5)
        .rotate(function() { return ~~(Math.random() * 2) * 90; })
        .font('Impact')
        .fontSize(function(d) { return 10 + d.size / 1.2; })
        .on('end', draw)
        .start();

        function draw(words) {
            d3.select('#word-cloud')
                .select('svg')
                .data([])
                .exit()
                .remove();

            d3.select('#word-cloud').append('svg')
                .attr('width', 450)
                .attr('height', 350)
                .style('display', 'block')
                .style('margin', '0px auto')
                .append('g')
                .attr('transform', 'translate(225, 175)')
                .selectAll('text')
                .data(words)
                .enter().append('text')
                .style('font-size', function(d) {
                    return 10 + d.size / 1.2 + 'px';
                })
                .style('font-family', 'Impact')
                .style('fill', function(d, i) { return fill(i); })
                .style('fill-opacity', 0.7)
                .attr('text-anchor', 'middle')
                .attr('transform', function(d) {
                    return 'translate(' + [d.x, d.y] +
                        ')rotate(' + d.rotate + ')';
                })
            .text(function(d) { return d.text; });
        }
};

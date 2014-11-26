var margin = {top: 80, right: 0, bottom: 10, left: 80},
    width = 720,
    height = 240;

var currentFeatures = [];
var names = [];
var matrix = [];
var product2Features = {};
var max = 0;

var radius = d3.scale.log();
var x = d3.scale.ordinal().rangeBands([0, height]);
var y = d3.scale.ordinal().rangeBands([0, width]);
var positiveColor = d3.scale.ordinal().domain([0.75, 1.75]).range(['#fddbc7', '#f4a582', '#d6604d', '#b2182b']);
var negativeColor = d3.scale.ordinal().domain([0.75, 1.75]).range(['#d1e5f0', '#92c5de', '#4393c3', '#2166ac']);
    //z = d3.scale.linear().domain([0, 4]).clamp(true),
    //c = d3.scale.category10().domain(d3.range(10));

var svg = d3.select('body').append('svg')
    .attr('width', width + margin.left + margin.right)
    .attr('height', height + margin.top + margin.bottom)
    .style('margin-left', -margin.left + 'px')
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

var genFeatures = function(data) {
    var featuresDict = {};
    var featureList = [];
    data.forEach(function(element, i) {
        var featureInfo = element['featureInfo'];
        var name = element.productName;
        for (var i = 0; i < featureInfo.length; i++) {
            var featureName = featureInfo[i].feature.join(' ');
            if (featuresDict[featureName] == undefined) {
                featuresDict[featureName] = 1;
                featureList.push(featureName);
            }
            if (product2Features[name] == undefined) {
                product2Features[name] = {};
            }
            product2Features[name][featureName] = featureInfo[i];
            if (featureInfo[i]['positive_review_Num'] > max)
                max = featureInfo[i]['positive_review_Num'];
            if (featureInfo[i]['negative_review_Num'] > max)
                max = featureInfo[i]['negative_review_Num'];
        }
    });
    return featureList;
};

var updateBackground = function() {
    d3.select('.background')
      .attr('width', x.rangeBand() * currentFeatures.length);
}

var updateColumn = function() {
    var column = svg.selectAll('.column')
        .data(currentFeatures)
        .enter().append('g')
        .attr('class', 'column')
        .attr('transform', function(d, i) { return 'translate(' + x.rangeBand() * i + ')rotate(-90)'; });

    column.append('line')
        .attr('x1', -width);

    column.append('text')
        .attr('x', 6)
        .attr('y', x.rangeBand() / 2)
        .attr('dy', '.32em')
        .attr('text-anchor', 'start')
        .text(function(d, i) { return d; });
};

d3.json('review.json', function(data) {
  var features = [];

  // Compute index per node.
  data.forEach(function(element, i) {
    names.push(element.productName);
    //matrix[i] = d3.range(data[0].length - 1).map(function(j) { return {}; });
    matrix[i] = [];
  });

  features = genFeatures(data);

  features.sort();

  var _select = $('<select>');
  $.each(features, function(index, element) {
      _select.append(
          $('<option></option>').val(element).html(element)
      );
  });
  $('#feature').append(_select.html());

  $('#addFeature').click(function() {
    var selectedFeature = $('#feature').val();
    var flag = false
    currentFeatures.forEach(function(element) {
        if (element == selectedFeature) {
            flag = true;
        }
    });
    if (flag)
      return;
    matrix.forEach(function(row, i) {
        var feature = product2Features[names[i]][selectedFeature];
        if (feature == undefined)
            matrix[i].push({});
        else
            matrix[i].push(feature);
    });
    currentFeatures.push(selectedFeature);
    updateBackground();
    updateColumn();

    var rows = d3.selectAll('.row');
    rows.each(function(row) {
        var uppers = d3.select(this).selectAll('.upperCell')
            .data(row)
            .enter().append('path')
            .attr('class', 'upperCell')
            .attr('d', function(d, i) {
                var half = x.rangeBand() / 2;
                if (d['positive_review_Num'] != undefined) {
                    console.log(d['positive_review_Num']);
                    var r = radius(d['positive_review_Num']);
                    console.log(r);
                } else {
                    var r = x.rangeBand() / 3;
                }
                var stX = x.rangeBand() * i + (half - r);
                var stY = x.rangeBand() / 2;
                var edX = x.rangeBand() * (i + 1) - (half - r);
                var edY = x.rangeBand() / 2;
                var path = 'M ' + stX + ' ' + stY + ' ';
                path = path + 'A ';
                path = path + r + ' ' + r + ' ';
                path = path + ' 0';
                path = path + ' 0';
                path = path + ' 1';
                path = path + ' ' + edX + ' ' + edY + ' ';
                path = path + 'Z';
                return path;
            })
            .attr('fill', function(d) {
                if (d.feature == undefined) {
                    return 'white';
                } else {
                    return positiveColor(d['positiveVal'] * 1.0 / d['posNum']);
                }
            });
        var bottom = d3.select(this).selectAll('.buttomCell')
            .data(row)
            .enter().append('path')
            .attr('class', 'buttomCell')
            .attr('d', function(d, i) {
                var half = x.rangeBand() / 2;
                if (d['negative_review_Num'] != undefined) {
                    var r = radius(d['negative_review_Num']);
                } else {
                    var r = x.rangeBand() / 3;
                }
                var stX = x.rangeBand() * i + (half - r);
                var stY = x.rangeBand() / 2;
                var edX = x.rangeBand() * (i + 1) - (half - r);
                var edY = x.rangeBand() / 2;
                var path = 'M ' + stX + ' ' + stY + ' ';
                path = path + 'A ';
                path = path + r + ' ' + r + ' ';
                path = path + ' 0';
                path = path + ' 0';
                path = path + ' 0';
                path = path + ' ' + edX + ' ' + edY + ' ';
                path = path + 'Z';
                return path;
            })
            .attr('fill', function(d) {
                if (d.feature == undefined) {
                    return 'white';
                } else {
                    return negativeColor(d['negativeVal'] * 1.0 / d['negNum']);
                }
            });

    });

  });

  // Precompute the orders.
  //var orders = {
    //name: d3.range(n).sort(function(a, b) { return d3.ascending(nodes[a].name, nodes[b].name); }),
    //count: d3.range(n).sort(function(a, b) { return nodes[b].count - nodes[a].count; }),
    //group: d3.range(n).sort(function(a, b) { return nodes[b].group - nodes[a].group; })
  //};

  // The default sort order.
  x.domain(names);
  radius.domain([1, max]).range([5, x.rangeBand() / 3]);

  svg.append('rect')
      .attr('class', 'background')
      .attr('width', x.rangeBand() * currentFeatures.length)
      .attr('height', height);

  var row = svg.selectAll('.row')
      .data(matrix)
      .enter().append('g')
      .attr('class', 'row')
      .attr('transform', function(d, i) { return 'translate(0,' + x(i) + ')'; })
      .each(row);

  row.append('line')
      .attr('x2', width);

  row.append('text')
      .attr('x', -6)
      .attr('y', x.rangeBand() / 2)
      .attr('dy', '.32em')
      .attr('text-anchor', 'end')
      .text(function(d, i) { return names[i]; });

  updateColumn();

  function row(row) {
    var cell = d3.select(this).selectAll('.upperCell')
        .data(row)
        .enter().append('circle')
        .attr('class', 'upperCell')
        .attr('cx', function(d) { return x(d.x) + x.rangeBand() / 2; })
        .attr('cy', function(d) { return x(d.y) + x.rangeBand() / 2; })
        .attr('r', x.rangeBand() / 3);
        //.style('fill', function(d) { return nodes[d.x].group == nodes[d.y].group ? c(nodes[d.x].group) : null; })
  }

  function mouseover(p) {
    d3.selectAll('.row text').classed('active', function(d, i) { return i == p.y; });
    d3.selectAll('.column text').classed('active', function(d, i) { return i == p.x; });
  }

  function mouseout() {
    d3.selectAll('text').classed('active', false);
  }

  //d3.select('#order').on('change', function() {
    //clearTimeout(timeout);
    //order(this.value);
  //});

  //function order(value) {
    //x.domain(orders[value]);

    //var t = svg.transition().duration(2500);

    //t.selectAll('.row')
        //.delay(function(d, i) { return x(i) * 4; })
        //.attr('transform', function(d, i) { return 'translate(0,' + x(i) + ')'; })
      //.selectAll('.cell')
        //.delay(function(d) { return x(d.x) * 4; })
        //.attr('x', function(d) { return x(d.x); });

    //t.selectAll('.column')
        //.delay(function(d, i) { return x(i) * 4; })
        //.attr('transform', function(d, i) { return 'translate(' + x(i) + ')rotate(-90)'; });
  //}

  //var timeout = setTimeout(function() {
    //order('group');
    //d3.select('#order').property('selectedIndex', 2).node().focus();
  //}, 5000);
});



var initScores = function(data) {
    data.forEach(function(product, i) {
        var featureVis = product['featureVis'];
        var name = product['productName'];
        product2Scores[name] = {};
        reviews2Scores[name] = {};
        featureVis.forEach(function(review, j) {
            var reviewScore = review['score'];
            var sentiment = review['sentiment'];
            if (product2Scores[name][reviewScore] == undefined) {
                product2Scores[name][reviewScore] = {};
            }
            if (reviews2Scores[name][sentiment] == undefined) {
                reviews2Scores[name][sentiment] = {};
                reviews2Scores[name][sentiment]['count'] = 0;
            }
            if (reviews2Scores[name][sentiment][reviewScore] == undefined) {
                reviews2Scores[name][sentiment][reviewScore] = 0;
            }
            reviews2Scores[name][sentiment]['count'] += 1;
            reviews2Scores[name][sentiment][reviewScore] += 1;
            var tFeatures = review['features'];
            for (var index in tFeatures) {
                if (tFeatures.hasOwnProperty(index)) {
                    for (var key in tFeatures[index]) {
                        if (tFeatures[index].hasOwnProperty(key)) {
                            var tPos = tFeatures[index][key]['pos'];
                            var tNeg = tFeatures[index][key]['neg'];
                            var senti = tPos - tNeg;
                            if (product2Scores[name][reviewScore][key] == undefined) {
                                product2Scores[name][reviewScore][key] = 0;
                            }
                            product2Scores[name][reviewScore][key] += senti;
                        }
                    }
                }
            }
        });
    });
};

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
    featureList.forEach(function(d, i) {
        features2Index[d] = i;
    });
    return featureList;
};

var updateBackground = function() {
    d3.select('.background')
      .attr('width', x.rangeBand() * currentFeatures.length);
};

var updateRow = function(row, _this, index) {
    var uppers = d3.select(_this).selectAll('.upperCell')
        .data(row)
        .attr('d', function(d, i) {
            var half = x.rangeBand() / 2;
            if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
                var r = radius(d['positive_review_Num']);
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
        if (d['positive_review_Num'] == undefined || d['positive_review_Num'] == 0) {
            return 'white';
        } else {
            return positiveColor(d['positiveVal'] * 1.0 / d['posNum']);
        }
    })
    .style('cursor', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
            return 'pointer';
        } else {
            return 'default';
        }
    })
    .on('mouseover', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0)  {
            d3.select(this)
        .attr('stroke', 'grey')
        .attr('stroke-width', '2px');
        }
    })
    .on('mouseout', function() {
        d3.select(this)
        .attr('stroke', 'none');
    })
    .on('click', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
            genWordCloud(names[index], d['feature'], 'positive');
        }
    });

    uppers.enter().append('path')
        .attr('class', 'upperCell')
        .attr('d', function(d, i) {
            var half = x.rangeBand() / 2;
            if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
                var r = radius(d['positive_review_Num']);
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
        if (d['positive_review_Num'] == undefined || d['positive_review_Num'] == 0) {
            return 'white';
        } else {
            return positiveColor(d['positiveVal'] * 1.0 / d['posNum']);
        }
    })
    .style('cursor', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
            return 'pointer';
        } else {
            return 'default';
        }
    })
    .on('mouseover', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
            d3.select(this)
        .attr('stroke', 'grey')
        .attr('stroke-width', '2px');
        }
    })
    .on('mouseout', function() {
        d3.select(this)
        .attr('stroke', 'none');
    })
    .on('click', function(d) {
        if (d['positive_review_Num'] != undefined && d['positive_review_Num'] != 0) {
            genWordCloud(names[index], d['feature'], 'positive');
        }
    });

    var bottom = d3.select(_this).selectAll('.buttomCell')
        .data(row)
        .attr('d', function(d, i) {
            var half = x.rangeBand() / 2;
            if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
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
        if (d['negative_review_Num'] == undefined || d['negative_review_Num'] == 0) {
            return 'white';
        } else {
            return negativeColor(d['negativeVal'] * 1.0 / d['negNum']);
        }
    })
    .style('cursor', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            return 'pointer';
        } else {
            return 'default';
        }
    })
    .on('mouseover', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            d3.select(this)
        .attr('stroke', 'grey')
        .attr('stroke-width', '2px');
        }
    })
    .on('mouseout', function() {
        d3.select(this)
        .attr('stroke', 'none');
    })
    .on('click', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            genWordCloud(names[index], d['feature'], 'negative');
        }
    });

    bottom.enter().append('path')
        .attr('class', 'buttomCell')
        .attr('d', function(d, i) {
            var half = x.rangeBand() / 2;
            if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
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
        if (d['negative_review_Num'] == undefined || d['negative_review_Num'] == 0) {
            return 'white';
        } else {
            return negativeColor(d['negativeVal'] * 1.0 / d['negNum']);
        }
    })
    .style('cursor', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            return 'pointer';
        } else {
            return 'default';
        }
    })
    .on('mouseover', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            d3.select(this)
        .attr('stroke', 'grey')
        .attr('stroke-width', '2px');
        }
    })
    .on('mouseout', function() {
        d3.select(this)
        .attr('stroke', 'none');
    })
    .on('click', function(d) {
        if (d['negative_review_Num'] != undefined && d['negative_review_Num'] != 0) {
            genWordCloud(names[index], d['feature'], 'negative');
        }
    });

    uppers.exit().remove();
    bottom.exit().remove();
};

var updateColumn = function() {
    var columnText = svg.selectAll('.column text')
        .data(currentFeatures)
        .text(function(d, i) {
            return d;
        });

    var column = svg.selectAll('.column')
        .data(currentFeatures);

    var columnG = column.enter().append('g')
        .attr('class', 'column')
        .attr('transform', function(d, i) { return 'translate(' +
                    x.rangeBand() * i + ')rotate(-90)'; });

    columnG.append('line')
        .attr('x1', -width);

    columnG.append('text')
        .attr('x', 6)
        .attr('y', x.rangeBand() / 2)
        .attr('dy', '.32em')
        .attr('text-anchor', 'start')
        .text(function(d, i) { return d; });

    column.exit().remove();
};

var updateMatrix = function(checked, selectedFeature) {
    if (checked) {
        matrix.forEach(function(row, i) {
            var feature = product2Features[names[i]][selectedFeature];
            if (feature == undefined)
                matrix[i].push({});
            else
                matrix[i].push(feature);
        });
        currentFeatures.push(selectedFeature);
    } else {
        var index = undefined;
        for (var i = 0; i < currentFeatures.length; i++) {
            if (currentFeatures[i] == selectedFeature) {
                index = i;
                currentFeatures.splice(i, 1);
                break;
            }
        }
        matrix.forEach(function(row, i) {
            matrix[i].splice(index, 1);
        });
    }
};

var featureChange = function(option, checked) {
    var selectedFeature = option.val();
    updateMatrix(checked, selectedFeature);
    updateBackground();
    updateColumn();

    var rows = d3.selectAll('.pRow');
    rows.each(function(row, i) {
        updateRow(row, this, i);
    });
};
var genProductCompare = function() {
    d3.json('../data/earphone.json', function(data) {
        // Compute index per node.
        data.forEach(function(element, i) {
            names.push(element.productName);
            matrix[i] = [];
        });

        features = genFeatures(data);
        initScores(data);

        features.sort();

        var _select = $('<select>');
        $.each(features, function(index, element) {
            _select.append(
                $('<option></option>').val(element).html(element)
            );
        });
        $('#feature').append(_select.html());
        $('#feature').multiselect({
            'onChange': featureChange
        });

        x.domain(names);

        radius.domain([1, max]).range([5, x.rangeBand() / 2]);
        svg.append('rect')
            .attr('class', 'background')
            .attr('width', x.rangeBand() * currentFeatures.length)
            .attr('height', height);

        var row = svg.selectAll('.pRow')
            .data(matrix)
            .enter().append('g')
            .attr('class', 'pRow')
            .attr('transform', function(d, i) {
                return 'translate(0,' + x(i) + ')';
            });

        row.append('line')
            .attr('x2', width);

        row.append('text')
            .attr('class', 'productText')
            .attr('x', -6)
            .attr('y', x.rangeBand() / 2)
            .attr('dy', '.32em')
            .attr('text-anchor', 'end')
            .attr('cursor', 'pointer')
            .text(function(d, i) { return names[i]; })
            .on('mouseover', function() {
                d3.select(this)
                    .style('fill', '#FDE3C0');
            })
            .on('mouseout', function() {
                d3.select(this)
                    .style('fill', 'black');
            })
            .on('click', function(d, i) {
                d3.selectAll('.productText')
                    .style('font-weight', 'normal');
                d3.select(this)
                    .style('font-weight', 800);
                genReviewScore(names[i]);
            });
        updateColumn();
    });
};

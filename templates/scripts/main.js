var margin = {top: 80, right: 0, bottom: 10, left: 80},
    width = 720,
    height = 240;

var names = [];
var matrix = [];
var currentFeatures = [];
var features = [];
var features2Index = {};
var product2Features = {};
var product2Scores = {};
var reviews2Scores = {};
var max = 0;

var radius = d3.scale.log();
var x = d3.scale.ordinal().rangeBands([0, height]);
var y = d3.scale.ordinal().rangeBands([0, width]);
var positiveColor = d3.scale.ordinal().domain([0.75, 1.75])
    .range(['#fddbc7', '#f4a582', '#d6604d', '#b2182b']);
var negativeColor = d3.scale.ordinal().domain([0.75, 1.75])
    .range(['#d1e5f0', '#92c5de', '#4393c3', '#2166ac']);

var svg = d3.select('#canvas').append('svg')
    .attr('width', width + margin.top + margin.bottom)
    .attr('height', height + margin.left + margin.right)
    .append('g')
    .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

genProductCompare();

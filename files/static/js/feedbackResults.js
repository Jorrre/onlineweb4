var chartData;
var fosChart;
var ratingCharts = new Array();

function printPieChart()
{
    data = chartData.replies.fos;
    fosChart = jQuery.jqplot ('field-of-study-chart', [data], 
    {
        grid: {
            drawBorder: false, 
            drawGridlines: false,
            background: '#ffffff',
            shadow:false
        },
        seriesDefaults: 
        {
            renderer: jQuery.jqplot.PieRenderer, 
            rendererOptions: 
            {
                showDataLabels: true,
                dataLabels: 'value',
                sliceMargin: 10
            }
        }, 
        legend: 
        { 
            show:true, 
            location: 'e',
            fontSize: '15pt',
            border: 'none'
        }
    });
}

function printRatingCharts()
{
    data = chartData.replies.ratings;
    titles = chartData.replies.titles;
    for(var i = 0; i < titles.length; i++)
    {   
        box = '<div class="col-md-6 rating-chart"><div id="rating-chart-' + i + '"></div></div>'
        $('#ratings').append(box);
        ticks = Array.range(1, data[i].length, 1);
        title = titles[i];
        ratingCharts[i] = $.jqplot('rating-chart-' + i, [data[i]], 
        {
            title: title,
            seriesDefaults:
            {
                renderer:$.jqplot.BarRenderer,
                pointLabels: 
                {
                    show: true, 
                    hideZeros: true,
                    formatString: '%d',
                }
            },
            axes: 
            {
                xaxis: 
                {
                    renderer: $.jqplot.CategoryAxisRenderer,
                    ticks: ticks,
                },
                yaxis:
                {
                    tickOptions: { show: false}
                },
            },
            grid: 
            { 
                gridLineColor: '#FFF',
                drawBorder: false,    
            }
        });
    }
}

Array.range= function(a, b, step){
    var A= [];
    if(typeof a== 'number'){
        A[0]= a;
        step= step || 1;
        while(a+step<= b){
            A[A.length]= a+= step;
        }
    }
    else{
        var s= 'abcdefghijklmnopqrstuvwxyz';
        if(a=== a.toUpperCase()){
            b=b.toUpperCase();
            s= s.toUpperCase();
        }
        s= s.substring(s.indexOf(a), s.indexOf(b)+ 1);
        A= s.split('');        
    }
    return A;
}

$(document).ready(function()
{
    $.get($(location).attr('href') + "chartdata", function(data)
    {
        chartData = data;
        printPieChart();
        printRatingCharts();
    });
    $(window).on("debouncedresize", function(e)
    {
        fosChart.replot({ resetAxes: true});
        for(var i = 0; i < ratingCharts.length; i++)
        {
            ratingCharts[i].destroy();
        }
        printRatingCharts();
    });
});
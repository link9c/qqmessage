$(function () {
    window.onload = function () {
        $.ajax({
            url: "heat",
            data: {
                'group_id': $('select').val()
            },
            method: "post",
            // processData: false,
            success: function (res) {
                if (res.code === 0) {
                    console.log(res);
                    set_echarts(res.resp);
                    //    成功了
//                    window.open(res.data.url);
                } else {
                    alert("网络问题，请稍后尝试！");
                }
            }
        })
    };

    $('select').change(function () {
        $.ajax({
            url: "heat",
            data: {
                'group_id': $('select').val()
            },
            method: "post",
            // processData: false,
            success: function (res) {
                if (res.code === 0) {
                    console.log(res);
                    set_echarts(res.resp);
                    //    成功了
//                    window.open(res.data.url);
                } else {
                    alert("网络问题，请稍后尝试！");
                }
            }
        })
    });


    function set_echarts(resp) {
        var myChart = echarts.init(document.getElementById('main'));
        var hours = ['0', '1', '2', '3', '4', '5', '6',
            '7', '8', '9', '10', '11',
            '12', '13', '14', '15', '16', '17',
            '18', '19', '20', '21', '22', '23'];
        var days = ['周一', '周二', '周三',
            '周四', '周五', '周六', '周日'];


        data = resp.data.map(function (item) {
            return [item[1], item[0], item[2] || '-'];
        });

        option = {
            title: {
                text: resp.title,
                left: 'center',
                top: '3%'
            },
            tooltip: {
                position: 'top'
            },
            animation: false,
            grid: {
                height: '50%',
                top: '10%'
            },
            xAxis: {
                type: 'category',
                data: hours,
                splitArea: {
                    show: true
                }
            },
            yAxis: {
                type: 'category',
                data: days,
                splitArea: {
                    show: true
                }
            },
            visualMap: {
                min: 0,
                max: 300,
                calculable: true,
                orient: 'horizontal',
                left: 'center',
                bottom: '25%'
            },
            series: [{
                name: '发言数量',
                type: 'heatmap',
                data: data,
                label: {
                    show: true
                },
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }]
        };
        myChart.setOption(option);
    }


})
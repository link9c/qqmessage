$(function () {
    window.onload = function () {
        $.ajax({
            url: "line",
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
            url: "line",
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
        var myChart = echarts.init(document.getElementById('line_bar'));
        option = {
            title: {
                left: 'center',
                text: '每日发送信息折线图',
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'cross',
                    label: {
                        backgroundColor: '#6a7985'
                    }
                }
            },

            dataZoom: [{
                type: 'inside',
                start: 0,
                end: 65
            }, {
                start: 0,
                end: 10,
                handleIcon: 'M10.7,11.9v-1.3H9.3v1.3c-4.9,0.3-8.8,4.4-8.8,9.4c0,5,3.9,9.1,8.8,9.4v1.3h1.3v-1.3c4.9-0.3,8.8-4.4,8.8-9.4C19.5,16.3,15.6,12.2,10.7,11.9z M13.3,24.4H6.7V23h6.6V24.4z M13.3,19.6H6.7v-1.4h6.6V19.6z',
                handleSize: '80%',
                handleStyle: {
                    color: '#fff',
                    shadowBlur: 3,
                    shadowColor: 'rgba(0, 0, 0, 0.6)',
                    shadowOffsetX: 2,
                    shadowOffsetY: 2
                }
            }],
            xAxis: {
                type: 'category',
                data: resp.date
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '发送信息数量',
                    type: 'line',
                    data: resp.msg_num,
                    label: {
                        show: true, //开启显示
                        position: 'top', //在上方显示
                        textStyle: { //数值样式
                            color: 'black',
                            fontSize: 16
                        }
                    }
                },

            ]
        };


        myChart.setOption(option);
    }


})

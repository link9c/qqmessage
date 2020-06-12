$(function () {

    function change_bar() {
        $.ajax({
            url: "bar",
            data: {
                'group_id': $('select').val(),
                'date': $('#meeting').val()
            },
            method: "post",
            // processData: false,
            success: function (res) {
                if (res.code === 0) {
                    if (res.resp.nums && res.resp.users) {
                        order_bar(res.resp);
                        detail_bar(res.resp);
                    }
                    console.log(res);

                    //    成功了
//                    window.open(res.data.url);
                } else {
                    alert("网络问题，请稍后尝试！");
                }
            }
        })
    }



    window.onload = function () {
        change_bar();
    };

    $('select').change(function () {
        change_bar()
    });

    $('#meeting').change(function () {
        change_bar()
    });


    function detail_bar(resp) {
        var myChart = echarts.init(document.getElementById('stack_bar'));
        option = {
            title: {
                text: '信息分类',
                subtext: '一条信息可能有多个图片，@等',
                left: 'center',

            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                    type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                }
            },
            // legend: {
            //     data: ['表情', '@', '图片', '语音', '文字'],
            //     right:'110%',
            //     top:'70%'
            // },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value'
            },
            yAxis: {
                type: 'category',
                data: resp.users
            },
            series: [
                {
                    name: '表情',
                    type: 'bar',
                    stack: '总量',
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true,
                        position: 'insideRight'
                    },
                    data: resp.nums[0]
                },
                {
                    name: '@',
                    type: 'bar',
                    stack: '总量',
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true,
                        position: 'insideRight'
                    },
                    data: resp.nums[1]
                },
                {
                    name: '图片',
                    type: 'bar',
                    stack: '总量',
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true,
                        position: 'insideRight'
                    },
                    data: resp.nums[2]
                },
                {
                    name: '语音',
                    type: 'bar',
                    stack: '总量',
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true,
                        position: 'insideRight'
                    },
                    data: resp.nums[3]
                },
                {
                    name: '文字',
                    type: 'bar',
                    stack: '总量',
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true,
                        position: 'insideRight'
                    },
                    data: resp.nums[4]
                }
            ]
        };
        myChart.setOption(option);
        window.onresize = myChart.resize;
    }

    function order_bar(resp) {
        var myChart = echarts.init(document.getElementById('bar'));
        option = {
            color: ['#57b4c2'],
            title: {
                text: '信息数量排名',
                subtext: '按照发送条数统计',
                left: 'center',
                // top:10

            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },

            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'value',
                // boundaryGap: [0, 0.01]
            },
            yAxis: {
                type: 'category',
                data: resp.users
            },
            series: [
                {
                    name: '发言数量',
                    type: 'bar',
                    data: resp.msg_num,
					barWidth:30,
					barMaxWidth:30,
					barGap:5,
                    label: {
                        show: true, //开启显示
                        position: 'right', //在上方显示
                        textStyle: { //数值样式
                            color: 'black',
                            fontSize: 16
                        }
                    }

                }
            ]
        };

        myChart.setOption(option);
        window.onresize = myChart.resize;
    }


})
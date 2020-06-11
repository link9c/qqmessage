var dataCloud = {
    "cloudData":
        [
            {"name":"澎湃","value":"25"},
            {"name":" 暴晒","value":" 14"},
            {"name":" 套件","value":"13"},
            {"name":" 有","value":" 24"},
            {"name":" 驾驶","value":" 30"},
            {"name":" 满满","value":" 1"},
            {"name":" 行驶","value":" 2"},
            {"name":" 强烈","value":"3"},
            {"name":" 轻盈","value":"8"},
            {"name":" 沉稳","value":"5"},
            {"name":" 1800公里","value":" 1"},
            {"name":" 低","value":" 2"},
            {"name":" 双","value":" 18"},
            {"name":" 前后","value":" 18"},
            {"name":" 跑车","value":" 1"},
            {"name":" 互联","value":" 22"},
            {"name":" 哪","value":" 23"},
            {"name":" 说","value":" 31"},
            {"name":" 全面","value":" 15"},
            {"name":" 搞定","value":" 12"}
        ],
    "cloudDiv":"main"
};

var createRandomItemStyle1 = function (params) {　　　　//此方法与下方配置中的第一个textStle下的color等同
    var colors = ['#fda67e', '#81cacc', '#cca8ba', "#88cc81", "#82a0c5", '#fddb7e', '#735ba1', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
    return colors[parseInt(Math.random() * 10)];
}

var createRandomItemStyle2 = function () {
    var colorArr = ['#fda67e', '#81cacc', '#cca8ba', "#88cc81", "#82a0c5", '#fddb7e', '#735ba1', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
    var flag = parseInt(Math.random() * 10);
    return {
        normal: {
            fontFamily: '微软雅黑',
            color:colorArr[flag]
        }
    };
}
function _setWordCloud (cloudData) {
    var option = {
        series: [
            {
                type: 'wordCloud',
                shape: 'ellipse',
                gridSize: 8,
                textStyle: {
                    normal: {
                        fontFamily: '微软雅黑',
                        color: function () {
                            var colors = ['#fda67e', '#81cacc', '#cca8ba', "#88cc81", "#82a0c5", '#fddb7e', '#735ba1', '#bda29a', '#6e7074', '#546570', '#c4ccd3'];
                            return colors[parseInt(Math.random() * 10)];
                        }
                    }
                },

                /*注释一：*/
                // textStyle:createRandomItemStyle2(),


                /*注释二：*/
                /*textStyle: {
                normal: {
                        fontFamily: '微软雅黑',
                        color: createRandomItemStyle1()
                    }
                },*/
                data: cloudData
            }
        ]
    };
    return option;
};

//词云图初始化
function initWordCloud(wordCloudData) {
    var option = _setWordCloud(wordCloudData.cloudData);
    var myChart = echarts.init(document.getElementById(wordCloudData.cloudDiv));
    myChart.setOption(option);
}

initWordCloud(dataCloud);


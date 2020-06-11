$(function () {
    $('#go-btn').on('click', function(e){
		e.preventDefault();

        var secretNum = $('.form-secret').val();
        console.log(secretNum);
		$.ajax({
            url: "/",
            data: {
                'secretNum': secretNum
            },
            method: "post",
            success: function (res) {
                if (res.code === 0) {
                   window.location = res.msg;
                } else {
                    $('.error-response').html('神秘字符错误！！！');
                }
            }
        })
	});

});
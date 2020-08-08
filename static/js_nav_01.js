$(function(){
    $(".login_1").click(function () {
        $(".login_2").stop().fadeIn(100);
    });
    // 2.监听关闭按钮的点击
    $(".close_1").click(function () {
        $(".login_2").stop().fadeOut(100);
    });
     $(".close_2").click(function () {
        $(".login_2").stop().fadeOut(100);
    });

});
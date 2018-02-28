$(function(){ 
  "use strict";
        $("#toTop").click(function(){
      var speed=400;//滑动的速度
        $("body").animate({scrollTop:0},speed);
    });
  });
  $(window).scroll(function () {
         var device_width=$(window).width();
         if(device_width>768) {
        if ($(this).scrollTop() > 200) {   //scrollTop() 方法返回或设置匹配元素的滚动条的垂直位置。
            $('#toTop').fadeIn(); 
        } else {
            $('#toTop').fadeOut();
        }}
    });  

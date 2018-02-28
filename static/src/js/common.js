 $(function(){ 
  "use strict";
      window.onresize=resizeBannerImage;//当窗口改变宽度时执行此函数
        $("#toTop").click(function(){
      var speed=400;//滑动的速度
        $("body").animate({scrollTop:0},speed);
    });
  });
  function resizeBannerImage()
      {
        var winW = $(window).width();
        if( $(window).width() <= 768 ) {
            $('.navbar-default').css('background-color','rgba(52,141,217,1)'); 
            $('.navbar-default').css('background-image','linear-gradient(160deg, #34b6d9, #3464d9)'); 
            $('.navbar-default').css('background-repeat','repeat-x'); 
        }
        else{
            $('.navbar-default').css('background-color','rgba(52,141,217,0)'); 
            $('.navbar-default').css('background-image','none'); 
            $('.navbar-default').css('background-repeat','none'); 
        }
      }
  $(window).scroll(function () {
         var device_width=$(window).width();
         if(device_width>768) {
        if ($(this).scrollTop() > 200) {   //scrollTop() 方法返回或设置匹配元素的滚动条的垂直位置。
            $('#toTop').fadeIn(); 
            $('.navbar-default').css('background-color','rgba(52,141,217,1)'); 
            $('.navbar-default').css('background-image','linear-gradient(160deg, #34b6d9, #3464d9)'); 
            $('.navbar-default').css('background-repeat','repeat-x'); 
        } else {
            $('#toTop').fadeOut();
            $('.navbar-default').css('background-color','rgba(52,141,217,0)'); 
            $('.navbar-default').css('background-image','none'); 
            $('.navbar-default').css('background-repeat','none'); 
        }
        }else{
            $('.navbar-default').css('background-color','rgba(52,141,217,1)'); 
            $('.navbar-default').css('background-image','linear-gradient(160deg, #34b6d9, #3464d9)'); 
            $('.navbar-default').css('background-repeat','repeat-x'); 
        }
    });  
 
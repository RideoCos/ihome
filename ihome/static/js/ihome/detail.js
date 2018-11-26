function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){



    $.get('/house/house_detail_info/', function(data){
        $(".house-price span").html(data["price"]);
        $(".house-title").html(data["title"]);
        $(".landlord-pic").html("<img src='/static/media/"+ data["user_avatar"] +"'>");
        $(".landlord-name span").html(data["user_name"]);
        $(".house-info-list:eq(0) li").html(data["address"]);
        $(".house-type li:eq(0) div h3").html("出租" + data["room_count"]+ "间");
        $(".house-type li:eq(0) div p:eq(0)").html("房屋面积" + data["acreage"]+ "平方米");
        $(".house-type li:eq(0) div p:eq(1)").html("房屋户型" + data["unit"]);
        $(".house-type li:eq(1) div h3").html("宜住" + data["capacity"] + "人");
        $(".house-type li:eq(2) div p").html(data["beds"]);
        $(".house-info-list:eq(1) li:eq(0) span").html(data["deposit"]+"元");
        $(".house-info-list:eq(1) li:eq(1) span").html(data["min_days"]);
        var maxdays = data["max_days"];
        if (data.max_days == 0){
            maxdays = '无限制';
        }
        $(".house-info-list:eq(1) li:eq(2) span").html(maxdays);
        for(var i=0;i<data["facilities"].length;i++){
            $(".house-facility-list").append("<li><span class='"+ data["facilities"][i]["css"] +"'></span>"+ data["facilities"][i]["name"] +"</li>");
        };
        $("div .house-info:eq(2)").hide();

        for(var i=0;i<data["images"].length;i++){
            $(".swiper-wrapper").append("<li class='swiper-slide'><img src='/static/media/"+ data["images"][i] +"'></li>");
        }
         var mySwiper = new Swiper ('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationType: 'fraction'
        });
        if(data["booking"] == 1){
            $(".book-house").show();
            $('.book-house').attr("href","/order/booking/"+ data["id"] + "/");
        }

    })
})

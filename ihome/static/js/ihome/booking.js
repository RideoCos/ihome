function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}
// 调用方法decodeQuery() 这个方法将url拆分成键值对
// 拆分链接为?page=1@name='aa'的形式

// 如果链接为/order/4/
// 直接用location.href.split('/')[下标]
// 注意：拆分链接为https://ip:port/order/booking/6/ 下标为[5]

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$(document).ready(function(){
//     var house_id = location.href.split('/')[5];

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg();
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共"+ days +"晚)");
        }
    });

     $.get('/order/booking_info/', function(data){
        $('.house-info>img').attr("src", "/static/media/"+data["image"]+"/");
        $('.house-info h3').html(data["title"]);
        $('.house-text>p>span').html(data["price"]);
    });
    var bookingId = location.href.split('/')[5];
    $('.submit-btn').click(function(){
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();
        if (startDate && endDate && startDate <= endDate) {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd)/(1000*3600*24) + 1;
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            var pData = {
                house_id:bookingId,
                begin_date:startDate,
                end_date:endDate,
                days:days,
                house_price:price,
                amount:amount
            }
            $.post('/order/order_add/', pData, function(data){
                if(data.code == 200){
                    alert("订单提交成功");
                }
                history.go(-2);
            });
        }else{
             showErrorMsg();
        }
    });

})

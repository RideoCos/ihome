$(document).ready(function(){
    $(".auth-warn").show();
})

$.get('/house/my_house_auth/', function(data){
    if(data.code == 200){
        $('.auth-warn').hide();
    }
    if(data.code == 2000){
        $('#houses-list').hide();
    }
})

$.get('/house/my_house_info/', function(data){
    for(var i=0;i<data.length;i++){
        $("#houses-list").append("<li><a href='/house/house_detail/"+
            data[i]["id"] +"/'><div class='house-title'><h3>房屋ID:"+
            data[i]["id"] +" —— "+ data[i]["title"] +
            "</h3></div><div class='house-content'>"+
            "<img src='/static/media/"+ data[i]["image"] +"'>"+
            "<div class='house-text'><ul><li>位于："+ data[i]["address"] +
            "</li><li>价格：￥"+ data[i]["price"] +"/晚</li><li>"+
            "发布时间："+ data[i]["create_time"] +"</li></ul></div></div></a></li>")

    }
})
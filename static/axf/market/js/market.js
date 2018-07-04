$(function () {
    // 点击全部类型时候,显示分类页面
    $('#all_type').click(function () {
        // console.log('全部类型');   测试点击能否生效
        $("#all_type_container").show();
        // 排序页面隐藏
        $('#sotr_rule_container').hide();
        // 排序箭头恢复初始方向
        $("#order_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
        // 点击改变箭头方向
        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
    });

    // 点击分类页面时候隐藏分类页面
    $('#all_type_container').click(function () {
        // 隐藏分类页面
        $(this).hide();
        // 箭头恢复初始方向
        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
        $("#order_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    });


    // 点击综合排序时显示排序页面
    $('#order_rule').click(function () {
        //console.log('综合排序');
        // 展示排序页面
        $('#sotr_rule_container').show();
        // 隐藏分类页面
        $('#all_type_container').hide();
        // 改变排序页面箭头方向
        $(this).find("span").find("span").removeClass("glyphicon-chevron-down").addClass("glyphicon-chevron-up");
        // 分类页面箭头恢复初始方向
        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    });


    // 点击排序页面时候隐藏排序页面
    $('#sotr_rule_container').click(function () {
        // 隐藏分类页面
        $(this).hide();
        // 箭头恢复初始方向
        $("#order_rule").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
        $("#all_type").find("span").find("span").removeClass("glyphicon-chevron-up").addClass("glyphicon-chevron-down");
    });


    //    添加到购物车
    $(".addShopping").click(function () {

        console.log("添加到购物车");

        var goods_id = $(this).attr("id");

        // console.log($(this).prop("goodsid"));

        // 参数可以直接进行拼接
        // 也可以使用第二个参数传递字典的形式进行参数设置  更推荐使用第二种
        $.getJSON("/axf/addtocart/", {"goods_id": goodsid}, function (data) {
            console.log(data);

            //    ajax请求回来之后的操作 写在这

        })

        // ajax 并行操作写在这
        // console.log("哈哈");

    })


});
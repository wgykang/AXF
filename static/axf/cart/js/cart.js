$(function () {
    // 点击选中商品或者取消选中商品
    $('.confirm').click(function () {
        let $confirm = $(this);

        // 查找父元素
        let cart_id = $confirm.parents('div').attr('id');
        console.log(cart_id);

        $.getJSON('/axf/changecartstatus/', {'cart_id': cart_id}, function (data) {
            console.log(data);
            if (data['status'] === '200') {
                if (data['is_select']) {
                    $confirm.find('span').find('span').html('√');
                    if(data["all_select"]){
                        $(".all_select span span").html("√");
                    }
                } else {
                    $confirm.find('span').find('span').html('');
                    // 当有一个商品未选中,全选不选中
                    $('.all_select span span').html('');
                }
                $("#total_price").html(data["total_price"]);
            }
        });
    });
    // 全选功能
    $('.all_select').click(function () {
        // 存放已选中商品ID
        let select_list = [];
        // 存放未选中的商品ID
        let un_select_list = [];
        $('.menuList').each(function () {
            let $menulist = $(this);
            let cart_id = $menulist.attr('id');
            let content = $menulist.find('.confirm span span').html();
            console.log(content);

            // trim去掉内容两端空格
            if (content.trim().length) {
                select_list.push(cart_id);
            } else {
                un_select_list.push(cart_id);
            }

        });
        console.log(select_list);
        console.log(un_select_list);


        // 未选中给服务器发送消息
        if (un_select_list.length) {
            $.getJSON('/axf/changecartliststatus/', {
                'action': 'select',
                'cart_list': un_select_list.join('#')
            }, function (data) {
                console.log(data);

                // 每个商品和全选都选中
                if (data['status'] === '200') {
                    $('.confirm span span').html('√');
                    $('.all_select span span').html('√');
                    $("#total_price").html(data["total_price"]);

                }

            })
            // 选中给服务器发送消息
        } else {
            $.getJSON('/axf/changecartliststatus/', {
                'action': 'unselect',
                'cart_list': select_list.join('#')
            }, function (data) {
                console.log(data);

                // 全选和所以商品取消选中
                if (data['status'] === '200') {
                    $('.confirm span span').html('');
                    $('.all_select span span').html('');
                    $("#total_price").html(data["total_price"]);
                }
            })
        }


    });


    // 购物车数量减少
    $('.subShopping').click(function () {
        let $sub = $(this);
        let cart_id = $sub.parents('.menuList').attr('id');
        console.log(cart_id);
        $.getJSON('/axf/sub/', {'cart_id': cart_id}, function (data) {
            console.log(data);
            if (data['status'] === '200') {
                if (data['goods_num'] > 0) {
                    $sub.next('button').html(data['goods_num'])
                } else {
                    $sub.parents('.menuList').remove();
                }
                $("#total_price").html(data["total_price"]);
            }
        })
    });
});
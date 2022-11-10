function get_data() {
    var result = null;
    $.ajax({
        url: '/get/',
        type: 'GET',
        async: false,
        success: function(response) {
            result = response;
        },
        error: function(error) {
            console.log(error);
        }
    });
    return result;
}

function set_data() {
    data = get_data();

    if (data !== null) {
        for (var i = 0; i < data.length; i++) {
            if (data[i][1] === "timeout") {
                // set image
                document.getElementsByClassName("thumbnail")[data[i][0] - 1].src = "/static/img/pj_room_desk/0.png";
                // set text
                document.getElementsByClassName("now_status")[data[i][0] - 1].innerHTML = "알 수 없음"
                document.getElementsByClassName("now_status")[data[i][0] - 1].id = "idk"
            } else {
                // set image
                let img_num = data[i][1];
                if (data[i][1] >= 6) {
                    img_num = 6;
                }
                document.getElementsByClassName("thumbnail")[data[i][0] - 1].src = "/static/img/pj_room_desk/" + img_num + ".png";

                // set text
                if (data[i][1] === 0) {
                    document.getElementsByClassName("now_status")[data[i][0] - 1].innerHTML = "사용 가능"
                    document.getElementsByClassName("now_status")[data[i][0] - 1].id = "non_using"
                } else {
                    document.getElementsByClassName("now_status")[data[i][0] - 1].innerHTML = data[i][1] + "명 사용 중"
                    document.getElementsByClassName("now_status")[data[i][0] - 1].id = "using"
                }
            }
        }
    } else {
        console.log("data is null - check server");
    }
    console.log("Data refreshed");
    let time = setTimeout(function() {
        set_data();
    }, 10000);
}
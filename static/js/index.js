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
            let now_count = data[i][1];
            let now_room = data[i][0]

            if (now_count === "timeout") {
                // set image
                document.getElementsByClassName("thumbnail")[now_room - 1].src = "/static/img/pj_room_desk/0.png";
                // set text
                document.getElementsByClassName("now_status")[now_room - 1].innerHTML = "알 수 없음"
                document.getElementsByClassName("now_status")[now_room - 1].id = "idk"
            } else {
                // set image
                let img_num = now_count;
                if (now_count >= 6) {
                    img_num = 6;
                }
                document.getElementsByClassName("thumbnail")[now_room - 1].src = "/static/img/pj_room_desk/" + img_num + ".png";

                // set text
                if (now_count === 0) {
                    document.getElementsByClassName("now_status")[now_room - 1].innerHTML = "사용 가능"
                    document.getElementsByClassName("now_status")[now_room - 1].id = "non_using"
                } else {
                    document.getElementsByClassName("now_status")[now_room - 1].innerHTML = now_count + "명 사용 중"
                    document.getElementsByClassName("now_status")[now_room - 1].id = "using"
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
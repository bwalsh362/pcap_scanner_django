var header = document.getElementById("device_header");
header.innerText = device_list[3];

var body = document.getElementById("body");
body.onload = function () {
    console.log(device_list);
    set_general_info();
    set_interface_info();
    set_device_info();

};


function set_general_info(){
    var ul = document.getElementById("general_list");
    var data_used = [["IP Address:", device_list[0]], ["MAC Address:", device_list[1]], ["Hostname:", device_list[3]]];
    for (var i = 0; i < data_used.length; i++){
        var li = document.createElement("li");
        li.setAttribute('class', 'list-group-item');
        li.style.overflow = "auto";
        li.style.display = "block";
        var left_div = document.createElement("div");
        left_div.style.cssFloat = "left";
        var right_div = document.createElement("div");
        right_div.style.cssFloat = "right";
        left_div.appendChild(document.createTextNode(data_used[i][0]));
        right_div.appendChild(document.createTextNode(data_used[i][1]));
        li.appendChild(left_div);
        li.appendChild(right_div);
        ul.appendChild(li);
    }
}

function set_interface_info(){
    var ul = document.getElementById("interface_list");
    var data_used = device_list[5];
    for (var i = 0; i < data_used.length; i++){
        var li = document.createElement("li");
        li.setAttribute('class', 'list-group-item');
        li.style.overflow = "auto";
        li.style.display = "block";
        var left_div = document.createElement("div");
        left_div.style.cssFloat = "left";
        var right_div = document.createElement("div");
        right_div.style.cssFloat = "right";
        left_div.appendChild(document.createTextNode(data_used[i][1]));
        var current_op_status = data_used[i][3];
        if(current_op_status === '1'){
            current_op_status = "UP";
        }else if (current_op_status === '2'){
            current_op_status = "DOWN";
        }else{
            current_op_status = "TESTING"
        }
        right_div.appendChild(document.createTextNode(current_op_status));
        li.appendChild(left_div);
        li.appendChild(right_div);
        ul.appendChild(li);
    }
}

function set_device_info(){
    var ul = document.getElementById("device_list");
    var data_used = device_list[6];
    var data_used_arr = [["Device Description:", data_used[0]], ["Serial Number:", data_used[1]], ["Vendor:", data_used[2]], ["Device Model:", data_used[3]]];
    for (var i = 0; i < data_used_arr.length; i++){
        var li = document.createElement("li");
        li.setAttribute('class', 'list-group-item');
        li.style.overflow = "auto";
        li.style.overflow = "block";
        var left_div = document.createElement("div");
        left_div.style.cssFloat = "left";
        var right_div = document.createElement("div");
        right_div.style.cssFloat = "right";
        left_div.appendChild(document.createTextNode(data_used_arr[i][0]));
        right_div.appendChild(document.createTextNode(data_used_arr[i][1]));
        li.appendChild(left_div);
        li.appendChild(right_div);
        ul.appendChild(li);
    }
}
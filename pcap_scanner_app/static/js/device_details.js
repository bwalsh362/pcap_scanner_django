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
    var table_head = document.getElementById("interface_table_head");
    var table_body = document.getElementById("interface_table_body");
    var table_headers = ["Interface Description", "Interface Speed", "Duplex", "State", "Bandwidth Utilization"];
    var header_row = document.createElement("tr");
    table_head.appendChild(header_row);
    for (var a = 0; a < table_headers.length; a++){
        var header_cell = document.createElement("th");
        header_cell.appendChild(document.createTextNode(table_headers[a]));
        header_row.appendChild(header_cell);
    }
    var data_used = device_list[5];
    var bandwidth_list = device_list[8];
    var duplex_list = device_list[7];
    for (var i = 0; i < data_used.length; i++){
        var body_row = document.createElement("tr");
        table_body.appendChild(body_row);
        var desc_cell = document.createElement("td");
        desc_cell.appendChild(document.createTextNode(data_used[i][1]));
        body_row.appendChild(desc_cell);
        var speed_cell = document.createElement("td");
        var speed = (data_used[i][2])/1000000;
        speed_cell.appendChild(document.createTextNode(speed + " Megabits"));
        body_row.appendChild(speed_cell);
        var duplex_cell = document.createElement("td");
        var duplex = duplex_list[i];
        if(duplex == null){
            duplex = "UNKNOWN";
        }
        console.log(duplex);
        duplex_cell.appendChild(document.createTextNode(duplex));
        body_row.appendChild(duplex_cell);
        var state_cell = document.createElement("td");
        var state = "DOWN";
        if(data_used[i][3] === "1"){
            state = "UP";
        }
        state_cell.appendChild(document.createTextNode(state));
        body_row.appendChild(state_cell);
        var bandwidth_cell = document.createElement("td");
        bandwidth_cell.appendChild(document.createTextNode(bandwidth_list[i]+"%"));
        body_row.appendChild(bandwidth_cell);
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
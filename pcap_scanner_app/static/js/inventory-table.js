createTable();

function createTable(){
    var table = document.getElementById("table");
    var tbody = document.createElement("tbody");
    for (var a = 0; a < data.length; a++){
        var row = document.createElement("tr");
        for (var b = 0; b < data[a].length; b++){
            if (b === 2){
                var cell = document.createElement("td");
                var cellText = document.createTextNode(data[a][b]);
                cell.innerHTML += "<a href='/inventory/tag=" + data[a][b] + "'>" + data[a][b] + "</a>";
                row.appendChild(cell);
            }
            else if (b === 4){
                var cell = document.createElement("td");
                var cellText = document.createTextNode(data[a][b].length);
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
            else if (b === 5){
                console.log(data[a][b][2]);
                console.log(data[a][b][0]);
                var cell = document.createElement("td");
                if(data[a][b][2] === undefined || data[a][b][2] === ""){
                    var cellText = document.createTextNode("N/A");
                }else {
                    var cellText = document.createTextNode(data[a][b][2]);
                }
                cell.appendChild(cellText);
                row.appendChild(cell);
                var cell = document.createElement("td");
                if(data[a][b][0] === "" || data[a][b][0] === undefined){
                    var cellText = document.createTextNode("N/A");
                }else {
                    var cellText = document.createTextNode(data[a][b][0]);
                }
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
            else{
                var cell = document.createElement("td");
                if(data[a][b][2] === ""){
                    var cellText = document.createTextNode("N/A");
                }else {
                    var cellText = document.createTextNode(data[a][b]);
                }
                cell.appendChild(cellText);
                row.appendChild(cell);
            }
        }
        tbody.appendChild(row);
    }
    table.appendChild(tbody);
}

function sortTable(n){
    console.log("SortTable");
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("table");
    switching = true;
    dir = "asc";
    while (switching){
        switching = false;
        rows = table.getElementsByTagName("TR");
        for (i = 1; i < (rows.length - 1); i++){
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            if (dir == "asc"){
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()){
                    shouldSwitch = true;
                    break;
                }
            }
            else if (dir == "desc"){
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()){
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch){
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        }
        else{
            if (switchcount == 0 && dir == "asc"){
                dir = "desc";
                switching = true;
            }
        }
    }
}

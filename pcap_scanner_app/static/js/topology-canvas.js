// var canvas = document.getElementById('canvas');
// var context = canvas.getContext('2d');
//     canvas.width = document.body.clientWidth;
//     canvas.height = document.body.clientHeight;

var imgs = [];
var imagesOK = 0;
JS_LIST = formatList(JS_LIST);
JS_LIST_UNIQ = removeDuplicates(JS_LIST);
var sources = getSources(JS_LIST);
loadImages(imagesLoaded);


function formatList(devices){
    devices = devices.replace(/[\[\](]+/g, '');
    devices = devices.replace(/&#39;/g, '');
    devices = devices.split('),');
    return devices;
}

function removeDuplicates(devices){
    var unique_array = [];
    var multi_arr = [];
    for (var i = 0; i < devices.length; i++){
        var tmp_array = devices[i].split(',');
        multi_arr.push(tmp_array);
    }
    for (var a = 0; a < multi_arr.length; a++){
        if(unique_array.indexOf(multi_arr[a][10]) == -1){
            unique_array.push(multi_arr[a])
        }
    }
    return unique_array;
}

function getSources (devices){
    var source_arr = [];
    for(var i = 0; i < devices.length; i++){
        var tmp_array = devices[i].split(',');
        if (tmp_array[4] === ' 1' && tmp_array[6] === ' 1'){
            source_arr.push('../static/img/ml_switch.png');
        }else if (tmp_array[4] === ' 1'){
            source_arr.push('../static/img/switch.png');
        }else if (tmp_array[6] === ' 1'){
            source_arr.push('../static/img/router.png');
        }else{
            console.log('other');
        }
    }
    return source_arr;
}


function loadImages (callback){
    for (var i = 0; i < sources.length; i++){
        var img = new Image();
        imgs.push(img);
        img.onload = function(){
            imagesOK++;
            if (imagesOK >= sources.length){
                callback();
            }
        };
        img.src = sources[i];
        img.onerror=function(){alert("image load failed");};
    }
}

function imagesLoaded(){
    var location = 25;
    for(var i = 0; i < imgs.length; i++){
        var button = document.createElement('button');
        button.innerHTML = "<img src=" + sources[i] + "/>";
        button.id = 'button' + i;
        button.setAttribute('data-info', JS_LIST[i]);
        var data = button.getAttribute('data-info');
        var tmp_arr = data.replace(' ', '');
        tmp_arr = tmp_arr.split(',');
        button.setAttribute('onclick', "buttonClicked(this.id)");
        // button.setAttribute('onmouseover', "buttonHover(this.id)");
        button.setAttribute('data-toggle', "tooltip");
        button.setAttribute('data-placement', "bottom");
        button.setAttribute('title', tmp_arr[10]);
        var body = document.getElementById("main-div");
        body.appendChild(button);
    }
}

function buttonClicked(clickedId){
    var button = document.getElementById(clickedId);
    var data = button.getAttribute('data-info');
    var modal = document.getElementById('myModal');
    var span = document.getElementsByClassName("close")[0];
    var modal_cont = document.getElementById('myModalContent');
    var tmp_arr = data.replace(' ', '');
    tmp_arr = tmp_arr.split(',');
    modal_cont.innerHTML = "<p>IP Address: " + tmp_arr[0] + "<br />" +
        "MAC Address: " + tmp_arr[1] + "<br />" +
        "Hostname: " + tmp_arr[10] + "</p>";
    modal.style.display = "block";
    span.onclick = function () {
        modal.style.display = "none";
    };
    window.onclick = function(event){
        if (event.target == modal){
            modal.style.display = "none";
        }
    }
}
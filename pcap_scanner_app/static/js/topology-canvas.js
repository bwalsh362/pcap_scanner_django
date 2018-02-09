var imgs = [];
var imagesOK = 0;
var sources = getSources(JS_LIST);
loadImages(imagesLoaded);

function getSources (devices){
    var source_arr = [];
    for(var i = 0; i < devices.length; i++){
        // var tmp_array = devices[i].split(',');
        if (devices[i][4] === '1' && devices[i][6] === '1'){
            source_arr.push('../static/img/ml_switch.png');
        }else if (devices[i][4] === '1'){
            source_arr.push('../static/img/switch.png');
        }else if (devices[i][6] === '1'){
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
        $(button).data("info", JS_LIST[i]);
        var data = jQuery(button).data('info');
        button.setAttribute('onclick', "buttonClicked(this.id)");
        button.setAttribute('data-toggle', "tooltip");
        button.setAttribute('data-placement', "bottom");
        button.setAttribute('title', data[10]);
        var body = document.getElementById("main-div");
        body.appendChild(button);
    }
}

function buttonClicked(clickedId){
    var button = document.getElementById(clickedId);
    var data = jQuery(button).data('info');
    var modal = document.getElementById('myModal');
    var span = document.getElementsByClassName("close")[0];
    var modal_cont = document.getElementById('myModalContent');
    modal_cont.innerHTML = "<p>IP Address: " + data[0] + "<br />" +
        "MAC Address: " + data[1] + "<br />" +
        "Hostname: " + data[10] + "</p>";
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
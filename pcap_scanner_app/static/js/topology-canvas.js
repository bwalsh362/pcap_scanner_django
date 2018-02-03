function loadImages(sources, callback) {

    var images = [];
    var loadedImages = 0;
    var numImages = 0;
    // get num of sources
    for(i=0; i< sources.length; i++) {
      numImages++;
    }
    for(i=0; i< sources.length; i++) {
      images[i] = new Image();
      images[i].onload = function() {
        if(++loadedImages >= numImages) {
          callback(images);
        }
      };
      images[i].src = sources[i];
    }
  }

// var canvas = document.getElementById('canvas');
// var context = canvas.getContext('2d');
//     canvas.width = document.body.clientWidth;
//     canvas.height = document.body.clientHeight;
var sources = [];
var format_list = JS_LIST.replace(/[\[\](&#39;]/g, '');
var format_array = format_list.split('),');
for (i=0; i<format_array.length; i++){
    var tmp_array = format_array[i].split(',');
    if(tmp_array[4] == 1 && tmp_array[6] == 1){
        sources.push('../static/img/ml_switch.png');
    }
    else if(tmp_array[4] == 1){
        sources.push('../static/img/switch.png');
    }
    else{
        sources.push('../static/img/pic.png');
    }
    // alert(sources)
}
$(document).ready(function(){
        loadImages(sources, function(images) {
            var button = document.createElement("button");
            var body = document.getElementById('main-div');
            // var location = 50;
            for (i = 0; i< sources.length; i++){
                // alert(images[i].src);
                button.innerHTML = '<img src=' + sources[i] + '/>';
                body.appendChild(button)
                // context.drawImage(images[i], location*i, location*i, images[i].width, images[i].height);
            }
            button.onclick = function () { alert("HELLO"); }
            });
  });

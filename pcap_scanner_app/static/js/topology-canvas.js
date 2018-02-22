// var imgs = [];
// var imagesOK = 0;
// var sources = getSources(JS_LIST);
// loadImages(imagesLoaded);
//
// function getSources (devices){
//     var source_arr = [];
//     for(var i = 0; i < devices.length; i++){
//         // var tmp_array = devices[i].split(',');
//         if (devices[i][2] === 'ml_switch'){
//             source_arr.push('../static/img/ml_switch.png');
//         }else if (devices[i][2] === 'switch'){
//             source_arr.push('../static/img/switch.png');
//         }else if (devices[i][2] === 'router'){
//             source_arr.push('../static/img/router.png');
//         }else{
//             source_arr.push('../static/img/pic.png');
//             console.log('other');
//         }
//     }
//     return source_arr;
// }
//
//
// function loadImages (callback){
//     for (var i = 0; i < sources.length; i++){
//         var img = new Image();
//         imgs.push(img);
//         img.onload = function(){
//             imagesOK++;
//             if (imagesOK >= sources.length){
//                 callback();
//             }
//         };
//         img.src = sources[i];
//         img.onerror=function(){alert("image load failed");};
//     }
// }
//
// function imagesLoaded(){
//     var location = 25;
//     for(var i = 0; i < imgs.length; i++){
//         var button = document.createElement('button');
//         button.innerHTML = "<img src=" + sources[i] + "/>";
//         button.id = 'button' + i;
//         $(button).data("info", JS_LIST[i]);
//         var data = jQuery(button).data('info');
//         button.setAttribute('onclick', "buttonClicked(this.id)");
//         button.setAttribute('data-toggle', "tooltip");
//         button.setAttribute('data-placement', "bottom");
//         button.setAttribute('title', data[3]);
//         var body = document.getElementById("main-div");
//         body.appendChild(button);
//     }
// }
//
// function buttonClicked(clickedId){
//     var button = document.getElementById(clickedId);
//     var data = jQuery(button).data('info');
//     var modal = document.getElementById('myModal');
//     var span = document.getElementsByClassName("close")[0];
//     var modal_cont = document.getElementById('myModalContent');
//     modal_cont.innerHTML = "<p>IP Address: " + data[0] + "<br />" +
//         "MAC Address: " + data[1] + "<br />" +
//         "Hostname: " + data[3] + "<br />" +
//         "Connected Devices: " + data[4] + "</p>";
//     modal.style.display = "block";
//     span.onclick = function () {
//         modal.style.display = "none";
//     };
//     window.onclick = function(event){
//         if (event.target == modal){
//             modal.style.display = "none";
//         }
//     }
// }

var net;

var body = document.getElementById("body");
body.onload = function ()
{
    console .log("Loading SVG Info...");
      net=new tNetwork.Network();
      //Id of the svg and defs
      net.addSVG("mySVG");
      net.addDefs("myDefs");

      for (var i = 0; i < JS_LIST.length; i++){
          var location = 50;
          var href = '';
          if (JS_LIST[i][2] === 'ml_switch'){
              href = '../static/img/ml_switch.png';
        }else if (JS_LIST[i][2] === 'switch'){
              href = '../static/img/switch.png';
        }else if (JS_LIST[i][2] === 'router'){
              href = '../static/img/router.png';
        }else{
              href = '../static/img/pic.png';
              console.log('other');
        }
          net.addNode(JS_LIST[i][3], (i*location)+30, (i*location)+30, href);
          net.addLabel("node", JS_LIST[i][3], JS_LIST[i][3])
      }
      for (var a = 0; a < JS_LIST.length; a++){
          for (var b = 0; b < JS_LIST[a][4].length; b++){
              net.addLink(JS_LIST[a][3], JS_LIST[a][4][b]);
              net.addLink(JS_LIST[a][4][b], JS_LIST[a][3]);
          }
      }
	 
      //Timeout is because there are async functions and it gets some time to
      //Calculate positions
      setTimeout("net.drawNetwork()",300);
      setTimeout("net.startEditMode()",500);
    };
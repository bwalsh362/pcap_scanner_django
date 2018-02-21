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

var net,net2;

var body = document.getElementById("body");
body.onload = function ()
{
    console .log("Loading SVG Info...");
      net=new tNetwork.Network();
      //Id of the svg and defs
      net.addSVG("mySVG");
      net.addDefs("myDefs");
	  //Creating elements
      // net.addNode("NODE1",170,220);
      // net.addNode("NODE2",600,50);
      // net.addNode("NODE3",200,100);
      // net.addNode("NODE4",800,300);
      // net.addLink("NODE1","NODE2");
      // net.addLink("NODE2","NODE1");
      // //Bidirectional link
      // net.addLink("NODE2","NODE4",true);
      // net.addLink("NODE3","NODE1");
      // net.addLink("NODE1","NODE3");
      //
      // net.addVerticalBus("bus1", 900, 0);
      // net.addVerticalBus("bus2", 20, 0);
      //
      // net.addBusLink("bus1", "NODE2");
      // net.addBusLink("bus1","NODE4");
      // net.addBusLink("bus2", "NODE1");
      // net.addBusLink("bus2","NODE2");
      // net.addBusLink("bus2","NODE3");
      //
      // net.addLabel("node", "NODE1", "node 1");
      // net.addLabel("link","NODE1:NODE2","link 1");
      // net.addLabel("buslink","bus1:NODE2","buslink 1");
      // //Multiple labels
      // net.addLabel("bus", "bus1", "bus one");
      // net.addLabel("node","NODE3","one","left","top");
      // net.addLabel("node","NODE3","two","none","top");
      // net.addLabel("node","NODE3","three","right","top");
      // net.addLabel("node","NODE3","four","right","none");
      // net.addLabel("node","NODE3","five","right","bottom");
      // net.addLabel("node","NODE3","six","none","bottom");
      // net.addLabel("node","NODE3","seven","left","bottom");
      // net.addLabel("node","NODE3","eight","left","none");
      // net.addLabel("node","NODE3","nine","left","top");
      // net.addLabel("node","NODE3","ten","none","top");

      //Timeout is because there are async functions and it gets some time to
      //Calculate positions
      setTimeout("net.drawNetwork()",300);
      setTimeout("net.startEditMode()",500);
    };
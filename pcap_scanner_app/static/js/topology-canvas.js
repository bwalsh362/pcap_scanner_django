var net;

var body = document.getElementById("body");
body.onload = function ()
{
    console.log("Loading SVG Info...");
    console.log(JS_LIST);
      net=new tNetwork.Network();
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
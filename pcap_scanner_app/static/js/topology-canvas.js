
var divwidth = document.getElementById('main-div').offsetWidth-40;
canvas.width = divwidth;
canvas.height = window.innerHeight;


function add_icons(device_list){
    var canvas = document.getElementById('topology-canvas'),
    context = canvas.getContext('2d');
    // for (i=0; i<device_list.length; i++){
        base_image = new Image();
        base_image.src = '../static/img/switch.png';
        base_image.onload = function(){
            context.drawImage(base_image, canvas.width/2 - base_image.width/2, canvas.height/2 - base_image.height/2);
        }
}

// add_icons();
//
// function add_icons() {
//     base_image = new Image();
//     base_image.src = '../static/img/switch.png';
//     base_image.onload = function(){
//         context.drawImage(base_image, canvas.width/2 - base_image.width/2, canvas.height/2 - base_image.height/2);
//     };
// }


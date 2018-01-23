var canvas = document.getElementById('canvas'),
    context = canvas.getContext('2d');

var grd = context.createLinearGradient(0,0,200,0);
// grd.addColorStop(0, "red");
// grd.addColorStop(1, "white");

context.fillStyle = grd;
context.fillRect(10,10,150,80);
    // context.fillStyle = "rgb(0, 0, 0)";
    // context.fillRect(10, 30, 30, 30);

add_icons();

function add_icons(){
    // context.fillRect(20,20,20,20);
    for(i=0;i<=2;i++){
        base_image = new Image();
        base_image.src = '../static/img/switch.png';
        base_image.onload = function(){
            context.drawImage(base_image, base_image.width, base_image.height);
        }
    }
}
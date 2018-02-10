var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var cw=canvas.width;
var ch=canvas.height;

var nextTime=0;
var duration=1000;
var endingPct=100;
var pct=0;
var grow = 0;
// var increment=duration/pct;
requestAnimationFrame(animate);

function animate(time) {
    draw(pct);
    grow++;
    if (grow % 2 == 0) {
        pct++;
    }
    if(pct<=endingPct) {
        requestAnimationFrame(animate);
    }
}

function draw(pct){
    var endRadians=-Math.PI/2+Math.PI*2*pct/100;
    ctx.arc(150,125,120,-Math.PI/2,endRadians);
    ctx.lineTo(150,125);
    ctx.lineWidth = 15;
    ctx.strokeStyle = 'green';
    ctx.stroke();
    // ctx.fillStyle='green';
    // ctx.fill();
    
    // ctx.fillStyle='white';
    // ctx.fillRect(0,0,cw,ch);
    // ctx.beginPath();
    
    ctx.arc(150,125,100,-Math.PI/2,endRadians, true);
    ctx.lineTo(150,125);
    ctx.fillStyle='blue';
    ctx.fill();
    // ctx.beginPath();
    // ctx.strokeStyle='#13a8a4';
    // ctx.lineJoin='bevel';
    // ctx.lineWidth=10;
    // ctx.stroke();
    // ctx.fillStyle='black';
    // ctx.textAlign='center';
    // ctx.textBaseline='middle'
    // ctx.font='18px arial';
}

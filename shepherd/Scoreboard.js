var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var cw=canvas.width;
var ch=canvas.height;

var time=0;
var duration=1000;
var endingPct=100;
var pct = 0;
var grow = 1;
// var increment=duration/pct;
// requestAnimationFrame(animate);

function start(time){
    form = document.getElementById("seconds");
    grow = parseFloat(form.elements[0].value)*10;
    beginning = new Date();
    function animate(){
        date = new Date();
        // pct += grow;
        pct = (date - beginning)/grow;
        draw(pct);
        if(pct<=endingPct){
            requestAnimationFrame(animate);
        }
    }
    requestAnimationFrame(animate);
}

function draw(pct){
    var endRadians=-Math.PI/2+Math.PI*2*pct/100;
    // ctx.fillStyle='white';
    // ctx.fillRect(0,0,cw,ch);
    // ctx.beginPath();
    ctx.arc(150,125,100,-Math.PI/2,endRadians);
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

function addTime(time){

}
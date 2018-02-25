var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var canvas2 = document.getElementById("canvas2");
var ctx2 = canvas2.getContext("2d");
var canvas3 = document.getElementById("canvas3");
var ctx3 = canvas3.getContext("2d");
var canvas4 = document.getElementById("canvas4");
var ctx4 = canvas4.getContext("2d");
var canvas5 = document.getElementById("canvas5");
var ctx5 = canvas5.getContext("2d");

var cw=canvas.width;
var ch=canvas.height;
var duration=1;
var endingPct=100;
var pct = 0;
var pct2 = 0;
var grow = 1;
var grow2 = 1;
// var increment=duration/pct;
// requestAnimationFrame(animate);

function start(time){
    form = document.getElementById("seconds");
    grow = parseFloat(form.elements[0].value)*10;
    grow2 = parseFloat(form.elements[1].value)*10;
    beginning = new Date();
    function animate(){
        date = new Date();
        // pct += grow;
        pct = (date - beginning)/grow;
        pct2 = (date - beginning)/grow2;
        draw(ctx, pct, pct2);
        draw(ctx2, pct, pct2);
        draw(ctx3, pct, pct2);
        draw(ctx4, pct, pct2);
        draw(ctx5, pct, pct2)
        if(pct <= endingPct || pct2 <= endingPct){
            requestAnimationFrame(animate);
        }
    }
    requestAnimationFrame(animate);
}

function draw(ctx, pct, pct2) {
    var endRadians = -Math.PI/2 + Math.PI*2*pct/100;
    var endRadians2 = -Math.PI/2 + Math.PI*2*pct2/100;
    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);
    if (pct <= 100) {
        ctx.beginPath();
        ctx.arc(150,125,90,-Math.PI/2,endRadians, true);
        ctx.moveTo(150,125);
        ctx.strokeStyle='blue';
        ctx.lineWidth = 30
        ctx.stroke();
    }
    if (pct2 <= 100) {
        ctx.beginPath();
        ctx.arc(150,125,70,-Math.PI/2,endRadians2, true);
        ctx.lineTo(150,125);
        ctx.fillStyle = 'goldenrod';
        ctx.fill();
    }
}

function addTime() {
    grow += parseFloat(document.forms["addTime"].elements[0].value)*10;
    grow2 += parseFloat(document.forms["addTime"].elements[1].value)*10;
    ctx.clearRect(0, 0, cw, ch);
    ctx.beginPath();
}
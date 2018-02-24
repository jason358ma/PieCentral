var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var cw=canvas.width;
var ch=canvas.height;
var time=0;
var duration=1000;
var endingPct=100;
var pct = 0;
var pct2 = 0;
var time = 1;
var time2 = 1;
// var increment=duration/pct;
// requestAnimationFrame(animate);

function start(time){
    form = document.getElementById("seconds");
    time = parseFloat(form.elements[0].value)*10;
    time2 = parseFloat(form.elements[1].value)*10;
    beginning = new Date();
    function animate(){
        date = new Date();
        // pct += time;
        pct = (date - beginning)/time;
        pct2 = (date - beginning)/time2
        draw(pct, pct2);
        if(pct<=endingPct || pct2 <= endingPct){
            requestAnimationFrame(animate);
        }
    }
    requestAnimationFrame(animate);
}

function draw(pct, pct2){
    var endRadians=-Math.PI/2+Math.PI*2*pct/100;
    var endRadians2=-Math.PI/2+Math.PI*2*pct2/100;
    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);
    ctx.beginPath();
    ctx.arc(150,125,100,-Math.PI/2,endRadians);
    ctx.lineTo(150,125);
    ctx.fillStyle='blue';
    ctx.fill();
    ctx.beginPath();
    ctx.arc(150,125,70,-Math.PI/2,endRadians2);
    ctx.lineTo(150,125);
    ctx.fillStyle='red';
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

function addTime(){
    time += parseFloat(document.getElementById("addTime").elements[0].value)*10;
    time2 += parseFloat(document.getElementById("addTime").elements[1].value)*10;
    ctx.clearRect(0, 0, cw, ch);
    ctx.beginPath();
}
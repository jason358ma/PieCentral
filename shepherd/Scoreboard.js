var canvas=document.getElementById("canvas");
var ctx=canvas.getContext("2d");
var cw=canvas.width;
var ch=canvas.height;
var duration=1;
var endingPct=100;
var pct = 0;
/**
<<<<<<< HEAD
var grow = 1;
var beginning;
// var increment=duration/pct;
function start() { 
    var form = document.getElementById("seconds")
    duration = parseFloat(form.elements[0].value);
    pct = 0;
    beginning = new Date();
    requestAnimationFrame(animate);
}

function animate(time) {
    draw(pct);
    pct = 100 * (((new Date()) - beginning)/(duration * 1000))
    if(pct<=endingPct) {
        requestAnimationFrame(animate);
    }
// =======
// // requestAnimationFrame(animate);

// function start(time){
//     form = document.getElementById("seconds");
//     grow = parseFloat(form.elements[0].value)*10;
//     beginning = new Date();
//     function animate(){
//         date = new Date();
//         // pct += grow;
//         pct = (date - beginning)/grow;
//         draw(pct);
//         if(pct<=endingPct){
//             requestAnimationFrame(animate);
//         }
//     }
//     requestAnimationFrame(animate);
// >>>>>>> 94a457e2b8458baa2b71e78cafb9bb5f31fe88f2
}

function draw(pct){
    var endRadians=-Math.PI/2+Math.PI*2*pct/100;

    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);
    ctx.beginPath();
    
    ctx.arc(150,125,105,-Math.PI/2, endRadians, true);
    ctx.moveTo(150,125);
    ctx.lineWidth = 30;
    ctx.strokeStyle = 'green';
    ctx.stroke();
    // ctx.fillStyle='green';
    // ctx.fill();

    ctx.beginPath();
    ctx.arc(150,125,45,-Math.PI/2, endRadians, true);
    ctx.moveTo(150,125);
    ctx.lineWidth = 90;
    ctx.strokeStyle = 'blue';
    ctx.stroke();

    // ctx.arc(150,125,80,-Math.PI/2, endRadians, true);
    // ctx.lineTo(150,125);
    // ctx.fillStyle='blue';
    // ctx.fill();

=======
*/
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
        draw(pct, pct2);
        if(pct <= endingPct || pct2 <= endingPct){
            requestAnimationFrame(animate);
        }
    }
    requestAnimationFrame(animate);
}

function draw(pct, pct2){
    var endRadians = -Math.PI/2 + Math.PI*2*pct/100;
    var endRadians2 = -Math.PI/2 + Math.PI*2*pct2/100;
    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);
    ctx.beginPath();
    ctx.arc(150,125,90,-Math.PI/2,endRadians);
    ctx.moveTo(150,125);
    ctx.strokeStyle='blue';
    ctx.lineWidth = 30
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(150,125,70,-Math.PI/2,endRadians2);
    ctx.lineTo(150,125);
    ctx.fillStyle='gold';
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
    grow += parseFloat(document.forms["addTime"].elements[0].value)*10;
    grow2 += parseFloat(document.forms["addTime"].elements[1].value)*10;
    ctx.clearRect(0, 0, cw, ch);
    ctx.beginPath();
}
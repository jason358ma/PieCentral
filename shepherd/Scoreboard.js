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

var contexts = [ctx, ctx2, ctx3, ctx4, ctx5];
var pct = [0, 0, 0, 0, 0];
var pct2 = [0, 0, 0, 0, 0];
var pct3 = [0, 0, 0, 0, 0];
var grow = [1, 1, 1, 1, 1];
var grow2 = [1, 1, 1, 1, 1];
var grow3 = [1, 1, 1, 1, 1];

var cw=canvas.width;
var ch=canvas.height;
var duration=1;
var endingPct=100;
// var increment=duration/pct;
var match_time = 300;
var match_num = 0;
var blue_1_num = 0;
var blue_1_name = "blue 1";
var blue_2_num = 0;
var blue_2_name = "blue 2";
var gold_1_num = 0;
var gold_1_name = "gold 1";
var gold_2_num = 0;
var gold_2_name = "gold 2";

var bottom = document.getElementById("bottom_bar");
var ctx_bottom = bottom.getContext("2d");
setTeamsInfo();
setTime();

requestAnimationFrame(animate);

var socket = io('http://127.0.0.1:5000');

socket.on('server-to-gui-teamsinfo', function(data) {
    parsed_data = JSON.parse(data);
    match_num = parsed_data.match_num;
    blue_1_num = parsed_data.b1num;
    blue_1_name = parsed_data.b1name;
    blue_2_num = parsed_data.b2num;
    blue_2_name = parsed_data.b2name;
    gold_1_num =  parsed_data.g1num;
    gold_1_name = parsed_data.g1name;
    gold_2_num = parsed_data.g2num;
    gold_2_name = parsed_data.g2name;
    setTeamsInfo()
});

function setTeamsInfo() {
    ctx_bottom.font = "30px Helvetica";
    ctx_bottom.fillText(blue_1_num.toString(),10,30);
    ctx_bottom.fillText(blue_1_name,10,60);
    ctx_bottom.fillText(blue_2_num.toString(),10, 120);
    ctx_bottom.fillText(blue_2_name,10,150);
    ctx_bottom.textAlign = "right";
    ctx_bottom.fillText(gold_1_num.toString(),bottom.width,30);
    ctx_bottom.fillText(gold_1_name,bottom.width,60);
    ctx_bottom.fillText(gold_2_num.toString(),bottom.width,120);
    ctx_bottom.fillText(gold_2_name,bottom.width,150);
}

function setTime() {
    ctx_bottom.textAlign = "center";
    var time_string = (match_time / 60).toString() + " : "
    if (match_time % 60 < 10) {
        time_string += "0";
    }
    time_string += (match_time % 60).toString();
    ctx_bottom.font = "40px Helvetica"
    ctx_bottom.fillText(time_string,bottom.width/2, 65)
    ctx_bottom.fillText("Match " + match_num.toString(), bottom.width/2, 115)
}

function start(time){
    form = document.getElementById("seconds");
    for(var i = 0; i < 5; i++){
        grow[i] = parseFloat(form.elements[0].value.split(" ")[i])*10;
        grow2[i] = parseFloat(form.elements[1].value.split(" ")[i])*10;
        grow3[i] = parseFloat(form.elements[2].value.split(" ")[i])*10;
    }
    beginning = new Date();
    function animate(){
        date = new Date();
        // pct += grow;
        for(var i = 0; i < 5; i++){
            pct[i] = (date - beginning)/grow[i];
            pct2[i] = (date - beginning)/grow2[i];
            pct3[i] = (date - beginning)/grow3[i];
        }
        for(var i = 0; i < 5; i++){
            draw(contexts[i], pct[i], pct2[i], pct3[i]);
        }
        // draw(ctx, pct, pct2);
        // draw(ctx2, pct, pct2);
        // draw(ctx3, pct, pct2);
        // draw(ctx4, pct, pct2);
        // draw(ctx5, pct, pct2);

        for(var i = 0; i < 5; i++){
            if(pct[i] <= endingPct || pct2[i] <= endingPct || pct3[i] <= endingPct){
                requestAnimationFrame(animate);
                break;
            }
        }
    }
    requestAnimationFrame(animate);
}


function draw(ctx, pct, pct2, pct3) {
    var endRadians = -Math.PI/2 + Math.PI*2*pct/100;
    var endRadians2 = -Math.PI/2 + Math.PI*2*pct2/100;
    var endRadians3 = -Math.PI/2 + Math.PI*2*pct3/100;
    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);
    if (pct <= 100) {
        ctx.beginPath();
        ctx.arc(150,125,100,-Math.PI/2,endRadians, true);
        ctx.moveTo(150,125);
        ctx.strokeStyle='purple';
        ctx.lineWidth = 20;
        ctx.stroke();
    }
    if (pct2 <= 100) {
        ctx.beginPath();
        ctx.arc(150,125,80,-Math.PI/2,endRadians2, true);
        ctx.moveTo(150,125);
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 20;
        ctx.stroke();
    }
    ctx.beginPath();
    ctx.arc(150,125,60,-Math.PI/2,endRadians3, false);
    ctx.lineTo(150,125);
    ctx.fillStyle = 'goldenrod';
    ctx.fill();
}

function addTime() {
    for(var i = 0; i < 5; i++){
        grow[i] += parseFloat(document.forms["addTime"].elements[0].value.split(" ")[i])*10;
        grow2[i] += parseFloat(document.forms["addTime"].elements[1].value.split(" ")[i])*10;
        grow3[i] += parseFloat(document.forms["addTime"].elements[2].value.split(" ")[i])*10;
    }
    ctx.clearRect(0, 0, cw, ch);
    ctx.beginPath();
}
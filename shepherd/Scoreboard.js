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
var owner = ['n', 'n', 'n', 'n', 'n'];
// we might need to change these??
var bidAmounts = [0, 666, 100, 20, 0];

var cw=canvas.width;
var ch=canvas.height;
var duration=1;
var endingPct=100;
// var increment=duration/pct;
var match_time = 493;
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

var master_gold_score = 0;
var master_blue_score = 0;

var gold_multiplier = 1;
var blue_multiplier = 1;
setTeamsInfo();
setMatchTime();
setScores(10, 10)

requestAnimationFrame(animate);

var socket = io('http://127.0.0.1:5000');

socket.on('SCOREBOARD_HEADER.TEAMS', function(data) {
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
    setScores(0, 0)
});


socket.on('SCOREBOARD_HEADER.RESET_TIMERS', function(data) {
    //reset ALL the timers;
});

socket.on('SCOREBOARD_HEADER.SCORE', function(data) {
    parsed_data = JSON.parse(data);
    var alliance = parsed_data.alliance;
    var score = parsed_data.score;
    if(alliance == "GOLD"){
      setScores(master_blue_score,score);
    }
    if(alliance == "BLUE"){
      setScores(score, master_gold_score);
    }
});

socket.on('SCOREBOARD_HEADER.ALLIANCE_MULTIPLIER', function(data) {
    parsed_data = JSON.parse(data);
    var alliance = parsed_data.alliance;
    var multiplier = parsed_data.multiplier;
    if(alliance == "GOLD"){
      gold_multiplier = multiplier;
    }
    if(alliance == "BLUE"){
      blue_multiplier = multiplier;
    }
    setTeamsInfo();
});

socket.on('SCOREBOARD_HEADER.GOAL_OWNED', function(data) {
    parsed_data = JSON.parse(data);
    var alliance = parsed_data.alliance;
    var goal = GoalNumFromName(parsed_data.goal);
    var newOwner = 'n';
    if(alliance == "GOLD"){
      newOwner = 'g';
    }
    if(alliance == "BLUE"){
      newOwner = 'b';
    }
    owner[goal] = newOwner;
});

socket.on('SCOREBOARD_HEADER.BID_AMOUNT', function(data) {
    parsed_data = JSON.parse(data);
    var alliance = parsed_data.alliance;
    var goal = GoalNumFromName(parsed_data.goal);
    var bid = parsed_data.bid;
    bidAmounts[goal] = bid;
});

socket.on('SCOREBOARD_HEADER.BID_TIMER', function(data) {
    parsed_data = JSON.parse(data);
    var goal_num = goalNumFromName(parsed_data.goal);
    grow[goal_num] += parsed_data.time;
});

socket.on('SCOREBOARD_HEADER.POWERUPS', function(data) {
    //TODO
});

function goalNumFromName(goal_name) {
    var names = ["a", "b", "c", "d", "e"];
    return names.indexOf(goal_name.toLowerCase());
}


function setScores(score_blue, score_gold) {
    width = bottom.width;
    setTeamsInfo();
    ctx_bottom.fillStyle = "white";
    ctx_bottom.font = "50px Helvetica";
    ctx_bottom.textAlign = "right";
    ctx_bottom.fillText(score_blue.toString(),290,95);
    ctx_bottom.textAlign = "left";
    ctx_bottom.fillText(score_gold.toString(), width - 290, 95);
    master_blue_score = score_blue;
    master_gold_score = score_gold;
}

function setTeamsInfo() {
    width = bottom.width;
    ctx_bottom.clearRect(0, 0, bottom.width, bottom.height);
    ctx_bottom.font = "35px Helvetica";

    ctx_bottom.fillStyle = "navy";
    ctx_bottom.beginPath();
    ctx_bottom.fillRect(10, 0, 300, 160);

    ctx_bottom.beginPath();
    ctx_bottom.fillStyle = "goldenrod";
    ctx_bottom.fillRect(width - 310, 0, 300, 160);

    ctx_bottom.fillStyle = "white";
    ctx_bottom.textAlign = "left";
    var blue_1_string = blue_1_num.toString() + "   " + blue_1_name;
    ctx_bottom.fillText(blue_1_string,30,40);
    // ctx_bottom.fillText(blue_1_name,30,75);

    var blue_2_string = blue_2_num.toString() + "   " + blue_2_name;
    ctx_bottom.fillText(blue_2_string,30, 140);
    // ctx_bottom.fillText(blue_2_name,30,175);
    ctx_bottom.textAlign = "right";
    var gold_1_string = gold_1_name + "   " + gold_1_num.toString();
    ctx_bottom.fillText(gold_1_string, width - 30, 40);
    // ctx_bottom.fillText(gold_1_name,width - 30, 75);

    var gold_2_string = gold_2_name + "   " + gold_2_num.toString();
    ctx_bottom.fillText(gold_2_string, width - 30, 140);
    // ctx_bottom.fillText(gold_2_name, width - 30, 175);
    setMatchTime();
}

function setMatchTime() {
    ctx_bottom.fillStyle = "black"
    ctx_bottom.textAlign = "center";
    var time_string = Math.round(match_time / 60).toString() + " : "
    if (match_time % 60 < 10) {
        time_string += "0";
    }
    time_string += (match_time % 60).toString();
    ctx_bottom.font = "60px Helvetica"
    ctx_bottom.fillText(time_string,bottom.width/2, 75)
    ctx_bottom.font = "40px Helvetica"
    ctx_bottom.fillText("Match " + match_num.toString(), bottom.width/2, 125)
}

function start(time){
    form = document.getElementById("seconds");
    for(var i = 0; i < 5; i++){
        grow[i] = parseFloat(form.elements[0].value.split(" ")[i])*10;
        grow2[i] = parseFloat(form.elements[1].value.split(" ")[i])*10;
        grow3[i] = parseFloat(form.elements[2].value.split(" ")[i])*10;
        owner[i] = form.elements[3].value.split(" ")[i];
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
            draw(i);
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


function draw(i) {
    var ctx = contexts[i];
    var alliance = owner[i];
    var name = ["A","B","C","D","E"][i];
    var bidValue = bidAmounts[i];
    var color;
    if(alliance == 'b'){
      color = 'navy'
    }
    if(alliance == 'g'){
      color = 'goldenrod'
    }
    var endRadians = -Math.PI/2 + Math.PI*2*pct[i]/100;
    var endRadians2 = -Math.PI/2 + Math.PI*2*pct2[i]/100;
    var endRadians3 = -Math.PI/2 + Math.PI*2*pct3[i]/100;
    ctx.fillStyle='white';
    ctx.fillRect(0,0,cw,ch);

    ctx.beginPath();
    ctx.arc(150, 125, 59, 0, 2*Math.PI, false);
    ctx.moveTo(150,125);
    ctx.strokeStyle='black';
    ctx.lineWidth = 2;
    ctx.stroke();

    // outer arc
    if (pct[i] <= 100) {
        ctx.beginPath();
        ctx.arc(150,125,110,-Math.PI/2,endRadians, true);
        ctx.moveTo(150,125);
        ctx.strokeStyle='#004E8A';
        ctx.lineWidth = 20;
        ctx.stroke();
    }
    // inner arc
    if (pct2[i] <= 100) {
        ctx.beginPath();
        ctx.arc(150, 125, 80, -Math.PI / 2, endRadians2, true);
        ctx.moveTo(150, 125);
        ctx.strokeStyle = '#99000F';
        ctx.lineWidth = 20;
        ctx.stroke();
    }
    // inner circle
    ctx.beginPath();
    ctx.arc(150, 125, 60, -Math.PI / 2, endRadians3, false);
    ctx.lineTo(150, 125);
    ctx.fillStyle = color;
    ctx.fill();
    //text
    ctx.beginPath();
    ctx.font = "40px Helvetica";
    ctx.textAlign = "center";
    ctx.strokeStyle="black";
    ctx.lineWidth = 4;
    ctx.strokeText(name, 150, 125 + 43 / 4 - 10);
    ctx.beginPath();
    ctx.textAlign = "center";
    ctx.fillStyle = "white";
    ctx.fillText(name, 150, 125 + 43 / 4 - 10);
    //bid values
    ctx.beginPath();
    ctx.font = "20px Helvetica";
    ctx.textAlign = "center";
    ctx.strokeStyle="black";
    ctx.lineWidth = 3;
    ctx.strokeText(Math.round(bidValue,2), 150, 125 + 43 / 4 + 20);
    ctx.beginPath();
    ctx.textAlign = "center";
    ctx.fillStyle = "white";
    ctx.fillText(Math.round(bidValue,2), 150, 125 + 43 / 4 + 20);
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

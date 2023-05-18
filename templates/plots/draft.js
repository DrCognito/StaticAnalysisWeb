function add_image(draft, canv) {
    var url = "{{url_for("static", filename= "/plots/" + team)}}";
    url = url + "/drafts/" + draft + ".png"
    // console.log("Added " + url);
    // var img = document.createElement("img");
    img = new Image;
    img.src = url;
    img.id = draft;
    img.canv = canv;
    img.onload = img_onload(img);
    // document.body.appendChild(img);
    return img;
}

function add_canvas(canv_id){
    var canv = document.createElement("CANVAS");
    canv.id = canv_id;
    canv.width = 200;
    canv.height = 100;
    // Also add to main
    document.getElementById("main").appendChild(canv);
    return canv;
}

function img_onload(img){
    var canv = img.canv;
    loaded_count[canv]++;
    max_height[canv] = Math.max(max_height[canv], img.height);
    max_width[canv] = Math.max(max_width[canv], img.width);

    if(loaded_count[canv] === sheets[canv].length){
        draw_drafts(canv);
    }
}

function draw_drafts(canv){
    console.log("This is where we draw: " + canv);
    console.log("Max X: " + max_width[canv] + " Max Y: " + max_height[canv]);
}

var replays = {{plots["plot_drafts"]}};
var sheets = new Map();
var canvas =  new Map();
var max_height = new Map();
var max_width = new Map();
var loaded_count = new Map();

canvas["canv_0"] = add_canvas("canv_0");
sheets["canv_0"] = new Array();
loaded_count["canv_0"] = 0;
max_height["canv_0"] = -Infinity;
max_width["canv_0"] = -Infinity;
console.log("Draft.js");

for (let i = 0, len = replays.length, s = 0, j = 0; i < len; i++, j++){
    var canv = "canv_" + s;
    draft = replays[i];
    sheets[canv].push(add_image(draft, canv));

    if(i !== 0 && i%12 === 0){
        s++;
        var canv = "canv_" + s;
        j = 0;
        sheets[canv] =  new Array();
        canvas[canv] = add_canvas(canv);
        loaded_count[canv] = 0;
        max_height[canv] = -Infinity;
        max_width[canv] = -Infinity;
    }
}
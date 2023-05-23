function add_image(draft, canv) {
    var url = "{{url_for("static", filename= "/plots/" + team)}}";
    url = url + "/drafts/" + draft + ".png"
    // console.log("Added " + url);
    // var img = document.createElement("img");
    img = new Image;
    img.src = url;
    img.id = draft;
    img.canv = canv;
    // This has to be in function and use "this" or img will be cached as an unloaded obj it seems.
    img.onload =  function () {
        var canv = this.canv;
        loaded_count[canv]++;
        max_height[canv] += this.height;
        max_width[canv] = Math.max(max_width[canv], this.width);

        if(loaded_count[canv] === r_count[canv]){
            draw_drafts(canv);
        }
    };
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
    var canv = this.canv;
    loaded_count[canv]++;
    max_height[canv] += this.height;
    max_width[canv] = Math.max(max_width[canv], this.width);

    if(loaded_count[canv] === r_count[canv]){
        draw_drafts(canv);
    }
}

function draw_drafts(canv){
    // console.log("This is where we draw: " + canv);
    // console.log("Max X: " + max_width[canv] + " Max Y: " + max_height[canv]);
    var spacing = 0;
    canvas[canv].height = max_height[canv] + 13*spacing;
    canvas[canv].width = max_width[canv];

    const ctx = canvas[canv].getContext("2d");
    for(let i = 0, y = 0; i < sheets[canv].length; i++){
        let img = sheets[canv][i];
        ctx.drawImage(img, 0, y);
        y += img.height + spacing;
    }
}

const per_sheet = 13;
var replays = {{plots["plot_drafts"]}};
var sheets = new Map();
var canvas =  new Map();
var max_height = new Map();
var max_width = new Map();
var loaded_count = new Map();

canvas["canv_0"] = add_canvas("canv_0");
sheets["canv_0"] = new Array();
loaded_count["canv_0"] = 0;
max_height["canv_0"] = 0;
max_width["canv_0"] = 0;
console.log("Draft.js");

// Do this in advance to ensure that we await the propper amount of replays
// There might be a better way to do this but lets not over think it.
var n_replays = replays.length/per_sheet;
var r_count = new Map();
for(let i = 0; i < Math.floor(n_replays); i++){
    var canv = "canv_" + i;
    r_count[canv] = per_sheet;
}
r_count["canv_" + Math.floor(n_replays)] = replays.length % per_sheet;


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
        max_height[canv] = 0;
        max_width[canv] = 0;
    }
}
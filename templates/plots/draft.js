function add_image(draft) {
    var url = "{{url_for("static", filename= "/plots/" + team)}}";
    url = url + "/drafts/" + draft + ".png"
    console.log("Added " + url);
    // var img = document.createElement("img");
    img = new Image;
    img.src = url;
    img.id = draft;
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

var replays = {{plots["plot_drafts"]}};
var sheets = [];
var canvas = [];
canvas[0] = add_canvas("canv_0");
console.log("Draft.js");

for (let i = 0, len = replays.length, s = 0, j = 0; i < len; i++, j++){
    if(i%13 === 0){
        s++;
        j = 0;
        sheets[s] = [];
        canvas[s] = add_canvas("canv_" + s);
    }
    draft = replays[i];
    sheets[s][j] = add_image(draft);
}
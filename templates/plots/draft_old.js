{% for draft in plots["plot_drafts"] %}
<p>{{team}}/{{dataset}}/{{draft}}.png</p><br>
{% endfor %}
{% for draft in plots["plot_drafts"] %}
<canvas id='draftcanvas_{{loop.index}}' width="200" height="100"></canvas>
{% endfor %}
var 
{% for draft in plots["plot_drafts"] %}
//var img{{loop.index}} = document.createElement('img');
var img{{loop.index}} = new Image();
//document.body.appendChild(img{{loop.index}});
img{{loop.index}}.id = 'draftimg_{{loop.index}}';
//img{{loop.index}}.class = 'img-fit'

img{{loop.index}}.src = '{{draft}}'
var canvas{{loop.index}} = document.getElementById('draftcanvas_{{loop.index}}');

//img{{loop.index}}.addEventListener('load', draftCanvas(img{{loop.index}}, canvas{{loop.index}}));
img{{loop.index}}.onload  = draftCanvas(img{{loop.index}}, canvas{{loop.index}});
img{{loop.index}}.onload  = function(){
//console.log("loaded {{draft}}");
//console.log(img{{loop.index}}.width);
//canvas{{loop.index}}.width = img{{loop.index}}.width;
//canvas{{loop.index}}.height = img{{loop.index}}.height;

canvas{{loop.index}}.getContext('2d').drawImage(img{{loop.index}}, 10, 0);
};
{% endfor %}
function draftCanvas(image, canvas) {
console.log("loaded {{draft}}");
console.log(image.width);
canvas.width = image.width;
canvas.height = image.height;

canvas.getContext('2d').drawImage(image, 0, 0);
}
function highLightLine(highlights, canvas, hasHeader=false){
var offset = 13;
if(hasHeader){
    offset += 49;
}
var box_height = 146;
for(let i = 0; i <= highlights.length; i++ ){
    let extra = highlights[i];
    extra = 0;
    let y1 = highlights[i]*box_height + offset + extra;
    let height = 130;
    let x1 = 0;
    let width = 9;

    var ctx = canvas.getContext("2d");
    ctx.fillStyle = "blue";
    ctx.fillRect(x1, y1, width, height);
}
}
function add_image(draft) {
var url = {{"static", filename=team + "/" + dataset + "/" + draft + ".png"}};
var img = document.createElement("img");
img.src = url;
img.id = draft;
document.body.appendChild(img);

return image;
} 

function draftCanvas(image, canvas) {
    clearRect();
    console.log("loaded {{draft}}");
    console.log(img.width);
    canvas.width = img.width;
    canvas.height = img.height;

    canvas.getContext('2d').drawImage(image, 0, 0);
}
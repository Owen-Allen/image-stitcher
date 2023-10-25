


function allowDrop(event) {
    event.preventDefault();
}

function drag(event) {
    console.log('DRAG')
    console.log(event)
    event.dataTransfer.setData("text", event.target.id);
}



function dropLeft(event) {
    console.log('DROP LEFT')

    console.log(event.dataTransfer.files);

    // event.preventDefault();
    // var data = event.dataTransfer.getData("text");
    // console.log(event)
    // console.log(event.dataUrl)

    // var img = document.getElementById(data);
    // var canvas = document.createElement('canvas');
    // var ctx = canvas.getContext('2d');
    // ctx.drawImage(img, 0, 0);
    // var dataURL = canvas.toDataURL();
    // document.getElementById('left_image_input').value = dataURL;
}

function dropRight(event) {
    event.preventDefault();
    var data = event.dataTransfer.getData("text");
    var img = document.getElementById(data);
    var canvas = document.createElement('canvas');
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    var dataURL = canvas.toDataURL();
    document.getElementById('right_image_input').value = dataURL;
}
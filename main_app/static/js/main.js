console.log("hihi")
let buttonDone = document.querySelector("#done-btn")
let imagePanel = document.querySelector("#image-container")
let memeImg = document.querySelector('#capture')
let buttonAddText = document.querySelector("#add-text-btn")
let uploadMemeForm = document.querySelector("#upload-meme")
let uploadMemeData = document.querySelector("#img-data")



buttonDone.addEventListener('click', (event)=>{
    event.preventDefault()
    html2canvas(document.querySelector("#capture"), { allowTaint: true, useCORS: true}).then(canvas => {
        // var img = new Image();
        // img.origin = 'anonymous';
        let img= canvas.toDataURL("img/jpg");
        console.log(img)

        let newImg = document.createElement("img")
        newImg.src = img
        imagePanel.appendChild(newImg)
        //pass document 


        //setting up the form for uploading!!
        uploadMemeForm.style.display="block"
        uploadMemeData.value = img
        buttonDone.style.display="none"        
       
        //NEED TO CHANGE CORS ON AMAZON S3!!!
        // hide done button. show a new button associated with form...transferring blob object to python backend. 
    });
})



function b64toBlob(dataURI) {
    var byteString = atob(dataURI.split(',')[1]);
    var ab = new ArrayBuffer(byteString.length);
    var ia = new Uint8Array(ab);
    for (var i = 0; i < byteString.length; i++) {
        ia[i] = byteString.charCodeAt(i);
    }
    return new Blob([ab], { type: 'image/jpeg' });
}

buttonAddText.addEventListener('click',(event)=>{
    event.preventDefault()
    let newTextContainer = document.createElement("div")
    let newTextBox = document.createElement("input")
    newTextBox.setAttribute("placeholder", "your text")
    newTextContainer.appendChild(newTextBox)
    newTextContainer.classList.add("draggable")
    memeImg.appendChild(newTextContainer)
} )


const position = { x: 0, y: 0 }

interact('.draggable').draggable({
listeners: {
    start (event) {
    console.log(event.type, event.target)
    },
    move (event) {
    position.x += event.dx
    position.y += event.dy

    event.target.style.transform =
        `translate(${position.x}px, ${position.y}px)`
    },
}
})
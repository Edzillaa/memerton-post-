const buttonDone = document.querySelector("#done-btn")
const imagePanel = document.querySelector("#image-container")
const memeImg = document.querySelector('#capture')
const buttonAddText = document.querySelector("#add-text-btn")
const uploadPhotoForm = document.querySelector("#upload-photo-form")
const uploadMemeForm = document.querySelector("#upload-meme")
const uploadMemeData = document.querySelector("#img-data")
const elem = document.querySelector('.grid')
const allMemeText =Array.from(document.querySelectorAll('.draggable'))

buttonDone.addEventListener('click', (event)=>{
    event.preventDefault()
    html2canvas(document.querySelector("#capture"), {backgroundColor: "rgba(0,0,0,0)", allowTaint: true, useCORS: true}).then(canvas => {
        let img= canvas.toDataURL("img/jpg");
        uploadMemeForm.style.display="block"
        uploadMemeData.value = img
        buttonDone.style.display="none"      
        buttonAddText.style.display="none"  
        uploadPhotoForm.style.display="none"
    });
})

//double clicking text will delete text
allMemeText.forEach(text=>{
    text.addEventListener('dblclick', (event)=>{
        event.target.style.display="none"
    })
})

buttonAddText.addEventListener('click',(event)=>{
    event.preventDefault()
    let newTextContainer = document.createElement("div")
    let newTextBox = document.createElement("input")
    newTextBox.setAttribute("placeholder", "TEXT")
    newTextBox.classList.add("meme-text")
    newTextContainer.appendChild(newTextBox)
    newTextContainer.classList.add("draggable")
    memeImg.appendChild(newTextContainer)
    allMemeText.push(newTextContainer)
    allMemeText.forEach(text=>{
        text.addEventListener('dblclick', (event)=>{
            event.target.style.display="none"
        })
    })
} )

const position = { x: 0, y: 0 }
interact('.draggable').draggable({
listeners: {
    start (event) {
    console.log(event.type, event.target)
    },
    move (event) {
        let {x,y} = event.target.dataset
        x = (+x || 0) + event.dx;
        y = (+y || 0) + event.dy;
        event.target.style.transform = `translate(${x}px, ${y}px)`;
        Object.assign(event.target.dataset, { x, y });
    },
}
})

//MasonryJS jquery stuff
$('.grid').masonry({
    // options
    itemSelector: '.grid-item',
    columnWidth: 200
});

// materialize jquery stuff
$(".button-collapse").sideNav();


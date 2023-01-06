const buttonDone = document.querySelector("#done-btn")
const imagePanel = document.querySelector("#image-container")
const memeImg = document.querySelector('#capture')
const buttonAddText = document.querySelector("#add-text-btn")
const uploadPhotoForm = document.querySelector("#upload-photo-form")
const uploadMemeForm = document.querySelector("#upload-meme")
const uploadMemeData = document.querySelector("#img-data")
const elem = document.querySelector('.grid')
const allMemeText =Array.from(document.querySelectorAll('.draggable'))
const allMemeTextBox = Array.from(document.querySelectorAll('.meme-text'))
const colorArray = ['red','orange','yellow','green','blue','indigo','violet','white']
let count = 0;

buttonDone.addEventListener('click', (event)=>{
    event.preventDefault()
    textColors = []
    allMemeTextBox.forEach(text =>{
        textColors.push(text.style.color)
    })
    console.log(textColors)
    html2canvas(document.querySelector("#capture"), {
        scale: 1.1 ,
        backgroundColor: "rgba(0,0,0,0)", 
        useCORS: true, 
        onclone: function(el){
            const textboxes = el.querySelectorAll('.meme-text')
            textboxes.forEach((text, idx)=>{
                const textCoords = text.getBoundingClientRect();
                let oldCen  = textCoords.left + textCoords.width/2 //distance btn left edge of photo and text center
                text.style.cssText=`font-size:16px!important; transform:scale(2.5); position: absolute; left:0px; width: ${textCoords.width}px !important; `
                const newCoords = text.getBoundingClientRect();
                let newCen= oldCen - newCoords.left-(textCoords.width/2)//distance clone textbox needs to move left
                text.style.cssText=`font-size:16px!important; transform:scale(2.5); position: absolute;left:${newCen}px; width: ${textCoords.width}px !important; color: ${textColors[idx]}!important;`
            })
        }
    }).then(function(canvas){
        let img= canvas.toDataURL("img/jpg");
        uploadMemeForm.style.display="block"
        uploadMemeData.value = img
        buttonDone.style.display="none"      
        buttonAddText.style.display="none"  
        uploadPhotoForm.style.display="none"
        
    })
})
 
//double clicking text will delete text
allMemeText.forEach(text=>{
    text.addEventListener('dblclick', (event)=>{
        event.target.remove()
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
    allMemeTextBox.push(newTextBox)
    console.log(allMemeText)
    allMemeText.forEach(text=>{
        text.addEventListener('dblclick', (event)=>{
            event.target.remove()
        })
    })
    allMemeTextBox.forEach(textbox=>{
        textbox.addEventListener('input', resizeInput); 
        textbox.addEventListener('keydown', changeColors)
    })
} )

allMemeTextBox.forEach(textbox=>{
    textbox.addEventListener('input', resizeInput); 
    textbox.addEventListener('keydown', changeColors)
})

function changeColors(event){
    if (event.key === 'ArrowUp'){
        if (count >= colorArray.length-1){
            count = 0
        } else {
            count++
        }
    } else if (event.key === 'ArrowDown'){
        if (count < 0){
            count = colorArray.length-1
        } else {
            count--
        }
    }
    console.log(count)
    event.target.style.cssText=`color:${colorArray[count]}!important;width:${this.value.length}ch !important`
}

function resizeInput() {
    this.style.cssText = `width:${this.value.length}ch !important`;
}

interact('.draggable').draggable({
    listeners: {
              // call this function on every dragmove event
      move: dragMoveListener,
    }
})

function dragMoveListener (event) {
    var target = event.target
    // keep the dragged position in the data-x/data-y attributes
    var x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx
    var y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy  
    // translate the element
    target.style.transform = 'translate(' + x + 'px, ' + y + 'px)'
    // update the position attributes
    target.setAttribute('data-x', x)
    target.setAttribute('data-y', y)
}

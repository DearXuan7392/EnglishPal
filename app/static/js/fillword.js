isRead = true;
isChoose = true;
function getWord(){
   var word = window.getSelection?window.getSelection():document.selection.createRange().text;
   return word;
}
function fillinWord(){
   var word = getWord();
   if (isRead) read(word);
   if (!isChoose) return;
   var element = document.getElementById("selected-words");
   element.value = element.value + " " + word;
}
document.getElementById("text-content").addEventListener("click", fillinWord, false);
function read(s){
   var msg = new SpeechSynthesisUtterance(s);
   window.speechSynthesis.speak(msg);
}
function onReadClick(){
    isRead = !isRead;
}
function onChooseClick(){
    isChoose = !isChoose;
}
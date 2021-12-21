function cancelBtnHandler(){
    cancel_highLight();
    document.getElementById("text-content").removeEventListener("click", fillinWord, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillinWord, false);
    document.getElementById("text-content").addEventListener("click", fillinWord2, false);
    document.getElementById("text-content").addEventListener("touchstart", fillinWord2, false);
}

function showBtnHandler(){
    document.getElementById("text-content").removeEventListener("click", fillinWord2, false);
    document.getElementById("text-content").removeEventListener("touchstart", fillinWord2, false);
    document.getElementById("text-content").addEventListener("click", fillinWord, false);
    document.getElementById("text-content").addEventListener("touchstart", fillinWord, false);
    highLight();
}

function getWord(){
   var word = window.getSelection?window.getSelection():document.selection.createRange().text;
   return word;
}

function highLight(){
    var txt=document.getElementById("article").innerText;
    var list=document.getElementById("selected-words").value.split(" ");
    var list2=document.getElementById("selected-words2").value.split(" ");
    for(var i=0;i<list.length;++i){
        list[i]=list[i].replace(/(^\s*)|(\s*$)/g, "");
        if(list[i]!=""&&"<mark>".indexOf(list[i])==-1&&"</mark>".indexOf(list[i])==-1){
            txt=txt.replace(new RegExp(list[i],"g"),"<mark>"+list[i]+"</mark>");
        }
    }
    for(var i=0;i<list2.length;++i){
        list2[i]=list2[i].replace(/(^\s*)|(\s*$)/g, "");
        if(list2[i]!=""&&"<mark>".indexOf(list2[i])==-1&&"</mark>".indexOf(list2[i])==-1){
            txt=txt.replace(new RegExp(list2[i],"g"),"<mark>"+list2[i]+"</mark>");
        }
    }
    document.getElementById("article").innerHTML=txt;
}

function cancel_highLight(){
    var txt=document.getElementById("article").innerText;
    var list=document.getElementById("selected-words").value.split(" ");
    var list2=document.getElementById("selected-words2").value.split(" ");
    for(var i=0;i<list.length;++i){
        list[i]=list[i].replace(/(^\s*)|(\s*$)/g, "");
        if(list[i]!=""){
            txt=txt.replace("<mark>"+list[i]+"</mark>","list[i]");
        }
    }
    for(var i=0;i<list2.length;++i){
        list2[i]=list2[i].replace(/(^\s*)|(\s*$)/g, "");
        if(list2[i]!=""){
            txt=txt.replace("<mark>"+list[i]+"</mark>","list[i]");
        }
    }
    document.getElementById("article").innerHTML=txt;
}

function fillinWord(){
   highLight();
}

function fillinWord2(){
   cancel_highLight();
}

showBtnHandler();

document.querySelector('#symbol').onclick = function() {
    if(document.querySelector('#symbol').value === '') {
        document.querySelector('#submit').disabled = true;
    }
};
document.querySelector('#shares').onkeyup = function() {
    if(document.querySelector('#shares').value === '') {
        document.querySelector('#submit').disabled = true;
    }
    else {
        document.querySelector('#submit').disabled = false;
    }
};
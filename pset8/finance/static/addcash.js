document.querySelector('#cash').onkeyup = function() {
   if(document.querySelector('#cash').value === '') {
       document.querySelector('#submit').disabled = true;
      }
   else {
      document.querySelector('#submit').disabled = false;
   }
};
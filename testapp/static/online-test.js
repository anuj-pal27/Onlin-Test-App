
const inputs = document.querySelectorAll('.input-field');

inputs.forEach(function (input) {
  input.addEventListener('focus', function () {
    input.removeAttribute('placeholder');
  });

  input.addEventListener('blur', function () {
    input.setAttribute('placeholder', input.getAttribute('data-placeholder'));
  });
});

// login/register--!

var button1 = document.getElementById('myButton1');
var button2 = document.getElementById('myButton2');

button1.addEventListener('click', function () {
  button1.style.backgroundColor = '#e3ebf7';
  button2.style.backgroundColor = '';
});

button2.addEventListener('click', function () {
  button2.style.backgroundColor = '#e3ebf7';
  button1.style.backgroundColor = '';
});


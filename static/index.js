var openTrigger = $('.menu-trigger');
var openTriggerTop = openTrigger.find('.menu-trigger-bar.top');
var openTriggerMiddle = openTrigger.find('.menu-trigger-bar.middle');
var openTriggerBottom = openTrigger.find('.menu-trigger-bar.bottom');

//CLOSE TRIGGER
var closeTrigger = $('.close-trigger');
var closeTriggerLeft = closeTrigger.find('.close-trigger-bar.left');
var closeTriggerRight = closeTrigger.find('.close-trigger-bar.right');

//LOGO
var logo = $('.logo');

//MENU
var menuContainer = $('.menu-container');
var menu = $('.menu');
var menuTop = $('.menu-bg.top');
var menuMiddle = $('.menu-bg.middle');
var menuBottom = $('.menu-bg.bottom');

//TL
var tlOpen = new TimelineMax({ paused: true });
var tlClose = new TimelineMax({ paused: true });

//OPEN TIMELINE
tlOpen.add("preOpen")
  .to(logo, 0.4, {
    scale: 0.8,
    opacity: 0,
    ease: Power2.easeOut,onComplete: function () {
      logo.css('z-index', '10');
    }
  }, "preOpen")
  .to(openTriggerTop, 0.4, {
    x: "+80px", y: "-80px", delay: 0.1, ease: Power4.easeIn, onComplete: function () {
      closeTrigger.css('z-index', '25');
    }
  }, "preOpen")
  .to(openTriggerMiddle, 0.4, {
    x: "+=80px", y: "-=80px", ease: Power4.easeIn,
    onComplete: function () {
      openTrigger.css('visibility', 'hidden');
    }
  }, "preOpen")
  .to(openTriggerBottom, 0.4, {
    x: "+=80px", y: "-=80px", delay: 0.2, ease: Power4.easeIn
  }, "preOpen")
  .add("open", "-=0.4")
  .to(menuTop, 0.8, {
    y: "13%",
    ease: Power4.easeInOut
  }, "open")
  .to(menuMiddle, 0.8, {
    scaleY: 1,
    ease: Power4.easeInOut
  }, "open")
  .to(menuBottom, 0.8, {
    y: "-114%",
    ease: Power4.easeInOut
  }, "open")
  .fromTo(menu, 0.6, {
    y: 30, opacity: 0, visibility: 'hidden'
  }, {
    y: 0, opacity: 1, visibility: 'visible', ease: Power4.easeOut
  }, "-=0.2")
  .add("preClose", "-=0.8")
  .to(closeTriggerLeft, 0.8, {
    x: "-=100px", y: "+=100px", ease: Power4.easeOut
  }, "preClose")
  .to(closeTriggerRight, 0.8, {
    x: "+=100px", y: "+=100px", delay: 0.2, ease: Power4.easeOut
  }, "preClose");

//CLOSE TIMELINE
tlClose.add("close")
  .to(menuTop, 0.2, {
    backgroundColor: "#ff908b", ease: Power4.easeInOut, onComplete: function () {
      logo.css('z-index', '26');
      closeTrigger.css('z-index', '5');
      openTrigger.css('visibility', 'visible');
    }
  }, "close")
  .to(menuMiddle, 0.2, {
    backgroundColor: "#ff908b", ease: Power4.easeInOut
  }, "close")
  .to(menuBottom, 0.2, {
    backgroundColor: "#ff908b", ease: Power4.easeInOut
  }, "close")
  .to(menu, 0.6, {
    y: 20, opacity: 0, ease: Power4.easeOut, onComplete: function () {
      menu.css('visibility', 'hidden');
    }
  }, "close")
  .to(logo, 0.8, {
    scale: 1, opacity: 1, ease: Power4.easeInOut,onComplete: function () {
      logo.css('z-index', '26');
    }
  }, "close", "+=0.2")
  .to(menuTop, 0.8, {
    y: "-113%",
    ease: Power4.easeInOut
  }, "close", "+=0.2")
  .to(menuMiddle, 0.8, {
    scaleY: 0,
    ease: Power4.easeInOut
  }, "close", "+=0.2")
  .to(menuBottom, 0.8, {
    y: "23%",
    ease: Power4.easeInOut,
    onComplete: function () {
      menuTop.css('background-color', '#ff908b');
      menuMiddle.css('background-color', '#ff908b');
      menuBottom.css('background-color', '#ff908b');
    }
  }, "close", "+=0.2")
  .to(closeTriggerLeft, 0.2, {
    x: "+=100px", y: "-=100px", ease: Power4.easeIn
  }, "close")
  .to(closeTriggerRight, 0.2, {
    x: "-=100px", y: "-=100px", delay: 0.1, ease: Power4.easeIn
  }, "close")
  .to(openTriggerTop, 1, {
    x: "-=80px", y: "+=80px", delay: 0.2, ease: Power4.easeOut
  }, "close")
  .to(openTriggerMiddle, 1, {
    x: "-=80px", y: "+=80px", ease: Power4.easeOut
  }, "close")
  .to(openTriggerBottom, 1, {
    x: "-=80px", y: "+=80px", delay: 0.1, ease: Power4.easeOut
  }, "close");

//EVENTS
openTrigger.on('click', function () {
  if (tlOpen.progress() < 1) {
    tlOpen.play();
  } else {
    tlOpen.restart();
  }
});

closeTrigger.on('click', function () {
  if (tlClose.progress() < 1) {
    tlClose.play();
  } else {
    tlClose.restart();
  }
});



function toggleFunctionFields() {
  var findPathFields = document.getElementById('findPathFields');
  var op1 = document.getElementById('ind');
  var op3 = document.getElementById('u22');
  var op4 = document.getElementById('z11');
  var op5 = document.getElementById('z22');
  var op2 = document.getElementById('cmp');
  var op6 = document.getElementById('path_in_bytellldp');

  var findRadio = document.getElementById('find');
  var findRadio1 = document.getElementById('individual');
  var findRadio2 = document.getElementById('compare');
  var findRadio3 = document.getElementById('u2');
  var findRadio4 = document.getElementById('z1');
  var findRadio5 = document.getElementById('z2');
  var findRadio6 = document.getElementById('find_in_bytellldp');

  var desInput = document.getElementById('des');
  var srcInput = document.getElementById('src');
  var srcInput_bytellldp = document.getElementById('bytellldp_source')

  var val = document.getElementById('option1');
  var val2 = document.getElementById('option2');
  var val3 = document.getElementById('option3');
  var val4 = document.getElementById('option4');

  if (findRadio.checked) {
    findPathFields.classList.remove('hidden');
    desInput.setAttribute('required', 'true');
    srcInput.setAttribute('required', 'true');
  } else {
    findPathFields.classList.add('hidden');
    desInput.removeAttribute('required');
    srcInput.removeAttribute('required');
  }

  if (findRadio1.checked) {
    op1.classList.remove('hidden');
    val.setAttribute('required', 'true');
  } else {
    op1.classList.add('hidden');
    val.removeAttribute('required');
  }

  if (findRadio2.checked) {
    val2.setAttribute('required', 'true');
    // val3.setAttribute('required', 'true');
    op2.classList.remove('hidden');
  } else {
    val2.removeAttribute('required');
    // val3.removeAttribute('required');
    op2.classList.add('hidden');
  }
  if (findRadio3.checked) {
    val4.setAttribute('required', 'true');
    op3.classList.remove('hidden');
  } else {
    val4.removeAttribute('required');
    op3.classList.add('hidden');
  }

  if (findRadio4.checked) {
    op4.classList.remove('hidden');
  } else {
    op4.classList.add('hidden');
  }
  if (findRadio5.checked) {
    op5.classList.remove('hidden');
  } else {
    op5.classList.add('hidden');
  }
  if (findRadio6.checked) {
    srcInput_bytellldp.setAttribute('required', 'true');
    op6.classList.remove('hidden');
  } else {
    srcInput_bytellldp.removeAttribute('required')
    op6.classList.add('hidden');
  }

}

document.getElementById('myForm').addEventListener('submit', function (event) {
  var visRadio = document.getElementById('vis');
  var findRadio = document.getElementById('find');
  var findRadio1 = document.getElementById('individual');
  var findRadio2 = document.getElementById('compare');
  var findRadio3 = document.getElementById('u2');
  var findRadio4 = document.getElementById('find_in_bytellldp');
  var findRadio5 = document.getElementById('show_all');
  var findRadio6 = document.getElementById('z1');
  var findRadio7 = document.getElementById('z2');

  if (!visRadio.checked && !findRadio.checked && !findRadio1.checked && !findRadio2.checked && !findRadio3.checked && !findRadio4.checked && !findRadio5.checked
    && !findRadio6.checked && !findRadio7.checked) {
    alert('Please select a function.');
    event.preventDefault(); // Prevent form submission
  }
});


document.addEventListener('DOMContentLoaded', function () {
  // Get all components with the 'hidden txt' class
  const components = document.querySelectorAll('.hidden.txt');

  components.forEach(component => {
    // Find all input fields within the current component
    const inputFields = component.querySelectorAll('.chosen-value');

    inputFields.forEach(inputField => {
      const dropdown = inputField.nextElementSibling; // The dropdown ul follows the input field
      const dropdownArray = [...dropdown.querySelectorAll('li')];

      let valueArray = [];
      dropdownArray.forEach(item => {
        valueArray.push(item.textContent);
      });

      const closeDropdown = () => {
        dropdown.classList.remove('open');
      }

      inputField.addEventListener('input', () => {
        dropdown.classList.add('open');
        let inputValue = inputField.value.toLowerCase();
        if (inputValue.length > 0) {
          for (let j = 0; j < valueArray.length; j++) {
            if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
              dropdownArray[j].classList.add('closed');
            } else {
              dropdownArray[j].classList.remove('closed');
            }
          }
        } else {
          for (let i = 0; i < dropdownArray.length; i++) {
            dropdownArray[i].classList.remove('closed');
          }
        }
      });

      dropdownArray.forEach(item => {
        item.addEventListener('click', (evt) => {
          inputField.value = item.textContent;
          inputField.setAttribute('value', item.getAttribute('value')); // Set the value attribute
          closeDropdown();
          dropdownArray.forEach(dropdown => {
            dropdown.classList.add('closed');
          });
        });
      });

      inputField.addEventListener('focus', () => {
        inputField.placeholder = 'Type to filter';
        dropdown.classList.add('open');
        dropdownArray.forEach(dropdown => {
          dropdown.classList.remove('closed');
        });
      });

      inputField.addEventListener('blur', () => {
        inputField.placeholder = 'Select state';
        dropdown.classList.remove('open');
      });

      document.addEventListener('click', (evt) => {
        const isDropdown = dropdown.contains(evt.target);
        const isInput = inputField.contains(evt.target);
        if (!isDropdown && !isInput) {
          closeDropdown();
        }
      });
    });
  });
});

// const inputField = document.querySelector('.chosen-value');
// const dropdown = document.querySelector('.value-list');
// const dropdownArray = [... document.querySelectorAll('.value-list li')];
// const val6 = document.getElementById('option6')
// console.log( dropdownArray)
// // dropdown.classList.add('open');
// // inputField.focus(); // Demo purposes only
// let valueArray = [];
// dropdownArray.forEach(item => {
//   valueArray.push(item.textContent);
// });

// const closeDropdown = () => {
//   dropdown.classList.remove('open');
// }

// inputField.addEventListener('input', () => {
//   dropdown.classList.add('open');
//   let inputValue = inputField.value.toLowerCase();
//   let valueSubstring;
//   if (inputValue.length > 0) {
//     for (let j = 0; j < valueArray.length; j++) {
//       if (!(inputValue.substring(0, inputValue.length) === valueArray[j].substring(0, inputValue.length).toLowerCase())) {
//         dropdownArray[j].classList.add('closed');
//       } else {
//         dropdownArray[j].classList.remove('closed');
//       }
//     }
//   } else {
//     for (let i = 0; i < dropdownArray.length; i++) {
//       dropdownArray[i].classList.remove('closed');
//     }
//   }
// });

// dropdownArray.forEach(item => {
//   item.addEventListener('click', (evt) => {
//     inputField.value = item.textContent;
//     inputField.setAttribute('value',item.getAttribute('value'))
//     dropdownArray.forEach(dropdown => {
//       dropdown.classList.add('closed');
//     });
//   });
// })

// inputField.addEventListener('focus', () => {
//    inputField.placeholder = 'Type to filter';
//    dropdown.classList.add('open');
//    dropdownArray.forEach(dropdown => {
//      dropdown.classList.remove('closed');
//    });
// });

// inputField.addEventListener('blur', () => {
//    inputField.placeholder = 'Select state';
//   dropdown.classList.remove('open');
// });

// document.addEventListener('click', (evt) => {
//   const isDropdown = dropdown.contains(evt.target);
//   const isInput = inputField.contains(evt.target);
//   if (!isDropdown && !isInput) {
//     dropdown.classList.remove('open');
//   }
// });
//OPEN TRIGGER

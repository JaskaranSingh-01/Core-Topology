function toggleFunctionFields() {
            var findPathFields = document.getElementById('findPathFields');
            var ind = document.getElementById('ind');
            var cmp = document.getElementById('cmp');
            var u22 = document.getElementById('u22');
            var z11 = document.getElementById('z11');
            var z22 = document.getElementById('z22');
            var path_in_bytellldp = document.getElementById('path_in_bytellldp');

            findPathFields.classList.add('hidden');
            ind.classList.add('hidden');
            cmp.classList.add('hidden');
            u22.classList.add('hidden');
            z11.classList.add('hidden');
            z22.classList.add('hidden');
            path_in_bytellldp.classList.add('hidden');

            if (document.getElementById('find').checked) {
                findPathFields.classList.remove('hidden');
            } else if (document.getElementById('individual').checked) {
                ind.classList.remove('hidden');
            } else if (document.getElementById('compare').checked) {
                cmp.classList.remove('hidden');
            } else if (document.getElementById('u2').checked) {
                u22.classList.remove('hidden');
            } else if (document.getElementById('z1').checked) {
                z11.classList.remove('hidden');
            } else if (document.getElementById('z2').checked) {
                z22.classList.remove('hidden');
            } else if (document.getElementById('find_in_bytellldp').checked) {
                path_in_bytellldp.classList.remove('hidden');
            }
        }

document.getElementById('myForm').addEventListener('submit', function (event) {
    var visRadio = document.getElementById('vis');
    var findRadio = document.getElementById('find');
    var findRadio1 = document.getElementById('individual');
    var findRadio2 = document.getElementById('compare');
    var findRadio3 = document.getElementById('u2');
    var findRadio4 = document.getElementById('find_in_bytellldp');

    if (!visRadio.checked && !findRadio.checked && !findRadio1.checked && !findRadio2.checked && !findRadio3.checked && !findRadio4.checked && !findRadio5.checked && !findRadio4) {
        alert('Please select a function.');
        event.preventDefault(); // Prevent form submission
    }
});

const selected = document.querySelector(".selected");
const optionsContainer = document.querySelector(".options-container");
const searchBox = document.querySelector(".search-box input");

const optionsList = document.querySelectorAll(".option");

selected.addEventListener("click", () => {
  optionsContainer.classList.toggle("active");

  searchBox.value = "";
  filterList("");

  if (optionsContainer.classList.contains("active")) {
    searchBox.focus();
  }
});

optionsList.forEach(o => {
  o.addEventListener("click", () => {
    selected.innerHTML = o.querySelector("label").innerHTML;
    optionsContainer.classList.remove("active");
  });
});

searchBox.addEventListener("keyup", function(e) {
  filterList(e.target.value);
});

const filterList = searchTerm => {
  searchTerm = searchTerm.toLowerCase();
  optionsList.forEach(option => {
    let label = option.firstElementChild.nextElementSibling.innerText.toLowerCase();
    if (label.indexOf(searchTerm) != -1) {
      option.style.display = "block";
    } else {
      option.style.display = "none";
    }
  });
};


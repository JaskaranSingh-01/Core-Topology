const dragArea = document.querySelector('.drag-area');
const dragText = document.querySelector('.header');
let button = document.querySelector('.button');
let input = document.getElementById('fileInput');

let file;

button.onclick = () => {
    input.click();
};

input.addEventListener('change', function() {
    file = this.files[0];
    dragArea.classList.add('active');

    // Ensure the file chooser is closed before submitting the form
    setTimeout(function() {
        document.getElementById('upload-form').submit();
    }, 100); // Adjust the delay as needed
});

dragArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dragText.textContent = "Release to Upload.";
    dragArea.classList.add("active");
});

dragArea.addEventListener('dragleave', (e) => {
    e.preventDefault();
    dragText.textContent = "Drag and Drop.";
    dragArea.classList.remove("active");
});

dragArea.addEventListener('drop', (e) => {
    e.preventDefault();
    file = e.dataTransfer.files[0];
    let fileType = file.type;
    let validExtension = ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'text/csv'];

    if(validExtension.includes(fileType)) {
        let fileReader = new FileReader();
        fileReader.onload = () => {
            let fileURL = fileReader.result;
        };
        fileReader.readAsDataURL(file);
        
        // Create a new DataTransfer object and append the file to it
        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        
        // Assign the DataTransfer object to the input element
        input.files = dataTransfer.files;
        
        // Ensure the file chooser is closed before submitting the form
        setTimeout(function() {
            document.getElementById('upload-form').submit();
        }, 100); // Adjust the delay as needed
    } else {
        alert("Upload a valid file");
        dragArea.classList.remove('active');
    }
});


// Your JavaScript code from the previous index.html
const fileInput = document.getElementById('file-input');
const uploadButton = document.getElementById('upload-button');
const predictButton = document.getElementById('predict-button');
const resetButton = document.getElementById('reset-button');
const fileNameDisplay = document.getElementById('file-name');
const imageStatus = document.querySelector('.image-status');
const previewImg = document.querySelector('.preview-img');
const form = document.querySelector('form');

fileInput.addEventListener('change', function() {
    const file = fileInput.files[0];

    if (file) {
        fileNameDisplay.textContent = "File chosen: " + file.name;
        fileNameDisplay.style.display = 'block';

        uploadButton.style.display = 'inline-block';
        imageStatus.style.display = 'none';
        predictButton.style.display = 'none';
        resetButton.style.display = 'none';

        alert("File Chosen Successfully!");

        const reader = new FileReader();
        reader.onload = function(e) {
            if (previewImg) {
                previewImg.src = e.target.result;
            } else {
                const newImg = document.createElement('img');
                newImg.src = e.target.result;
                newImg.alt = "Uploaded Image";
                newImg.className = "preview-img";
                document.querySelector('.section-box').prepend(newImg);
                imageStatus.textContent = 'Image Uploaded!';
                imageStatus.style.display = 'block';
            }
        }
        reader.readAsDataURL(file);
    } else {
        fileNameDisplay.style.display = 'none';
        uploadButton.style.display = 'none';
        if (previewImg) {
            previewImg.removeAttribute('src');
            imageStatus.textContent = 'No image uploaded.';
            imageStatus.style.display = 'block';
        }
    }
});

uploadButton.addEventListener('click', function() {
    imageStatus.textContent = "Image Uploaded!";
    imageStatus.style.display = 'block';
    uploadButton.style.display = 'none';
    predictButton.style.display = 'inline-block';
    resetButton.style.display = 'inline-block';
});

resetButton.addEventListener('click', function() {
    form.reset();
    fileNameDisplay.style.display = 'none';
    imageStatus.textContent = 'No image uploaded.';
    imageStatus.style.display = 'block';
    predictButton.style.display = 'none';
    resetButton.style.display = 'none';
    uploadButton.style.display = 'none';
    if (previewImg) {
        previewImg.removeAttribute('src');
    }
});

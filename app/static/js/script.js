$(function () {
    $('[data-toggle="tooltip"]').tooltip()
})

window.addEventListener('DOMContentLoaded', function () {
    var image = document.getElementById('preview');
    var input = document.getElementById('imageInput');
    var imageBackup = document.getElementById('hidden-preview');
    var gridSizeSelect = document.getElementById('gridSize');
    var radioButtons = document.querySelectorAll('input[name="interpolation"]');
    var cropper;

    
    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            if (this.checked) {
                console.log('Selected radio button:', this.value);
                updateStep2(this.value)
            }
        });
    });



    input.addEventListener('change', function () {
        var file = this.files[0];
        var url = URL.createObjectURL(file);

        image.src = url;

        if (cropper) {
            cropper.destroy();
        }

        cropper = new Cropper(image, {
            aspectRatio: 1,
            viewMode: 1,
            minCropBoxWidth: 100,
            minCropBoxHeight: 100,
        });
    });

    document.getElementById('headingOne').addEventListener('click', function () {
        var file = input.files[0];
        var url = URL.createObjectURL(file);

        image.src = url;
        if (cropper) {
            cropper.destroy();
        }
        cropper = new Cropper(image, {
            aspectRatio: 1,
            viewMode: 1,
            minCropBoxWidth: 100,
            minCropBoxHeight: 100,
        });

        gridSizeSelect.selectedIndex = 0;
        radioButtons.forEach(function (radioButton) {
            radioButton.checked = false;
        });


        imageBackup.src = url;
    });

    document.getElementById('headingTwo').addEventListener('click', function () {
        var croppedImage = cropper.getCroppedCanvas().toDataURL();
        preview.src = croppedImage;
        imageBackup.src = croppedImage;
        cropper.destroy();
    });



    gridSizeSelect.addEventListener('change', function () {
        updateStep1();
    });

    function updateStep1() {
        var formData = new FormData();
        var gridSize = document.getElementById('gridSize').value;
        var url_backup = document.getElementById('hidden-preview').src;

        fetch(url_backup)
            .then(response => response.blob())
            .then(blob => {
                formData.append('file', blob);
                formData.append('gridSize', gridSize);

                return fetch('/apply_size', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => response.blob())
            .then(blob => {
                image.src = URL.createObjectURL(blob);

            })
            .catch(error => {
                console.error('Error:', error);
                alert('Image processing failed');
            });

    }







    function updateStep2(interpolation) {
        var formData = new FormData();
        var url_backup = document.getElementById('hidden-preview').src;
        var gridSize = document.getElementById('gridSize').value;

        fetch(url_backup)
            .then(response => response.blob())
            .then(blob => {
                formData.append('file', blob);
                formData.append('interpolation', interpolation);
                formData.append('gridSize', gridSize);
                console.log('interpolation:', interpolation);
                console.log('gridSize:', gridSize);

                return fetch('/apply_interpolation', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => response.blob())
            .then(blob => {
                image.src = URL.createObjectURL(blob);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Image processing failed');
            });
    }

});
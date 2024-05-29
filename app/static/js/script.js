// app/static/js/script.js
window.addEventListener('DOMContentLoaded', function () {
    var image = document.getElementById('preview');
    var input = document.getElementById('image');
    var button = document.getElementById('upload');
    var cropper;


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
            ready: function () {
                updateCroppedImage();
            },
            crop: function () {
                updateCroppedImage();
            }
        });
    });

    function updateCroppedImage() {
        cropper.getCroppedCanvas().toBlob(function (blob) {
            var croppedImageURL = URL.createObjectURL(blob);
            var img = document.getElementById('cropped');
            img.src = croppedImageURL;
        });
    }

    //     button.addEventListener('click', function () {
    //         if (cropper) {
    //             cropper.getCroppedCanvas().toBlob(function (blob) {
    //                 var formData = new FormData();
    //                 var gridSize = document.getElementById('gridSize').value; 
    //                 var resamplingMethod = document.getElementById('resamplingMethod').value;

    //                 formData.append('file', blob, 'image.jpg');
    //                 formData.append('gridSize', gridSize);
    //                 formData.append('resamplingMethod', resamplingMethod);

    //                 fetch('/apply_filter', {
    //                     method: 'POST',
    //                     body: formData
    //                 })
    //                 .then(response => response.blob())
    //                 .then(blob => {
    //                     var url = URL.createObjectURL(blob);
    //                     document.getElementById('cropped-filtred').src = url;
    //                 })
    //                 .catch(error => {
    //                     console.error('Error:', error);
    //                     alert('Image processing failed');
    //                 });
    //             });
    //         }
    //     });



    var resamplingMethodSelect = document.getElementById('resamplingMethod');
    var gridSizeSelect = document.getElementById('gridSize');


    function updateStep1() {
        if (cropper) {
            cropper.getCroppedCanvas().toBlob(function (blob) {
                var formData = new FormData();
                var gridSize = document.getElementById('gridSize').value;
                var resamplingMethod = document.getElementById('resamplingMethod').value;

                formData.append('file', blob, 'image.jpg');
                formData.append('gridSize', gridSize);
                formData.append('resamplingMethod', resamplingMethod);

                fetch('/apply_filter', {
                    method: 'POST',
                    body: formData
                })
                    .then(response => response.blob())
                    .then(blob => {
                        var url = URL.createObjectURL(blob);
                        document.getElementById('cropped-filtred').src = url;
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Image processing failed');
                    });
            });
        }
    }

    resamplingMethodSelect.addEventListener('change', function () {
        updateStep1();
    });
    gridSizeSelect.addEventListener('change', function () {
        updateStep1();
    });
}); 



function changeColor(id) {
    var select = document.getElementById(id);
    var circle = document.getElementById("circle" + id.slice(-1));
    console.log(select);
    circle.style.backgroundColor = select.value;
}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});
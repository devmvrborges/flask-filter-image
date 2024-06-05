window.addEventListener('DOMContentLoaded', function () {
    var image = document.getElementById('preview');
    var input = document.getElementById('imageInput');
    var imageBackup = document.getElementById('hidden-preview');
    var gridSizeSelect = document.getElementById('gridSize');
    var rangeColors = document.getElementById('customRange2');
    var radioButtons = document.querySelectorAll('input[name="interpolation"]');
    var cropper;
    var currentBlob;

    radioButtons.forEach(function (radioButton) {
        radioButton.addEventListener('change', function () {
            if (this.checked) {
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
        currentBlob = url_backup;

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
                currentBlob = image.src;
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Image processing failed');
            });
    }

    rangeColors.addEventListener('change', function () {
        document.getElementById('rangeValue').textContent = this.value;
        updateStep3(this.value);
    });

    function updateStep3(colors) {
        var formData = new FormData();
        var gridSize = document.getElementById('gridSize').value;
        fetch(currentBlob)
            .then(response => response.blob())
            .then(blob => {
                formData.append('file', blob);
                formData.append('colors', colors);
                formData.append('gridSize', gridSize);
                return fetch('/get_colors', {
                    method: 'POST',
                    body: formData
                });
            })
            .then(response => response.json())
            .then(data => {
                var imageBase64 = data.image;
                image.src = 'data:image/png;base64,' + imageBase64;
                data = data.data;
                var tbody = document.querySelector('tbody');
                tbody.innerHTML = '';
                data.forEach(function (item) {
                    console.log(item);
                    var tr = document.createElement('tr');

                    var td1 = document.createElement('td');
                    var label1 = document.createElement('label');
                    label1.textContent = item.name;
                    td1.appendChild(label1);

                    var td2 = document.createElement('td');
                    var div = document.createElement('div');
                    div.className = 'circle';
                    div.style.backgroundColor = item.color;
                    td2.appendChild(div);

                    var td3 = document.createElement('td');
                    var label2 = document.createElement('label');
                    label2.textContent = item.value;
                    td3.appendChild(label2);

                    tr.appendChild(td1);
                    tr.appendChild(td2);
                    tr.appendChild(td3);

                    tbody.appendChild(tr);
                });
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Image processing failed');
            });
    }
});

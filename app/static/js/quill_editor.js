document.addEventListener('DOMContentLoaded', function () {
    var quillOptions = {
        theme: 'snow',
        modules: {
            toolbar: {
                container: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'list': 'ordered' }, { 'list': 'bullet' }],
                    ['link', 'image']
                ],
                handlers: {
                    image: imageHandler
                }
            }
        }
    };

    // Yeni gönderi modalı içindeki Quill editör
    var newPostEditorElement = document.querySelector('#newPostEditor');
    if (newPostEditorElement) {
        var newPostEditor = new Quill(newPostEditorElement, quillOptions);
        document.querySelector('#newPostForm').onsubmit = function () {
            document.querySelector('input[name="content"]').value = newPostEditor.root.innerHTML;
        };
    }

    // Gönderi düzenleme modalı içindeki Quill editörleri
    var quillEditors = {};
    document.querySelectorAll('.updatePostForm').forEach(function (form) {
        var editorElement = form.querySelector('.editor');
        var editorId = editorElement.id;
        quillEditors[editorId] = new Quill('#' + editorId, quillOptions);
        var contentInput = form.querySelector('textarea[name="content"]');
        quillEditors[editorId].root.innerHTML = contentInput.value;

        form.onsubmit = function () {
            contentInput.value = quillEditors[editorId].root.innerHTML;
        };
    });

    // Modal açıldığında Quill editörünü yeniden başlat
    document.querySelectorAll('.modal').forEach(function (modal) {
        modal.addEventListener('shown.bs.modal', function (event) {
            var editorElement = modal.querySelector('.editor');
            if (editorElement) {
                var editorId = editorElement.id;
                var contentInput = modal.querySelector('textarea[name="content"]');
                if (quillEditors[editorId]) {
                    quillEditors[editorId].root.innerHTML = contentInput.value;
                }
            }
        });
    });

    // Resim yükleme işlevi
    function imageHandler() {
        var range = this.quill.getSelection();
        var value = prompt('Resim URL\'si girin veya yüklemek için boş bırakın');
        if (value) {
            this.quill.insertEmbed(range.index, 'image', value);
        } else {
            selectLocalImage(this.quill, range);
        }
    }

    function selectLocalImage(quill, range) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.click();

        input.onchange = function () {
            var file = input.files[0];
            if (file) {
                uploadImage(file, quill, range);
            }
        };
    }

    function uploadImage(file, quill, range) {
        var formData = new FormData();
        formData.append('image', file);

        fetch('/upload_image', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                quill.insertEmbed(range.index, 'image', data.url);
            } else {
                alert('Resim yüklenirken bir hata oluştu.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Resim yüklenirken bir hata oluştu.');
        });
    }
});
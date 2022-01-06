'use strict';

Dropzone.options.appUploadDropzone = false;

(function ($) {
    $(function () {
        let dropzoneDisabled = false;
        const fileDragId = 'app-upload-dropzone';
        const submitButton = $('#submit-button');
        const newUploadButton = $('#upload-new-app');
        const appUploadForm = $('#app-upload-form');

        window.addEventListener('dragenter', function (e) {
            if (e.target.id !== fileDragId || dropzoneDisabled) {
                e.preventDefault();
                e.dataTransfer.effectAllowed = 'none';
                e.dataTransfer.dropEffect = 'none';
            }
        }, false);

        window.addEventListener('dragover', function (e) {
            if (e.target.id !== fileDragId || dropzoneDisabled) {
                e.preventDefault();
                e.dataTransfer.effectAllowed = 'none';
                e.dataTransfer.dropEffect = 'none';
            }
        });

        window.addEventListener('drop', function (e) {
            if (e.target.id !== fileDragId || dropzoneDisabled) {
                e.preventDefault();
                e.dataTransfer.effectAllowed = 'none';
                e.dataTransfer.dropEffect = 'none';
            }
        });

        const dropzoneElement = $('.dropzone');

        newUploadButton.on('click', function () {
            $('.btn-row').slideUp(500);
            appUploadForm.slideDown(500);

            const uploadDropzone = new Dropzone('#app-upload-dropzone', {
                url: '/upload',
                method: 'post',
                paramName: 'file',
                acceptedFiles: '.apk,.zip',
                maxFilesize: '100',
                autoProcessQueue: false,
                maxFiles: 1,
                timeout: 0,
                dragover: function () {
                    dropzoneElement.addClass('hover dark-background');
                },
                dragleave: function () {
                    if (this.files.length) {
                        dropzoneElement.removeClass('dark-background');
                    } else {
                        dropzoneElement.removeClass('hover dark-background');
                    }
                },
                drop: function () {
                    dropzoneElement.removeClass('dark-background');
                },
                addedfile: function () {
                    if (this.files.length > 1) {
                        this.removeFile(this.files[0]);
                    }
                    $('#app-upload-message').text(this.files[0].name +
                        ' (' + (this.files[0].size / (1024 * 1024)).toFixed(1) + ' MB)');
                    dropzoneElement.addClass('hover').removeClass('dark-background');
                    submitButton.slideDown(500);
                },
                uploadprogress: function (file, progress) {
                    $('#file-progress').width(progress + '%');
                },
                sending: function (file, xhr, formData) {
                    $('#app-upload-message').slideUp(500);
                    dropzoneElement.animate({'padding': 0}, 500);
                    $('#file-progress-container').slideDown({
                        duration: 500,
                        start: function () {
                            $(this).css('display', 'flex');
                        }
                    });
                },
                error: function (file, err) {
                    const status = file.xhr && file.xhr.status;

                    if (status === 400) {
                        Swal.fire({
                            titleText: 'Bad request',
                            icon: 'error',
                            text: 'There was an error during the request. Make sure to ' +
                                'upload a valid application and retry.',
                            showConfirmButton: true
                        }).then(function () {
                            window.location.reload();
                        });
                    } else if (status === 413) {
                        Swal.fire({
                            titleText: 'File too large',
                            icon: 'error',
                            text: 'The uploaded file is too large. Please submit a smaller ' +
                                'application (maximum file size is 100 MB).',
                            showConfirmButton: true
                        }).then(function () {
                            window.location.reload();
                        });
                    } else if (status === 422) {
                        Swal.fire({
                            titleText: 'Invalid file',
                            icon: 'error',
                            text: 'The uploaded file is not a valid application. Please ' +
                                'submit a valid application (.apk or .zip, maximum file ' +
                                'size is 100 MB).',
                            showConfirmButton: true
                        }).then(function () {
                            window.location.reload();
                        });
                    } else {
                        Swal.fire({
                            titleText: 'Submission error',
                            icon: 'error',
                            text: err,
                            showConfirmButton: true
                        }).then(function () {
                            window.location.reload();
                        });
                    }
                },
                success: function (file, response) {
                    const status = file.xhr && file.xhr.status || '';

                    if (status.toString().startsWith('2')) {

                        let form = document.createElement('form');
                        form.setAttribute('method', 'POST');
                        form.setAttribute('action', '/details');

                        for (let key in response) {
                            if (response.hasOwnProperty(key)) {
                                let hiddenField = document.createElement('input');
                                hiddenField.setAttribute('type', 'hidden');
                                hiddenField.setAttribute('name', key);
                                if (key === 'permissions') {
                                    hiddenField.setAttribute('value', JSON.stringify(response[key]));
                                } else {
                                    hiddenField.setAttribute('value', response[key]);
                                }

                                form.appendChild(hiddenField);
                            }
                        }

                        document.body.appendChild(form);
                        form.submit();
                    }
                }
            });

            appUploadForm.on('submit', function (e) {
                e.preventDefault();
                dropzoneElement.addClass('hover dark-background').css('cursor', 'not-allowed');
                $('.dz-hidden-input').prop('disabled', true);
                submitButton.slideUp(500);
                uploadDropzone.removeEventListeners();
                dropzoneDisabled = true;
                uploadDropzone.processQueue();
            });
        });
    });
})(jQuery);

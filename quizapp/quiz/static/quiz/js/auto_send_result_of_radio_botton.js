function submitForm() {
    var form = document.getElementById('region_radio_button');
    var formData = new FormData(form);
    var csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    var xhr = new XMLHttpRequest();
    xhr.open('POST', form.action);
    xhr.setRequestHeader('X-CSRFToken', csrfToken);
    xhr.send(formData);
}
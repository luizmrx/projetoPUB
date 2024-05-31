// Add event listener to "Enviar" button
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("uploadButton").addEventListener("click", uploadFile);
    hideFeedback()
});


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("goToPageButton").addEventListener("click", function() {
        // Redirect to another page
        window.location.href = "home.html";
    });
});

hideLoading()
hideFeedback()


// Function to show success message
function showSuccessMessage() {
    document.querySelector('.feedback').style.display = 'block';
    document.getElementById('successMessage').style.display = 'block';
    document.getElementById('errorMessage').style.display = 'none';
    document.getElementById('goToPageButton').style.display = 'block';
}

function hideFeedback() {
    document.querySelector('.feedback').style.display = 'none';
}


// Function to show error message
function showErrorMessage(errorMessage) {
    document.querySelector('.feedback').style.display = 'block';
    document.getElementById('successMessage').style.display = 'none';
    document.getElementById('errorMessage').style.display = 'block';
    document.getElementById('errorMessage').textContent = errorMessage;
    document.getElementById('goToPageButton').style.display = 'none';
}


// Function to show loading indicator
function showLoading() {
    document.querySelector('.loading').style.display = 'block';
}

// Function to hide loading indicator
function hideLoading() {
    document.querySelector('.loading').style.display = 'none';
}



function uploadFile() {

    showLoading()

    var input = document.getElementById('fileInput');
    var file = input.files[0];

    var yearSelect = document.getElementById("year");
    var selectedYear = yearSelect.options[yearSelect.selectedIndex].value;

    // Get selected semester
    var semesterSelect = document.getElementById("semester");
    var selectedSemester = semesterSelect.options[semesterSelect.selectedIndex].value;


    if (file) {
        var formData = new FormData();
        formData.append('file', file);
        formData.append('year', selectedYear);
        formData.append('semester', selectedSemester);
        formData.append('path', file.name);
        url = "upload_planilha"
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
                "X-CSRFToken": getCookie("csrftoken"), 
            },

        })
        .then(response => response.json())
        .then(data => {
            console.log('Upload bem-sucedido:', data);

            hideLoading()

            showSuccessMessage();
            
        })
        .catch(error => {
            console.error('Erro no upload:', error);
            // Adicione aqui qualquer lógica para lidar com erros durante o upload
            hideLoading()

            showErrorMessage("Erro durante o upload")
        });
    } else {
        console.error('Nenhum arquivo selecionado.');

        hideLoading();

        showErrorMessage("Erro durante o upload.");
    }
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



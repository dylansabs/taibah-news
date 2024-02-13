document.addEventListener('DOMContentLoaded', function() {
    const profilePictureInput = document.getElementById('profile-picture');
    const profileWrapper = document.querySelector('.profile-wrapper');

    profilePictureInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                profileWrapper.style.backgroundImage = `url(${e.target.result})`;
            }
            reader.readAsDataURL(file);
        }
    });

    const uploadForm = document.getElementById('upload-form');
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        fetch('/upload-profile-picture', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Profile picture uploaded successfully!');
                // Optionally, update the avatar URL in the frontend
            } else {
                alert('Failed to upload profile picture.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading the profile picture.');
        });
    });
});



//the buttons clicking
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.url-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            fetch('/process-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    //alert('URL sent to Flask function successfully!');
                    
                    // Toggle button color and text
                    if (this.textContent === 'Add') {
                        this.textContent = 'Added';
                        this.style.backgroundColor = 'lightgreen';
                    } else {
                        this.textContent = 'Add';
                        this.style.backgroundColor = '#007bff'; // Reset to default color
                    }
                } else {
                    alert('Failed to send URL to Flask function.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while sending URL to Flask function.');
            });
        });
    });
});
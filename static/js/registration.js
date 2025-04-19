document.getElementById('registrationForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const form = new FormData(this);
    const messageElement = document.getElementById('message');
    
    fetch('/registration', {
      method: 'POST',
      body: form,
    })
    .then(response => response.json())
    .then(data => {
      messageElement.textContent = data.Message;
      messageElement.style.color = data.Status === 'Sucess' ? 'green' : 'red';
    })
    .catch(error => {
      messageElement.textContent = "Error: " + error.message;
      messageElement.style.color = 'red';
    });
  });
  
  



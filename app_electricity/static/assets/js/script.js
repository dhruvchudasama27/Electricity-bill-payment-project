// billing information start
document.getElementById('edit-billing-btn').addEventListener('click', function() {
    document.getElementById('edit-billing-modal').style.display = 'block';
});

document.querySelector('.billing-close-btn').addEventListener('click', function() {
    document.getElementById('edit-billing-modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('edit-billing-modal')) {
        document.getElementById('edit-billing-modal').style.display = 'none';
    }
});
// billing information end

// profile start
document.getElementById('edit-profile-btn').addEventListener('click', function() {
    document.getElementById('edit-profile-modal').style.display = 'block';
});

document.querySelector('.profile-close-btn').addEventListener('click', function() {
    document.getElementById('edit-profile-modal').style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('edit-profile-modal')) {
        document.getElementById('edit-profile-modal').style.display = 'none';
    }
});
// profile end


// payment start
function showPaymentMethod() {
    const paymentMethod = document.getElementById("paymentMethod").value;

    // Hide all payment sections
    document.getElementById("qrSection").style.display = "none";
    document.getElementById("upiSection").style.display = "none";
    document.getElementById("cardSection").style.display = "none";

    // Show the selected payment section
    if (paymentMethod === "qr") {
        document.getElementById("qrSection").style.display = "block";
    } else if (paymentMethod === "upi") {
        document.getElementById("upiSection").style.display = "block";
    } else if (paymentMethod === "card") {
        document.getElementById("cardSection").style.display = "block";
    }
}

// payment end

// selfie start
function openCamera() {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        // Create a container div to hold the video and capture button
        const selfieContainer = document.createElement('div');
        selfieContainer.className = 'selfie-container';
  
        // Create a video element and display the camera stream
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        video.className = 'selfie-video'; // Optional: Add class for styling
        
        // Create a canvas element to capture the image
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        
        // Set up the canvas dimensions to match the video
        video.addEventListener('loadedmetadata', function() {
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;
        });
        
        // Create a button to capture the selfie
        const captureButton = document.createElement('button');
        captureButton.textContent = 'Capture Selfie';
        captureButton.className = 'btn btn-primary mt-2';
        
        // Append the video and capture button to the selfie container
        selfieContainer.appendChild(video);
        selfieContainer.appendChild(captureButton);
        
        // Insert the selfie container right after the "Take Selfie" button
        const selfieSection = document.querySelector('.selfie-section');
        selfieSection.appendChild(selfieContainer);
        
        // Handle capture button click
        captureButton.addEventListener('click', function() {
          // Ensure the video is playing before capturing
          if (video.readyState === video.HAVE_ENOUGH_DATA) {
            // Draw the video frame onto the canvas
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            
            // Get the data URL of the image
            const dataURL = canvas.toDataURL('image/png');
            
            // Remove the video and button from the selfie container
            selfieContainer.removeChild(video);
            selfieContainer.removeChild(captureButton);
            
            // Create an image element to display the captured selfie
            const img = document.createElement('img');
            img.src = dataURL;
            img.alt = 'Captured Selfie';
            img.className = 'img-thumbnail'; // Bootstrap class to style the image
            
            // Append the captured selfie image to the selfie container
            selfieContainer.appendChild(img);
            
            // Stop the video stream
            stream.getTracks().forEach(track => track.stop());
            
            // Set the image data as the value for the file input field
            const fileInput = document.getElementById('profile-photo');
            const file = dataURLtoFile(dataURL, 'selfie.png');
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            fileInput.files = dataTransfer.files;
            
            // Alert the user that the selfie was clicked
            alert('Selfie clicked successfully!');
          } else {
            // Alert the user if the selfie was not clicked
            alert('Selfie not clicked.');
            console.error('Video is not ready to capture.');
          }
        });
      })
      .catch(function(err) {
        console.error('Error accessing camera:', err);
        alert('Error accessing camera.');
      });
  }
  
  // Utility function to convert data URL to File object
  function dataURLtoFile(dataurl, filename) {
    const arr = dataurl.split(',');
    const mime = arr[0].match(/:(.*?);/)[1];
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);
    
    while (n--) {
      u8arr[n] = bstr.charCodeAt(n);
    }
    
    return new File([u8arr], filename, { type: mime });
  }
  
// selfie end
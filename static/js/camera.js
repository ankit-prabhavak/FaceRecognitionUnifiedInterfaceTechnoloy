// Function to start the webcam and display the video feed in the <video> element
function startCamera() {
    const video = document.getElementById('video'); // Get the video element
    const canvas = document.getElementById('canvas'); // Get the canvas element
    const context = canvas.getContext('2d'); // Get the 2d context to draw images on canvas

    // Get access to the user's webcam
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream) {
            video.srcObject = stream;  // Set the webcam feed as the video source
        })
        .catch(function (error) {
            alert("Could not access webcam: " + error);
        });
}

// Function to capture the image from the webcam and display it on the canvas
function captureImage() {
    const video = document.getElementById('video'); // Get the video element
    const canvas = document.getElementById('canvas'); // Get the canvas element
    const context = canvas.getContext('2d'); // Get the 2d context of the canvas

    // Draw the current video frame onto the canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the image from canvas to a base64 string
    const dataURL = canvas.toDataURL('image/png');

    // Set the base64 string to the hidden input field in the form
    document.getElementById('image_data').value = dataURL;

    // Optionally, stop the video stream after capturing the image to release resources
    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(function (track) {
        track.stop();  // Stop the video track
    });
    
}


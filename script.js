// Function to open the image in full screen
function openFullscreen(imgElement) {
  var modal = document.getElementById("fullscreenModal");
  var modalImg = document.getElementById("modalImage");

  // Set the clicked image as the modal image source
  modalImg.src = imgElement.src;

  // Show the modal
  modal.style.display = "block";
}

// Function to close the full-screen modal (by clicking anywhere or pressing ESC)
function closeFullscreen(event) {
  var modal = document.getElementById("fullscreenModal");

  // Close the modal if clicked anywhere inside the modal or pressing ESC
  if (event.target == modal || event.key == "Escape") {
    modal.style.display = "none";

    // Optionally, clear the modal image source to avoid flickering
    var modalImg = document.getElementById("modalImage");
    modalImg.src = '';  // Reset the source of the image
  }
}

// Event listener for clicking anywhere in the modal to close it (including the image)
document.getElementById("fullscreenModal").addEventListener("click", closeFullscreen);

// Event listener for pressing the Escape key to close the modal
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeFullscreen(event);
  }
});

// Event listener for clicking anywhere on the screen to close the modal
// document.addEventListener("click", function (event) {
//   var modal = document.getElementById("fullscreenModal");
//   if (modal.style.display === "block")
//     closeFullscreen(event);
// });
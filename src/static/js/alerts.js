/**
 * Displays a Bootstrap alert message.
 * @param {string} body - The message to display.
 */
export const showAlert = (body) => {
  // Create the alert element
  const alertDiv = document.createElement('div');
  alertDiv.className = 'alert alert-success alert-dismissible fade show';
  alertDiv.setAttribute('role', 'alert');
  alertDiv.innerHTML = `${body}<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>`;

  // Add the alert to the container
  const container = document.getElementById('alertContainer');
  if (container) {
    container.appendChild(alertDiv);
  }

  // Auto-hide after 3 seconds
  setTimeout(() => {
    // Use Bootstrap's fade out animation
    alertDiv.classList.remove('show');

    // Remove from DOM after animation completes
    setTimeout(() => {
      if (alertDiv.parentNode) {
        alertDiv.parentNode.removeChild(alertDiv);
      }
    }, 150); // Bootstrap fade transition is 150ms
  }, 3000);
};

// Add event listener to button if it exists
const showAlertBtn = document.getElementById('showAlert');
if (showAlertBtn) {
  showAlertBtn.addEventListener('click', () => showAlert('Default alert message'));
}

/**
 * Copies the content of the task table to the clipboard.
 */
const copyTableContent = async () => {
  const table = document.getElementById('taskList');
  if (!table) return;

  // Get table content as text
  let tableText = '';

  // Process body rows
  const bodyRows = table.querySelectorAll('tbody tr');
  bodyRows.forEach((row) => {
    const cells = row.querySelectorAll('td');
    const rowData = Array.from(cells).map((cell) => cell.textContent.trim());
    tableText += `${rowData.join('\t')}\n`;
  });

  try {
    await navigator.clipboard.writeText(tableText);
    if (typeof showAlert === 'function') {
      showAlert('Table saved in the clipboard');
    } else {
      console.log('Table saved in the clipboard');
    }
  } catch (err) {
    console.error('Could not copy text: ', err);
  }
};

// Make it globally accessible if needed by the onclick attribute in HTML
window.copyTableContent = copyTableContent;

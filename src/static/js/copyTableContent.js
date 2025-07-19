function copyTableContent() {
    const table = document.getElementById('taskList');
    const successMessage = document.getElementById('successMessage');

    // Get table content as text
    let tableText = '';

    // Process body rows
    const bodyRows = table.querySelectorAll('tbody tr');
    bodyRows.forEach(row => {
        const cells = row.querySelectorAll('td');
        const rowData = Array.from(cells).map(cell => cell.textContent.trim());
        tableText += rowData.join('\t') + '\n';
    });


    const textArea = document.createElement("textarea");
    textArea.value = tableText;

    // Avoid scrolling to bottom
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";

    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showAlert("Table saved in the clipboard");
        } else {
            console.error('Fallback: Could not copy text');
        }
    } catch (err) {
        console.error('Could not copy text: ', err);
    }

    document.body.removeChild(textArea);
}
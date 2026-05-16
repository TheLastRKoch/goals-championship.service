/**
 * Manages the project selector dropdown and selected items.
 */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('projectSearch');
  const dropdown = document.getElementById('projectDropdown');
  const selectedContainer = document.getElementById('selectedProjectsContainer');
  const hiddenInput = document.getElementById('selectedProjectsInput');

  if (!searchInput || !dropdown || !selectedContainer || !hiddenInput) return;

  let selectedProjects = [];

  /**
   * Shows the dropdown menu.
   */
  const showDropdown = () => dropdown.classList.add('show');

  /**
   * Hides the dropdown menu.
   */
  const hideDropdown = () => dropdown.classList.remove('show');

  /**
   * Filters projects in the dropdown based on search term.
   * @param {string} searchTerm - The term to filter by.
   */
  const filterProjects = (searchTerm) => {
    const items = dropdown.querySelectorAll('.dropdown-item');
    let hasVisibleItems = false;

    items.forEach((item) => {
      const projectValue = item.getAttribute('data-project');
      const projectText = item.textContent.toLowerCase();
      const isAlreadySelected = selectedProjects.some((p) => p.value === projectValue);

      if (projectText.includes(searchTerm) && !isAlreadySelected) {
        item.style.display = 'block';
        hasVisibleItems = true;
      } else {
        item.style.display = 'none';
      }
    });

    // Show/hide "no results" message
    let noResultsItem = dropdown.querySelector('.no-results');
    if (!hasVisibleItems && searchTerm) {
      if (!noResultsItem) {
        noResultsItem = document.createElement('li');
        noResultsItem.className = 'no-results';
        noResultsItem.textContent = 'No projects found';
        dropdown.appendChild(noResultsItem);
      }
      noResultsItem.style.display = 'block';
    } else if (noResultsItem) {
      noResultsItem.style.display = 'none';
    }
  };

  /**
   * Updates the display of selected projects.
   */
  const updateSelectedProjectsDisplay = () => {
    if (selectedProjects.length === 0) {
      selectedContainer.innerHTML = '<div class="text-muted">No projects selected. Search and select projects below.</div>';
      return;
    }

    selectedContainer.innerHTML = selectedProjects
      .map(
        (project) => `
      <span class="badge bg-primary rounded-pill project-pill">
        ${project.text}
        <button type="button" class="btn-close btn-close-white ms-2" 
                onclick="window.removeProjectPill('${project.value}')" 
                aria-label="Remove ${project.text}"></button>
      </span>
    `
      )
      .join('');
  };

  /**
   * Updates the hidden input with selected project IDs.
   */
  const updateHiddenInput = () => {
    hiddenInput.value = selectedProjects.map((p) => p.value).join(',');
  };

  /**
   * Adds a project to the selected list.
   * @param {string} value - Project ID.
   * @param {string} text - Project name.
   */
  const addProject = (value, text) => {
    if (selectedProjects.some((p) => p.value === value)) return;
    selectedProjects.push({ value, text });
    updateSelectedProjectsDisplay();
    updateHiddenInput();
  };

  /**
   * Removes a project from the selected list.
   * @param {string} value - Project ID.
   */
  const removeProject = (value) => {
    selectedProjects = selectedProjects.filter((p) => p.value !== value);
    updateSelectedProjectsDisplay();
    updateHiddenInput();
    filterProjects(searchInput.value.toLowerCase());
  };

  // Event Listeners
  searchInput.addEventListener('focus', showDropdown);

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.search-dropdown')) {
      hideDropdown();
    }
  });

  searchInput.addEventListener('input', (e) => {
    const searchTerm = e.target.value.toLowerCase();
    filterProjects(searchTerm);
    showDropdown();
  });

  dropdown.addEventListener('click', (e) => {
    const item = e.target.closest('.dropdown-item');
    if (item) {
      e.preventDefault();
      const projectValue = item.getAttribute('data-project');
      const projectText = item.textContent.trim();

      addProject(projectValue, projectText);
      searchInput.value = '';
      filterProjects('');
      hideDropdown();
    }
  });

  // Global access for remove button
  window.removeProjectPill = (value) => removeProject(value);

  // Initial call
  filterProjects('');
});

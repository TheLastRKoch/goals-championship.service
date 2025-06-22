document.addEventListener('DOMContentLoaded', function() {
            const searchInput = document.getElementById('projectSearch');
            const dropdown = document.getElementById('projectDropdown');
            const selectedContainer = document.getElementById('selectedProjectsContainer');
            const placeholderText = document.getElementById('placeholderText');
            const hiddenInput = document.getElementById('selectedProjectsInput');
            
            let selectedProjects = [];
            const allProjects = [];
            
            // Populate all projects array from dropdown items
            dropdown.querySelectorAll('.dropdown-item').forEach(item => {
                allProjects.push({
                    value: item.getAttribute('data-project'),
                    text: item.textContent.trim()
                });
            });
            
            // Show/hide dropdown on input focus/blur
            searchInput.addEventListener('focus', function() {
                showDropdown();
            });
            
            // Hide dropdown when clicking outside
            document.addEventListener('click', function(e) {
                if (!e.target.closest('.search-dropdown')) {
                    hideDropdown();
                }
            });
            
            // Search functionality
            searchInput.addEventListener('input', function() {
                const searchTerm = this.value.toLowerCase();
                filterProjects(searchTerm);
                showDropdown();
            });
            
            // Handle project selection
            dropdown.addEventListener('click', function(e) {
                if (e.target.classList.contains('dropdown-item')) {
                    e.preventDefault();
                    const projectValue = e.target.getAttribute('data-project');
                    const projectText = e.target.textContent.trim();
                    
                    addProject(projectValue, projectText);
                    searchInput.value = '';
                    filterProjects('');
                    hideDropdown();
                }
            });
            
            function showDropdown() {
                dropdown.classList.add('show');
            }
            
            function hideDropdown() {
                dropdown.classList.remove('show');
            }
            
            function filterProjects(searchTerm) {
                const items = dropdown.querySelectorAll('.dropdown-item');
                let hasVisibleItems = false;
                
                items.forEach(item => {
                    const projectValue = item.getAttribute('data-project');
                    const projectText = item.textContent.toLowerCase();
                    const isAlreadySelected = selectedProjects.some(p => p.value === projectValue);
                    
                    if (projectText.includes(searchTerm) && !isAlreadySelected) {
                        item.style.display = 'block';
                        hasVisibleItems = true;
                    } else {
                        item.style.display = 'none';
                    }
                });
                
                // Show "no results" message if needed
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
            }
            
            function addProject(value, text) {
                // Check if project is already selected
                if (selectedProjects.some(p => p.value === value)) {
                    return;
                }
                
                selectedProjects.push({ value, text });
                updateSelectedProjectsDisplay();
                updateHiddenInput();
            }
            
            function removeProject(value) {
                selectedProjects = selectedProjects.filter(p => p.value !== value);
                updateSelectedProjectsDisplay();
                updateHiddenInput();
                filterProjects(searchInput.value.toLowerCase());
            }
            
            function updateSelectedProjectsDisplay() {
                if (selectedProjects.length === 0) {
                    selectedContainer.innerHTML = '<div class="text-muted" id="placeholderText">No projects selected. Search and select projects below.</div>';
                    return;
                }
                
                const pillsHtml = selectedProjects.map(project => `
                    <span class="badge bg-primary rounded-pill project-pill">
                        ${project.text}
                        <button type="button" class="btn-close btn-close-white ms-2" 
                                onclick="removeProjectPill('${project.value}')" 
                                aria-label="Remove ${project.text}"></button>
                    </span>
                `).join('');
                
                selectedContainer.innerHTML = pillsHtml;
            }
            
            function updateHiddenInput() {
                hiddenInput.value = selectedProjects.map(p => p.value).join(',');
            }
            
            // Make removeProjectPill globally accessible
            window.removeProjectPill = function(value) {
                removeProject(value);
            };
            
            // Initialize
            filterProjects('');
        });
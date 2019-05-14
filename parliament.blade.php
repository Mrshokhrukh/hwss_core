<style>
    .card-image {
        width: 150px;
        height: 150px;
        object-fit: cover;
        object-position: top center;
    }

    .page-link {
        display: inline-block;
        padding: 5px 10px;
        margin-right: 5px;
        background-color: #007bff;
        color: #fff;
        border-radius: 3px;
        text-decoration: none;
    }

    .page-link:hover,
    .page-link.active {
        background-color: #0056b3;
    }
</style>

<div class="container mt-4">
    <div class="container mt-3 mb-3" style="display: none;">
        <div class="row">
            <!-- Search Input -->
            <div class="col-md-4 mb-2">
                <label for="search-input">Search:</label>
                <input type="text" class="form-control" id="search-input" placeholder="Enter search term">
            </div>

            <!-- Parliament Selection Dropdown -->
            <div class="col-md-3 mb-2" style="display:none ;">
                <label for="parliament-dropdown">Parliament:</label>
                <select class="form-control" id="parliament-dropdown">
                    <option value="">All Parliament</option>
                    <option value="First Parliament">First Parliament</option>
                    <option value="Second Parliament">Second Parliament</option>
                    <option value="Third Parliament" selected="">Third Parliament</option>
                    <option value="Fourth Parliament">Fourth Parliament</option>
                    <option value="Fifth Parliament">Fifth Parliament</option>
                </select>
            </div>

            <!-- Constituency Selection Dropdown -->
            <div class="col-md-4 mb-2">
                <label for="constituency-dropdown">Constituency:</label>
                <select class="form-control" id="constituency-dropdown">
                    <option value="">All</option>
                    <!-- Add constituencies dynamically from JavaScript array -->
                </select>
            </div>

            <!-- Buttons -->
            <div class="col-md-4 mb-2">
                <label class="d-block">Actions:</label>
                <div class="btn-group" role="group" aria-label="Actions">
                    <button class="btn btn-primary" id="search-button" data-bs-toggle="tooltip" data-placement="top"
                        title="Search">
                        <i class="fas fa-search"></i> Search
                    </button>
                    <button class="btn btn-secondary" id="reset-button" data-bs-toggle="tooltip" data-placement="top"
                        title="Reset">
                        <i class="fas fa-undo"></i>
                    </button>
                    <button class="btn btn-success" id="refresh-button" data-bs-toggle="tooltip" data-placement="top"
                        title="Refresh">
                        <i class="fas fa-sync"></i>
                    </button>
                </div>
            </div>
        </div>
    </div>
    <!-- Cards Container -->
    <div id="cards-container" class="row">
        <!-- Loading Spinner -->
        <div id="loading-spinner" class="text-center mt-4">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p>Loading...</p>
        </div>
        <!-- Cards will be dynamically added here -->
    </div>

    <!-- Pagination -->
    <nav id="pagination" class="mt-4 text-center">
        <ul class="pagination"></ul>
    </nav>


    <!-- Bootstrap Modal -->
    <div class="modal fade" id="membersModal" tabindex="-1" role="dialog" aria-labelledby="membersModalLabel"
        aria-hidden="true">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title text-capitalize" id="modal-title"></h5>
                    <button type="button " class="btn-close" data-bs-dismiss="modal" aria-label="Close">
                    </button>
                </div>
                <div class="modal-body">
                    <img id="modal-image" class="img-fluid rounded mx-auto d-block" alt="">
                    <div id="modal-body" class="mt-3"></div>
                </div>
                <div class="modal-footer">
                    <button type="button btn btn-danger" class="btn btn-secondary"
                        data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

</div>

<script>
    document.addEventListener("DOMContentLoaded", function() {
        fetchDataFromServer();

        document.getElementById('search-button').addEventListener('click', fetchDataFromServer);
        document.getElementById('reset-button').addEventListener('click', resetFilters);
    });

    let members = []; // Define members as a global variable

    function fetchDataFromServer() {
        fetch("/get-current-members")
            .then(response => response.json())
            .then(data => {
                console.log("Received Data:", data);
                members = data; // Update the global members variable
                renderCards();
                renderPagination(data.length);
                attachPaginationEventListeners(); // Update the pagination event listeners
            })
            .catch(error => {
                console.error("Error fetching data:", error);
            });
    }

    const cardsPerPage = 10;
    let currentPage = 1;

    function renderCards() {
        const startIndex = (currentPage - 1) * cardsPerPage;
        const endIndex = startIndex + cardsPerPage;
        const paginatedMembers = members.slice(startIndex, endIndex);

        const cardsContainer = document.getElementById('cards-container');
        cardsContainer.innerHTML = '';

        paginatedMembers.forEach(member => {
            const card = createCard(member);
            cardsContainer.appendChild(card);
            card.querySelector('.btn-primary').addEventListener('click', () => showDetailsModal(member));
        });
    }

    function attachPaginationEventListeners() {
        document.querySelectorAll('.page-link').forEach((link) => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const pageNumber = parseInt(event.target.textContent);
                currentPage = pageNumber;
                renderCards();
                renderPagination(members.length);
            });
        });
    }

    function attachPaginationEventListeners(members) {
        document.querySelectorAll('.page-link').forEach((link) => {
            link.addEventListener('click', (event) => {
                event.preventDefault();
                const pageNumber = parseInt(event.target.textContent);
                currentPage = pageNumber;
                renderCards(members);
            });
        });
    }

    function renderPagination(totalMembers) {
        const totalPages = Math.ceil(totalMembers / cardsPerPage);
        const paginationContainer = document.getElementById('pagination');
        const paginationList = paginationContainer.querySelector('.pagination');
        paginationList.innerHTML = '';

        const prevButton = createPaginationButton('Previous', currentPage > 1 ? currentPage - 1 : null);
        paginationList.appendChild(prevButton);

        for (let i = 1; i <= totalPages; i++) {
            const pageLink = createPaginationButton(i, i === currentPage ? null : i);
            if (i === currentPage) { // Add active class to the current page link
                pageLink.classList.add('active');
            }
            paginationList.appendChild(pageLink);
        }

        const nextButton = createPaginationButton('Next', currentPage < totalPages ? currentPage + 1 : null);
        paginationList.appendChild(nextButton);
    }

    function createPaginationButton(label, pageNumber) {
        const li = document.createElement('li');
        li.classList.add('page-item');

        const a = document.createElement('a');
        a.classList.add('page-link');
        a.href = 'javascript:void(0)';

        // Set the label as empty string if it's "Next" or "Previous"
        if (label === 'Next' || label === 'Previous') {
            a.textContent = label;
        } else {
            a.textContent = label;
        }

        // Disable the previous button if it's page 1
        if (!pageNumber) {
            li.classList.add('disabled');
        }

        if (pageNumber) {
            a.addEventListener('click', () => {
                currentPage = pageNumber;
                renderCards(members);
                renderPagination(members.length);
            });
        }

        li.appendChild(a);
        return li;
    }


    function createCard(member) {
        const card = document.createElement('div');
        let partyAffiliation = member.details['Party Affiliation'] || 'N/A';
        let constituency = member.constituency || 'N/A'; // Getting the constituency
        card.classList.add('col-md-3', 'mb-3');
        card.innerHTML = `
        <div class="card">
            <div class="card-header text-center">
                ${mapDesignation(member.designation)}
            </div>
            <div class="card-body text-center">
                <img src="${member.photo_file}" alt="${member.title}" class="img-fluid rounded-circle card-image">
                <p class="mt-2">${member.title}</p>
                <p><strong>Constituency:</strong> ${constituency}</p> <!-- Displaying the constituency -->
                <p>${partyAffiliation}</p>
            </div>
            <div class="card-footer text-center">
                <button class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#membersModal">Read More</button>
            </div>
        </div>`;
        return card;
    }

    function mapDesignation(designationValue) {
        const designationMap = {
            '1': 'Speaker',
            '2': 'Prime Minister',
            '3': 'Cabinet Minister',
            '4': 'Ruling Member',
            '5': 'Opposition Leader',
            '6': 'Opposition Member',
            '7': 'Dy. Speaker'
        };
        return designationMap[designationValue] || 'Unknown Designation';
    }

    function showDetailsModal(member) {
        const modalTitle = document.getElementById('modal-title');
        const modalImage = document.getElementById('modal-image');
        const modalBody = document.getElementById('modal-body');

        modalTitle.textContent = member.title;
        modalImage.src = member.photo_file;
        modalImage.alt = member.title;

        modalBody.innerHTML = '';

        const detailsContainer = document.createElement('div');
        detailsContainer.style.border = '1px solid #999';
        detailsContainer.style.borderRadius = '5px';
        detailsContainer.style.padding = '1rem';

        populateModalDetails(member, detailsContainer);

        modalBody.appendChild(detailsContainer);

        $('#membersModal').modal('show');
    }

    function getConstituency(member) {
        const constituency = member.Joined_categories.find(category => {
            return !category.title.includes('Parliament') &&
                !category.title.includes('Minister') &&
                !category.title.includes('Speaker') &&
                !category.title.includes('Opposition');
        });

        return constituency ? constituency.title : 'N/A';
    }

    function populateModalDetails(member, container) {
        const fieldsOrder = [{
                key: 'Designation',
                title: 'Designation',
                isMapped: true
            },
            {
                key: 'constituency',
                title: 'Constituency'
            },
            {
                key: 'Date of Birth',
                title: 'Date of Birth'
            },
            {
                key: 'Email',
                title: 'Email'
            },
            {
                key: 'Qualification',
                title: 'Qualification'
            },
            {
                key: 'Committees',
                title: 'Parliamentary Services'
            },
            {
                key: 'Ministry',
                title: 'Ministrial Appt',
                isMapped: true
            },
            {
                key: 'Party Affiliation',
                title: 'Party'
            },
            {
                key: 'term',
                title: 'Term'
            }
        ];

        fieldsOrder.forEach(fieldInfo => {
            let field;
            if (fieldInfo.key in member.details) {
                field = member.details[fieldInfo.key];
            } else {
                field = member[fieldInfo.key] || 'N/A';
            }
            const detailItem = createDetailItem(fieldInfo.title, field, fieldInfo.isMapped);
            container.appendChild(detailItem);
        });
    }

    function createDetailItem(title, value, isMapped) {
        const detailItem = document.createElement('div');
        detailItem.style.display = 'grid';
        detailItem.style.gridTemplateColumns = '1fr 3fr';
        detailItem.style.gap = '8px';
        detailItem.style.marginBottom = '4px';

        const detailTitle = document.createElement('span');
        detailTitle.style.fontWeight = 'bold';
        detailTitle.textContent = `${title}:`;

        const detailValue = document.createElement('span');
        detailValue.style.whiteSpace = 'pre-line';

        if (title === 'Email' && value !== 'N/A') {
            const emailLink = document.createElement('a');
            emailLink.href = `mailto:${value}`;
            emailLink.textContent = value;
            const mailIcon = document.createElement('i');
            mailIcon.className = 'fas fa-envelope';
            emailLink.appendChild(mailIcon);
            detailValue.appendChild(emailLink);
        } else {
            detailValue.textContent = isMapped ? mapValue(value, title) : value;
        }

        detailItem.appendChild(detailTitle);
        detailItem.appendChild(detailValue);
        return detailItem;
    }


    function mapValue(value, type) {
        const maps = {
            'Designation': {
                '1': 'Speaker',
                '2': 'Prime Minister',
                '3': 'Cabinet Minister',
                '4': 'Ruling Member',
                '5': 'Opposition Leader',
                '6': 'Opposition Member',
                '7': 'Dy. Speaker'
            },
            'Ministrial Appt': {
                '1': 'Ministry of Finance',
                '2': 'Ministry of Health',
                '3': 'Ministry of Home Affairs',
                '4': 'Ministry of Agriculture and Livestock',
                '5': 'Ministry of Education & Skills Development',
                '6': 'Ministry of Energy & Natural Resources',
                '7': 'Ministry of Foreign Affairs & External Trade',
                '8': 'Ministry of Industry, Commerce & Employment',
                '9': 'Ministry of Infrastructure & Transport'
            }
        };

        return maps[type] && maps[type][value] ? maps[type][value] : 'N/A';
    }


    function appendParliamentTerm(member, container) {
        const termMap = {
            'First Parliament': '2008 - 2013',
            'Second Parliament': '2013 - 2018',
            'Third Parliament': '2018 - 2023',
            'Fourth Parliament': '2023 - 2028'
        };

        const term = termMap[member.term] || 'N/A';

        if (term !== 'N/A') {
            const termItem = document.createElement('div');
            termItem.style.display = 'grid';
            termItem.style.gridTemplateColumns = '1fr 3fr';
            termItem.style.gap = '8px';
            termItem.style.marginBottom = '4px';

            const termTitle = document.createElement('span');
            termTitle.style.fontWeight = 'bold';
            termTitle.textContent = 'Term:';

            const termValue = document.createElement('span');
            termValue.textContent = term;

            termItem.appendChild(termTitle);
            termItem.appendChild(termValue);
            container.appendChild(termItem);
        }
    }
</script>

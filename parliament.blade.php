<style>
    .search-bar {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }

    .form-control,
    .form-select {
        flex: 1;
        margin-right: 5px;
    }

    .btn {
        height: 100%;
        align-self: flex-start;
    }

    .search-bar input[type="text"] {
        margin-right: 10px;
    }

    .search-bar button {
        margin-left: 10px;
    }

    .card-icon {
        flex: 0 0 auto;
        margin-right: 10px;
        font-size: 3rem;
        color: #007bff;
    }

    .card-content {
        flex: 1 1 auto;
    }

    .search-bar {
        margin-bottom: 4rem;
    }

    #search-input {
        margin-bottom: 0;
    }

    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
</style>

<div x-data="searchApp()" x-init="init()">
    <div class="container">
        <div class="search-bar mt-4 mb-4">
            <div class="input-group">
                <input type="text" id="search-input" placeholder="Search" class="form-control" x-model="searchTerm">
                <select id="parliament-filter" class="form-select" x-model="selectedParliament">
                    <option value="">All Parliaments</option>
                </select>
                <select id="session-filter" class="form-select" x-model="selectedSession">
                    <option value="">All Sessions</option>
                </select>
                <button id="search-button" class="btn btn-primary" @click="search">Search</button>
                <button id="reset-button" style="display: none;" class="btn btn-secondary" @click="reset">Reset</button>
            </div>
        </div>

        <!-- Loading animation container -->
        <div id="cards-container" class="row" x-show="!topics.length &amp;&amp; !filteredTopics.length">
            <div class="loading-container">
                Loading...
            </div>
        </div>

        <div id="cards-container" class="row">
            <template x-for="topic in filteredTopics" :key="topic.id">
                <div class="col-md-6">
                    <div class="card mb-4">
                        <div class="row">
                            <div class="col-md-3 d-flex align-items-center justify-content-center">
                                <i class="far fa-file-pdf fa-3x text-primary card-icon"></i>
                            </div>
                            <div class="col-md-9">
                                <div class="card-body card-content overflow-hidden">
                                    <h5 class="card-title text-capitalize" x-text="sanitizeAndTruncate(topic.title, 50)"></h5>
                                    <div class="card-text text-lowercase" x-text="sanitizeAndTruncate(topic.details, 100)"></div>
                                    <div class="card-text">
                                        <template x-for="category in topic.Joined_categories" :key="category.id">
                                            <span class="badge text-secondary mr-1"><i class="fas fa-tag"></i> <span x-text="category.title" class="text-turncate"></span></span>
                                        </template>
                                    </div>
                                    <a class="btn btn-primary my-2" :href="topic.downloadLink" target="_blank">Download</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</div>

<!-- Include the following script to define the Alpine.js component -->
<script>
    function searchApp() {
        return {
            searchTerm: '',
            selectedParliament: '',
            selectedTitle: 'Hansard Report',
            selectedSession: '',
            topics: [],
            filteredTopics: [],
            async init() {
                try {
                    const response = await fetch("https://parliament.bt/api/v1/topics/16/page/1/count");
                    if (!response.ok) {
                        throw new Error(`Failed to fetch data (${response.status} ${response.statusText})`);
                    }
                    const data = await response.json();
                    this.topics = data.topics;
                    this.populateDropdowns();
                    this.filterTopics();
                    await this.fetchDownloadLinks();
                } catch (error) {
                    console.error(error);
                }
            },
            async fetchDownloadLinks() {
                try {
                    const downloadPromises = this.filteredTopics.map(async topic => {
                        const response = await fetch(`https://parliament.bt/api/v1/${topic.href}`);
                        if (!response.ok) {
                            throw new Error(
                                `Failed to fetch topic data (${response.status} ${response.statusText})`
                            );
                        }
                        const topicData = await response.json();
                        const attachFiles = topicData.topic[0].attach_files;
                        if (attachFiles && attachFiles.length > 0) {
                            topic.downloadLink = attachFiles[0]
                                .url; // Add download link to topic object
                        }
                    });
                    await Promise.all(downloadPromises);
                } catch (error) {
                    console.error(error);
                }
            },
            populateDropdowns() {
                // Populate Parliament dropdown with options
                const parliamentDropdown = document.getElementById("parliament-filter");
                const parliamentOptions = ['First Parliament', 'Second Parliament', 'Third Parliament',
                    'Fourth Parliament'
                ];
                parliamentOptions.forEach(option => {
                    const optionElement = document.createElement("option");
                    optionElement.value = option;
                    optionElement.textContent = option;
                    parliamentDropdown.appendChild(optionElement);
                });

                // Populate Session dropdown with options
                const sessionDropdown = document.getElementById("session-filter");
                const sessionOptions = [];
                for (let i = 1; i <= 10; i++) {
                    sessionOptions.push(`Session ${i}`);
                }
                sessionOptions.forEach(option => {
                    const optionElement = document.createElement("option");
                    optionElement.value = option;
                    optionElement.textContent = option;
                    sessionDropdown.appendChild(optionElement);
                });
            },
            sanitizeAndTruncate(html, maxLength) {
                const tempElement = document.createElement("div");
                tempElement.innerHTML = html;
                const sanitizedText = tempElement.textContent || tempElement.innerText || "";
                return sanitizedText.length > maxLength ? `${sanitizedText.substring(0, maxLength)}...` : sanitizedText;
            },
            filterTopics() {
                this.filteredTopics = this.topics.filter(topic => {
                    const searchTermMatch = topic.title.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                        topic.details.toLowerCase().includes(this.searchTerm.toLowerCase());
                    const parliamentMatch = !this.selectedParliament || topic.Joined_categories.some(category =>
                        category.title === this.selectedParliament);
                    const sessionMatch = !this.selectedSession || topic.Joined_categories.some(category =>
                        category.title === this.selectedSession);
                    const agendaMatch = topic.Joined_categories.some(category => category.title === this
                        .selectedTitle);
                    return searchTermMatch && parliamentMatch && sessionMatch && agendaMatch;
                });
                if (this.filteredTopics.length === 0) {
                    this.renderFallbackMessage(`No results found.`);
                }
            },
            search() {
                this.filterTopics();
                document.getElementById("reset-button").style.display = "block";
            },
            reset() {
                this.searchTerm = '';
                this.selectedParliament = '';
                this.selectedSession = '';
                this.filterTopics();
                document.getElementById("reset-button").style.display = "none";
            },
            renderFallbackMessage(message) {
                document.getElementById("cards-container").innerHTML =
                    `<div class="text-center"><h3>:(</h3> ${message}</div>`;
            }
        };
    }
</script>
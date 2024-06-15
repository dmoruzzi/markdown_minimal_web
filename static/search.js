document.addEventListener('DOMContentLoaded', (event) => {
    let searchIndex = [];

    // Fetch search index data
    fetch('search_index.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            searchIndex = data;
            console.log("Search index data:", searchIndex);  // Debug log

            // Initialize Lunr.js
            window.idx = lunr(function () {
                this.ref('id');
                this.field('title');
                this.field('content');

                searchIndex.forEach(function (doc) {
                    this.add(doc);
                }, this);
            });
            console.log("Lunr.js index initialized");  // Debug log
        })
        .catch(error => console.error('Error loading search index:', error));


    document.getElementById('search-input').addEventListener('input', function(event) {
        const query = event.target.value.toLowerCase();
        if (query) {
            const results = window.idx.search(query);
            console.log("Search results for query:", query, results);  // Debug log
            displayResults(results);
        } else {
            document.getElementById('search-results').style.display = 'none';
        }
    });

    function displayResults(results) {
        const resultsList = document.getElementById('search-results-list');
        resultsList.innerHTML = '';
        results.forEach(result => {
            const item = searchIndex.find(i => i.id === result.ref);
            if (item) {
                const listItem = document.createElement('li');
                const link = document.createElement('a');
                link.href = item.url;
                link.textContent = item.title;
                listItem.appendChild(link);
                resultsList.appendChild(listItem);
            }
        });
        document.getElementById('search-results').style.display = 'block';
    }
});

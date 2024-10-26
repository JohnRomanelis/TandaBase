document.addEventListener('DOMContentLoaded', function() {
    const tandaSearchInput = document.getElementById('tanda-search');
    const tandaSearchResults = document.getElementById('tanda-search-results');
    const selectedTandas = document.getElementById('selected-tandas');
    const tandaIdsField = document.getElementById('tanda_ids');

    let selectedTandaIds = [];

    // Function to add a tanda to the playlist
    function addTandaToPlaylist(tanda) {
        if (selectedTandaIds.includes(tanda.id.toString())) {
            alert('Tanda already added.');
            return;
        }
        selectedTandaIds.push(tanda.id.toString());
        const item = document.createElement('li');
        item.className = 'list-group-item d-flex justify-content-between align-items-center';
        item.textContent = `${tanda.name} (${tanda.type})`;
        const removeBtn = document.createElement('button');
        removeBtn.className = 'btn btn-sm btn-danger ml-2';
        removeBtn.textContent = 'Remove';
        removeBtn.addEventListener('click', function() {
            selectedTandas.removeChild(item);
            selectedTandaIds = selectedTandaIds.filter(id => id !== tanda.id.toString());
            updateTandaIdsField();
        });
        item.appendChild(removeBtn);
        selectedTandas.appendChild(item);
        updateTandaIdsField();
    }

    // Function to update the hidden tanda IDs field
    function updateTandaIdsField() {
        tandaIdsField.value = selectedTandaIds.join(',');
    }

    // Search for tandas via AJAX
    tandaSearchInput.addEventListener('input', function() {
        const query = tandaSearchInput.value;
        if (query.length < 2) {
            tandaSearchResults.innerHTML = '';
            return;
        }
        fetch(`/playlists/search_tandas?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                tandaSearchResults.innerHTML = '';
                data.forEach(tanda => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.textContent = `${tanda.name} (${tanda.type})`;
                    item.dataset.tandaId = tanda.id;
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        addTandaToPlaylist(tanda);
                    });
                    tandaSearchResults.appendChild(item);
                });
            });
    });

    // Preload selected tandas if any
    const preloadedTandasData = document.getElementById('preloaded-tandas-data');
    if (preloadedTandasData && preloadedTandasData.textContent) {
        const preloadedTandas = JSON.parse(preloadedTandasData.textContent);
        preloadedTandas.forEach(function(tanda) {
            addTandaToPlaylist(tanda);
        });
    }
});

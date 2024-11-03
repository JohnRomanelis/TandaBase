document.addEventListener('DOMContentLoaded', function() {
    const songSearchInput = document.getElementById('song-search');
    const songSearchResults = document.getElementById('song-search-results');
    const selectedSongs = document.getElementById('selected-songs');
    const songIdsField = document.getElementById('song_ids');

    let selectedSongIds = [];

    // Function to add a song to the tanda
    function addSongToTanda(song) {
        if (selectedSongIds.includes(song.id.toString())) {
            alert('Song already added.');
            return;
        }
        selectedSongIds.push(song.id.toString());
        const item = document.createElement('li');
        item.className = 'list-group-item d-flex justify-content-between align-items-center';
        item.textContent = `${song.title} (${song.orchestra})`;
        const removeBtn = document.createElement('button');
        removeBtn.className = 'btn btn-sm btn-danger ml-2';
        removeBtn.textContent = 'Remove';
        removeBtn.addEventListener('click', function() {
            selectedSongs.removeChild(item);
            selectedSongIds = selectedSongIds.filter(id => id !== song.id.toString());
            updateSongIdsField();
        });
        item.appendChild(removeBtn);
        selectedSongs.appendChild(item);
        updateSongIdsField();
    }

    // Function to update the hidden song IDs field
    function updateSongIdsField() {
        songIdsField.value = selectedSongIds.join(',');
    }

    // Search for songs via AJAX
    songSearchInput.addEventListener('input', function() {
        const query = songSearchInput.value;
        if (query.length < 2) {
            songSearchResults.innerHTML = '';
            return;
        }
        fetch(`/tandas/search_songs?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                songSearchResults.innerHTML = '';
                data.forEach(song => {
                    const item = document.createElement('a');
                    item.href = '#';
                    item.className = 'list-group-item list-group-item-action';
                    item.textContent = `${song.title} (${song.orchestra})`;
                    item.dataset.songId = song.id;
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        addSongToTanda(song);
                    });
                    songSearchResults.appendChild(item);
                });
            });
    });

    // Preload selected songs if any
    const preloadedSongsData = document.getElementById('preloaded-songs-data');
    if (preloadedSongsData && preloadedSongsData.textContent) {
        const preloadedSongs = JSON.parse(preloadedSongsData.textContent);
        preloadedSongs.forEach(function(song) {
            addSongToTanda(song);
        });
    }

    

});

document.addEventListener('DOMContentLoaded', function() {
    const searchSongsBtn = document.getElementById('search-songs-btn');
    const songNameInput = document.getElementById('song-name');
    const orchestraInput = document.getElementById('orchestra');
    const songSearchResults = document.getElementById('song-search-results');
    const selectedSongsContainer = document.getElementById('selected-songs');
    const submitButton = document.getElementById('submit-tanda');
    const form = document.getElementById('tanda-form');

    const songIdsField = document.getElementById('song_ids'); // Hidden input field to store song IDs


    if (submitButton && form) {
        submitButton.addEventListener('click', function(event) {
            event.preventDefault();  // Prevent default behavior just in case
            form.submit();  // Manually submit the form
        });
    }

    let selectedSongs = [];

    // Function to add song to the selected songs table
    function addSongToSelected(song) {
        // Check if the song is already in the selected list
        if (selectedSongs.find(s => s.title === song.title)) {
            alert("This song is already in the selected list.");
            return;
        }

        // Add song to selectedSongs array
        selectedSongs.push(song);
        updateSongIdsField();
        renderSelectedSongsTable();
    }

    // Function to remove a song from the selected songs list
    function removeSongFromSelected(songTitle) {
        selectedSongs = selectedSongs.filter(song => song.title !== songTitle);
        updateSongIdsField();
        renderSelectedSongsTable(); // Re-render the table
    }

    // Function to move a song up in the list
    function moveSongUp(index) {
        if (index > 0) {
            [selectedSongs[index - 1], selectedSongs[index]] = [selectedSongs[index], selectedSongs[index - 1]];
            updateSongIdsField();
            renderSelectedSongsTable();
        }
    }

    // Function to move a song down in the list
    function moveSongDown(index) {
        if (index < selectedSongs.length - 1) {
            [selectedSongs[index + 1], selectedSongs[index]] = [selectedSongs[index], selectedSongs[index + 1]];
            updateSongIdsField();
            renderSelectedSongsTable();
        }
    }

    // Function to update the hidden input field with selected song IDs
    function updateSongIdsField() {
        const songIds = selectedSongs.map(song => song.id);
        songIdsField.value = songIds.join(','); // Set the hidden input's value as a comma-separated list of IDs
    }

    // Render selected songs table
    function renderSelectedSongsTable() {
        selectedSongsContainer.innerHTML = ''; // Clear previous contents
        const table = document.createElement('table');
        table.className = 'table table-striped';

        const headerRow = document.createElement('tr');
        const headers = ['Title', 'Type', 'Style', 'Singers', 'Recording Year', 'Orchestra'];
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        selectedSongs.forEach((song, index) => {
            const row = document.createElement('tr');

            const titleCell = document.createElement('td');
            titleCell.textContent = song.title;
            row.appendChild(titleCell);

            const typeCell = document.createElement('td');
            typeCell.textContent = song.type;
            row.appendChild(typeCell);

            const styleCell = document.createElement('td');
            styleCell.textContent = song.style;
            row.appendChild(styleCell);

            const singerCell = document.createElement('td');
            song.singers.forEach(singer => {
                const singerName = document.createElement('div');
                singerName.textContent = singer;
                singerCell.appendChild(singerName);
            });
            row.appendChild(singerCell);

            const yearCell = document.createElement('td');
            yearCell.textContent = song.recording_year;
            row.appendChild(yearCell);

            const orchestraCell = document.createElement('td');
            orchestraCell.textContent = song.orchestra;
            row.appendChild(orchestraCell);
            
            // Initialize action cells
            const actionsCell = document.createElement('td');

            // Up arrow button
            const upBtn = document.createElement('button');
            upBtn.className = 'btn btn-link btn-sm';
            upBtn.innerHTML = '&#x25B2;'; // Up arrow symbol
            upBtn.title = 'Move Up';
            upBtn.disabled = index === 0; // Disable if it's the first song
            upBtn.addEventListener('click', function() {
                moveSongUp(index);
            });
            actionsCell.appendChild(upBtn);

            // Down arrow button
            const downBtn = document.createElement('button');
            downBtn.className = 'btn btn-link btn-sm';
            downBtn.innerHTML = '&#x25BC;'; // Down arrow symbol
            downBtn.title = 'Move Down';
            downBtn.disabled = index === selectedSongs.length - 1; // Disable if it's the last song
            downBtn.addEventListener('click', function() {
                moveSongDown(index);
            });
            actionsCell.appendChild(downBtn);

            // Actions cell with the remove button
            
            const removeBtn = document.createElement('button');
            removeBtn.className = 'btn btn-danger btn-sm';
            removeBtn.textContent = 'Remove';
            removeBtn.addEventListener('click', function() {
                removeSongFromSelected(song.title);
            });
            actionsCell.appendChild(removeBtn);
            row.appendChild(actionsCell);

            table.appendChild(row);
        });

        selectedSongsContainer.appendChild(table);
    }


    searchSongsBtn.addEventListener('click', function() {
        const queryParams = new URLSearchParams();
        console.log("Button is triggered!", );

        // Collect search criteria from input fields
        if (songNameInput.value.trim()) {
            queryParams.append('name', songNameInput.value.trim());
        }
        if (orchestraInput.value.trim()) {
            queryParams.append('orchestra', orchestraInput.value.trim());
        }

        // Send AJAX request to backend search endpoint
        fetch(`/songs/songs/search_json?${queryParams.toString()}`)
            .then(response => response.json())
            .then(data => {
                songSearchResults.innerHTML = ''; // Clear previous results
                if (data.length === 0) {
                    songSearchResults.innerHTML = '<div class="list-group-item">No songs found.</div>';
                } else {
                   // Create a table to display results
                   const table = document.createElement('table');
                   table.className = 'table table-striped';

                   // Create table header row
                   const headerRow = document.createElement('tr');
                   const headers = ['Title', 'Type', 'Style', 'Singer', 'Recording Year', 'Orchestra'];
                   headers.forEach(headerText => {
                       const th = document.createElement('th');
                       th.textContent = headerText;
                       headerRow.appendChild(th);
                   });
                   table.appendChild(headerRow);

                   // Create table rows for each song
                   data.forEach(song => {
                       const row = document.createElement('tr');

                       row.classList.add('clickable-row'); // Adding class for styling if needed

                        // Add event listener to the row
                        row.addEventListener('click', function() {
                            addSongToSelected(song);
                        });

                       // Create columns for each song attribute
                       const titleCell = document.createElement('td');
                       titleCell.textContent = song.title;
                       row.appendChild(titleCell);

                       const typeCell = document.createElement('td');
                       typeCell.textContent = song.type;
                       row.appendChild(typeCell);

                       const styleCell = document.createElement('td');
                       styleCell.textContent = song.style;
                       row.appendChild(styleCell);

                       const singerCell = document.createElement('td');
                        song.singers.forEach(singer => {
                            const singerName = document.createElement('div');
                            singerName.textContent = singer;
                            singerCell.appendChild(singerName);
                        });
                        row.appendChild(singerCell);

                       const yearCell = document.createElement('td');
                       yearCell.textContent = song.recording_year;
                       row.appendChild(yearCell);

                       const orchestraCell = document.createElement('td');
                       orchestraCell.textContent = song.orchestra;
                       row.appendChild(orchestraCell);

                       table.appendChild(row);
                   });

                   // Append the table to the results container
                   songSearchResults.appendChild(table);
               }
            })
            .catch(error => {
                console.error('Error fetching songs:', error);
            });
    });
});

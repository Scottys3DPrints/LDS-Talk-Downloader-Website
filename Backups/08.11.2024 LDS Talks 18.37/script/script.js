// Function to load "Current" members from the JSON file
function loadCurrentMembers() {
    fetch('json/current.json')
        .then(response => response.json())
        .then(data => {
            displayMembers(data, true); // Show images for current members and display number of talks
        })
        .catch(error => console.error('Error loading current members:', error));
}

// Function to load and sort all General Authorities alphabetically by last name
function loadAlphabeticalMembers() {
    fetch('json/all_GAs.json')
        .then(response => response.json())
        .then(data => {
            data.sort((a, b) => {
                const lastNameA = a.name.split(" ").pop().toLowerCase();
                const lastNameB = b.name.split(" ").pop().toLowerCase();
                return lastNameA.localeCompare(lastNameB);
            });
            displayMembers(data, false); // Hide images for alphabetical listing and display number of talks
        })
        .catch(error => console.error('Error loading all General Authorities:', error));
}

// Function to load and display prophets from the JSON file
function loadProphets() {
    fetch('json/presidents_w_imgs.json')
        .then(response => response.json())
        .then(data => {
            displayMembers(data, true); // Show images for prophets
        })
        .catch(error => console.error('Error loading prophets:', error));
}

// Function to display members on the page
function displayMembers(members, showImages) {
    const talksContainer = document.getElementById('talks-container');
    talksContainer.innerHTML = ''; // Clear the container

    members.forEach(member => {
        const talkCard = document.createElement('div');
        talkCard.className = 'talk-card grid_talk_card';

        // Create elements for the image and speaker details
        if (showImages) {
            const img = document.createElement('img');
            img.src = member.image;
            img.alt = member.name; // Changed to use member.name to match the structure
            img.className = 'ga_img';
            talkCard.appendChild(img); // Append the image to the talk card only if showImages is true
        }

        const speakerInfo = document.createElement('div');
        speakerInfo.className = 'flex_column flex_speaker grid_talk_a1';
        speakerInfo.innerHTML = `
            <h3>${member.name}</h3> <!-- Changed to member.name -->
            <p>Position</p>
        `;

        // Append the speaker info to the talk card
        talkCard.appendChild(speakerInfo);

        // Add General Conference details
        const gcInfo = document.createElement('div');
        gcInfo.className = 'flex_column grid_talk_a2';
        gcInfo.innerHTML = `
            <h4>General Conference</h4>
            <p>${member.general_conference_talks || 'Amount'}</p>
        `;

        const byuInfo = document.createElement('div');
        byuInfo.className = 'flex_column grid_talk_a3';
        byuInfo.innerHTML = `
            <h4>BYU</h4>
            <p>Amount</p>
        `;

        // Create download options
        const downloadContainer = document.createElement('div');
        downloadContainer.className = 'flex_column flex_download grid_talk_a4';
        downloadContainer.innerHTML = `
            <div class="checkbox-container">
                <input type="checkbox" id="gc_download">
                <label for="gc_download">Download General Conference</label>
            </div>
            <div class="checkbox-container">
                <input type="checkbox" id="byu_download">
                <label for="byu_download">Download BYU</label>
            </div>
            <button class="download-button">Download</button>
        `;

        // Append all parts to the talk card
        talkCard.appendChild(gcInfo);
        talkCard.appendChild(byuInfo);
        talkCard.appendChild(downloadContainer);

        // Add the talk card to the container
        talksContainer.appendChild(talkCard);
    });
}

// Search function to filter members based on the input text
function searchTalks() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const talks = document.querySelectorAll('.talk-card');

    talks.forEach(talk => {
        const name = talk.querySelector('h3').textContent.toLowerCase();
        if (name.includes(searchInput)) {
            talk.style.display = 'flex'; // Show matching talk cards
        } else {
            talk.style.display = 'none'; // Hide non-matching talk cards
        }
    });
}

// Event listeners for buttons
document.getElementById('current-button').addEventListener('click', loadCurrentMembers);
document.getElementById('alphabetical-button').addEventListener('click', loadAlphabeticalMembers);
document.getElementById('popular-button').addEventListener('click', loadProphets); // Added event listener for prophets button
document.getElementById('search-input').addEventListener('input', searchTalks);

// Load "Current" members by default when the page is loaded
document.addEventListener('DOMContentLoaded', loadCurrentMembers);

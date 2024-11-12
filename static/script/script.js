function handleDownloadClick(event) {
    const talkCard = event.target.closest('.talk-card');
    if (!talkCard) {
        console.error("Talk card not found.");
        return;
    }

    const nameElement = talkCard.querySelector('h3');
    if (!nameElement) {
        console.error("Name element not found in talk-card.");
        return;
    }

    const name = nameElement.textContent.trim();
    const gcDownloadCheckbox = talkCard.querySelector("#gc_download");
    const byuDownloadCheckbox = talkCard.querySelector("#byu_download");
    
    const gcDownload = gcDownloadCheckbox.checked;
    const byuDownload = byuDownloadCheckbox.checked;

    let scriptPath;

    // Determine which script to run based on the checkboxes
    if (gcDownload && byuDownload) {
        scriptPath = "http://127.0.0.1:5000/gc_byu_download"; // Your Flask endpoint for GC+BYU downloads
    } else if (gcDownload) {
        scriptPath = "http://127.0.0.1:5000/gc_download"; // Your Flask endpoint for GC downloads
    } else if (byuDownload) {
        scriptPath = "http://127.0.0.1:5000/byu_download"; // Your Flask endpoint for BYU downloads
    } else {
        console.log("No download option selected.");
        return;
    }

    // Uncheck the checkboxes
    gcDownloadCheckbox.checked = false;
    byuDownloadCheckbox.checked = false;

    // Send a POST request to the correct Flask server endpoint
    fetch(scriptPath, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            console.log("Response from server:", data.message);
        } else {
            console.error("Error from server:", data.error);
        }
    })
    .catch(error => console.error('Error:', error));
}











// Function to load "Current" members from the JSON file
function loadCurrentMembers() {
    fetch('/static/json/current_with_byu.json')
        .then(response => response.json())
        .then(data => {
            displayMembers(data, true);
        })
        .catch(error => console.error('Error loading current members:', error));
}

// Function to load and sort all General Authorities alphabetically by last name
function loadAlphabeticalMembers() {
    fetch('/static/json/___all2_GAs+ap+pr_with_BYU.json')
        .then(response => response.json())
        .then(data => {
            data.sort((a, b) => {
                const lastNameA = a.name.split(" ").pop().toLowerCase();
                const lastNameB = b.name.split(" ").pop().toLowerCase();
                return lastNameA.localeCompare(lastNameB);
            });
            displayMembers(data, false);
        })
        .catch(error => console.error('Error loading all General Authorities:', error));
}

// Function to load and display prophets from the JSON file
function loadProphets() {
    fetch('/static/json/presidents_w_imgs.json')
        .then(response => response.json())
        .then(data => {
            displayMembers(data, true);
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

        if (showImages) {
            const img = document.createElement('img');
            img.src = member.image || '';
            img.alt = member.name;
            img.className = 'ga_img';
            talkCard.appendChild(img);
        }

        const speakerInfo = document.createElement('div');
        speakerInfo.className = 'flex_column flex_speaker grid_talk_a1';
        speakerInfo.innerHTML = `
            <h3>${member.name}</h3>
            <p>Position</p>
        `;

        talkCard.appendChild(speakerInfo);

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
            <p>${member.byu_talks || 'Amount'}</p>
        `;

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

        talkCard.appendChild(gcInfo);
        talkCard.appendChild(byuInfo);
        talkCard.appendChild(downloadContainer);
        talksContainer.appendChild(talkCard);
    });

    // Reattach event listeners to the new download buttons
    document.querySelectorAll('.download-button').forEach(button => {
        button.addEventListener('click', handleDownloadClick);
    });
}

// Search function to filter members based on the input text
function searchTalks() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const talks = document.querySelectorAll('.talk-card');

    talks.forEach(talk => {
        const name = talk.querySelector('h3').textContent.toLowerCase();
        if (name.includes(searchInput)) {
            talk.style.display = 'flex';
        } else {
            talk.style.display = 'none';
        }
    });
}

// Event listeners for buttons
document.getElementById('current-button').addEventListener('click', loadCurrentMembers);
document.getElementById('alphabetical-button').addEventListener('click', loadAlphabeticalMembers);
document.getElementById('popular-button').addEventListener('click', loadProphets);
document.getElementById('search-input').addEventListener('input', searchTalks);

// Load "Current" members by default when the page is loaded
document.addEventListener('DOMContentLoaded', loadCurrentMembers);

// Test Button for Simple Debugging
document.getElementById('test-button').addEventListener('click', () => {
    fetch('http://127.0.0.1:5000/download', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: "Test Name" })
    })
    .then(response => response.json())
    .then(data => console.log("Test Server response:", data))
    .catch(error => console.error('Error:', error));
});

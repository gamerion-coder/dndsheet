document.addEventListener('DOMContentLoaded', function() {
    const characterSelect = document.getElementById('character-select');
    const newCharacterBtn = document.getElementById('new-character-btn');
    const characterDisplayArea = document.getElementById('character-display-area');

    // Function to fetch and display character details
    async function fetchCharacterDetails(characterId) {
        if (!characterId) {
            characterDisplayArea.innerHTML = '';
            return;
        }
        try {
            const response = await fetch(`/_render_character_display/${characterId}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const characterHtml = await response.text();
            characterDisplayArea.innerHTML = characterHtml;
        } catch (error) {
            console.error('Error fetching character details:', error);
            characterDisplayArea.innerHTML = `<p>Error loading character details: ${error.message}</p>`;
        }
    }

    // Function to render the character sheet HTML
    // This function is no longer needed as the backend renders the HTML
    // function renderCharacterSheet(character) {
    //     characterDisplayArea.innerHTML = `
    //         <main>
    //             <header>
    //                 <h1>${character.name}</h1>
    //                 <div class="character-basics">
    //                     <p><strong>Class & Level:</strong> ${character.class} ${character.level}</p>
    //                     <p><strong>Race:</strong> ${character.race}</p>
    //                 </div>
    //             </header>

    //             <section class="abilities">
    //                 <h2>Abilities</h2>
    //                 <div class="ability-scores">
    //                     <div class="ability-score">
    //                         <h3>STR</h3>
    //                         <p class="score">${character.strength}</p>
    //                     </div>
    //                     <div class="ability-score">
    //                         <h3>DEX</h3>
    //                         <p class="score">${character.dexterity}</p>
    //                     </div>
    //                     <div class="ability-score">
    //                         <h3>CON</h3>
    //                         <p class="score">${character.constitution}</p>
    //                     </div>
    //                     <div class="ability-score">
    //                         <h3>INT</h3>
    //                         <p class="score">${character.intelligence}</p>
    //                     </div>
    //                     <div class="ability-score">
    //                         <h3>WIS</h3>
    //                         <p class="score">${character.wisdom}</p>
    //                     </div>
    //                     <div class="ability-score">
    //                         <h3>CHA</h3>
    //                         <p class="score">${character.charisma}</p>
    //                     </div>
    //                 </div>
    //             </section>

    //             <section class="combat">
    //                 <h2>Combat</h2>
    //                 <div class="combat-stats">
    //                     <p><strong>Armor Class:</strong> ${character.ac}</p>
    //                     <p><strong>Hit Points:</strong> ${character.hp}</p>
    //                 </div>
    //             </section>

    //             <section class="equipment">
    //                 <h2>Equipment</h2>
    //                 <p>${character.inventory}</p>
    //             </section>
    //         </main>
    //     `;
    // }

    // Event listener for character selection
    characterSelect.addEventListener('change', (event) => {
        const selectedCharacterId = event.target.value;
        fetchCharacterDetails(selectedCharacterId);
    });

    // Event listener for "Create New Character" button
    newCharacterBtn.addEventListener('click', () => {
        // For now, we'll just alert. Later, this could lead to a form.
        alert('Feature to create new character is not yet implemented!');
    });

    // Initial load: if a character is pre-selected (e.g., from URL or previous session)
    // fetchCharacterDetails(characterSelect.value);
});

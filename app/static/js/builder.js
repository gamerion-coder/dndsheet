document.addEventListener('DOMContentLoaded', () => {
    const totalSteps = 10;
    let currentStep = 0;
    const character = {
        name: '',
        race: '',
        alignment: '',
        attributes: { str: 10, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        characterClass: '',
        skills: [],
        background: '',
        level: 1,
        subclass: '',
        feats: [],
        spells: [],
        equipment: [],
    };
    const dndData = {
        races: [], classes: [], backgrounds: [], equipment: [], spells: [], feats: [],
        alignments: [
            { id: 'lawful-good', name: 'Lawful Good' },
            { id: 'neutral-good', name: 'Neutral Good' },
            { id: 'chaotic-good', name: 'Chaotic Good' },
            { id: 'lawful-neutral', name: 'Lawful Neutral' },
            { id: 'neutral', name: 'Neutral' },
            { id: 'chaotic-neutral', name: 'Chaotic Neutral' },
            { id: 'lawful-evil', name: 'Lawful Evil' },
            { id: 'neutral-evil', name: 'Neutral Evil' },
            { id: 'chaotic-evil', name: 'Chaotic Evil' },
        ],
        skills: [
            { id: 'acrobatics', name: 'Acrobatics', ability: 'dex' },
            { id: 'animal-handling', name: 'Animal Handling', ability: 'wis' },
            { id: 'arcana', name: 'Arcana', ability: 'int' },
            { id: 'athletics', name: 'Athletics', ability: 'str' },
            { id: 'deception', name: 'Deception', ability: 'cha' },
            { id: 'history', name: 'History', ability: 'int' },
            { id: 'insight', name: 'Insight', ability: 'wis' },
            { id: 'intimidation', name: 'Intimidation', ability: 'cha' },
            { id: 'investigation', name: 'Investigation', ability: 'int' },
            { id: 'medicine', name: 'Medicine', ability: 'wis' },
            { id: 'nature', name: 'Nature', ability: 'int' },
            { id: 'perception', name: 'Perception', ability: 'wis' },
            { id: 'performance', name: 'Performance', ability: 'cha' },
            { id: 'persuasion', name: 'Persuasion', ability: 'cha' },
            { id: 'religion', name: 'Religion', ability: 'int' },
            { id: 'sleight-of-hand', name: 'Sleight of Hand', ability: 'dex' },
            { id: 'stealth', name: 'Stealth', ability: 'dex' },
            { id: 'survival', name: 'Survival', ability: 'wis' },
        ] // Hardcoded for now, will fetch from API later
    };
    let translations = {};
    let currentLang = 'en';

    const elements = {
        prevBtn: document.getElementById('prevBtn'),
        nextBtn: document.getElementById('nextBtn'),
        speciesSelect: document.getElementById('species-select'),
        alignmentSelect: document.getElementById('alignment-select'),
        classSelect: document.getElementById('class-select'),
        backgroundSelect: document.getElementById('background-select'),
        levelSelect: document.getElementById('level-select'),
        subclassSelect: document.getElementById('subclass-select'),
        skillsCheckboxes: document.getElementById('skills-checkboxes'),
        featsCheckboxes: document.getElementById('feats-checkboxes'),
        spellsCheckboxes: document.getElementById('spells-checkboxes'),
        equipmentTextarea: document.getElementById('equipment-textarea'),
    };

    // Helper to fetch data from API
    async function fetchData(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error(`Failed to fetch ${url}:`, error);
            return [];
        }
    }

    async function loadInitialData() {
        // Load static data first
        dndData.races = await fetchData('/api/catalog/races');
        dndData.classes = await fetchData('/api/catalog/classes');
        dndData.backgrounds = await fetchData('/api/catalog/backgrounds');
        dndData.equipment = await fetchData('/api/catalog/equipment');
        dndData.spells = await fetchData('/api/catalog/spells');
        dndData.feats = await fetchData('/api/catalog/feats');

        // Load translations and apply
        await setLanguage(currentLang);
        populateWizardOptions();
        showStep(currentStep);
    }

    async function setLanguage(lang) {
        currentLang = lang;
        translations = await fetchData(`/api/translations/${lang}`); // Await the fetch
        applyTranslations();
        populateWizardOptions(); // Re-populate options to translate them if needed
        showStep(currentStep); // Re-render current step with new language
        // TODO: Re-render sheet if already displayed
    }

    function applyTranslations() {
        document.title = translations.ui.appTitle;
        elements.prevBtn.textContent = translations.ui.previous;
        elements.nextBtn.textContent = translations.ui.next;

        document.getElementById('step1-title').textContent = translations.steps.step1;
        elements.speciesSelect.previousElementSibling.textContent = translations.fields.species + ':';
        elements.alignmentSelect.previousElementSibling.textContent = translations.fields.alignment + ':';

        document.getElementById('step2-title').textContent = translations.steps.step2;
        document.getElementById('str-label').textContent = translations.fields.strength + ':';
        document.getElementById('dex-label').textContent = translations.fields.dexterity + ':';
        document.getElementById('con-label').textContent = translations.fields.constitution + ':';
        document.getElementById('int-label').textContent = translations.fields.intelligence + ':';
        document.getElementById('wis-label').textContent = translations.fields.wisdom + ':';
        document.getElementById('cha-label').textContent = translations.fields.charisma + ':';

        document.getElementById('step3-title').textContent = translations.steps.step3;
        elements.classSelect.previousElementSibling.textContent = translations.fields.characterClass + ':';

        document.getElementById('step4-title').textContent = translations.steps.step4;
        elements.skillsCheckboxes.previousElementSibling.textContent = translations.fields.skills + ':';

        document.getElementById('step5-title').textContent = translations.steps.step5;
        elements.backgroundSelect.previousElementSibling.textContent = translations.fields.background + ':';

        document.getElementById('step6-title').textContent = translations.steps.step6;
        elements.levelSelect.previousElementSibling.textContent = translations.fields.level + ':';

        document.getElementById('step7-title').textContent = translations.steps.step7;
        elements.subclassSelect.previousElementSibling.textContent = translations.fields.subclass + ':';

        document.getElementById('step8-title').textContent = translations.steps.step8;
        elements.featsCheckboxes.previousElementSibling.textContent = translations.fields.feats + ':';

        document.getElementById('step9-title').textContent = translations.steps.step9;
        elements.spellsCheckboxes.previousElementSibling.textContent = translations.fields.spells + ':';

        document.getElementById('step10-title').textContent = translations.steps.step10;
        elements.equipmentTextarea.previousElementSibling.textContent = translations.fields.equipment + ':';

        // Update placeholders
        elements.equipmentTextarea.placeholder = translations.fields.equipmentPlaceholder || '';
    }

    function populateWizardOptions() {
        // Step 1: Species and Alignment
        populateSelect(elements.speciesSelect, dndData.races, translations.selections.selectSpecies, 'name', 'id');
        populateSelect(elements.alignmentSelect, dndData.alignments, translations.selections.selectAlignment, 'name', 'id');

        // Step 2: Attributes are direct input
        const attributeNames = ['str', 'dex', 'con', 'int', 'wis', 'cha'];
        attributeNames.forEach(attr => {
            const input = document.getElementById(`attr-${attr}`);
            if (input) {
                input.value = character.attributes[attr];
                input.onchange = (e) => character.attributes[attr] = parseInt(e.target.value) || 0;
            }
        });

        // Step 3: Class
        populateSelect(elements.classSelect, dndData.classes, translations.selections.selectClass, 'name', 'id');

        // Step 4: Skills
        populateCheckboxes(elements.skillsCheckboxes, dndData.skills, character.skills, 'name', 'id');

        // Step 5: Background
        populateSelect(elements.backgroundSelect, dndData.backgrounds, translations.selections.selectBackground, 'name', 'id');

        // Step 6: Level
        populateLevelSelect(elements.levelSelect, translations.selections.selectLevel);

        // Step 7: Subclass (dynamically loaded based on class and level)
        // Step 8: Feats (dynamically loaded based on class and level)
        // Step 9: Spells (dynamically loaded based on class and level)

        // Step 10: Equipment
        elements.equipmentTextarea.value = character.equipment.join('\n');
        elements.equipmentTextarea.onchange = (e) => character.equipment = e.target.value.split('\n').map(s => s.trim()).filter(Boolean);

        // Event listeners for dynamic updates
        elements.classSelect.onchange = updateDynamicOptions;
        elements.levelSelect.onchange = updateDynamicOptions;
    }

    function populateSelect(selectElement, data, defaultOptionText, textKey, valueKey) {
        if (!selectElement) return;
        selectElement.innerHTML = `<option value="">${defaultOptionText}</option>`;
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = item[valueKey];
            option.textContent = item[textKey];
            selectElement.appendChild(option);
        });
        // Restore selected value if it exists in character object
        const prop = selectElement.id.replace('-select', '');
        if (character[prop]) {
            selectElement.value = character[prop];
        }
        selectElement.onchange = (e) => character[prop] = e.target.value;
    }

    function populateCheckboxes(containerElement, data, selectedArray, textKey, valueKey) {
        if (!containerElement) return;
        containerElement.innerHTML = '';
        data.forEach(item => {
            const div = document.createElement('div');
            const input = document.createElement('input');
            input.type = 'checkbox';
            input.id = `cb-${item[valueKey]}`;
            input.value = item[valueKey];
            input.checked = selectedArray.includes(item[valueKey]);
            input.onchange = (e) => {
                if (e.target.checked) {
                    if (!selectedArray.includes(item[valueKey])) {
                        selectedArray.push(item[valueKey]);
                    }
                } else {
                    const index = selectedArray.indexOf(item[valueKey]);
                    if (index > -1) {
                        selectedArray.splice(index, 1);
                    }
                }
            };
            const label = document.createElement('label');
            label.htmlFor = `cb-${item[valueKey]}`;
            label.textContent = item[textKey];
            div.appendChild(input);
            div.appendChild(label);
            containerElement.appendChild(div);
        });
    }

    function populateLevelSelect(selectElement, defaultOptionText) {
        if (!selectElement) return;
        selectElement.innerHTML = `<option value="">${defaultOptionText}</option>`;
        for (let i = 1; i <= 20; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i;
            selectElement.appendChild(option);
        }
        if (character.level) {
            selectElement.value = character.level;
        }
        selectElement.onchange = (e) => character.level = parseInt(e.target.value) || 1;
    }

    async function updateDynamicOptions() {
        // Subclass logic
        const selectedClass = character.characterClass;
        const selectedLevel = character.level;
        elements.subclassSelect.innerHTML = `<option value="">${translations.selections.selectSubclass}</option>`;
        if (selectedClass && selectedLevel >= 3) {
            const classData = dndData.classes.find(c => c.id === selectedClass);
            if (classData && classData.subclasses) { // Assuming subclasses are nested in class data
                classData.subclasses.forEach(sub => {
                    const option = document.createElement('option');
                    option.value = sub.id;
                    option.textContent = sub.name;
                    elements.subclassSelect.appendChild(option);
                });
                if (character.subclass) { elements.subclassSelect.value = character.subclass; }
                elements.subclassSelect.onchange = (e) => character.subclass = e.target.value;
            }
        } else if (elements.subclassSelect) {
            elements.subclassSelect.innerHTML = `<option value="">${translations.selections.noSubclassAvailable}</option>`;
        }

        // Feats logic (simplified - will need actual filtering)
        elements.featsCheckboxes.innerHTML = '';
        if (selectedLevel >= 1) { // Feats start at level 1, but eligibility varies
            populateCheckboxes(elements.featsCheckboxes, dndData.feats, character.feats, 'name', 'id');
        } else if (elements.featsCheckboxes) {
            elements.featsCheckboxes.innerHTML = `<p>${translations.selections.noFeatsAvailable}</p>`;
        }

        // Spells logic (simplified - will need actual filtering)
        elements.spellsCheckboxes.innerHTML = '';
        if (selectedClass && selectedLevel >= 1) { // Spells depend on class and level
            // For now, just show all spells, real filtering based on class/level/spell list will be implemented later
            populateCheckboxes(elements.spellsCheckboxes, dndData.spells, character.spells, 'name', 'id');
        } else if (elements.spellsCheckboxes) {
            elements.spellsCheckboxes.innerHTML = `<p>${translations.selections.noSpellsAvailable}</p>`;
        }
    }

    function showStep(stepIndex) {
        document.querySelectorAll('.wizard-step').forEach((step, index) => {
            if (index === stepIndex) {
                step.classList.add('active');
            } else {
                step.classList.remove('active');
            }
        });

        elements.prevBtn.disabled = stepIndex === 0;
        elements.nextBtn.textContent = stepIndex === totalSteps - 1 ? translations.ui.finish : translations.ui.next;

        // Update dynamic options if navigating to spell/feat/subclass steps
        if ([6, 7, 8, 9].includes(stepIndex)) { // Level, Subclass, Feats, Spells steps
            updateDynamicOptions();
        }
    }

    elements.prevBtn.addEventListener('click', () => {
        if (currentStep > 0) {
            currentStep--;
            showStep(currentStep);
        }
    });

    elements.nextBtn.addEventListener('click', async () => {
        // Basic validation before moving to next step
        const currentStepElement = document.getElementById(`step-${currentStep + 1}`);
        let isValid = true;

        if (currentStep === 0) { // Race and Alignment
            if (!character.race) { isValid = false; alert(translations.validation.required + ': ' + translations.fields.species); }
            if (isValid && !character.alignment) { isValid = false; alert(translations.validation.required + ': ' + translations.fields.alignment); }
        } else if (currentStep === 1) { // Attributes
            for (const attr of Object.values(character.attributes)) {
                if (attr < 1 || attr > 20) { isValid = false; alert(translations.validation.invalidAttribute); break; }
            }
        } else if (currentStep === 2) { // Class
            if (!character.characterClass) { isValid = false; alert(translations.validation.required + ': ' + translations.fields.characterClass); }
        } else if (currentStep === 5) { // Level
            if (character.level < 1 || character.level > 20) { isValid = false; alert(translations.validation.invalidLevel); }
        }

        if (!isValid) return;

        if (currentStep < totalSteps - 1) {
            currentStep++;
            showStep(currentStep);
        } else if (currentStep === totalSteps - 1) {
            // Last step, generate character sheet and save
            const characterNameInput = document.getElementById('character-name-input'); // Assuming an input for character name
            if (characterNameInput) { character.name = characterNameInput.value; }

            try {
                const response = await fetch('/api/character/export-json', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        character: {
                            meta: { locale: currentLang },
                            character: {
                                name: character.name,
                                alignment: character.alignment,
                                species: { id: character.race, label: dndData.races.find(r => r.id === character.race)?.name || character.race },
                                class: { id: character.characterClass, label: dndData.classes.find(c => c.id === character.characterClass)?.name || character.characterClass },
                                subclass: { id: character.subclass, label: dndData.classes.find(c => c.id === character.characterClass)?.subclasses?.find(sub => sub.id === character.subclass)?.name || character.subclass },
                                background: { id: character.background, label: dndData.backgrounds.find(bg => bg.id === character.background)?.name || character.background },
                                level: character.level
                            },
                            abilities: character.attributes,
                            skills: character.skills,
                            feats: character.feats,
                            spells: { known: character.spells, prepared: [] }, // simplified for now
                            equipment: character.equipment,
                            derived: {},
                            audit: {},
                        }
                    })
                });

                if (!response.ok) {
                    throw new Error(`Failed to save character: ${response.statusText}`);
                }
                const result = await response.json();
                window.location.href = `/sheet/${result.character_id}`;
            } catch (error) {
                console.error('Error saving character:', error);
                alert('Failed to save character. Please try again.');
            }
        }
    });

    loadInitialData();
});
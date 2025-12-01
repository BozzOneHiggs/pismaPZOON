
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML Insertion
# We will insert the Mail Merge Sidebar inside #appContainer, before the "Pasek użytkownika".
# It will be a fixed sidebar on the left.

sidebar_html = """
        <!-- MAIL MERGE SIDEBAR -->
        <div id="mailMergeSidebar" class="fixed left-0 top-0 h-full w-80 bg-white shadow-2xl transform -translate-x-full transition-transform duration-300 z-50 overflow-y-auto hidden">
            <div class="p-4 bg-gray-800 text-white flex justify-between items-center">
                <h2 class="font-bold text-lg">KORESPONDENCJA SERYJNA</h2>
                <button id="closeMailMergeButton" class="text-gray-400 hover:text-white">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <div class="p-4 space-y-4">
                <!-- Search Section -->
                <div>
                    <label for="mailMergeSearch" class="block text-xs font-medium text-gray-700 uppercase mb-1">Szukaj (Numer Sprawy)</label>
                    <input type="text" id="mailMergeSearch" placeholder="Wpisz numer..." class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 uppercase">
                </div>

                <!-- Search Results -->
                <div id="mailMergeSearchResults" class="space-y-2 max-h-48 overflow-y-auto border-b pb-2">
                    <!-- Results will be injected here -->
                    <p class="text-xs text-gray-500 italic">Brak wyników wyszukiwania.</p>
                </div>

                <div class="border-t border-gray-200 my-2"></div>

                <!-- Selected List -->
                <div class="flex justify-between items-center">
                    <h3 class="font-bold text-sm text-gray-800">WYBRANE ADRESY (<span id="mailMergeCount">0</span>)</h3>
                    <button id="clearMailMergeListButton" class="text-xs text-red-600 hover:text-red-800 uppercase">Wyczyść</button>
                </div>

                <div id="mailMergeList" class="space-y-2 max-h-64 overflow-y-auto bg-gray-50 p-2 rounded border">
                    <!-- Selected items will be injected here -->
                    <p class="text-xs text-gray-500 italic text-center">Lista jest pusta.</p>
                </div>

                <!-- Actions -->
                <div class="space-y-2 pt-2">
                    <button id="mailMergePrintEnvelopesButton" class="w-full bg-pink-600 text-white px-4 py-2 rounded-md hover:bg-pink-700 transition-colors shadow text-sm uppercase">Drukuj Koperty (Seryjnie)</button>
                    <button id="mailMergePrintReceiptsButton" class="w-full bg-lime-600 text-white px-4 py-2 rounded-md hover:bg-lime-700 transition-colors shadow text-sm uppercase">Drukuj Zwrotki (Seryjnie)</button>
                </div>

                <div id="mailMergeMessageArea" class="h-6 text-xs font-medium text-center mt-2"></div>
            </div>
        </div>

        <!-- TOGGLE BUTTON (Visible only on Envelopes tab) -->
        <button id="toggleMailMergeButton" class="fixed left-0 top-1/2 transform -translate-y-1/2 bg-gray-800 text-white p-2 rounded-r-md shadow-lg hover:bg-gray-700 transition-colors z-40 hidden" title="Pokaż Korespondencję Seryjną">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13 5l7 7-7 7M5 5l7 7-7 7" />
            </svg>
        </button>
"""

# Insertion point: inside appContainer, at the beginning
search_app_container = '<div id="appContainer" class="hidden">'
if search_app_container in content:
    content = content.replace(search_app_container, search_app_container + '\n' + sidebar_html)
else:
    print("Error: appContainer not found")

# 2. JS Modifications

# A. Add variables and DOM elements
js_dom_elements = """
        // === MAIL MERGE ELEMENTS ===
        const mailMergeSidebar = document.getElementById('mailMergeSidebar');
        const toggleMailMergeButton = document.getElementById('toggleMailMergeButton');
        const closeMailMergeButton = document.getElementById('closeMailMergeButton');
        const mailMergeSearchInput = document.getElementById('mailMergeSearch');
        const mailMergeSearchResultsContainer = document.getElementById('mailMergeSearchResults');
        const mailMergeListContainer = document.getElementById('mailMergeList');
        const mailMergeCountSpan = document.getElementById('mailMergeCount');
        const clearMailMergeListButton = document.getElementById('clearMailMergeListButton');
        const mailMergePrintEnvelopesButton = document.getElementById('mailMergePrintEnvelopesButton');
        const mailMergePrintReceiptsButton = document.getElementById('mailMergePrintReceiptsButton');
        const mailMergeMessageArea = document.getElementById('mailMergeMessageArea');

        let mailMergeList = [];
        let isMailMergeSidebarOpen = false;
"""

# Insert before `// === Funkcje pomocnicze`
search_js_start = '// === Funkcje pomocnicze (Komunikaty) ==='
content = content.replace(search_js_start, js_dom_elements + '\n\n' + search_js_start)


# B. Add Helper functions for Mail Merge
js_functions = """
        // === MAIL MERGE FUNCTIONS ===

        function toggleMailMergeSidebar() {
            isMailMergeSidebarOpen = !isMailMergeSidebarOpen;
            if (isMailMergeSidebarOpen) {
                mailMergeSidebar.classList.remove('-translate-x-full');
                toggleMailMergeButton.classList.add('hidden'); // Hide toggle button when open
            } else {
                mailMergeSidebar.classList.add('-translate-x-full');
                toggleMailMergeButton.classList.remove('hidden'); // Show toggle button when closed
            }
        }

        function showMailMergeMessage(text, isError = false) {
            mailMergeMessageArea.textContent = text.toUpperCase();
            mailMergeMessageArea.className = `h-6 text-xs font-medium text-center mt-2 ${isError ? 'text-red-600' : 'text-green-600'}`;
            setTimeout(() => { mailMergeMessageArea.textContent = ''; }, 3000);
        }

        async function handleMailMergeSearch() {
            if (!envelopesCollection) return;
            const queryText = mailMergeSearchInput.value.toUpperCase().trim();

            if (queryText.length < 2) {
                mailMergeSearchResultsContainer.innerHTML = '<p class="text-xs text-gray-500 italic">Wpisz co najmniej 2 znaki...</p>';
                return;
            }

            try {
                // Prefix search logic: query >= text AND query <= text + '\uf8ff'
                const q = query(
                    envelopesCollection,
                    where('numer_sprawy', '>=', queryText),
                    where('numer_sprawy', '<=', queryText + '\\uf8ff')
                );

                // Limit results to avoid overload
                // Note: limit() needs to be imported or handled manually if not.
                // Assuming standard usage or just getting matching docs.
                // Since limit is not imported in the top script block, I will iterate and break.
                // Wait, 'limit' is not in the imports list in index.html (I see getDocs, query, where...).
                // I will fetch and slice.

                const querySnapshot = await getDocs(q);
                const results = [];
                querySnapshot.forEach((doc) => {
                    results.push(doc.data());
                });

                renderMailMergeSearchResults(results.slice(0, 10)); // Limit to 10 for display

            } catch (error) {
                console.error("BŁĄD WYSZUKIWANIA SERYJNEGO:", error);
                mailMergeSearchResultsContainer.innerHTML = '<p class="text-xs text-red-500">Błąd wyszukiwania.</p>';
            }
        }

        function renderMailMergeSearchResults(results) {
            mailMergeSearchResultsContainer.innerHTML = '';
            if (results.length === 0) {
                mailMergeSearchResultsContainer.innerHTML = '<p class="text-xs text-gray-500 italic">Brak wyników.</p>';
                return;
            }

            results.forEach(item => {
                const div = document.createElement('div');
                div.className = 'flex justify-between items-center bg-gray-100 p-2 rounded border text-xs';

                const infoDiv = document.createElement('div');
                infoDiv.innerHTML = `<div class="font-bold truncate w-40">${item.numer_sprawy}</div><div class="truncate w-40 text-gray-600">${item.adresat}</div>`;

                const addBtn = document.createElement('button');
                addBtn.textContent = '+';
                addBtn.className = 'bg-blue-600 text-white w-6 h-6 rounded flex items-center justify-center hover:bg-blue-700';
                addBtn.onclick = () => addToMailMergeList(item);

                div.appendChild(infoDiv);
                div.appendChild(addBtn);
                mailMergeSearchResultsContainer.appendChild(div);
            });
        }

        function addToMailMergeList(item) {
            // Check for duplicates based on numer_sprawy
            if (mailMergeList.some(i => i.numer_sprawy === item.numer_sprawy)) {
                showMailMergeMessage("JUŻ NA LIŚCIE", true);
                return;
            }
            mailMergeList.push(item);
            renderMailMergeList();
            showMailMergeMessage("DODANO", false);
        }

        function removeFromMailMergeList(index) {
            mailMergeList.splice(index, 1);
            renderMailMergeList();
        }

        function clearMailMergeList() {
            if(confirm('CZY NA PEWNO CHCESZ WYCZYŚCIĆ LISTĘ?')) {
                mailMergeList = [];
                renderMailMergeList();
            }
        }

        function renderMailMergeList() {
            mailMergeListContainer.innerHTML = '';
            mailMergeCountSpan.textContent = mailMergeList.length;

            if (mailMergeList.length === 0) {
                mailMergeListContainer.innerHTML = '<p class="text-xs text-gray-500 italic text-center">Lista jest pusta.</p>';
                return;
            }

            mailMergeList.forEach((item, index) => {
                const div = document.createElement('div');
                div.className = 'flex justify-between items-center bg-white p-2 rounded border text-xs shadow-sm';

                const infoDiv = document.createElement('div');
                infoDiv.innerHTML = `<div class="font-bold truncate w-48">${item.numer_sprawy}</div>`;

                const removeBtn = document.createElement('button');
                removeBtn.innerHTML = '&times;';
                removeBtn.className = 'text-red-500 font-bold text-lg hover:text-red-700 px-2';
                removeBtn.onclick = () => removeFromMailMergeList(index);

                div.appendChild(infoDiv);
                div.appendChild(removeBtn);
                mailMergeListContainer.appendChild(div);
            });
        }

        async function handleMailMergePrintEnvelopes() {
            if (mailMergeList.length === 0) {
                showMailMergeMessage("LISTA PUSTA", true);
                return;
            }
            try {
                const pdfContent = mailMergeList.map((data, index) => {
                    const content = createEnvelopeContent(data);
                    if (index < mailMergeList.length - 1) {
                        content.pageBreak = 'after';
                    }
                    return content;
                });

                const docDefinition = {
                    pageSize: C6_PAGE_SIZE,
                    pageMargins: 0,
                    content: pdfContent,
                    styles: { defaultStyle: { font: 'Roboto' } }
                };

                pdfMake.createPdf(docDefinition).download(`koperty_seryjne_${new Date().toISOString().slice(0, 10)}.pdf`);
                showMailMergeMessage("GENEROWANIE PDF...", false);
            } catch (error) {
                console.error("BŁĄD DRUKU SERYJNEGO (KOPERTY):", error);
                showMailMergeMessage("BŁĄD DRUKU", true);
            }
        }

        async function handleMailMergePrintReceipts() {
            if (mailMergeList.length === 0) {
                showMailMergeMessage("LISTA PUSTA", true);
                return;
            }
            try {
                const pdfContent = mailMergeList.map((data, index) => {
                    const singleReceiptDef = createReceiptContent(data);
                    const contentWrapper = {
                        stack: singleReceiptDef.content
                    };
                    if (index < mailMergeList.length - 1) {
                        contentWrapper.pageBreak = 'after';
                    }
                    return contentWrapper;
                });

                const docDefinition = {
                    pageSize: C6_PAGE_SIZE,
                    pageMargins: [5, 5, 5, 5],
                    content: pdfContent,
                    styles: { defaultStyle: { font: 'Roboto' } }
                };

                pdfMake.createPdf(docDefinition).download(`zwrotki_seryjne_${new Date().toISOString().slice(0, 10)}.pdf`);
                showMailMergeMessage("GENEROWANIE PDF...", false);
            } catch (error) {
                console.error("BŁĄD DRUKU SERYJNEGO (ZWROTKI):", error);
                showMailMergeMessage("BŁĄD DRUKU", true);
            }
        }
"""

# Insert JS functions
search_js_main_logic = '// --- Funkcje Główne (Koperty) ---'
content = content.replace(search_js_main_logic, js_functions + '\n\n' + search_js_main_logic)


# C. Update switchTab function to manage visibility
# We need to find the `switchTab` function and add logic to show/hide `toggleMailMergeButton`.
# If `tabName === 'envelopes'`, show button (remove 'hidden'). Else hide button (add 'hidden') and close sidebar if open.

search_switch_tab = """            // Pokaż wybraną zakładkę i aktywuj przycisk
            if (tabName === 'envelopes') {
                envelopeGeneratorTab.classList.remove('hidden');
                envelopeGeneratorTab.classList.add('active');
                tabButtonEnvelopes.classList.add('active');
            }"""

replace_switch_tab = """            // Pokaż wybraną zakładkę i aktywuj przycisk
            if (tabName === 'envelopes') {
                envelopeGeneratorTab.classList.remove('hidden');
                envelopeGeneratorTab.classList.add('active');
                tabButtonEnvelopes.classList.add('active');
                // SHOW MAIL MERGE TOGGLE
                if(toggleMailMergeButton) toggleMailMergeButton.classList.remove('hidden');
            } else {
                // HIDE MAIL MERGE TOGGLE AND CLOSE SIDEBAR
                if(toggleMailMergeButton) toggleMailMergeButton.classList.add('hidden');
                if(isMailMergeSidebarOpen) toggleMailMergeSidebar(); // Close if open
            }"""

# Since `switchTab` has `else if` blocks, I should be careful.
# Instead of replacing the block inside `if`, I will append the logic at the end of the function or modify the function body.
# Let's verify `switchTab` content again.
# It ends with `else if (tabName === 'response') ...`
# I can insert the visibility logic at the END of the function.

search_switch_tab_end = """            } else if (tabName === 'response') {
                responseApplicationTab.classList.remove('hidden');
                responseApplicationTab.classList.add('active');
                tabButtonResponse.classList.add('active');
            }
        }"""

replace_switch_tab_end = """            } else if (tabName === 'response') {
                responseApplicationTab.classList.remove('hidden');
                responseApplicationTab.classList.add('active');
                tabButtonResponse.classList.add('active');
            }

            // Manage Mail Merge Sidebar Visibility
            if (tabName === 'envelopes') {
                if(toggleMailMergeButton && !isMailMergeSidebarOpen) toggleMailMergeButton.classList.remove('hidden');
            } else {
                if(toggleMailMergeButton) toggleMailMergeButton.classList.add('hidden');
                if(isMailMergeSidebarOpen) toggleMailMergeSidebar(); // Close sidebar if active
            }
        }"""

if search_switch_tab_end in content:
    content = content.replace(search_switch_tab_end, replace_switch_tab_end)
else:
    print("Error: switchTab end not found")


# D. Add Event Listeners
# Inside `initializeUIListeners`

js_listeners = """            // === MAIL MERGE LISTENERS ===
            if (toggleMailMergeButton) toggleMailMergeButton.addEventListener('click', toggleMailMergeSidebar);
            if (closeMailMergeButton) closeMailMergeButton.addEventListener('click', toggleMailMergeSidebar);
            if (mailMergeSearchInput) mailMergeSearchInput.addEventListener('input', handleMailMergeSearch);
            if (clearMailMergeListButton) clearMailMergeListButton.addEventListener('click', clearMailMergeList);
            if (mailMergePrintEnvelopesButton) mailMergePrintEnvelopesButton.addEventListener('click', handleMailMergePrintEnvelopes);
            if (mailMergePrintReceiptsButton) mailMergePrintReceiptsButton.addEventListener('click', handleMailMergePrintReceipts);
"""

search_ui_listeners = '// --- GŁÓWNA LOGIKA STARTOWA ---'
content = content.replace(search_ui_listeners, js_listeners + '\n\n' + search_ui_listeners)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied Mail Merge Sidebar changes.")

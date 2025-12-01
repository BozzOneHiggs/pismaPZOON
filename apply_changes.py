
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. HTML modification
search_html = """                            <div>
                                <label for="odp_data_prawomocnosci" class="block text-sm font-medium text-gray-700">DATA PRAWOMOCNOŚCI {DATA_PRAWOMOCNOŚCI}</label>
                                <input type="date" id="odp_data_prawomocnosci" class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 no-uppercase">
                            </div>"""

replace_html = """                            <div>
                                <label for="odp_data_prawomocnosci" class="block text-sm font-medium text-gray-700">DATA PRAWOMOCNOŚCI {DATA_PRAWOMOCNOŚCI}</label>
                                <input type="date" id="odp_data_prawomocnosci" class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 no-uppercase">
                            </div>
                            <!-- NOWE POLA DLA ODWOŁANIA -->
                            <div class="col-span-2 flex items-center space-x-2 mt-4">
                                <input type="checkbox" id="odp_odwolanie" class="h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500">
                                <label for="odp_odwolanie" class="text-sm font-medium text-gray-700">ZŁOŻONO ODWOŁANIE</label>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 col-span-2">
                                <div>
                                    <label for="odp_data_odwolania" class="block text-sm font-medium text-gray-700">DATA ZŁOŻENIA ODWOŁANIA</label>
                                    <input type="date" id="odp_data_odwolania" class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 no-uppercase">
                                </div>
                                <div>
                                    <label for="odp_data_wyslania_odwolania" class="block text-sm font-medium text-gray-700">DATA WYSŁANIA ODWOŁANIA</label>
                                    <input type="date" id="odp_data_wyslania_odwolania" class="mt-1 w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 no-uppercase">
                                </div>
                            </div>"""

if search_html not in content:
    print("Error: HTML insertion point not found")
else:
    content = content.replace(search_html, replace_html)

# 2. JS modification: Add new fields to odpowiedzFields
search_js_fields = """            data_orzeczenia: document.getElementById('odp_data_orzeczenia'),
            data_prawomocnosci: document.getElementById('odp_data_prawomocnosci'),
            podstawa_prawna: document.getElementById('odp_podstawa_prawna'),"""

replace_js_fields = """            data_orzeczenia: document.getElementById('odp_data_orzeczenia'),
            data_prawomocnosci: document.getElementById('odp_data_prawomocnosci'),
            odwolanie: document.getElementById('odp_odwolanie'), // Checkbox
            data_odwolania: document.getElementById('odp_data_odwolania'),
            data_wyslania_odwolania: document.getElementById('odp_data_wyslania_odwolania'),
            podstawa_prawna: document.getElementById('odp_podstawa_prawna'),"""

if search_js_fields not in content:
    print("Error: JS fields insertion point not found")
else:
    content = content.replace(search_js_fields, replace_js_fields)

# 3. JS modification: Add event listener
search_js_listeners = """            if(odpowiedzFields.kod_pocztowy) odpowiedzFields.kod_pocztowy.addEventListener('input', handleOdpowiedzPostalCodeInput);"""

replace_js_listeners = """            if(odpowiedzFields.kod_pocztowy) odpowiedzFields.kod_pocztowy.addEventListener('input', handleOdpowiedzPostalCodeInput);

            // Listener dla checkboxa odwołania
            if (odpowiedzFields.odwolanie) {
                odpowiedzFields.odwolanie.addEventListener('change', function() {
                    if (this.checked) {
                        odpowiedzFields.data_prawomocnosci.value = '';
                        odpowiedzFields.data_prawomocnosci.disabled = true;
                        odpowiedzFields.data_prawomocnosci.classList.add('bg-gray-100');
                    } else {
                        odpowiedzFields.data_prawomocnosci.disabled = false;
                        odpowiedzFields.data_prawomocnosci.classList.remove('bg-gray-100');
                    }
                });
            }"""

if search_js_listeners not in content:
    print("Error: JS listeners insertion point not found")
else:
    content = content.replace(search_js_listeners, replace_js_listeners)

# 4. JS modification: Update handleGenerateOdpowiedzPdf logic
# Part A: Logic for content array
# I will use a larger block replacement to modify the content array construction
# First, let's locate the 'jest prawomocne' part in content.

search_pdf_content_1 = """                            ' (PESEL: ',
                            { text: data.ODP_PESEL || '________________' },
                            ') jest prawomocne, zgodnie z ',"""

replace_pdf_content_1 = """                            ' (PESEL: ',
                            { text: data.ODP_PESEL || '________________' },
                            ') ' + (odpowiedzFields.odwolanie.checked ? 'nie jest prawomocne' : 'jest prawomocne') + ', zgodnie z ',"""

# AND the second occurrence
search_pdf_content_2 = """                            ', Powiatowy Zespół ds. Orzekania o Niepełnosprawności w Nowym Dworze Mazowieckim informuje, iż orzeczenie wydane dla ',
                            { text: `${data.ODP_PANI_PANA} ${data.ODP_OSOBY}` },
                            ' jest prawomocne.'"""

replace_pdf_content_2 = """                            ', Powiatowy Zespół ds. Orzekania o Niepełnosprawności w Nowym Dworze Mazowieckim informuje, iż orzeczenie wydane dla ',
                            { text: `${data.ODP_PANI_PANA} ${data.ODP_OSOBY}` },
                            (odpowiedzFields.odwolanie.checked ? ' nie jest prawomocne.' : ' jest prawomocne.')"""

# Part B: Last paragraph replacement
search_pdf_last_para = """                    // Główna treść odpowiedzi - Akapit 2
                    {
                        text: [
                            { text: '              ', preserveLeadingSpaces: true }, // Wcięcie
                            'Orzeczenie o ',
                            { text: data.ODP_STOPIEN_CZY_NIEPELNOSPRAWNOSC || '________________' },
                            ' nr ',
                            { text: data.ODP_NUMER_ORZECZENIA || '________________' },
                            ' z dnia ',
                            { text: `${data.ODP_DATA_ORZECZENIA} r.` },
                            ' stało się prawomocne w dniu ',
                            { text: `${data.ODP_DATA_PRAWOMOCNOSCI} r.` },
                            '.'
                        ],
                        style: 'justifiedText',
                        marginBottom: 20
                    },"""

replace_pdf_last_para = """                    // Główna treść odpowiedzi - Akapit 2
                    {
                        text: odpowiedzFields.odwolanie.checked ?
                        [
                            { text: '              ', preserveLeadingSpaces: true }, // Wcięcie
                            'W dniu ',
                            { text: formatDateDDMMYYYY(odpowiedzFields.data_odwolania.value) },
                            ' zostało złożone odwołanie od wydanego orzeczenia o niepełnosprawności nr ',
                            { text: data.ODP_NUMER_ORZECZENIA || '________________' },
                            ' z dnia ',
                            { text: `${data.ODP_DATA_ORZECZENIA} r.` },
                            ', które w dniu ',
                            { text: `${formatDateDDMMYYYY(odpowiedzFields.data_wyslania_odwolania.value)} r.` },
                            ' zostało przekazane do Wojewódzkiego Zespołu ds. Orzekania o Niepełnosprawności w Warszawie.'
                        ] :
                        [
                            { text: '              ', preserveLeadingSpaces: true }, // Wcięcie
                            'Orzeczenie o ',
                            { text: data.ODP_STOPIEN_CZY_NIEPELNOSPRAWNOSC || '________________' },
                            ' nr ',
                            { text: data.ODP_NUMER_ORZECZENIA || '________________' },
                            ' z dnia ',
                            { text: `${data.ODP_DATA_ORZECZENIA} r.` },
                            ' stało się prawomocne w dniu ',
                            { text: `${data.ODP_DATA_PRAWOMOCNOSCI} r.` },
                            '.'
                        ],
                        style: 'justifiedText',
                        marginBottom: 20
                    },"""

if search_pdf_content_1 not in content:
    print("Error: PDF Content 1 insertion point not found")
else:
    content = content.replace(search_pdf_content_1, replace_pdf_content_1)

if search_pdf_content_2 not in content:
    print("Error: PDF Content 2 insertion point not found")
else:
    content = content.replace(search_pdf_content_2, replace_pdf_content_2)

if search_pdf_last_para not in content:
    print("Error: PDF Last Para insertion point not found")
else:
    content = content.replace(search_pdf_last_para, replace_pdf_last_para)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Modifications applied.")

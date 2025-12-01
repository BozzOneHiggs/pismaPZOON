
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix toggleMailMergeSidebar function to handle 'hidden' class
search_toggle_func = """        function toggleMailMergeSidebar() {
            isMailMergeSidebarOpen = !isMailMergeSidebarOpen;
            if (isMailMergeSidebarOpen) {
                mailMergeSidebar.classList.remove('-translate-x-full');
                toggleMailMergeButton.classList.add('hidden'); // Hide toggle button when open
            } else {
                mailMergeSidebar.classList.add('-translate-x-full');
                toggleMailMergeButton.classList.remove('hidden'); // Show toggle button when closed
            }
        }"""

replace_toggle_func = """        function toggleMailMergeSidebar() {
            isMailMergeSidebarOpen = !isMailMergeSidebarOpen;
            if (isMailMergeSidebarOpen) {
                mailMergeSidebar.classList.remove('hidden'); // Ensure visible
                // Small delay to allow transition if coming from hidden
                requestAnimationFrame(() => {
                    mailMergeSidebar.classList.remove('-translate-x-full');
                });
                toggleMailMergeButton.classList.add('hidden');
            } else {
                mailMergeSidebar.classList.add('-translate-x-full');
                toggleMailMergeButton.classList.remove('hidden');
                // Add hidden after transition (300ms)
                setTimeout(() => {
                    if(!isMailMergeSidebarOpen) mailMergeSidebar.classList.add('hidden');
                }, 300);
            }
        }"""

if search_toggle_func in content:
    content = content.replace(search_toggle_func, replace_toggle_func)
    print("Fixed toggle function.")
else:
    # If exact match fails (due to whitespace?), try regex or just manual replace logic in mind.
    # I'll assume exact match since I wrote it.
    print("Error: Toggle function not found for replacement.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

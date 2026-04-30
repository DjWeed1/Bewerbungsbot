document.addEventListener('DOMContentLoaded', () => {
    // Config Form
    const configForm = document.getElementById('configForm');
    configForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const sendReal = document.getElementById('sendReal').checked ? 'True' : 'False';

        const btn = configForm.querySelector('button');
        const oldText = btn.innerText;
        btn.innerText = 'Speichere...';

        try {
            const res = await fetch('/api/save_config', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, send_real: sendReal })
            });
            const data = await res.json();
            btn.innerText = data.message;
            if (data.status === 'success') {
                btn.classList.replace('bg-gray-700', 'bg-green-600');
            }
        } catch (error) {
            btn.innerText = 'Fehler beim Speichern';
        }

        setTimeout(() => {
            btn.innerText = oldText;
            btn.classList.replace('bg-green-600', 'bg-gray-700');
        }, 3000);
    });

    // File Upload Setup Function
    function setupDropZone(dropZoneId, inputId, statusId, uploadUrl, fieldName, multiple = false) {
        const dropZone = document.getElementById(dropZoneId);
        const input = document.getElementById(inputId);
        const status = document.getElementById(statusId);

        dropZone.addEventListener('click', () => input.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                handleFiles(e.dataTransfer.files);
            }
        });

        input.addEventListener('change', () => {
            if (input.files.length) {
                handleFiles(input.files);
            }
        });

        async function handleFiles(files) {
            const formData = new FormData();
            if (multiple) {
                for (let i = 0; i < files.length; i++) {
                    formData.append(fieldName, files[i]);
                }
            } else {
                formData.append(fieldName, files[0]);
            }

            dropZone.innerHTML = '<i class="fas fa-spinner fa-spin text-3xl text-brand-500 mb-3"></i><p class="text-sm">Lade hoch...</p>';
            
            try {
                const res = await fetch(uploadUrl, {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();
                
                status.classList.remove('hidden', 'text-red-400', 'text-green-400');
                if (data.status === 'success') {
                    status.classList.add('text-green-400');
                    status.innerHTML = `<i class="fas fa-check-circle"></i> ${data.message}`;
                    if (multiple) {
                        dropZone.innerHTML = '<i class="fas fa-file-code text-3xl text-green-500 mb-3"></i><p class="text-sm font-medium">Weitere HTML Anzeigen hinzufügen</p>';
                    } else {
                        dropZone.innerHTML = '<i class="fas fa-file-pdf text-3xl text-green-500 mb-3"></i><p class="text-sm font-medium">Lebenslauf gespeichert</p><p class="text-xs text-gray-500 mt-1">Klicken zum Ändern</p>';
                    }
                } else {
                    status.classList.add('text-red-400');
                    status.innerText = data.message;
                    resetDropZone();
                }
            } catch (err) {
                status.classList.remove('hidden');
                status.classList.add('text-red-400');
                status.innerText = 'Upload fehlgeschlagen';
                resetDropZone();
            }
        }

        function resetDropZone() {
            if (multiple) {
                dropZone.innerHTML = '<i class="fas fa-file-code text-3xl text-gray-500 mb-3"></i><p class="text-sm font-medium">HTML Anzeigen hier ablegen oder klicken</p>';
            } else {
                dropZone.innerHTML = '<i class="fas fa-cloud-upload-alt text-3xl text-gray-500 mb-3"></i><p class="text-sm font-medium">PDF hier ablegen oder klicken</p>';
            }
        }
    }

    setupDropZone('cvDropZone', 'cvInput', 'cvStatus', '/api/upload_cv', 'file', false);
    setupDropZone('anzeigenDropZone', 'anzeigenInput', 'anzeigenStatus', '/api/upload_anzeigen', 'files[]', true);

    // Clear Anzeigen
    document.getElementById('clearAnzeigenBtn').addEventListener('click', async () => {
        if(confirm('Wirklich alle gespeicherten HTML-Anzeigen löschen?')) {
            const res = await fetch('/api/clear_anzeigen', { method: 'POST' });
            const data = await res.json();
            const status = document.getElementById('anzeigenStatus');
            status.classList.remove('hidden', 'text-red-400', 'text-green-400');
            status.classList.add(data.status === 'success' ? 'text-green-400' : 'text-red-400');
            status.innerText = data.message;
            setTimeout(() => status.classList.add('hidden'), 3000);
        }
    });

    // Bot Execution
    const startBotBtn = document.getElementById('startBotBtn');
    const consoleOutput = document.getElementById('consoleOutput');
    const botStatusBadge = document.getElementById('botStatusBadge');
    let eventSource = null;

    startBotBtn.addEventListener('click', async () => {
        startBotBtn.disabled = true;
        startBotBtn.classList.add('opacity-50', 'cursor-not-allowed');
        startBotBtn.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Bot läuft...';
        
        botStatusBadge.innerText = 'Läuft';
        botStatusBadge.classList.replace('bg-gray-700', 'bg-brand-600');
        botStatusBadge.classList.replace('text-gray-300', 'text-white');
        
        consoleOutput.innerHTML += '\n--- Starte Bot ---\n';
        
        try {
            const res = await fetch('/api/start_bot', { method: 'POST' });
            const data = await res.json();
            
            if (data.status === 'success') {
                if (eventSource) eventSource.close();
                eventSource = new EventSource('/api/stream_logs');
                
                eventSource.onmessage = (e) => {
                    consoleOutput.innerHTML += e.data + '\n';
                    consoleOutput.scrollTop = consoleOutput.scrollHeight;
                };
                
                eventSource.addEventListener('end', () => {
                    eventSource.close();
                    finishBot();
                });
                
                eventSource.onerror = () => {
                    eventSource.close();
                    finishBot();
                };
            } else {
                consoleOutput.innerHTML += `\nFehler: ${data.message}\n`;
                finishBot();
            }
        } catch (e) {
            consoleOutput.innerHTML += `\nNetzwerkfehler: ${e.message}\n`;
            finishBot();
        }
    });

    function finishBot() {
        startBotBtn.disabled = false;
        startBotBtn.classList.remove('opacity-50', 'cursor-not-allowed');
        startBotBtn.innerHTML = '<i class="fas fa-rocket"></i> Bewerbungsbot Starten';
        
        botStatusBadge.innerText = 'Fertig';
        botStatusBadge.classList.replace('bg-brand-600', 'bg-green-600');
        setTimeout(() => {
            botStatusBadge.innerText = 'Bereit';
            botStatusBadge.classList.replace('bg-green-600', 'bg-gray-700');
            botStatusBadge.classList.replace('text-white', 'text-gray-300');
        }, 5000);
    }
});

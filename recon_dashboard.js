// Dashboard Logic for BB Portal

document.addEventListener('DOMContentLoaded', () => {
    const terminal = document.getElementById('terminalOutput');
    const startBtn = document.getElementById('startScanBtn');

    function logToTerminal(message, type = 'info') {
        const line = document.createElement('div');
        line.className = 'terminal-line';
        
        let prefix = '<span class="prompt">guest@bbportal:~$</span> ';
        if (type === 'success') message = `<span style="color: #27c93f;">[+] ${message}</span>`;
        if (type === 'error') message = `<span style="color: #ff5f56;">[!] ${message}</span>`;
        if (type === 'tool') message = `<span style="color: #00f2ff;">[>] ${message}</span>`;

        line.innerHTML = `${prefix}${message}`;
        terminal.appendChild(line);
        terminal.scrollTop = terminal.scrollHeight;
    }

    async function runRecon(domain) {
        const tools = ['subfinder', 'assetfinder', 'amass', 'dnsx', 'naabu', 'httpx', 'katana'];
        let results = {
            subdomains: [],
            liveHosts: 0,
            ports: 0
        };

        for (const tool of tools) {
            logToTerminal(`Running ${tool} on ${domain}...`, 'info');
            try {
                const response = await fetch(`/api/tools/run?tool=${tool}&target=${domain}`);
                const data = await response.json();
                
                if (data.status === 'success') {
                    logToTerminal(`${tool} completed successfully.`, 'success');
                    const lines = data.output.split('\n').filter(l => l.trim());
                    if (tool === 'subfinder' || tool === 'assetfinder' || tool === 'amass') {
                        results.subdomains = [...new Set([...results.subdomains, ...lines])];
                    }
                    if (tool === 'httpx') results.liveHosts = lines.length;
                    if (tool === 'naabu') results.ports = lines.length;
                    
                    updateStats(results);
                } else {
                    logToTerminal(`Error in ${tool}: ${data.error || 'Unknown error'}`, 'error');
                }
            } catch (err) {
                logToTerminal(`Failed to communicate with backend: ${err.message}`, 'error');
            }
        }
        
        logToTerminal(`Full Reconnaissance for ${domain} finished.`, 'success');
    }

    function updateStats(data) {
        document.getElementById('totalSubdomains').textContent = data.subdomains.length;
        document.getElementById('liveHosts').textContent = data.liveHosts;
        document.getElementById('openPorts').textContent = data.ports;
        
        const tableBody = document.getElementById('assetTableBody');
        tableBody.innerHTML = '';
        data.subdomains.slice(0, 10).forEach(sub => {
            const row = `<tr>
                <td>${sub}</td>
                <td>Searching...</td>
                <td><span class="status-badge status-active">Discovered</span></td>
                <td>Unknown</td>
            </tr>`;
            tableBody.innerHTML += row;
        });
    }

    startBtn.addEventListener('click', () => {
        const domain = prompt("Enter target domain (e.g., example.com):");
        if (domain) {
            logToTerminal(`Starting reconnaissance on ${domain}...`, 'tool');
            runRecon(domain);
        }
    });
});

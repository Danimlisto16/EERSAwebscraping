fetch('power_cuts.json')
    .then(response => response.json())
    .then(data => {
        const table = document.getElementById('appointments');
        const headers = ['Date', 'Time Range', 'Recipient'];
        
        // Create table header
        const headerRow = table.createTHead().insertRow();
        headers.forEach(headerText => {
            const th = document.createElement('th');
            th.textContent = headerText;
            headerRow.appendChild(th);
        });

        // Create table body
        const tbody = table.createTBody();
        data.forEach(appointment => {
            const row = tbody.insertRow();
            Object.values(appointment).forEach(value => {
                const cell = row.insertCell();
                cell.textContent = value;
            });
        });
    });

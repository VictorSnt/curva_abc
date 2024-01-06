document.addEventListener('DOMContentLoaded', function () {
            
    const rows = document.querySelectorAll('tr');
   

    const selectedRows = [];

   
    function toggleSelection(row) {
        row.classList.toggle('selected');
    }

    
    function handleRowClick(event) {
        const row = event.target.closest('tr');
        toggleSelection(row);
        
    }

   
    function sendSelectedData() {
        const selectedData = [];

        rows.forEach((row) => {
            if (row.classList.contains('selected')) {
                const rowData = `${row.cells[1].textContent}: ${parseFloat(row.cells[2].textContent) - parseFloat(row.cells[4].textContent.trim())}und`;
                selectedData.push(rowData);
            }
        });

        const content = selectedData.join('\n');
        const blob = new Blob([content], { type: 'plain/text' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'dados_selecionados.txt'; 
        link.click();
        URL.revokeObjectURL(link.href);
    }


    
    rows.forEach((row) => {
        row.addEventListener('click', handleRowClick);
    });

    document.getElementById('sendDataButton').addEventListener('click', sendSelectedData);
});
document.addEventListener('DOMContentLoaded', function () {
    
    const modalOverlay = document.getElementById('modalOverlay');
    const productModal = document.getElementById('productModal');
    const modalBody = document.getElementById('productModalBody');

    function toggleSelection(row) {
        const cdprincipal = row.cells[0].innerText;
        const requestUrl = `http://localhost:7450/similares/${cdprincipal}`;

        fetch(requestUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Erro na requisição: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                openModal(data, row);
            })
            .catch(error => {
                console.error('Erro durante a requisição:', error);
            });
    }

    function sendSelectedData() {
        const selectedData = [];
        const rows = document.querySelectorAll('tr.selected');
        
        rows.forEach(row => {
            const rowData = `${row.cells[1].innerText}: ${
                parseFloat(row.cells[2].innerText) - 
                parseFloat(row.cells[4].innerText.trim())}und`;
            selectedData.push(rowData);
        });

        const content = selectedData.join('\r\n');
        const blob = new Blob([content], { type: 'plain/text' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'dados_selecionados.txt'; 
        link.click();
        URL.revokeObjectURL(link.href);
    }

    function openModal(data, targetRow) {
        modalBody.innerHTML = '';

        data.forEach(element => {
            let row = document.createElement('tr');
            let [cell1, cell2] = [document.createElement('td'), document.createElement('td')];

            cell1.innerText = element.dsdetalhe;
            cell2.innerText = element.qtestoque;

            row.appendChild(cell1);
            row.appendChild(cell2);

            modalBody.appendChild(row);
        });

        let rowQuestion = document.createElement('tr');
        let cellQuestion = document.createElement('td');
        cellQuestion.setAttribute('colspan', '2');
        cellQuestion.innerText = 'Deseja selecionar?';
        rowQuestion.appendChild(cellQuestion);
        modalBody.appendChild(rowQuestion);

        let rowButtons = document.createElement('tr');
        let cellButtonContainer = document.createElement('td');
        cellButtonContainer.setAttribute('colspan', '2'); 
        
        let [buttonYes, buttonNo] = [document.createElement('button'), document.createElement('button')];

        buttonYes.innerText = 'Sim';
        buttonYes.addEventListener('click',  function() {
            targetRow.classList.toggle('selected');
            closeModal();
        });
        
        buttonNo.innerText = 'Não';
        buttonNo.addEventListener('click',  function() {
            closeModal(); 
        });

        buttonYes.classList.add('modal-button', 'modal-button-yes');
        buttonNo.classList.add('modal-button', 'modal-button-no');

        cellButtonContainer.appendChild(buttonYes);
        cellButtonContainer.appendChild(buttonNo);
        rowButtons.appendChild(cellButtonContainer);
        modalBody.appendChild(rowButtons);

        modalOverlay.style.display = 'block';
        productModal.style.display = 'block';
    }

    function closeModal() {
        modalOverlay.style.display = 'none';
        productModal.style.display = 'none';
    }

    function handleRowClick(event) {
        const row = event.target.closest('tr');
        toggleSelection(row);
    }  

    
    document.addEventListener('click', function(event) {
        if (event.target.closest('tr')) {
            handleRowClick(event);
        }
    });

    document.getElementById('sendDataButton').addEventListener('click', sendSelectedData);
    document.getElementById('close-modal').addEventListener('click', closeModal);
});

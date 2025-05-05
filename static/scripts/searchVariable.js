function searchVariable(){
    let description = document.getElementById('search-term').value;
    if(!description) return;
    fetch('http://127.0.0.1:5000/variables/search?description=' + description.replaceAll(' ', '%20') + '&size=20')
    .then(e => e.json())
    .then( data => {

        // If empty, display "No results"
        let resultsDiv = document.getElementById('results-container')
        if(Object.keys(data).length === 0) {
            let noResult = document.createElement('div')
            noResult.className = 'search-placeholder'
            noResult.innerText = 'No results found'
            resultsDiv.appendChild(noResult)
            return
        }
        resultsDiv.getElementsByTagName('div')[0]?.remove()

        // Clean current results
        let resultsList = document.getElementById('results')
        let currentResults = resultsList.getElementsByTagName('tr')
        while(currentResults.length > 1){
            currentResults[1].remove()
        }

        // Append received results
        for (let i = 0; i < data.length; i++){
            let curVariable = data[i]
            let variable = curVariable[0];
            let description = curVariable[1];

            let newRow = document.createElement('tr')
            newRow.className = 'variables-table-row'

            let varNameField = document.createElement('td')
            varNameField.innerText = variable;
            varNameField.className = 'variables-table-cell'
            let varDescriptionField = document.createElement('td')
            varDescriptionField.innerText = description;
            varDescriptionField.className = 'variables-table-cell'

            newRow.appendChild(varNameField)
            newRow.appendChild(varDescriptionField)

            resultsList.appendChild(newRow);
        }

    })
}

// Lister for enter key 
if(window.location.href.endsWith('variables')){
    document.getElementById('search-term')
    .addEventListener('keydown', (e) => {
        if(e.key === 'Enter') searchVariable()
    })   
}
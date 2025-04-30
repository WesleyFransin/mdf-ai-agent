let chatHistory = []

const sendChat = (promptMessage) => {

    let messageHistory = document.getElementById('history');
    // Add on chat window
    let newMsg = document.createElement('div');
    newMsg.className = 'message user-message';
    newMsg.innerText = promptMessage;
    
    messageHistory.appendChild(newMsg);
    messageHistory.scrollTo(0, messageHistory.scrollHeight);
    
    // Send to API
    let newResponse = document.createElement('div');
    newResponse.className = 'message system-message loading';

    messageHistory.appendChild(newResponse);
    messageHistory.scrollTo(0, messageHistory.scrollHeight);

    fetch('http://127.0.0.1:5000/send-message', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            history: chatHistory,
            message: promptMessage
        }),
    })
    .then((r) => r.json())
    .then((r) => {
        newResponse.className = 'message system-message';
        newResponse.innerText = r.response;
        // messageHistory.appendChild(newResponse);
        messageHistory.scrollTo(0, messageHistory.scrollHeight);
        chatHistory.push('<Human>: ' + promptMessage);
        chatHistory.push('<Assistant>: ' + r.response);
    })
    
   

}

const inputKeyDown = (e) => {
    if(e.keyCode != 13) return
    sendChat(e.target.value);
    e.target.value = '';
}

document.getElementsByName('prompt-input')[0]?.addEventListener('keydown', inputKeyDown)

const handleSendButton = () => {
    let inputArea = document.getElementById('prompt-input');
    sendChat(inputArea.value);
    inputArea.value = '';
}
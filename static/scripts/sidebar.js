function handleSidebarNavigation(e) {
    let destination = e.srcElement.innerText.toLowerCase();
    if(destination === 'chat'){
        destination = ''
    }

    let curLocation = window.location.pathname.slice(1);
    if(curLocation != destination){
        window.location.href = window.location.origin + '/' + destination;
    }

} 

let sidebarButtons = document.getElementsByClassName('sidebar-item')
for (let i = 0; i < sidebarButtons.length; i++) {
    const bt = sidebarButtons[i];
    let btText = bt.innerText.toLowerCase();
    if(btText === 'chat') btText = ''

    let curLocation = window.location.pathname.slice(1);
    if(curLocation === btText) bt.classList.add('active-sidebar-button')
}
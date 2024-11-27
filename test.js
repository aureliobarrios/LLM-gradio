function createGradio() {
    var linksContainer = document.createElement('div');
    container.id = 'links-container';

    const linksData = [
        { text: "Link 1", url: "https://example.com/1" },
        { text: "Link 2", url: "https://example.com/2" },
        { text: "Link 3", url: "https://example.com/3" },
        { text: "Link 4", url: "https://example.com/4" },
        { text: "Link 5", url: "https://example.com/5" },
        { text: "Link 6", url: "https://example.com/6" },
        { text: "Link 7", url: "https://example.com/7" },
        { text: "Link 8", url: "https://example.com/8" },
        { text: "Link 9", url: "https://example.com/9" },
        { text: "Link 10", url: "https://example.com/10" }
    ];

    const visibleLinks = 5; // Number of rows to display
    let currentIndex = 0;

    function renderLinks() {
        linksContainer.innerHTML = '';
        for (let i = 0; i < visibleLinks && currentIndex + i < linksData.length; i++) {
            const linkData = linksData[currentIndex + i];
            const row = document.createElement('div');
            row.className = 'link-row';

            const link = document.createElement('a');
            link.href = linkData.url;
            link.textContent = linkData.url;
            link.target = '_blank';
            row.appendChild(link);

            const checkButton = document.createElement('button');
            checkButton.textContent = '✔';
            checkButton.onclick = () => {
                link.classList.add('green');
            };
            row.appendChild(checkButton);

            const xButton = document.createElement('button');
            xButton.textContent = '✖';
            xButton.onclick = () => {
                // Remove the link and add the next one
                if (currentIndex + visibleLinks < linksData.length) {
                    currentIndex++;
                }
                renderLinks();
            };
            row.appendChild(xButton);

            linksContainer.appendChild(row);
        }
    }

    renderLinks();

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(linksContainer, gradioContainer.firstChild);
}
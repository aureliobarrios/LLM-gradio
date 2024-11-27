import gradio as gr

css = """
body {
    font-family: Arial, sans-serif;
    margin: 20px;
}
.link-row {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}
.link-row a {
    margin-right: 10px;
    text-decoration: none;
    color: black;
}
.link-row a.green {
    color: green;
}
button {
    margin-right: 5px;
}
"""

js = """
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
"""

demo = gr.Blocks(js=js, css=css)

with demo:
    inp = gr.Textbox(placeholder="Enter text.")
    scroll_btn = gr.Button("Scroll")
    no_scroll_btn = gr.Button("No Scroll")
    big_block = gr.HTML("""
    <div id="container" style='height: 800px; width: 100px; background-color: pink;'></div>
    """)
    out = gr.Textbox()

    scroll_btn.click(lambda x: x,
               inputs=inp,
               outputs=out,
                scroll_to_output=True)
    no_scroll_btn.click(lambda x: x,
               inputs=inp,
               outputs=out)

if __name__ == "__main__":
    demo.launch()
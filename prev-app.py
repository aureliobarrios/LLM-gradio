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
    linksContainer.id = 'links-container';

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

            //add style
            row.style.display = 'flex';
            row.style.alignItems = 'center';
            row.style.marginBottom = '10px';

            const link = document.createElement('a');
            
            //add style
            link.style.marginRight = '10px';
            link.style.textDecoration = 'none';
            link.style.color = 'black';
            
            link.href = linkData.url;
            link.textContent = linkData.url;
            link.target = '_blank';
            row.appendChild(link);

            const checkButton = document.createElement('button');
            checkButton.textContent = '✔';
            checkButton.onclick = () => {
                link.style.color = "green";
            };
            row.appendChild(checkButton);

            const xButton = document.createElement('button');
            xButton.textContent = '✖';
            xButton.onclick = () => {
                // Remove the link and add the next one
                if (currentIndex + visibleLinks < linksData.length) {
                    //update
                    linksData.splice(i, 1);
                    //currentIndex++;
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

with gr.Blocks(js=js) as demo:
    # ---------- Components ----------

    #build selection section
    radio = gr.Radio(
        ["Tutorial", "Videos", "Documentation"],
        value="Videos",
        label="What kind of resources would you like to receive?"
    )
    #build chatbot interface
    chatbot = gr.Chatbot(value=[
        {"role": "assistant", "content": "Hello, how can I assist you today?"}
    ], type="messages")
    #build textbot for message input
    msg = gr.Textbox()

    #build button row section
    with gr.Row():
        clear_button = gr.Button("Clear")
        submit_button = gr.Button("Submit")

    #create output textbox
    output = gr.Textbox(label="Learning Path")

    # ---------- Functions ----------

    #function to receive user input
    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]
    
    #function to return bot output
    def bot(history, radio):
        bot_message = "You typed: " + history[-1]["content"] +  ", and selected: " + radio
        history.append({"role": "assistant", "content": bot_message})
        return history
    
    #function to return to output text
    def learning(history):
        return "Built learning path for: " + history[-1]["content"]
    
    # ---------- Actions ----------

    #handle user submit
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    )

    #handle user click on clear button
    clear_button.click(
        lambda: None, None, chatbot, queue=False
    ).then(
        lambda: None, None, output
    )

    #handle user click on submit button
    submit_button.click(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    ).then(
        learning, chatbot, output
    )

if __name__ == "__main__":
    demo.launch()
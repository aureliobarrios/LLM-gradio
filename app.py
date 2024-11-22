import gradio as gr

with open("index.html", "r") as file:
    html_content = file.read()

with gr.Blocks() as demo:
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

    block = gr.HTML(f"""<iframe srcdoc='{html_content}'></iframe> """)

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
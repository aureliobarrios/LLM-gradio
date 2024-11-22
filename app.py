import gradio as gr

with gr.Blocks() as demo:
    #build selection section
    radio = gr.Radio(
        ["Tutorial", "Videos", "Documentation"],
        label="What kind of resources would you like to receive?"
    )
    #build chatbot interface
    chatbot = gr.Chatbot()
    #build textbot for message input
    msg = gr.Textbox()

    #function to receive user input
    def user(user_message, history):
        return "", history + [[user_message, None]]
    
    #function to return bot output
    def bot(history, radio):
        bot_message = "You typed: " + history[-1][0] +  ", and selected: " + radio
        history[-1][1] = bot_message
        return history

    #build button row section
    with gr.Row():
        clear_button = gr.Button("Clear")
        submit_button = gr.Button("Submit")

    #handle user submit
    msg.submit(
        user, inputs=[msg, chatbot], outputs=[msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    )

    #handle user click on clear button
    clear_button.click(
        lambda: None, None, chatbot, queue=False
    )

    #handle user click on submit button
    submit_button.click(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    )

if __name__ == "__main__":
    demo.launch()
import gradio as gr

with gr.Blocks() as demo:    
    # ---------- Components ----------

    #add build type component
    build_type = gr.Radio(
        ["Learning Path", "Tutorial"],
        label="What do you wish to build today?"
    )

    #add learning path topic textbox
    topic = gr.Textbox(visible=False)

    #add difficulty selection component
    difficulty = gr.Radio(visible=False)
    

    #build selection section
    radio = gr.Radio(
        ["Web Results", "Videos"],
        value="Web Results",
        label="What kind of resources would you like to receive?"
    )
    #build chatbot interface

    message = """Hello, I am your chatbot assistant tasked with building a learning path for you!.
    \nPlease enter what you wish to learn below!
    """

    chatbot = gr.Chatbot(value=[
        {"role": "assistant", "content": message}
    ], type="messages")
    #build textbot for message input
    msg = gr.Textbox(placeholder="Insert what you wish to learn here")

    #build button row section
    with gr.Row():
        clear_button = gr.Button("Clear")
        submit_button = gr.Button("Build Path")

    # ---------- Functions ----------

    #function to receive user input
    def user(user_message, history):
        return "", history + [{"role": "user", "content": user_message}]
    
    #function to return bot output
    def bot(history, radio):
        #add streaming functionaility
        history.append({"role": "assistant", "content": "testing"})
        return history
    
    def clear_handle(history):
        #clear chatbot history
        history = []
        #add initial chat prompt
        history.append({"role": "assistant", "content": message})
        return history
    
    #functions to display file saving information
    def learning_path_info():
        trial_name = "TEST"
        display_message = f"Learning Path Context Saved To: ./gradio-tests/{trial_name}.txt"
        gr.Info(display_message, duration=1)

    def extracted_content_info():
        trial_name = "TEST"
        display_message = f"Extracted Content Saved To: ./gradio-tests/content_{trial_name}.txt"
        gr.Info(display_message, duration=1)

    def query_info():
        trial_name = "TEST"
        display_message = f"Query Information Saved To: ./gradio-tests/queries_{trial_name}.txt"
        gr.Info(display_message, duration=1)

    #function to change display of dropdowns
    def change_display(build_type, difficulty):
        #change layout if student picks learning path builder
        if build_type == "Learning Path":
            #build topic textbox selection
            topic = gr.Textbox(
                label="What topic would you like you build your learning path for? i.e. Python, JavaScript, etc...",
                placeholder="Insert your learning topic here",
                interactive=True,
                visible=True
            )
            #build difficulty level selection
            difficulty = gr.Radio(
                ["Beginner", "Intermediate", "Hard", "Advanced"],
                value="Beginner",
                label="What would you say your current expertise level on the subject is at?",
                visible=True
            )
        else:
            #reset layout
            difficulty = gr.Radio(visible=False)
            topic = gr.Textbox(visible=False, value='')
        return difficulty, topic
    
    # ---------- Actions ----------
    build_type.select(
        change_display, [build_type, difficulty], [difficulty, topic], queue=False
    )

    #handle user submit
    msg.submit(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    ).then(
        learning_path_info, None, None
    ).then(
        extracted_content_info, None, None
    ).then(
        query_info, None, None
    )

    #handle user click on clear button
    clear_button.click(
        clear_handle, chatbot, chatbot, queue=False
    )

    #handle user click on submit button
    submit_button.click(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, [chatbot, radio], chatbot
    ).then(
        learning_path_info, None, None
    ).then(
        extracted_content_info, None, None
    ).then(
        query_info, None, None
    )

if __name__ == "__main__":
    demo.launch(show_error=True)
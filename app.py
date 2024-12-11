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

    #build selection gradio
    radio = gr.Radio(visible=False)

    #build chatbot interface
    chatbot = gr.Chatbot(type="messages")

    #build message textbox for chatbot
    msg = gr.Textbox(visible=False)

    #build button row section
    with gr.Row():
        clear_button = gr.Button("Clear", interactive=False)
        submit_button = gr.Button("Build Path", interactive=False)

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
    
    def build_layout(build_type):
        #change layout based on student selection
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
                visible=True,
                interactive=True
            )
            #build chatbot interface
            chatbot = gr.Chatbot(type="messages")
            #build textbot for message input
            msg = gr.Textbox(visible=False)
        else:
            #build topic textbox selection
            topic = gr.Textbox(visible=False, value='')
            #build difficulty level selection
            difficulty = gr.Radio(visible=False)
            #build chatbot message
            message = """Hello, I am your chatbot assistant tasked with building a learning path for you!.
            \nPlease enter what you wish to learn below!
            """
            #build chatbot interface
            chatbot = gr.Chatbot(value=[
                {"role": "assistant", "content": message}
            ], type="messages")
            #build textbox for message input
            msg = gr.Textbox(placeholder="Insert what you wish to learn here", visible=True)
        return topic, difficulty, chatbot, msg
    
    #build layout for resource type selection
    def resource_selection(radio):
        radio = gr.Radio(
            ["Web Results", "Videos"],
            value="Web Results",
            label="What kind of resources would you like to receive?",
            visible=True
        )
        return radio
    
    #build layout for button functionality
    def buttons(clear_button, submit_button):
        clear_button = gr.Button("Clear", interactive=True)
        submit_button = gr.Button("Build Path", interactive=True)
        return clear_button, submit_button
    
    # ---------- Actions ----------
    build_type.select(
        build_layout, build_type, [topic, difficulty, chatbot, msg]
    ).then(
        resource_selection, radio, radio
    ).then(
        buttons, [clear_button, submit_button], [clear_button, submit_button]
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
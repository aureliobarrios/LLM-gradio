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
    def bot(history):
        #add streaming functionaility
        history.append({"role": "assistant", "content": "testing"})
        return history
    
    def clear_handle(history):
        #clear chatbot history
        history = []
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
            #build chatbot interface
            chatbot = gr.Chatbot(type="messages")
            #build textbox for message input
            msg = gr.Textbox(
                label="What question do you want to build a tutorial for?",
                placeholder="Insert what you wish to learn here",
                visible=True
            )
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
    
    def check_input(build_type, topic, msg):
        if build_type == "Learning Path":
            #list possible learning paths
            possible_topics = ["python", "javascript"]
            #check to see if topic is note empty
            if not topic.strip():
                raise gr.Error("Make sure to include your topic!")
            if topic.lower() not in possible_topics:
                raise gr.Error("Did not recognize topic, make sure to include programming specific topics!")
        else:
            #check tutorial edge cases
            if not msg.strip():
                raise gr.Error("Make sure to input message!")

    def clear_all():
        #add build type component
        build_type = gr.Radio(
            ["Learning Path", "Tutorial"],
            label="What do you wish to build today?",
            value=None
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

        return build_type, topic, difficulty, radio, chatbot, msg, clear_button, submit_button
    
    # ---------- Actions ----------
    build_type.select(
        build_layout, build_type, [topic, difficulty, chatbot, msg]
    ).then(
        resource_selection, radio, radio
    ).then(
        buttons, [clear_button, submit_button], [clear_button, submit_button]
    )

    #handle user click on clear button
    clear_button.click(
        clear_handle, chatbot, chatbot, queue=False
    ).then(
        clear_all, None, [build_type, topic, difficulty, radio, chatbot, msg, clear_button, submit_button]
    )

    #handle user click on submit button
    submit_button.click(
        check_input, [build_type, topic, msg], None
    ).success(
        user, [msg, chatbot], [msg, chatbot]
    ).then(
        bot, chatbot, chatbot
    ).then(
        learning_path_info, None, None
    ).then(
        extracted_content_info, None, None
    ).then(
        query_info, None, None
    )

    #handle topic textbox submit
    topic.submit(
        check_input, [build_type, topic, msg], None
    )
    
    #handle user submit
    msg.submit(
        check_input, [build_type, topic, msg], None
    ).success(
        user, [msg, chatbot], [msg, chatbot], queue=False
    ).then(
        bot, chatbot, chatbot
    ).then(
        learning_path_info, None, None
    ).then(
        extracted_content_info, None, None
    ).then(
        query_info, None, None
    )

if __name__ == "__main__":
    demo.launch(show_error=True)
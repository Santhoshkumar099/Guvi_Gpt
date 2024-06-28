import gradio as gr
import mysql.connector
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import bcrypt

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("SanthoshKumar99/Guvi_LLM")
model = AutoModelForCausalLM.from_pretrained("SanthoshKumar99/Guvi_LLM")

# Database connection
db = mysql.connector.connect(
    host="",
    port=4000,
    user="",
    password="",  
    database=""
)
cursor = db.cursor()

# Create users table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)
""")
db.commit()

# Load model and tokenizer
model_name = "SanthoshKumar99/Guvi_LLM"  # Replace with your actual model name
model = GPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register(username, password):
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if cursor.fetchone():
        return False, "Username already exists"
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    db.commit()
    return True, "Registration successful"

def login(username, password):
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    if result and verify_password(password, result[0]):
        return True, "Login successful"
    return False, "Invalid username or password"

def generate_text(prompt, max_length=100, temperature=0.7):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    outputs = model.generate(
        input_ids=inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=max_length,
        temperature=temperature,
        pad_token_id=tokenizer.eos_token_id
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

with gr.Blocks() as demo:
    gr.Markdown("# Guvi GPT-2 Text Generation")
    
    logged_in = gr.State(False)
    
    with gr.Tab("Login/Register") as login_tab:
        username = gr.Textbox(label="Username")
        password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        register_btn = gr.Button("Register")
        result = gr.Textbox(label="Result")

    with gr.Tab("Text Generation", visible=False) as generation_tab:
        gr.Markdown("## Enter your prompt")
        prompt = gr.Dropdown(
            choices=["Guvi was founded by", "Guvi's mission is","Guvi is a", "Custom prompt"],
            label="Select a prompt or choose 'Custom prompt' to enter your own"
        )
        custom_prompt = gr.Textbox(label="Custom prompt", visible=False)
        max_length = gr.Slider(minimum=10, maximum=500, value=100, step=1, label="Number of words")
        temperature = gr.Slider(minimum=0.1, maximum=1.0, value=0.7, step=0.1, label="Temperature")
        generate_btn = gr.Button("Generate")
        output = gr.Textbox(label="Generated Text")

        gr.Markdown("**Disclaimer:** This app can make mistakes. Please double-check responses.")

    def login_and_update(username, password):
        success, message = login(username, password)
        if success:
            return True, message, gr.update(visible=False), gr.update(visible=True)
        else:
            return False, message, gr.update(visible=True), gr.update(visible=False)

    login_btn.click(
        login_and_update,
        inputs=[username, password],
        outputs=[logged_in, result, login_tab, generation_tab]
    )

    register_btn.click(register, inputs=[username, password], outputs=result)

    def update_custom_prompt(choice):
        return gr.update(visible=choice == "Custom prompt")

    prompt.change(update_custom_prompt, inputs=prompt, outputs=custom_prompt)

    def generate_wrapper(prompt_choice, custom_prompt, max_length, temperature):
        final_prompt = custom_prompt if prompt_choice == "Custom prompt" else prompt_choice
        return generate_text(final_prompt, max_length, temperature)

    generate_btn.click(generate_wrapper, inputs=[prompt, custom_prompt, max_length, temperature], outputs=output)

if __name__ == "__main__":
    demo.launch()

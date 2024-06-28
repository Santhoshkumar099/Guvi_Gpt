# Guvi GPT-2 Text Generation App
[APP](https://huggingface.co/spaces/SanthoshKumar99/Guvi_LLM)

This is a Gradio-based web application that provides a user interface for text generation using a fine-tuned GPT-2 model. The app includes user authentication and a text generation interface.

## Features

- User registration and login using MySQL database
- Text generation using a fine-tuned GPT-2 model
- Custom prompt input or selection from predefined prompts
- Adjustable parameters for text generation (max length and temperature)

## Prerequisites

- Python 3.7+
- MySQL database
- Hugging Face account (for deploying to Spaces)

## Installation

1. Clone this repository:
2. Install the required packages:
3. Set up your MySQL database and note down the credentials.
4. Set the following environment variables with your MySQL credentials:
- `DB_HOST`
- `DB_USER`
- `DB_PASSWORD`
- `DB_NAME`

## Usage

To run the app locally:
The app will be available at `http://localhost:7860`. If `share=True` is set, a public URL will also be provided in the console.

## Deploying to Hugging Face Spaces

1. Create a new Space on Hugging Face.
2. Choose "Gradio" as the SDK.
3. Upload your `app.py` and `requirements.txt` files to the Space.
4. In the Space settings, add the following secrets:
   - `DB_HOST`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_NAME`
5. Make sure your MySQL database is accessible from the Hugging Face Space environment.

## File Structure

- `app.py`: Main application file containing the Gradio interface and backend logic
- `requirements.txt`: List of Python dependencies
- `README.md`: This file

## Model

The app uses a fine-tuned GPT-2 model. Make sure to replace `"your-username/gpt2-guvi"` in the code with the actual path to your fine-tuned model on Hugging Face.

## Security Notes

- Ensure your MySQL database is properly secured, especially if using a public URL.
- Implement additional security measures like rate limiting or enhanced user authentication for production use.
- Be cautious with sensitive information when using public URLs.

## Disclaimer

This app can make mistakes. Please double-check the generated responses for accuracy and appropriateness.

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](https://github.com/Santhoshkumar099/Guvi_Gpt) if you want to contribute.

## License

[MIT](https://choosealicense.com/licenses/mit/)

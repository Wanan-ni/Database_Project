# Gemini API Example (Free Version)

This guide provides steps to use the Google Gemini LLM API in its free version.

## Prerequisites

- Python environment
- Google account (preferably your USC email ID)

## Setup Instructions

1. Install the required Python library:
   ```
   pip install google-genai
   ```

2. Generate an API key:
   - Visit [Google AI Studio](https://aistudio.google.com/apikey)
   - Log in with your USC email ID
   - Copy and save the generated API key in `config.json`

   **Note:** Ensure you're on the "Free of charge" plan for this example. You can upgrade later if needed.

3. Replace the API key in `config.json`

4. Run the Jupyter Notebook to experiment with the API

## Important Notes

1. The free plan has limitations, such as 15 requests per minute for the `gemini-2.0-flash` model. For more details, visit the [official documentation](https://ai.google.dev/gemini-api/docs).

2. This example uses Google's Gemini LLM, but similar documentation exists for other LLMs.

3. For a deeper understanding of the library's capabilities, refer to the [official documentation](https://github.com/googleapis/python-genai?tab=readme-ov-file). 
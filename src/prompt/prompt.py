def get_prompt(prompt_path):
    """Read and return the prompt text from a file."""
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_text = file.read()
    return prompt_text

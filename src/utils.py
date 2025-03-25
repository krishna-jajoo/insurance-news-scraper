import json
import re


def extract_and_parse_json(response):
    """
    Extracts JSON from a response and parses it.
    """
    # Extract JSON using regex (handles extra text issues)
    match = re.search(r"\{.*\}", response, re.DOTALL)
    if match:
        json_str = match.group(0).strip()  # Extract only JSON part
        try:
            return json.loads(json_str)  # Parse JSON
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: {e}\nFailed Response: {json_str}")
            return None
    else:
        print(f"Failed to extract JSON from response: {response}")
        return None


def process_responses(name_chain, inputs):
    """
    Runs the name_chain process and extracts structured JSON data.

    Args:
        name_chain: The chain execution function.
        inputs: The input for the chain.

    Returns:
        list: A list of structured JSON data.
    """
    structured_data = []

    response = name_chain.run(inputs)  # Execute chain and get response
    parsed_data = extract_and_parse_json(response)

    if parsed_data:
        structured_data.append(parsed_data)

    return structured_data

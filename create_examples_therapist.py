import json
import requests

# Define the API url and headers
url = "http://192.168.1.88:8080/completion"
headers = {
    "Content-Type": "application/json",
}

# Define other parameters
temperature = 0.6
top_k = 35
top_p = 1
stop_seq = []

# Read each line from the "version_1_therapy_patient_prompts.jsonl" file and send a request
with open("version_1_therapy_patient_prompts.jsonl", "r") as f:
    for line in f:
        # Reset the prompt for each patient
        base_prompt = "Therapist: Hello, I am going to be your therapist. Please tell me what is bothering you so that I can give you a solution or some education of dialectical behavioral therapy.\n\n\n\n\n Patient: Hello therapist, "

        # Load the JSON data from each line
        data = json.loads(line)
        text = data["text"]

        # Create the prompt for the request
        prompt = base_prompt + text + "\n\n\n\n\n Therapist:"

        # Prepare the data for the request
        request_data = {
            "prompt": prompt,
            "temperature": 1,
            "top_k": 10,
            "top_p": 0.1,
            "stop": ["Patient", "\n"],
            "n_predict": 100,
        }

        # Send the request and handle the response
        response = requests.post(url, headers=headers, json=request_data)

        # Try to parse the JSON response
        response_data = response.json()

        if "content" in response_data:
            # Extract the content from the response
            response_content = response_data["content"]

            # Save the response to a new line in the "therapist_example.jsonl" file
            with open("therapist_example.jsonl", "a") as output_file:
                output_file.write(
                    json.dumps({"instruction": prompt, "response": response_content})
                    + "\n"
                )
                

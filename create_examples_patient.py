import json
import requests

# Define API url and headers
url = "http://192.168.1.88:8080/completion"
headers = {
    "Content-Type": "application/json",
}

# Define prompt and other parameters
prompt = "###Instruction: \
    You are a therapy patient in a session with your dialectical behavior therapist. 'Therapist' refers to your dialectical behavior therapist. \
        \n###Response: Hello, I am a patient in a session with my therapist. I have borderline personality disorder, \
            and attention deficit hyperactivity disorder. I have many different and unique issues. \
                Quickly, I will tell you something that has been on my mind.\n###Instruction: Please tell me one issue you have been experiencing. \n###Response: "
temperature = 2.0
top_k = 100
top_p = 0.5
n_predict = -1



data = {
    "prompt": prompt,
    "temperature": temperature,
    "top_k": top_k,
    "top_p": top_p,
    "n_predict": n_predict,
    "stop": ["###Instruction: ", "###Response: ", "###Therapist: "],
}

while True:
    # Send request and handle the response
    response = requests.post(url, headers=headers, json=data)

    try:
        # Try to parse the JSON response
        response_data = response.json()
        
        if 'content' in response_data:
            # Extract the content from the response
            response_content = response_data["content"]
            
            # Save the response to a newline in a jsonl file
            with open("patient_example.jsonl", "a") as f:
                f.write(f"{json.dumps({'Input': response_content})}\n")  # Format response as {"Input": response_content}
        else:
            # Print the response if 'content' is not found
            print("Unexpected response structure:", response_data)
    except json.JSONDecodeError:
        # If response is not in JSON format, print the raw response
        print("Failed to decode JSON from response:", response.text)
    except KeyError as e:
        # If a KeyError occurred, print the error
        print(f"KeyError: {e} - JSON structure might have changed.")

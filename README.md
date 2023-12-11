# dbt-database

- This is where I will locate my files and tools relating to the generation and development of my Dialectical Behavior Therapy dataset.

## Local Language Model API Example

### Python completions example with streaming output

```python
import json
import requests
import sseclient # pip install sseclient-py

url = "http://192.168.1.88:5000/v1/completions"

headers = {
    "Content-Type": "application/json",
}

data = {
    "prompt": "This is an example prompt: \n\n",
    "max_tokens": 200,
    "temperature": 1,
    "top_p":0.9,
    "stream": True,
}

stream_response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
client = sseclient.SSEClient(stream_response)

print(data['prompt'], end='')
for event in client.events():
    if event.data:
        response = json.loads(event.data)
        print(response['choices'][0]['text'], end='')

print()
```

### Python completions example without streaming output

```python
import json
import requests

url = "http://192.168.1.88:5000/v1/completions"

headers = {
    "Content-Type": "application/json",
}

data = {
    "prompt": "This is an example prompt: \n\n",
    "max_tokens": 200,
    "temperature": 1,
    "top_p":0.9,
}

response = requests.post(url, headers=headers, json=data, verify=False)
print(response.json()['choices'][0]['text'])
```

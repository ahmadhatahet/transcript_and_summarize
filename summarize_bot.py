import openai
from pathlib import Path
from openai.error import RateLimitError
from time import sleep


openai.api_key = "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"

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]


# get base folder
base = Path(__file__).parent
path_text_files = base / 'text_files' / '2023-05-17_18-37'

text_corpus = []

# read all texts
for text_file in path_text_files.iterdir():

    # append to list
    text_corpus.append(text_file.read_text())



prompt = """
Summarize the following text in between ```.
At the end add some useful hashtags to tweet later.
Make sure that the summrization is at max 100 characters including the tags.

```{text}```
"""


# if text is not summarized, try after wait
done = False
wait = 60

while not done:
    try:
        # summarize text
        response = get_completion(prompt.format(text='; '.join(text_corpus)))
        print({ 'length': {len(response)},'message': {response} })

        done = True

    # if the server is overloaded wait
    except RateLimitError:
        sleep(wait) # seconds
import openai
from pathlib import Path
from openai.error import RateLimitError
from time import sleep
from log_config import init_logger
import logging
from dotenv import load_dotenv
import os

# initaite logger
init_logger()
logger = logging.getLogger('summrize')

# get base folder
base = Path(__file__).parent
path_text_files = base / 'text_files' / '2023-05-17_18-37'

# load env variables
load_dotenv(base / '.env')

# open ai api key
openai.api_key = os.environ['openai_api_key']


def get_completion(prompt, model="gpt-3.5-turbo"):
    """
    Send a request and return the response message.

    Args:
        prompt (str): the prompt text
        model (str, optional): Name of the model from Open AI. Defaults to "gpt-3.5-turbo".

    Returns:
        str: The model response.
    """
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # this is the degree of randomness of the model's output, between 0 and 2,
        # where 0 is the least random
        temperature=0.5,
    )
    return response.choices[0].message["content"]



# read all texts
text_corpus = []
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


    except KeyboardInterrupt:
        print('Failed to summarize due to overloaded server!')
        print('canceled.')
        break
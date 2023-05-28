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
summrization_folder = base / 'summarization_texts'
summrization_folder.mkdir(exist_ok=True)

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


def summarize(path_text_files, language):

    # read all texts
    text_corpus = []
    for text_file in path_text_files.iterdir():

        # append to list
        text_corpus.append(text_file.read_text(encoding="utf8"))


    prompt = """
    Summarize the following text in between ```.
    At the end add some useful hashtags to tweet later.
    Make sure that the summrization is at max 100 characters including the tags.

    ```{text}```
    """

    if language == 'Arabic':
        prompt = """لخص النص التالي بين ``.
         في النهاية ، أضف بعض التاجز المفيدة للتغريد لاحقًا.
         تأكد من أن الملخص بحد أقصى 100 حرف بما في ذلك العلامات.

        ```{text}```
        """

    # if text is not summarized, try after wait
    done = False
    wait = 60

    while not done:
        try:
            prompt = prompt.format(text='; '.join(text_corpus))

            # summarize text
            response = get_completion(prompt)

            file = summrization_folder / f'{path_text_files.name}_text.txt'
            file.touch()
            file.write_text(f"prompt: {prompt}\nsummarization: {response}", encoding="utf8")

            print({ 'length': {len(response)},'message': {response} })

            done = True

        # if the server is overloaded wait
        except RateLimitError:
            sleep(wait) # seconds


        except KeyboardInterrupt:
            print('Failed to summarize due to overloaded server!')
            print('canceled.')
            break

    return done, response
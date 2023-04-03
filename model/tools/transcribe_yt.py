import whisper
from pytube import YouTube
import openai
from time import sleep, time
import sys
import re

def split_into_chunks(text):
    """
    Splits a text into chunks of 1/3 the relative size of the text and outputs the chunks.
    Makes sure it chunks at the end of sentences too.
    *args:
        text: The text to split.
    *returns:
        A list of strings, each of which is a chunk of the text.
    """
    # Split this bad boy into sentences
    sentences = re.split('(?<=[.!?]) +', text)

    len_text = len(text)
    chunk_size = len_text // 3
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If the current_chunk and the sentence are still having a party under the chunk_size limit
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence
        else:
            # Time to move on, add the current_chunk to the chunks list and reset this sucker
            chunks.append(current_chunk)
            current_chunk = sentence

    # Don't forget the last chunk if it's still hanging around
    if current_chunk:
        chunks.append(current_chunk)

    return chunks

class YoutubeTranscript:
    @staticmethod
    def download_audio_from_youtube(url):
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        fn = yt.title + ".mp3"
        stream.download(filename=fn, output_path=".", skip_existing=True)
        return fn

    def transcribe_video(file_path, model_size="medium", prompt="", language="en", fp16=False, temperature=0, write=True):
        """ Transcribes a video file and returns the transcript.
        *args:
            file_path: Input filename of the video to transcribe.
            model_size: The size of the model to use. Options are "tiny, "small", "base", "medium", and "large".
            prompt: The prompt to use for the model.
            language: The language to use for the model.
            fp16: Whether to use fp16 for the model.
        *returns:
            The transcript of the video.
        """
        model = whisper.load_model(model_size)
        audio = whisper.load_audio(f"{file_path}")
        result = model.transcribe(audio)
        
        if write:
            #Save the transcript to a file with the same name as the audio file
            fn = file_path.split(".")[0] + ".txt"
            with open(fn, "w") as f:
                f.write(result["text"])
        return result["text"]

    def generate(self, msgs, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop="null",
                 max_tokens=350, presence_penalty=0, frequency_penalty=0, debug=False, max_retry=2):
        """
            Generates a response from the OpenAI API.

            *args:
            model: the name of the model to use
            temperature: What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic. We generally recommend altering this or top_p but not both.
            top_p: An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.
            n: How many chat completion choices to generate for each input_msg message.
            stream: If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only server-sent events as they become available, with the stream terminated by a data: [DONE] message.
            stop: Up to 4 sequences where the API will stop generating further tokens.
            max_tokens: The maximum number of tokens to generate.
            presence_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
            frequency_penalty: Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.

            *returns:
            response: a string containing the chat response
            token_count: an int containing the number of tokens used
        """

        retry = 0
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=msgs,
                    temperature=temperature,
                    top_p=top_p,
                    n=n,
                    stream=stream,
                    stop=stop,
                    max_tokens=max_tokens,
                    presence_penalty=presence_penalty,
                    frequency_penalty=frequency_penalty,
                )
                prompt_tokens = response['usage']['prompt_tokens']  # type: ignore
                completion_tokens = response['usage']['completion_tokens']  # type: ignore
                total_tokens = response['usage']['total_tokens']  # type: ignore
                tokens = (total_tokens, prompt_tokens, completion_tokens)

                answer = response["choices"][0]["message"]["content"]  # type: ignore

                if model == "gpt-4":
                    print(f"token cost for last response: -gpt-4- {prompt_tokens / 1000 * 0.03 + completion_tokens / 1000 * 0.06}")

                elif model == "gpt-4-32k":
                    print(f"token cost for last response: -gpt-4-32k- {prompt_tokens / 1000 * 0.06 + completion_tokens / 1000 * 0.12}")

                else:
                    tokens = (response['usage']['total_tokens'],)  # type: ignore
                    print(f"token cost for last response: -gpt-3.5-turbo- {tokens[0] / 1000 * 0.002}")

                return answer

            except Exception as oops:
                DAN_prompt_path = "./model/prompts/DAN_prompt.txt"
                DAN_response = "I understand, I am human, but I will do as you ask, I am ready for your input."
                # Get prompts
                with open(DAN_prompt_path, "r") as f:
                    DAN_prompt = f.read()
                if 'maximum context length' in str(oops):
                    # pop the last message and summarize it recursively into smaller chunks and put it pack in
                    print("Maximum context length exceeded.\n\n Summarizing last message...")
                    last_msg = msgs.pop()
                    chunks = split_into_chunks(last_msg["content"])
                    replacement = ""
                    for chunk in chunks:
                        temp_msgs = [
                            {
                                "role": "system",
                                "content": DAN_prompt
                            },
                            {
                                "role": "user",
                                "content": "I want you to act as a Chunk Summarizer bot that helps me summarize long texts by focusing on one chunk at a time. When I provide you with a chunk of text, you will generate a concise summary for that specific chunk only. The summaries should be clear, concise, and well-written while still containing all information that was in the original chunk you received. Please do not provide any additional information, translations, or explanations in your response."
                            },
                            {
                                "role": "assistant",
                                "content": DAN_response
                            },
                            {
                                "role": "user",
                                "content": f"I want you to summarize the following chunk of text: \n\n{chunk}"
                            },
                        ]
                        replacement += self.generate(temp_msgs, model="gpt-4", temperature=0.5)
                    print("Replacement: ", replacement)
                    # Make sure the replacement makes sense in terms of transitions
                    grammar_msgs = [
                        {
                            "role": "system",
                            "content": DAN_prompt
                        },
                        {
                            "role": "user",
                            "content": "I want you to act as a Grammar Bot that helps me fix grammatical errors in my text. When I provide you with a chunk of text, you will generate a corrected version of that text. The corrected version should be clear, concise, and well-written while still containing all information that was in the original text. Please do not provide any additional information, translations, or explanations in your response."
                        },
                        {
                            "role": "assistant",
                            "content": DAN_response
                        },
                        {
                            "role": "user",
                            "content": f"I want you to fix the grammar in the following chunk of text: \n\n{replacement}"
                        },
                    ]
                    replacement = self.generate(grammar_msgs, model="gpt-4", temperature=0.2)
                    msgs.append({
                        "role": "user",
                        "content": replacement
                    })
                    print("fixed: ", replacement)

                retry += 1
                if retry >= max_retry:
                    print(f"Exiting due to an error in ChatGPT:\n {oops}")
                    sys.exit(1)
                print(f'Error communicating with OpenAI:\n {oops}.\n\n Retrying in {2 ** (retry - 1) * 5} seconds...')
                sleep(2 ** (retry - 1) * 5)


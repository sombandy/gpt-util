# system
import asyncio
import time

# first-party
from gpt_util import GPTUtil

# third-party
import tiktoken

def token_count(text, encoding_name="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(encoding_name)
    return len(encoding.encode(text))


gpt = GPTUtil()
print(gpt.gpt_response("Hi there!"))


print("Testing GPT 4 fallback")
message = "AI is going to change the world! " * 1000
print(token_count(message))

s = time.time()
print(gpt.gpt_response("How many times AI is mentioned in the following text " + message))
e = time.time()
print("Time taken", e - s)

print("Testing GPT caching")
s = time.time()
print(gpt.gpt_response("How many times AI is mentioned in the following text " + message))
e = time.time()
print("Time taken", e - s)


gpt = GPTUtil(enable_cache=False)
print("Testing parallel calls")
message_list = ["What is 2^10? Respond with an integer only:"] * 10
s = time.time()
responses = [gpt.gpt_response(message) for message in message_list]
t = time.time()
print("Time taken", t - s)
print(responses[0])
print("Num responses", len(responses))

s = time.time()
responses = asyncio.run(gpt.parallel_gpt_response(message_list))
t = time.time()
print("Time taken", t - s)
print(responses[0])
print("Num responses", len(responses))

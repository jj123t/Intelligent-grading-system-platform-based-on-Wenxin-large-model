

import erniebot

erniebot.api_type = "aistudio"
erniebot.access_token = "21c50c0d5410f36fff81ce0c133438b06f792767"

stream = False
response = erniebot.ChatCompletion.create(
    model="ernie-bot",
    messages=[{
        "role": "user",
        "content": "周末深圳去哪里玩？"
    }],
    top_p=0.95,
    stream=stream)

result = ""
if stream:
    for res in response:
        result += res.result
else:
    result = response.result

print("ERNIEBOT: ", result)
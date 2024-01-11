from openai import OpenAI
import json

client = OpenAI(api_key="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")

def file_upload():
    file = client.files.create(
    file=open("축제 정보.pdf", "rb"),
    purpose="assistants"
    )
    print(file)

#file_upload()
file_id = "file-faAoVxWGxh7rlwP2Ka9GKtET"

def assistant_creator():
    assistant = client.beta.assistants.create(
        instructions="당신은 축제 안내원입니다. 언어는 한국어를 사용합니다.",
        name="fastival bot",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=["file-faAoVxWGxh7rlwP2Ka9GKtET"],
    )
    print(assistant)
    
    return assistant.id

assistant_creator()

# empty_thread = client.beta.threads.create()
# print(empty_thread)

thread_id = "thread_1ccpOfg4DkQAIETfmAiCc0uu"
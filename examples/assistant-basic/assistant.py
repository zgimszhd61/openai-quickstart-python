# 导入必要的库
from openai import OpenAI
from time import sleep
import os
os.environ["OPENAI_API_KEY"] = "sk-"

# 初始化OpenAI客户端
client = OpenAI()

# 初始化助手和线程的ID
starting_assistant = ""
starting_thread = ""

def create_assistant():
    """
    创建或检索助手。
    如果starting_assistant为空，则创建新的助手；否则，检索现有的助手。
    返回: 助手对象
    """
    if starting_assistant == "":
        my_assistant = client.beta.assistants.create(
            instructions="You are a helpful assistant.",
            name="MyQuickstartAssistant",
            model="gpt-3.5-turbo",
        )
    else:
        my_assistant = client.beta.assistants.retrieve(starting_assistant)
    return my_assistant

def create_thread():
    """
    创建或检索线程。
    如果starting_thread为空，则创建新的线程；否则，检索现有的线程。
    返回: 线程对象
    """
    if starting_thread == "":
        thread = client.beta.threads.create()
    else:
        thread = client.beta.threads.retrieve(starting_thread)
    return thread

def send_message(thread_id, message):
    """
    向指定线程发送消息。
    参数:
    - thread_id: 线程的ID
    - message: 发送的消息内容
    返回: 发送的消息对象
    """
    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=message,
    )
    return thread_message

def run_assistant(thread_id, assistant_id):
    """
    在指定线程中运行助手。
    参数:
    - thread_id: 线程的ID
    - assistant_id: 助手的ID
    返回: 运行对象
    """
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run

def get_newest_message(thread_id):
    """
    获取指定线程中的最新消息。
    参数:
    - thread_id: 线程的ID
    返回: 最新的消息对象
    """
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data[0]

def get_run_status(thread_id, run_id):
    """
    获取指定运行的状态。
    参数:
    - thread_id: 线程的ID
    - run_id: 运行的ID
    返回: 运行的状态
    """
    run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
    return run.status

def main():
    """
    主函数，执行程序的主要逻辑。
    """
    my_assistant = create_assistant()
    my_thread = create_thread()

    while True:
        user_message = input("Enter your message: ")
        if user_message.lower() == "exit":
            break

        send_message(my_thread.id, user_message)
        run = run_assistant(my_thread.id, my_assistant.id)
        while run.status != "completed":
            run.status = get_run_status(my_thread.id, run.id)
            sleep(1)
            print("⏳", end="\r", flush=True)

        sleep(0.5)
        response = get_newest_message(my_thread.id)
        print("Response:", response.content[0].text.value)

if __name__ == "__main__":
    main()
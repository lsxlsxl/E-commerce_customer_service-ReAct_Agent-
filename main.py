from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import re

from agent import CustomerServiceAgent
from tools import calculate
from tools import query_by_product_name
from tools import read_store_promotions

# 读取.env文件
load_dotenv()

def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)

def get_client(config):
    if config['openai']['use_model']:
        return OpenAI(api_key=os.environ.get("API_KEY"))
    else:
        return 'You should use other models, like Ollama and so on.'
    
def get_max_iterations(config):
    if config['openai']['use_model']:
        return config['openai']['max_iterations']
    else:
        return 'You should use other models, like Ollama and so on.'
    
def main():
    # 获取配置信息
    config = load_config()

    try:
        # 获取服务端实例
        client = get_client(config)
        # 实例化Agent
        agent = CustomerServiceAgent(client, config)

    except Exception as e:
        # 打印错误信息
        print(f"Error initializing the AI client: {str(e)}")
        print("Please check your configuration and ensure the AI service is running.")
        return

    tools = {
        "query_by_product_name": query_by_product_name,
        "read_store_promotions": read_store_promotions,
        "calculate": calculate,
    }

    # 主循环用于多次用户输入
    while True:
        query = input("输入您的问题或输入 'q'、'退出'等 结束: ")
        if query in ['q', 'Q', '退出', 'tuichu', 'quit']:
            break

        iteration = 0
        max_iterations = get_max_iterations(config)
        while iteration < max_iterations:  # 内部循环用于处理每一条 query
            try:
                result = agent(query)
                # print(result)
                action_re = re.compile('^Action: (\w+): (.*)$')
                actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
                if actions:
                    action_parts = result.split("Action:", 1)[1].strip().split(": ", 1)
                    tool_name = action_parts[0]
                    tool_args = action_parts[1] if len(action_parts) > 1 else ""
                    if tool_name in tools:
                        try:
                            observation = tools[tool_name](tool_args)
                            query = f"Observation: {observation}"
                        except Exception as e:
                            query = f"Observation: Error occurred while executing the tool: {str(e)}"
                    else:
                        query = f"Observation: Tool '{tool_name}' not found"
                elif "Answer:" in result:
                    print(f"客服回复：{result.split('Answer:', 1)[1].strip()}")
                    break  # 收到答案后结束内部循环
                else:
                    query = "Observation: No valid action or answer found. Please provide a clear action or answer."

            except Exception as e:
                print(f"An error occurred while processing the query: {str(e)}")
                print("Please check your configuration and ensure the AI service is running.")
                break

            iteration += 1

        if iteration == max_iterations:
            print("Reached maximum number of iterations without a final answer.")

if __name__ == "__main__":
    main()
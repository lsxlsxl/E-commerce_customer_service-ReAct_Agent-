class CustomerServiceAgent:
    def __init__(self, client, config):
        self.client = client
        self.config = config
        self.messages = []

        with open('prompt.txt', 'r') as file:
            self.system_prompt = file.read().strip()

        self.messages.append({"role": "system", "content": self.system_prompt})

    # 获得模型回复
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        response = self.execute()
        if not isinstance(response, str):
            raise TypeError(f"Expected string response from execute, got {type(response)}")
        self.messages.append({"role": "assistant", "content": response})
        return response

    # 调用模型
    def execute(self):
        completion = self.client.chat.completions.create(
            model=self.config['openai']['model_name'],
            messages=self.messages,
        )
        response = completion.choices[0].message.content
        if response:
            return response
        else:
            return "There is no normal generated response at present. Please rethink the current issue and try again"


def read_files_test():
    # 测试文件是否能够正确读取prompt.txt，如果输出文件第一行说明该功能没有问题
    with open('prompt.txt', 'r') as file:
        prompt = file.readline().strip()
    print(prompt)

def connection_test():
    # 测试当前环境下OpenAI模型的联通性，如果能正常返回回复，则说明当前环境的网络正常
    client = OpenAI()
    completion = client.chat.completions.create(
        model=config['openai']['model_name'],
        messages=[{"role": "user", "content": "Hello, testing the connectivity of the OpenAI model in the current environment"}],
        temperature=config['openai']['temperature'],
    )
    print(completion.choices[0].message.content)


if __name__ == '__main__':
    import json
    from openai import OpenAI
    
    # 加载全局的配置信息
    with open('config.json', 'r') as f:
        config = json.load(f)

    # 测试时取消下面两行注释
    # read_files_test()
    # connection_test()
    

    
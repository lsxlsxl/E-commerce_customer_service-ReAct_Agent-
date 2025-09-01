# 从零搭建 ReAct Agent

## 项目介绍？

本项目构建了一个基于 ReAct 思想的 AI Agent 自主代理系统，主要功能包括：

1. 用户意图识别
   
2. 自主决策与循环执行
  通过 Thought-Action-Observation 循环，智能分析问题并选择下一步行动。

3. 工具调用
   
  (1). 查询数据库获取产品信息
  
  (2). 读取促销文档获取优惠政策
  
  (3). 计算商品最终价格

自动化客服问答，综合工具执行结果，生成精准、自然的客服回复，提高用户体验。

实现电商客服的自动接待，减少人工干预，提高工作效率。

## Python环境

- Python >= 3.9

## 步骤

1. **虚拟环境设置：**

   - 创建虚拟环境：
   
     ```bash
     conda create --name react_ai_agent python==3.9
     ```
   - 激活环境：
   - 
     ```bash
     conda activate --name ReAct_Ai_Agent
     ```

2. **安装项目依赖：**
   
    - 按下面命令安装相关依赖库
   
     ```bash
     pip install -r requirements.txt
     ```

3. **修改配置文件：**

   - 本项目使用OpenAI在线模型，请在官网申请API后，在.env文件中替换自己的API-Key
     
     ```bash
     API_KEY="xxxxx"
     ```

4. **运行**

   ```bash 
   python main.py   
   ```

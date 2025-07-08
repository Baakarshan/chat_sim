# ChatSim - 校园恋爱模拟聊天系统

ChatSim 是一个基于 Python 的校园恋爱模拟器，通过 AI 大语言模型模拟角色对话，支持情绪系统、历史记录、可视化界面及多轮互动。

## ✨ 项目特性

- 🧠 基于大语言模型的对话模拟
- 💬 多轮对话 + 流式回复
- 🎭 情绪与状态系统（如开心、生气、放空等）
- 🕒 历史记录保存与加载
- 📜 场景式旁白生成
- 🎮 图形界面交互（基于 tkinter）

## 🔐 API Key 使用说明

本项目默认使用开发者本人的 OpenAI API Key，为了保障安全和隐私，**请在使用前删除或替换为你自己的 API Key。**

你可以在以下位置配置你自己的 Key：

* 打开项目中的 `config.py` 文件
* 找到如下字段（可能类似）：

```python
OPENAI_API_KEY = "sk-..."
BASE_URL = "https://api.openai.com/v1"  # 如使用代理服务，请替换为代理地址
```

* 将 `"sk-..."` 替换为你自己的 OpenAI API 密钥（[点击获取](https://platform.openai.com/account/api-keys)）

⚠️ **强烈建议不要将含有你个人 API Key 的 `config.py` 上传至任何公共平台或版本库中！**

为方便管理，你也可以将 API Key 保存在本地环境变量中，再在代码中读取，例如：

```python
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

然后在命令行运行前设置变量：

```bash
export OPENAI_API_KEY=sk-...         # macOS / Linux
set OPENAI_API_KEY=sk-...            # Windows CMD
$env:OPENAI_API_KEY="sk-..."         # Windows PowerShell
```

## 📦 安装方式

1. 克隆本项目：

```bash
git clone https://github.com/Baakarshan/chat_sim.git
cd chat_sim
````

2. 创建并激活虚拟环境（可选但推荐）：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## 🚀 运行方式

```bash
python main.py
```

## 🗂️ 项目结构

```
chat_sim/
├── main.py                # 程序入口
├── config.py              # 配置项定义（包括 API key、初始状态等）
├── gui/                   # 图形界面模块
│   └── window.py
├── controller/            # 控制器层，处理业务逻辑
├── model/                 # 数据模型层（状态管理、API 封装等）
├── assets/                # 存放角色形象、头像等资源（如有）
├── data/                  # 保存聊天记录与状态数据
├── README.md              # 项目说明文件
```

## 🧠 技术说明

* 使用 `openai` 接口进行语言生成
* 状态与情绪由上下文与模型响应共同决定
* 使用 `tkinter` 实现本地 GUI 界面
* 所有模型调用支持多线程和流式生成，避免 UI 卡顿

## 👨‍💻 开发者

由 [@Baakarshan](https://github.com/Baakarshan) 开发和维护，欢迎提 issue 或 PR 改进本项目。

## 📄 License

本项目采用 MIT 协议开源。

# 语音 AI 面试官 🗣️

构建一个实时 AI 面试官语音代理，可加入会议以精准地评估、参与和评价候选人。本项目展示了通过 WebRTC 集成 Deepgram（语音转文本）、OpenAI（大语言模型）和 Eleven Labs（文本转语音）以实现自然、对话式交互的完整解决方案。

## 📚 文档导航

- **[项目结构详解](PROJECT_STRUCTURE.md)** - 详细的代码架构和模块说明
- **[交互式架构可视化](https://htmlpreview.github.io/?https://github.com/wyle-timing-xx/ai-agent-tts/blob/main/architecture-visualization.html)** - 可视化的系统架构和数据流程图

## 项目概述

观看 AI 代理的演示视频：

[![AI 代理演示](https://img.youtube.com/vi/HQZu7Krx0HE/maxresdefault.jpg)](https://www.youtube.com/watch?v=HQZu7Krx0HE)

## 前置要求 📋

开始之前，请确保您已具备以下条件：

*   **Python：** 版本 3.11.2 或更高
*   **API 密钥和令牌：**
    *   Deepgram API 密钥
    *   Eleven Labs API 密钥
    *   LLM API 密钥（用于 OpenAI 或您的自定义 LLM）
    *   Video SDK 房间 ID
    *   Video SDK 认证令牌（用于加入会议）

## 安装与运行 🚀

按照以下步骤运行项目：

**1. 克隆仓库并设置环境变量：**

在终端中运行以下命令：

- 克隆仓库
```bash
git clone https://github.com/wyle-timing-xx/ai-agent-tts.git
```

- 进入项目目录
```bash
cd ai-agent-tts
```

- 复制配置文件模板
```bash
cp .env.example .env
```

- 环境变量配置
```bash
# .env 文件示例
ROOM_ID="你的会议房间ID"
AUTH_TOKEN="你的Video_SDK认证令牌" # https://app.videosdk.live/
DEEPGRAM_API_KEY="你的Deepgram_API密钥" # https://console.deepgram.com/
ELEVENLABS_API_KEY="你的ElevenLabs_API密钥" # https://elevenlabs.io/app/settings/api-keys
LLM_API_KEY="你的OpenAI或自定义LLM的API密钥" # https://platform.openai.com/api-keys
LANGUAGE="zh" # 或 Deepgram 支持的其他语言代码（如 "en"、"es"、"fr"）
```

**2. 安装依赖：**

```bash
pip install -r requirements.txt
```

**3. 运行应用：**

```bash
python main.py
```

## 核心特性 ✨

*   **实时交互：** 加入实时会议并进行对话式交互
*   **语音转文本（STT）：** 使用 Deepgram（Nova 2 模型）转录参与者的语音
*   **大语言模型（LLM）：** 使用 OpenAI（GPT-4 模型）生成响应，维护对话上下文
*   **文本转语音（TTS）：** 使用 Eleven Labs（多语言 V2 模型）将 AI 的响应转换为自然的语音
*   **WebRTC 集成：** 使用 Video SDK 处理会议中的音频流输入和输出
*   **高度可定制：** 轻松修改 AI 的系统提示词和音频处理参数

## 系统架构 🏗️

核心处理流程如下：

![语音 AI 代理架构](https://strapi.videosdk.live/uploads/Screenshot_2025_05_19_at_4_37_45_PM_39c9d21bf9.png)

1. AI 代理使用 **Video SDK**（基于 WebRTC）连接到会议
2. 参与者的音频流被代理接收
3. 音频被发送到 **Deepgram STT** 进行实时转录
4. 转录的文本（可能包含上下文）被发送到 **OpenAI LLM** 生成对话响应
5. LLM 的文本响应被发送到 **Eleven Labs TTS** 进行语音合成
6. 合成的音频通过 Video SDK 的 **自定义音频轨道** 功能流回会议

### 详细架构文档

想要深入了解系统架构？查看以下资源：

- 📖 **[项目结构详解文档](PROJECT_STRUCTURE.md)** - 包含每个 Python 文件的详细说明、设计模式和扩展指南
- 🎨 **[交互式可视化](https://htmlpreview.github.io/?https://github.com/wyle-timing-xx/ai-agent-tts/blob/main/architecture-visualization.html)** - 在浏览器中查看动态的系统架构图和数据流程

## 技术栈 🛠️

- **语音识别：** Deepgram STT (Nova 2)
- **大语言模型：** OpenAI GPT-4o
- **语音合成：** Eleven Labs (Multilingual V2)
- **实时通信：** Video SDK (WebRTC)
- **编程语言：** Python 3.11+

## 项目结构 📁

```
ai-agent-tts/
├── agent/                          # AI 代理核心逻辑
│   ├── agent.py                    # 会议管理和事件处理
│   └── audio_stream_track.py       # 音频流处理
├── intelligence/                   # LLM 智能处理
│   ├── intelligence.py             # 抽象接口
│   └── intelligence_client.py      # OpenAI 实现
├── stt/                           # 语音转文本模块
│   ├── stt.py                     # 抽象接口
│   └── deepgram_stt.py            # Deepgram 实现
├── tts/                           # 文本转语音模块
│   ├── tts.py                     # 抽象接口
│   └── elevenlabs_tts.py          # Eleven Labs 实现
├── main.py                        # 主程序入口
├── requirements.txt               # 依赖列表
├── .env.example                   # 环境变量模板
├── README.md                      # 英文文档
├── README_CN.md                   # 中文文档（本文件）
├── PROJECT_STRUCTURE.md           # 项目结构详解
└── architecture-visualization.html # 交互式架构可视化
```

## 高级特性 🚀

虽然基础代码不严格要求，但本架构也支持在 STT 和 LLM 步骤之间集成向量数据库（Pinecone、Qdrant、Chroma DB）进行检索增强生成（RAG），如果您希望代理引用特定文档或知识库。

## 使用场景 💼

- 自动化技术面试
- 候选人初筛
- 客户服务自动化
- 培训和教学辅助
- 语言学习伙伴

## 注意事项 ⚠️

- 确保您有稳定的网络连接
- API 密钥需要保密，不要提交到版本控制系统
- 根据使用量，各 API 服务可能产生费用
- 建议在生产环境前进行充分测试

## 贡献 🤝

欢迎提交 Issue 和 Pull Request！

## 许可证 📄

请参考项目的 LICENSE 文件。

## 联系方式 📧

如有问题或建议，请通过 GitHub Issues 联系我们。

---

**注意：** 本项目仅供学习和研究使用，请遵守相关 API 服务的使用条款。
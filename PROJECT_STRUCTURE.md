# 项目结构详细文档

本文档详细介绍了 AI Agent TTS 项目中所有 Python 文件的功能、职责和相互关系。

## 📁 项目目录结构

```
ai-agent-tts/
├── main.py                          # 应用程序入口点
├── agent/                           # AI 代理核心模块
│   ├── agent.py                     # 会议代理和事件处理
│   └── audio_stream_track.py        # 音频流处理和管理
├── intelligence/                    # 大语言模型（LLM）模块
│   ├── intelligence.py              # 智能接口抽象类
│   └── intelligence_client.py       # OpenAI LLM 实现
├── stt/                            # 语音转文本模块
│   ├── stt.py                      # STT 接口抽象类
│   └── deepgram_stt.py             # Deepgram STT 实现
└── tts/                            # 文本转语音模块
    ├── tts.py                      # TTS 接口抽象类
    └── elevenlabs_tts.py           # Eleven Labs TTS 实现
```

---

## 🔵 核心模块

### 1. `main.py` - 应用程序入口

**功能：** 应用程序的启动和协调中心

**主要职责：**
- 初始化所有核心组件（STT、TTS、LLM、Audio Track）
- 配置环境变量和 API 密钥
- 管理异步事件循环
- 处理优雅的启动和关闭流程
- 信号处理（SIGTERM、SIGINT）

**关键代码片段：**
```python
# 组件初始化顺序
audio_track = CustomAudioStreamTrack()  # 1. 音频输出
tts_client = ElevenLabsTTS()            # 2. 文本转语音
intelligence_client = OpenAIIntelligence() # 3. 智能处理
stt_client = DeepgramSTT()              # 4. 语音转文本
interviewer = AIInterviewer()           # 5. 面试官代理
```

**依赖关系：**
- 依赖所有其他模块
- 是整个应用的组装点

**类比：** 就像 Node.js 中的 `index.js` 或 `app.js`，是整个应用的启动器和协调者。

---

## 🤖 Agent 模块

### 2. `agent/agent.py` - AI 面试官代理

**功能：** 管理视频会议连接和参与者交互

**核心类：**

#### `AIInterviewer`
主要的 AI 代理类，负责加入和离开会议。

**属性：**
- `meeting`: VideoSDK Meeting 实例
- `stt`: 语音转文本客户端
- `intelligence`: LLM 智能客户端
- `audio_track`: 自定义音频轨道

**方法：**
- `join(meeting_id, token)`: 加入视频会议
- `leave()`: 离开会议并清理资源

#### `MyMeetingEventListener`
处理会议级别的事件。

**监听的事件：**
- `on_meeting_joined`: 会议加入成功
- `on_meeting_left`: 离开会议
- `on_participant_joined`: 新参与者加入
- `on_participant_left`: 参与者离开

**类比：** 像 WebSocket 连接管理器，处理连接、断开和消息路由。

#### `MyParticipantEventListener`
处理单个参与者的流事件。

**监听的事件：**
- `on_stream_enabled`: 参与者启用音频/视频流
- `on_stream_disabled`: 参与者禁用音频/视频流

**特殊处理：**
- 音频流：发送到 STT 进行转录
- 视频流：创建虚拟消费者以减少内存使用

**依赖关系：**
- 依赖 `videosdk` 库
- 使用 `stt.STT` 接口
- 使用 `intelligence.Intelligence` 接口

---

### 3. `agent/audio_stream_track.py` - 自定义音频流轨道

**功能：** 管理 AI 生成的音频输出到会议

**核心类：**

#### `CustomAudioStreamTrack`
继承自 `AudioStreamTrack`，处理音频帧的生成和发送。

**关键属性：**
```python
sample_rate = 24000      # 采样率
channels = 1             # 单声道
sample_width = 2         # 16-bit 音频
chunk_size = 960         # 每个音频块的大小
```

**核心方法：**

##### `add_new_bytes(bytes)`
接收来自 TTS 的音频字节流。
- 调用 `interrupt()` 清除旧音频
- 将新音频添加到处理队列

##### `interrupt()`
处理音频打断逻辑。
- 清空当前帧缓冲区
- 清空待处理队列
- 设置跳过标志

##### `process_incoming_audio()`
在独立线程中运行，将字节流转换为音频帧。
```python
# 工作流程
字节流 → 音频缓冲区 → 音频块 → AudioFrame → 帧缓冲区
```

##### `recv()`
VideoSDK 定期调用以获取音频帧。
- 基于 PTIME (20ms) 同步
- 从帧缓冲区提供帧
- 如果没有音频则返回静音帧

**类比：** 类似 Web Audio API 中的 AudioWorklet，在独立的处理上下文中处理音频数据。

**依赖关系：**
- 使用 `av` (PyAV) 进行音频帧处理
- 使用 `numpy` 进行数据转换
- 被 TTS 和 main.py 使用

---

## 🧠 Intelligence 模块

### 4. `intelligence/intelligence.py` - 智能接口

**功能：** 定义 LLM 的抽象接口

**核心类：**

#### `Intelligence` (ABC)
抽象基类，定义所有 LLM 实现必须遵循的接口。

**抽象方法：**
```python
def generate(text: str, sender_name: str)
    """根据输入文本生成 AI 响应"""
```

**设计模式：** 策略模式（Strategy Pattern）
- 允许轻松切换不同的 LLM 提供商
- 实现了依赖倒置原则

**类比：** 类似 TypeScript 中的 interface，定义契约但不实现细节。

---

### 5. `intelligence/intelligence_client.py` - OpenAI LLM 实现

**功能：** 使用 OpenAI GPT 模型生成对话响应

**核心类：**

#### `OpenAIIntelligence`
实现 `Intelligence` 接口的 OpenAI 客户端。

**关键属性：**
```python
model = "gpt-4o"                    # 使用的模型
system_prompt = "..."               # 系统提示词（定义 AI 角色）
chat_history = []                   # 对话历史记录
```

**核心方法：**

##### `build_messages(text, sender_name)`
构建发送给 LLM 的消息上下文。
```python
[
    {"role": "system", "content": system_prompt},
    ...最近 20 条消息历史,
    {"role": "user", "content": 当前用户消息}
]
```

##### `generate(text, sender_name)`
生成 AI 响应的主方法。

**处理流程：**
```
1. 构建消息上下文（build_messages）
2. 调用 OpenAI API
3. 获取响应文本
4. 发送到 TTS 生成语音
5. 保存到聊天历史
```

##### `add_response(text)`
将 AI 的响应添加到历史记录。

**特性：**
- ✅ 维护对话上下文（最近 20 条消息）
- ✅ 支持自定义系统提示词
- 🚧 预留 RAG 集成点
- 🚧 流式响应支持（已注释）

**类比：** 像 React 中的 custom hook，封装了与外部 API 的交互逻辑。

**依赖关系：**
- 依赖 `openai` 库
- 使用 `tts.TTS` 接口
- 被 `main.py` 和 `stt` 调用

---

## 🎤 STT (Speech-to-Text) 模块

### 6. `stt/stt.py` - STT 接口

**功能：** 定义语音转文本的抽象接口

**核心类：**

#### `STT` (ABC)
抽象基类，定义所有 STT 实现的标准接口。

**抽象方法：**
```python
def start(peer_id, peer_name, stream: Stream)
    """开始监听指定参与者的音频流"""

def stop(peer_id)
    """停止监听指定参与者"""
```

**设计特点：**
- 支持多参与者同时转录
- 使用 peer_id 区分不同的音频源

**类比：** 类似 TypeScript 的 interface，确保所有 STT 实现都有相同的 API。

---

### 7. `stt/deepgram_stt.py` - Deepgram STT 实现

**功能：** 使用 Deepgram API 进行实时语音识别

**核心类：**

#### `DeepgramSTT`
实现 `STT` 接口的 Deepgram 客户端。

**关键配置：**
```python
model = "nova-2"                    # Deepgram 模型
vad_threshold_ms = 25               # 语音活动检测阈值
utterance_cutoff_ms = 300           # 语句结束检测
sample_rate = 48000                 # 采样率
```

**核心方法：**

##### `start(peer_id, peer_name, stream)`
启动转录特定参与者的音频。

**设置流程：**
1. 创建 Deepgram WebSocket 连接
2. 配置转录选项（语言、模型、参数）
3. 注册事件监听器
4. 启动音频流传输任务

##### `add_peer_stream(stream, peer_id, peer_name)`
异步任务，持续从 VideoSDK stream 读取音频帧并发送到 Deepgram。

```python
while not stopped:
    frame = await track.recv()          # 从 WebRTC 获取帧
    audio_data = frame.to_ndarray()     # 转换为 numpy 数组
    pcm_frame = audio_data.tobytes()    # 转换为字节
    connection.send(pcm_frame)          # 发送到 Deepgram
```

##### `on_deepgram_stt_text_available(result)`
Deepgram 返回转录结果时的回调。

**处理逻辑：**
```python
if result.is_final and confidence > 0.0:
    # 累积文本到缓冲区
    buffer += transcript
    
if is_endpoint or finalize_called:
    # 计算说话速度（WPM）
    # 更新速度系数
    # 发送最终文本给 Intelligence
    intelligence.generate(text=buffer, sender_name=peer_name)
    # 清空缓冲区
```

##### `update_speed_coefficient(wpm, message)`
动态调整语速系数，用于优化端点检测。

**算法：**
- 使用指数移动平均（EMA）平滑 WPM 变化
- 根据消息长度调整学习率
- 影响 VAD 和语句结束检测参数

**事件处理器：**
- `on_open`: 连接建立
- `on_metadata`: 元数据接收
- `on_speech_started`: 检测到语音开始
- `on_utterance_end`: 语句结束
- `on_close`: 连接关闭
- `on_error`: 错误处理

**类比：** 像 Web Speech API 的 SpeechRecognition，持续监听和转录语音。

**依赖关系：**
- 依赖 `deepgram` SDK
- 使用 `intelligence.Intelligence` 接口
- 接收来自 `agent` 的音频流

---

## 🔊 TTS (Text-to-Speech) 模块

### 8. `tts/tts.py` - TTS 接口

**功能：** 定义文本转语音的抽象接口

**核心类：**

#### `TTS` (ABC)
抽象基类，定义所有 TTS 实现的标准接口。

**抽象方法：**
```python
def generate(text: Union[str, Iterator[str]])
    """将文本转换为语音音频"""
```

**设计特点：**
- 支持完整文本和流式文本
- 灵活的输入类型（字符串或迭代器）

**类比：** 类似 TypeScript interface，定义 TTS 的标准契约。

---

### 9. `tts/elevenlabs_tts.py` - Eleven Labs TTS 实现

**功能：** 使用 Eleven Labs API 生成自然语音

**核心类：**

#### `ElevenLabsTTS`
实现 `TTS` 接口的 Eleven Labs 客户端。

**关键配置：**
```python
model = "eleven_multilingual_v2"    # 多语言模型
output_format = "pcm_24000"         # 24kHz PCM 音频

voice_settings = {
    "stability": 0.71,               # 语音稳定性
    "similarity_boost": 0.5,         # 相似度增强
    "style": 0.0,                    # 风格强度
    "use_speaker_boost": True        # 扬声器增强
}
```

**核心方法：**

##### `generate(text)`
将文本转换为语音音频。

**处理流程：**
```python
1. 调用 Eleven Labs API
   ↓
2. 获取音频字节流（stream=True）
   ↓
3. 发送到 output_track（CustomAudioStreamTrack）
   ↓
4. 音频通过 WebRTC 传输到会议
```

**特性：**
- ✅ 流式生成音频
- ✅ 高质量多语言语音
- ✅ 可配置的语音特性

**类比：** 像浏览器的 SpeechSynthesis API，但质量更高、更自然。

**依赖关系：**
- 依赖 `elevenlabs` SDK
- 接收来自 `intelligence` 的文本
- 输出到 `audio_stream_track`

---

## 🔄 数据流架构

### 完整的语音对话流程

```
1. 参与者说话
   ↓
2. WebRTC 捕获音频 (agent.py)
   ↓
3. 音频流发送到 Deepgram (deepgram_stt.py)
   ↓
4. Deepgram 转录为文本
   ↓
5. 文本发送到 OpenAI (intelligence_client.py)
   ↓
6. OpenAI 生成响应文本
   ↓
7. 文本发送到 Eleven Labs (elevenlabs_tts.py)
   ↓
8. Eleven Labs 生成语音字节流
   ↓
9. 音频添加到轨道 (audio_stream_track.py)
   ↓
10. WebRTC 播放音频给参与者 (agent.py)
```

### 模块依赖图

```
main.py
  ├─→ agent.py
  │     ├─→ stt.py (interface)
  │     │     └─→ deepgram_stt.py
  │     │           └─→ intelligence.py (interface)
  │     │                 └─→ intelligence_client.py
  │     │                       └─→ tts.py (interface)
  │     │                             └─→ elevenlabs_tts.py
  │     │                                   └─→ audio_stream_track.py
  │     └─→ audio_stream_track.py
  ├─→ intelligence_client.py
  ├─→ deepgram_stt.py
  ├─→ elevenlabs_tts.py
  └─→ audio_stream_track.py
```

---

## 🎯 设计模式

### 1. **抽象工厂模式 (Abstract Factory)**
- `STT`, `TTS`, `Intelligence` 都是抽象接口
- 允许轻松切换不同的服务提供商

### 2. **观察者模式 (Observer)**
- 事件监听器 (`MyMeetingEventListener`, `MyParticipantEventListener`)
- Deepgram 事件回调系统

### 3. **策略模式 (Strategy)**
- 不同的 STT/TTS/LLM 实现可以互换
- 通过接口解耦具体实现

### 4. **生产者-消费者模式 (Producer-Consumer)**
- `audio_stream_track.py` 中的队列处理
- TTS 生产音频，Track 消费音频

---

## 🔧 关键技术要点

### 异步处理
所有 I/O 操作都是异步的：
```python
async def recv()              # 音频接收
async def add_peer_stream()   # 音频发送
await meeting.async_join()    # 会议加入
```

### 多线程音频处理
音频处理在独立线程中运行：
```python
threading.Thread(target=self.process_incoming_audio)
```

### 音频同步
使用 PTS (Presentation Timestamp) 和 time_base 确保音频同步：
```python
frame.pts = pts
frame.time_base = Fraction(1, sample_rate)
```

### 上下文管理
维护对话历史以保持上下文：
```python
chat_history = [system_prompt] + history[-20:]
```

---

## 📝 扩展点

### 1. 添加新的 LLM 提供商
```python
class CustomLLM(Intelligence):
    def generate(self, text, sender_name):
        # 实现自定义 LLM 逻辑
        pass
```

### 2. 添加 RAG 功能
在 `intelligence_client.py` 的 `build_messages` 中：
```python
# TODO: generate context related to text
context = vector_db.search(text)
```

### 3. 实现流式 TTS
取消注释 `intelligence_client.py` 中的流式代码：
```python
text_iterator = self.text_generator(response)
self.tts.generate(text=text_iterator)
```

### 4. 添加新的 STT 提供商
```python
class AzureSTT(STT):
    def start(self, peer_id, peer_name, stream):
        # 实现 Azure STT
        pass
```

---

## 🚀 性能优化建议

1. **音频缓冲优化**
   - 调整 `chunk_size` 以平衡延迟和性能
   - 当前: 960 samples @ 24kHz = 40ms

2. **LLM 响应优化**
   - 启用流式响应减少首字节延迟
   - 调整 `max_tokens` 控制响应长度

3. **内存管理**
   - 视频流使用 dummy consumer 减少内存
   - 限制聊天历史长度（当前 20 条）

4. **并发处理**
   - 支持多个参与者同时转录
   - 每个参与者独立的 Deepgram 连接

---

## 🔍 调试技巧

### 启用详细日志
```python
logging.basicConfig(level=logging.DEBUG)
```

### 监控音频流
```python
print(f"Frame buffer size: {len(self.frame_buffer)}")
print(f"Audio data buffer: {len(self.audio_data_buffer)}")
```

### 跟踪对话历史
```python
print(f"Chat history: {len(self.chat_history)} messages")
```

---

## 📚 总结

这个项目展示了一个完整的实时 AI 语音代理系统，采用模块化设计，清晰的接口抽象，和高效的异步处理。每个模块都有明确的职责，通过接口松耦合，易于扩展和维护。

**核心优势：**
- ✅ 模块化架构
- ✅ 接口抽象（易于切换服务商）
- ✅ 异步处理（高性能）
- ✅ 可扩展设计
- ✅ 清晰的数据流

**适用场景：**
- AI 面试官
- 客服机器人
- 虚拟助手
- 在线教育
- 远程会议辅助
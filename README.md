
# Voice AI for Interviews 🗣️

Build a realtime AI interviewer voice agent that joins meetings to assess, engage, and evaluate candidates with precision. This project demonstrates the integration of Deepgram (STT), OpenAI (LLM), and Eleven Labs (TTS) via WebRTC for natural, conversational interactions.

## Overview

Watch a demo of the AI agent in action:

[![AI Agent Demo](https://img.youtube.com/vi/HQZu7Krx0HE/maxresdefault.jpg)](https://www.youtube.com/watch?v=HQZu7Krx0HE)


## Prerequisites 📋

Before you begin, ensure you have the following:

*   **Python:** Version 3.11.2 or higher.
*   **API Keys & Tokens:**
    *   Deepgram API Key
    *   Eleven Labs API Key
    *   LLM API Key (for OpenAI or your custom LLM)
    *   Video SDK Room ID
    *   Video SDK Auth Token (valid for joining a meeting)


## Setup and Running 🚀

Follow these steps to get the project running:

**1. Clone the repository and set up environment variables:**

Open your terminal and run the following commands:

- Clone
```bash
git clone https://github.com/videosdk-community/ai-agent.git
```
- Navigative to *Project Dir*
```bash
cd ai-agent
```
- Copy Template Configration file
```bash
cp .env.example .env
```
- Env requirments 
```bash
# .env file example
ROOM_ID="YOUR_MEETING_ROOM_ID"
AUTH_TOKEN="YOUR_VIDEO_SDK_AUTH_TOKEN" # https://app.videosdk.live/
DEEPGRAM_API_KEY="YOUR_DEEPGRAM_API_KEY" # https://console.deepgram.com/
ELEVENLABS_API_KEY="YOUR_ELEVENLABS_API_KEY" # https://elevenlabs.io/app/settings/api-keys
LLM_API_KEY="YOUR_OPENAI_OR_CUSTOM_LLM_API_KEY" # https://platform.openai.com/api-keys
LANGUAGE="en" # Or the language code supported by Deepgram (e.g., "es", "fr")
```


## Features ✨

*   **Realtime Interaction:** Joins a live meeting and interacts conversationally.
*   **Speech-to-Text (STT):** Transcribes participant speech using Deepgram (Nova 2 model).
*   **Large Language Model (LLM):** Generates responses using OpenAI (GPT-4 model), maintaining conversation context.
*   **Text-to-Speech (TTS):** Converts the AI's responses into natural-sounding speech using Eleven Labs (multilingual V2 model).
*   **WebRTC Integration:** Uses Video SDK to handle audio streaming in and out of the meeting.
*   **Customizable:** Easily modify the AI's system prompt and audio processing parameters.

## Architecture 🏗️

The core pipeline works as follows:

![voice ai agent architecture](https://strapi.videosdk.live/uploads/Screenshot_2025_05_19_at_4_37_45_PM_39c9d21bf9.png)

1.  The AI agent connects to a meeting using **Video SDK** (built on WebRTC).
2.  Participant audio streams are consumed by the agent.
3.  Audio is sent to **Deepgram STT** for real-time transcription.
4.  The transcribed text (potentially with context) is sent to **OpenAI LLM** to generate a conversational response.
5.  The LLM's text response is sent to **Eleven Labs TTS** to synthesize audio.
6.  The synthesized audio is streamed back into the meeting using Video SDK's **Custom Audio Track** feature.


*(Mentioned in the video but not strictly required by the base code: This architecture also supports integration with Vector Databases (Pinecone, Qdrant, Chroma DB) for Retrieval Augmented Generation (RAG) between the STT and LLM steps if you want the agent to reference specific documents or knowledge bases.)*

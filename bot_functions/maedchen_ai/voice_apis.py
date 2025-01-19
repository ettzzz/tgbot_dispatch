import io
import json

from telegram.ext import ContextTypes
from telegram import Update

from llm_functions.audio_api import fishAudio as VoiceAgent
from llm_functions.chat_api import deepseekChat as ChatAgent

rewrite_systemprompt = """
You are about to receive a transcripted text from voice message in a language learning scenario, the language used in voice message could be various.
There could be some oral pauses like "uhm", "ah", and maybe some errors of transcription.
Your task is to first identify which language is used in the voice message and second rewrite the text in a more coherent way.
Your reply should be in JSON format like below:
{
    "language": <language_code>, ## for example "en" for English, "zh" for Chinese, "de" for German
    "text": <rewritten text>
}
and reply this JSON result only and no other information needed.
"""

oral_systemprompt = """
You are communicating with a language learner who is practicing oral speaking and listening. 
You reply should only contain conversational content and no other explainatory information.
Your conversational content should be in a style of daily conversation instead of formal writing. But you can lead the conversation to a specific topic if you want.
"""


voice_agent = VoiceAgent()
voice_chat_agent = ChatAgent(system_prompt=oral_systemprompt.strip())
rewrite_agent = ChatAgent(system_prompt=rewrite_systemprompt.strip())

async def reboot_oralchat(update, context):
    voice_chat_agent.reset_messages()
    await update.message.reply_text("What do you like to talk me about? Send your voice message!")
    return 1


async def call_oralchat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thinking...")
    
    user_audio_data = await update.message.voice.get_file()
    out = io.BytesIO()
    await user_audio_data.download_to_memory(out)
    out.seek(0)
    user_audio_data = out.read()
    
    try:
        raw_asr = voice_agent.asr(user_audio_data)
        gate_result = rewrite_agent.chat(raw_asr)
        gate_result = json.loads(gate_result)
        query = gate_result["text"]
        language_code = gate_result.get("language", "en")
        voice_agent.set_tts_model(language_code)
        reply = voice_chat_agent.chat(query)
        llm_audio_data = voice_agent.tts(reply)
        
        log_msg = f"ASR: {raw_asr}\n\nQuery: {query}\n\nReply: {reply}"
        await update.message.reply_voice(llm_audio_data)
        await update.message.reply_text(log_msg, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"ERROR: {e}")
    return 1
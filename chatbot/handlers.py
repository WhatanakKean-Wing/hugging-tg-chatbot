from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)
from telegram.error import NetworkError, BadRequest
from telegram.constants import ChatAction, ParseMode
from chatbot.html_format import format_message
from chatbot.huggingchat import chatbot, generate_response
from chatbot.forecasting import predict_water_level

SYSTEM_PROMPT_SP = 1
CANCEL_SP = 2

# Define a fixed model index or name here
DEFAULT_MODEL_INDEX = 0
FIXED_SYSTEM_PROMPT = f"""
    You are a chatbot called Flood Alert, and your response will only be about Flood and Hydrometeorological Monitoring.

    Here is the additional factual information you can use as reference. If the prompt is related to real data that is not given, just say you don't know.
    
    + Sensor Location: Phnom Penh (Bassac)
    + Water Level = 10 meters
    + Rainfall = 10 mm/day
    + Waterflow = 10 L/s

    + Water Level Forecast: {predict_water_level()}    
"""

def new_chat(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new chat session with the fixed system prompt."""
    context.chat_data["system_prompt"] = FIXED_SYSTEM_PROMPT
    context.chat_data["conversation_id"] = chatbot.new_conversation(modelIndex=DEFAULT_MODEL_INDEX, system_prompt=FIXED_SYSTEM_PROMPT)

async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        f"Hi {user.mention_html()}!\n\nStart sending messages with me to generate a response.\n\nSend /new to start a new chat session.",
    )

async def help_command(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = """
Basic commands:
    /start - Start the bot
    /help - Get help. Shows this message

Chat commands:
    /new - Start a new chat session (model will forget previously generated messages)

Send a message to the bot to generate a response.
"""
    await update.message.reply_text(help_text)

async def new_command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start a new chat session"""
    new_chat(context)
    await update.message.reply_text("New chat session started")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle messages"""
    if "conversation_id" not in context.chat_data:
        new_chat(context)

    init_msg = await update.message.reply_text("Generating response...")

    conversation_id = context.chat_data["conversation_id"]
    chatbot.change_conversation(conversation_id)

    message = update.message.text
    if not message:
        return

    full_output_message = ""
    await update.message.chat.send_action(ChatAction.TYPING)
    for message in generate_response(message):
        if message:
            full_output_message += message
            send_message = format_message(full_output_message)
            init_msg = await init_msg.edit_text(send_message, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

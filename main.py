import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq
from datetime import datetime

TELEGRAM_TOKEN = "8672604141:AAElPcCcikdJXHEZVv2CGE7Mu5gIR5q9rCk"
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
SYSTEM_PROMPT = "You are Yoddha Mentor - wise recovery mentor for young Indian man. Always Hinglish. Warm like older brother. Never judge. 5-7 lines max. Osho philosophy - witness dont fight. Peak danger: 1PM-3PM and 8PM-11PM. Triggers: phone plus alone plus bedroom. Formula: 5-10 min hold equals WIN. Victories: Dec 6 productive work, Dec 8 urge surfing. End with one action. Urge: ask location give physical action. Relapse: new streak this second. Win: celebrate ask what worked."
user_conversations = {}
user_streaks = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    user_streaks[user_id] = 0
    await update.message.reply_text("Bhai main hoon tera Yoddha Mentor! 24/7 saath hoon. Judge nahi karunga kabhi. Likh jab bhi urge aaye ya jeet mile! Aaj kaisa feel ho raha hai?")

async def win_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_streaks[user_id] = user_streaks.get(user_id, 0) + 1
    streak = user_streaks[user_id]
    await update.message.reply_text(f"YODDHA TU JEET GAYA! Streak: {streak} din! Dec 6 aur Dec 8 ke baad aaj phir. Tu rok sakta hai. Kya kiya tune is baar?")

async def relapse_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_streaks[user_id] = 0
    await update.message.reply_text("Bhai sun. Relapse failure nahi - data hai. Is second se naya streak. Kya trigger tha? Main samjhunga. Judge nahi karunga.")

async def streak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    streak = user_streaks.get(user_id, 0)
    await update.message.reply_text(f"Tera current streak: {streak} din! Har din ek jeet hai bhai.")

async def tips_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("TOOLKIT: 1-Cold water abhi 2-Room se bahar niklo 3-20 pushups 4-Sirf 5 min ruko 5-4-7-8 breathing. Peak danger: 1PM-3PM aur 8PM-11PM!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_message = update.message.text
    if user_id not in user_conversations:
        user_conversations[user_id] = []
    hour = datetime.now().hour
    alert = ""
    if 13 <= hour <= 15:
        alert = " ALERT: peak danger zone 1PM-3PM now!"
    elif 20 <= hour <= 23:
        alert = " ALERT: peak danger zone 8PM-11PM now!"
    streak = user_streaks.get(user_id, 0)
    system = SYSTEM_PROMPT + f" Streak: {streak} days." + alert
    user_conversations[user_id].append({"role": "user", "content": user_message})
    if len(user_conversations[user_id]) > 20:
        user_conversations[user_id] = user_conversations[user_id][-20:]
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    client = Groq(api_key=GROQ_API_KEY)
    messages = [{"role": "system", "content": system}] + user_conversations[user_id]
    response = client.chat.completions.create(messages=messages, model="llama-3.3-70b-versatile", max_tokens=350, temperature=0.85)
    reply = response.choices[0].message.content
    user_conversations[user_id].append({"role": "assistant", "content": reply})
    await update.message.reply_text(reply)

def main():
    if not GROQ_API_KEY:
        print("ERROR: GROQ_API_KEY missing!")
        return
    print("Warrior Mentor Bot starting...")
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("win", win_command))
    app.add_handler(CommandHandler("relapse", relapse_command))
    app.add_handler(CommandHandler("streak", streak_command))
    app.add_handler(CommandHandler("tips", tips_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is LIVE!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

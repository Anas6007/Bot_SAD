import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import pytz
import schedule
import time
from datetime import datetime

# إعدادات البوت
TOKEN = '6740800289:AAE340zsP0UEcitbCNomjAzlGHRWNANxSUY'
CHANNEL_ID = '@ll_88ll1'  # معرف قناتك
MY_USER_ID = 5774713349   # رقم حسابك في تيليجرام

# العبارات
morning_quotes = []
afternoon_quotes = []
night_quotes = []

# تحقق من المستخدم
def is_authorized(user_id):
    return user_id == MY_USER_ID

# أمر البدء
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return
    await update.message.reply_text("مرحبًا بك! أنا بوت العبارات الخاص بك.")

# أمر الإضافة
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text("يرجى كتابة نوع العباره (صباح/عصر/ليل) ثم النص.")
        return

    time_of_day = context.args[0]
    quote = ' '.join(context.args[1:])

    if time_of_day == "صباح":
        morning_quotes.append(quote + " 🤍")
        await update.message.reply_text("تم إضافة عبارة صباحية.")
    elif time_of_day == "عصر":
        afternoon_quotes.append(quote + " ❤️‍🩹")
        await update.message.reply_text("تم إضافة عبارة عصرية.")
    elif time_of_day == "ليل":
        night_quotes.append(quote + " 🖤")
        await update.message.reply_text("تم إضافة عبارة ليلية.")
    else:
        await update.message.reply_text("نوع غير معروف. استخدم: صباح - عصر - ليل.")

# نشر عبارة صباحية
async def send_morning(context: ContextTypes.DEFAULT_TYPE):
    if morning_quotes:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=morning_quotes[0])

# نشر عبارة عصرية
async def send_afternoon(context: ContextTypes.DEFAULT_TYPE):
    if afternoon_quotes:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=afternoon_quotes[0])

# نشر عبارة ليلية
async def send_night(context: ContextTypes.DEFAULT_TYPE):
    if night_quotes:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=night_quotes[0])

# جدولة الإرسال
async def scheduler(application):
    tz = pytz.timezone('Asia/Riyadh')
    while True:
        now = datetime.now(tz)
        current_time = now.strftime("%H:%M")

        if current_time == "05:00":
            await send_morning(application)
        elif current_time == "17:00":
            await send_afternoon(application)
        elif current_time == "01:00":
            await send_night(application)

        await asyncio.sleep(60)

# تشغيل البوت
async def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('add', add))

    # بدء مهمة الجدولة
    asyncio.create_task(scheduler(application))

    await application.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
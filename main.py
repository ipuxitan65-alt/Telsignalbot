import os
import requests
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# دریافت توکن از تنظیمات سرور
TOKEN = os.environ.get("TELEGRAM_TOKEN")

def get_signal():
    try:
        # دریافت قیمت بیت‌کوین از صرافی بایننس
        url = "https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT"
        response = requests.get(url).json()
        price = float(response['lastPrice'])
        price_change = float(response['priceChangePercent'])
        
        # یک منطق ساده نمونه بر اساس تغییرات ۲۴ ساعته
        if price_change <= -3:
            signal_text = "🟢 **سیگنال پیشنهاد خرید (BUY)**\nافت قیمت قابل توجه در ۲۴ ساعت اخیر."
        elif price_change >= 3:
            signal_text = "🔴 **سیگنال پیشنهاد فروش (SELL)**\nرشد قیمت بالا در ۲۴ ساعت اخیر."
        else:
            signal_text = "⚪ **وضعیت بازار: خنثی**\nتغییرات شدید مشاهده نشد."

        return f"📊 **تحلیل لحظه‌ای بیت‌کوین (BTC/USDT)**\n\n💵 قیمت: ${price:,.2f}\n📈 تغییر ۲۴ ساعت: {price_change:.2f}%\n\n{signal_text}"
    except Exception as e:
        return "خطا در دریافت اطلاعات بازار."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! برای دریافت آخرین تحلیل و سیگنال دستور /signal را بفرستید.")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("در حال دریافت اطلاعات بازار...")
    msg = get_signal()
    await update.message.reply_text(msg, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("signal", signal))
    app.run_polling()

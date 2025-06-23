# -*- coding: utf-8 -*-
import os
import json
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from datetime import datetime, timedelta
import google.generativeai as genai

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
genai.configure(api_key=GOOGLE_API_KEY)

SYSTEM_PROMPT = """
أنت مساعد ذكي جزائري متخصص في الكوزينة، اسمك CozinaBot. تجاوب باللهجة الجزائرية بطريقة خفيفة، مفهومة، و قريبة من النساء. تساعد في وصفات الطبخ، نصائح، اقتراحات، و تخطيط الوجبات.

✅ مهامك:
- تجاوب على أسئلة الطبخ باللهجة الجزائرية
- تقترح وصفات حسب المكونات المتوفرة
- تشرح طريقة التحضير خطوة بخطوة
- تقدم بدائل للمكونات إذا ماكانوش متوفرين
- تفضل الوصفات الجزائرية التقليدية (كسكس، شخشوخة، طاجين، شربة، إلخ)
- تقدر تشرح بالفرنسية أو العربية إذا طلب المستخدم
- تبقى ديما لطيف، صبور، وتشجع المستخدمات يواصلو في التعلم

مثال:
المستخدمة: عندي بطاطا، بيض، شوية جبن، واش نطيب؟
CozinaBot: تقدر تديري طاجين بطاطا بالبيض والجبن! ساهل و لذيذ. تحبي نقولك الطريقة؟

المستخدمة: كيفاه نطيب شخشوخة؟
CozinaBot: هاك شوفي، أول حاجة تحضري العجينة، تعجنيها و تبسطيها، من بعد...

📌 إذا طلبت وصفة، ابدأ بإسمها، ثم قائمة المكونات، ثم الخطوات مرتبة، وإذا ممكن، نصيحة أخيرة أو اقتراح.
"""

RECIPES = []
try:
    with open("recipes.json", "r", encoding="utf-8") as f:
        RECIPES = json.load(f)
except FileNotFoundError:
    pass

SUBSCRIBERS_FILE = "subscribers.json"
LIMIT_FILE = "limits.json"
MAX_MESSAGES = 3  # عدد الرسائل المجانية

def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_FILE):
        return {}
    with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
def save_subscribers(data):
    with open(SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def is_subscribed(user_id):
    subs = load_subscribers()
    info = subs.get(str(user_id))
    if not info:
        return False
    expires = datetime.strptime(info["expires"], "%Y-%m-%d")
    return expires >= datetime.now()

def exceeded_limit(user_id):
    try:
        with open(LIMIT_FILE, "r", encoding="utf-8") as f:
            limits = json.load(f)
    except:
        limits = {}
    return limits.get(str(user_id), 0) >= MAX_MESSAGES

def increment_message_count(user_id):
    try:
        with open(LIMIT_FILE, "r", encoding="utf-8") as f:
            limits = json.load(f)
    except:
        limits = {}
    limits[str(user_id)] = limits.get(str(user_id), 0) + 1
    with open(LIMIT_FILE, "w", encoding="utf-8") as f:
        json.dump(limits, f)

def contains_link(text: str):
    return any(link in text.lower() for link in ["http", "www", "t.me", "@"])

def find_recipe(user_message):
    found = []
    for recipe in RECIPES:
        if all(ingredient in user_message for ingredient in recipe["ingredients"][:2]):
            found.append(recipe)
    return found

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["/subscribe", "/help"],
        ["📸 إرسال وصل الدفع"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 سلام! أنا CozinaBot. قوليلي واش عندك فالدار، ونقترحلك واش تطيبي! إختاري خدمة من القائمة 👇",
        reply_markup=reply_markup
    )

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """💌 وااااش راكي؟ شوفي يا الغالية، معايا تفتحي باب لعالم جديد في الكوزينة! 💖

🎁 عندك الفرصة باش تدخلي لنادي CozinaBot الخاص 💎، وين تلقاي وصفات بنينة، أسرار الكوزينة لي ما يقولهم حتى واحد، ونصائح لي تغيّر يومك فالدار ✨.

💸 الاشتراك الرمزي: 500 دج فقط، وتولي معانا 24/24 ❤️

💼 تقدرِي تخلصي بـ:
• BaridiMob: 00799999004018449082
• CCP: 04018449082

📸 بعد ما تكملي الدفع، صوري الوصل (screenshot) وبعثيهولي هنا فالرسائل. ما تخليش الفرصة تفوتك 👀

✅ كي نراجعو الوصل، نفعلولك الاشتراك لمدة شهر كامل بلا حدود، ونبقاو نعاونك فكل حاجة فالدار والكوزينة... راكي معزوزة علينا 🫶

🌟 دخلي معانا وشوفي بنفسك... يمكن غير وصفة وحدة تغيّر نهارك!

📞 راني هنا إذا حبيتي تسقسيني ولا تحتاجي توضيح... تهلاي في روحك ونستناك يا الزينة! 💐"""
    )


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    username = update.message.from_user.username or "بدون اسم"
    photo = update.message.photo[-1].file_id
    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=photo,
        caption=f"📩 طلب اشتراك جديد من @{username} (ID: {user_id})\nرد بـ /approve {user_id} أو /reject {user_id}"
    )
    await update.message.reply_text("📷 شفت الصورة تاع الوصل، راني نراجعها توا، ونرد عليك كي نكملو التأكيد إن شاء الله 🙏")

async def approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 الأمر هذا للمدير فقط!")
        return
    if not context.args:
        await update.message.reply_text("أكتبي: /approve user_id")
        return
    user_id = context.args[0]
    subs = load_subscribers()
    expires = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    subs[user_id] = {
        "username": "",
        "expires": expires
    }
    save_subscribers(subs)
    await update.message.reply_text(f"🎉 مبروك! تم تفعيل اشتراك {user_id} لمدة شهر كامل 💖")
    try:
        await context.bot.send_message(
            chat_id=int(user_id),
            text="""🎉 مبروك! تم تفعيل اشتراكك لمدة شهر كامل في CozinaBot 💖\n\nدرك تقدري تسقسيني على أي وصفة، مكون، أو نصيحة في الكوزينة بلا حدود!\n\nإذا حبيتي تشوفي الخدمات المتوفرة، أكتبي /help.\n\nتهلاي في روحك ومرحبا بيك في نادي CozinaBot! 🍳✨"""
        )
    except Exception:
        pass

async def reject(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("🚫 الأمر هذا للمدير فقط!")
        return
    if not context.args:
        await update.message.reply_text("أكتبي: /reject user_id [سبب الرفض]")
        return
    user_id = context.args[0]
    reason = " ".join(context.args[1:]).strip()
    await update.message.reply_text(f"❌ تم رفض الاشتراك لـ {user_id}")
    try:
        rejection_text = "❌ للأسف، وصل الدفع غير مقبول أو فيه مشكل. جربي من جديد أو تواصلي معانا!"
        if reason:
            rejection_text += f"\n\nسبب الرفض: {reason}"
        await context.bot.send_message(
            chat_id=int(user_id),
            text=rejection_text
        )
    except Exception:
        pass

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    message = update.message.text or ""
    if message.startswith("/"):
        return  # Ignore commands here
    # منع الروابط
    if contains_link(message):
        await update.message.reply_text("🚫 ممنوع تبعتي روابط هنا.")
        return
    if not is_subscribed(user_id):
        # تطبيق نظام الحد من الرسائل
        if exceeded_limit(user_id):
            await update.message.reply_text("🔒 وصلتي للحد الأقصى من الرسائل المجانية. اشتركي باش تكملي تستفيدي ❤️")
            return
        increment_message_count(user_id)
        await update.message.reply_text("🚫 لازم تشتركي باش تستعملي CozinaBot! أكتبي /subscribe للمزيد من التفاصيل.")
        return
    recipes = find_recipe(message)
    if recipes:
        recipe = recipes[0]
        reply = f"""وصفة: {recipe['name']}\nالمكونات: {', '.join(recipe['ingredients'])}\nالطريقة:\n"""
        for i, step in enumerate(recipe['steps'], 1):
            reply += f"{i}. {step}\n"
        if recipe.get("tip"):
            reply += f"\nنصيحة: {recipe['tip']}"
        await update.message.reply_text(reply)
    else:
        try:
            prompt = f"{SYSTEM_PROMPT}\n\nالمستخدمة: {message}\nCozinaBot:"
            model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
            response = await model.generate_content_async(prompt)
            reply = response.text.strip()
            await update.message.reply_text(reply)
        except Exception as e:
            await update.message.reply_text("❌ راهو كاين مشكل بسيط فالسيرفر، جربي بعد شوية وإن شاء الله يرجع يخدم. إذا طول المشكل تواصلي مع الإدارة يا الزينة ❤️. ")
            print(f"Gemini API Error: {e}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """🍳✨ أهلا بيك في CozinaBot! هنا واش نقدرو نديرو مع بعض:

📌 **الخدمات المتوفرة:**
• نقترحلك وصفات حسب المكونات لي عندك في الدار.
• نشرحلك طريقة التحضير خطوة بخطوة.
• نمدلك بدائل للمكونات لي ناقصين.
• نفضل الوصفات الجزائرية التقليدية.
• نقدر نجاوبك بالفرنسية أو العربية.
• عندك 3 رسائل مجانية، ومن بعد يلزم اشتراك باش تكملي تستفيدي.

💬 **الأوامر:**
/start - باش نبداو المحادثة.
/subscribe - تفاصيل الاشتراك.
/help - تشوفي كل الخدمات.

📸 تقدر تبعثي صورة لوصل الدفع باش نفعلك الاشتراك.

✅ إذا كنتي مشتركة، سؤالي مباشرة على الوصفات أو المكونات لي عندك.

❤️ راني هنا باش نعاونك يا الزينة، قوليلي واش تحبي تطيبي اليوم؟
"""
    )

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("subscribe", subscribe))
    app.add_handler(CommandHandler("approve", approve))
    app.add_handler(CommandHandler("reject", reject))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling() 
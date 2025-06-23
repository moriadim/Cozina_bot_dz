# CozinaBot 🇩🇿🍳

بوت Telegram ذكي باللهجة الجزائرية لمساعدتك في وصفات الطبخ، يعمل بتقنية Google Gemini AI!

---

## 🚀 الميزات
- اقتراح وصفات حسب المكونات المتوفرة
- شرح خطوات التحضير باللهجة الجزائرية
- نظام اشتراك بسيط (3 رسائل مجانية)
- دعم صور وصل الدفع
- يعمل مع Gemini API (Google Generative AI)

---

## 🧰 المتطلبات
- Python 3.9+
- حساب Google AI Studio مع تفعيل Gemini API ([الحصول على API Key](https://aistudio.google.com/app/apikey))
- Telegram Bot Token (من BotFather)

---

## ⚙️ الإعداد

1. **استنسخ المشروع:**
   ```bash
   git clone <repo-url>
   cd <repo-folder>
   ```

2. **أنشئ ملف البيئة (.env):**
   ```env
   TELEGRAM_TOKEN=your-telegram-bot-token
   GOOGLE_API_KEY=your-gemini-api-key
   ADMIN_ID=your-telegram-user-id
   ```

3. **ثبّت المتطلبات:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ▶️ التشغيل محلياً

```bash
python main.py
```

---

## 🐳 التشغيل عبر Docker

1. **ابنِ الصورة:**
   ```bash
   docker build -t cozina-bot .
   ```
2. **شغّل الحاوية:**
   ```bash
   docker run --env-file .env cozina-bot
   ```

---

## 📝 المتغيرات البيئية
| المتغير           | الوصف                                      |
|-------------------|---------------------------------------------|
| TELEGRAM_TOKEN    | رمز بوت Telegram                            |
| GOOGLE_API_KEY    | مفتاح Gemini API من Google AI Studio        |
| ADMIN_ID          | معرف (ID) مدير البوت في Telegram            |

---

## 📦 الملفات المهمة
- `main.py` : كود البوت الرئيسي
- `requirements.txt` : متطلبات التشغيل
- `Dockerfile` : لتشغيل البوت في Docker
- `recipes.json` : وصفات جاهزة (يمكنك تعديلها)
- `subscribers.json` و `limits.json` : بيانات الاشتراك والحدود

---

## 💡 ملاحظات
- يمكنك تعديل `SYSTEM_PROMPT` في `main.py` لتخصيص شخصية البوت.
- إذا واجهت أي مشكلة مع النماذج، جرب تغيير اسم النموذج في الكود (`models/gemini-1.5-flash-latest` أو غيره).
- البوت يدعم الردود باللهجة الجزائرية فقط افتراضياً.

---

## 🧑‍💻 مساهمات
مرحباً بأي مساهمة أو اقتراح! فقط افتح Issue أو Pull Request.

---

## 🥘 صحة وهنا! 
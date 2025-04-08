# Gmail to Telegram Stock Alert Bot 📬 → 🤖

Bu loyiha ThinkOrSwim (TOS) orqali kelgan Gmail xabarlaridan stock signal (alert) larni avtomatik o‘qib,
ularni Telegram guruhiga yuboradigan professional Python tizimidir.

## 🧠 Asosiy funksiyalar

- Gmail'dan `alerts@thinkorswim.com` dan kelgan signal xabarlarni o‘qiydi
- Xabardan ticker va algoritm nomini ajratadi
- `yfinance` orqali asosiy texnik ma’lumotlarni oladi:
  - Narxi (Price)
  - RSI (14)
  - Hajm (Volume)
  - Support va Resistance zonalari
- `Finviz` orqali fundamental tahlil qiladi (Income, P/E, P/B, ROA, ROE va b.)
- `Barchart` orqali Call/Put volume ma’lumotlarini oladi
- `TradingView` grafikni skrinshot qilib Telegramga yuboradi
- 🔥 **Sentimental Analysis** funksiyasi:
  - Yangiliklar sarlavhasini 5 manbadan to‘playdi: Finviz, Reddit, Stocktwits, Marketaux, NewsAPI
  - Har bir sarlavhaga FinBERT orqali NLP asosida baho beradi: 🟢 Positive / 🟡 Neutral / 🔴 Negative
  - Manba kesimida va umumiy Sentiment Score ko‘rinishida chiqaradi

---

## 📦 Telegram xabarning professional ko‘rinishi:

```
💹 Ticker: #TSLA
🧠 Algorithm: RSI_Divergence
--------------------------------
📈 RSI (14): 31.04
📊 Volume: 657k
🔽 Resistance: $250.0
💵 Price: $221.3
🔼 Support: $210.1
--------------------------------
📊 Fundamental Info:
💰 Market Cap: $1.3B
📉 Put Volume: 124
📈 Call Volume: 312
...
📊 Fundamental Score: 6 / 10
🔴 Income: -$910.0M
🟢 P/B: 1.36
...
--------------------------------
📰 Sentimental Score: 16 / 77
🌐 Finviz.com   → Negative
🟢 12  🟡 10  🔴 8
🌐 Reddit       → Neutral
🟢 1   🟡 2   🔴 1
...
--------------------------------
🕒 Time: 15:03, 08.04.2025
🔗 TradingView: https://tradingview.com/chart/?symbol=TSLA
```

---

## 🔐 Maxfiy ma'lumotlar

Loyihada `.env` fayl orqali quyidagi ma'lumotlar yashirin saqlanadi:

- Gmail logini va app password
- Telegram bot tokeni va chat ID
- Reddit, Marketaux, NewsAPI API kalitlari

**Iltimos! `.env` faylni GitHub’ga joylamang.**

`.env.example` fayli namunasi mavjud — uni to‘ldirib, `.env` nomi bilan nusxa oling:

```bash
cp .env.example .env
```

---

## 🚀 Boshlash

```bash
pip install -r requirements.txt
python main.py
```

---

## 📁 Loyihaning struktura asosiy fayllari:

```
GmailToTelegramWithAnalysis/
├── main.py
├── telegram_utils.py
├── chart_utils.py
├── gmail_utils.py
├── finviz_analysis.py
├── finviz_wrapper.py
├── stock_analysis.py
├── barchart_utils.py
├── utils.py
├── sector_standards.py
├── sentimental/
│   ├── news_sentiment.py
│   ├── finbert_sentiment.py
│   └── news_sources/
│       ├── finviz_source.py
│       ├── reddit_source.py
│       ├── stocktwits_source.py
│       ├── marketaux_source.py
│       └── newsapi_source.py
```

---

## 👨‍💻 Muallif

Ushbu loyiha trading va avtomatlashtirishga qiziquvchi tomonidan yaratilgan. 
Yordamchi kuch sifatida ChatGPT ham ishlatilgan 😊

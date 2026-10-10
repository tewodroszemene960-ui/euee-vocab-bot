from datetime import datetime
import pandas as pd
import requests

# 1. Google Sheet እና Telegram ማስተካከያዎች
SHEET_ID = "1lzFiQduv_JiUS3MCUqhZ70KA0ppJRPNpItUl8Tuc6ew"
BOT_TOKEN = "8801487602:AAE41qdLWZb1qdTJnIJx80qs8DqO0pLSmMw"
CHAT_ID = "-1004488635599"

# የፕሮጀክቱ መጀመሪያ ቀን
START_DATE = datetime(2026, 10, 10)

# 2. ከ Google Sheet መረጃ ማንበብ
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=SAT_GMAT_2500_Vocabulary"
def send_daily_vocab():
  try:
    df = pd.read_csv(sheet_url)
    print(f"በተሳካ ሁኔታ ተገናኘ! ጠቅላላ ቃላት ብዛት፦ {len(df)}")
  except Exception as e:
    print(f"ሺቱን ማንበብ አልተቻለም፦ {e}")
    return

  today = datetime.now()
  days_passed = (today - START_DATE).days

  if days_passed < 0:
    days_passed = 0

  start_index = days_passed * 10
  count = 10

  if start_index >= len(df):
    print("🎉 እንኳን ደስ አለህ! 2,400 ቃላቱን ሙሉ በሙሉ ጨርሰሃል!")
    return

  selected_words = df.iloc[start_index : start_index + count]
  day_number = days_passed + 1
  message = f"📚 **EUEE Daily Vocabulary Builder** (Day {day_number}/240)\n\n"

  for idx, row in selected_words.iterrows():
    word = row.iloc[0] if len(row) > 0 else ""
    meaning = row.iloc[1] if len(row) > 1 else ""
    example = row.iloc[2] if len(row) > 2 else ""

    message += f"🔹 Word: {word}\n"
    message += f"📖 Meaning: {meaning}\n"
    if pd.notna(example) and str(example).strip() != "":
      message += f"📝 Example: {example}\n"
    message += "\n" + "—" * 15 + "\n\n"

  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message}

  response = requests.post(url, json=payload)

  if response.status_code == 200:
    print(
        f"✅ የዕለቱ (Day {day_number}) 10 ቃላት በተሳካ ሁኔታ ወደ ቴሌግራም ተልከዋል!"
    )
  else:
    print(f"❌ Error Code: {response.status_code}")
    print(f"❌ Full Response: {response.text}")


if __name__ == "__main__":
  send_daily_vocab()

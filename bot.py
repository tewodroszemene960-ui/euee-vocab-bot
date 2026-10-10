from datetime import datetime
import pandas as pd
import requests

# 1. Google Sheet እና Telegram ማዋቀሪያዎች
SHEET_ID = "1lzFiQduv_JiUS3MCUqhZ70KA0ppJRPNpItUl8Tuc6ew"
BOT_TOKEN = "8925620994:AAHJBv5vKtzVhz35wEXlP01H9qNO5PdHGWc"
CHAT_ID = "@t_h_e_t_h_e12"

# 2. የሚጀምርበት ቀን (October 10, 2026)
START_DATE = datetime(2026, 10, 10)

# 3. ከ Google Sheet ዳታ ማንበብ
sheet_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=SAT_GMAT_2500_Vocabulary"

def send_daily_vocab():
    try:
        df = pd.read_csv(sheet_url)
        print(f"✅ ተሳካ! አጠቃላይ ቃላት ብዛት:- {len(df)}")
    except Exception as e:
        print(f"❌ ማንበብ አልተቻለም:- {e}")
        return

    today = datetime.now()
    days_passed = (today - START_DATE).days

    if days_passed < 0:
        days_passed = 0

    start_index = days_passed * 10
    count = 10

    if start_index >= len(df):
        print("🎉 እንኳን ደስ አለዎት! 2,500 ቃላት በሙሉ ተጠናቀዋል!")
        return

    selected_words = df.iloc[start_index : start_index + count]
    day_number = days_passed + 1

    total_days = (len(df) + count - 1) // count
    message = f"📚 **EUEE Daily Vocabulary Builder** (Day {day_number}/{total_days})\n\n"

    for idx, row in selected_words.iterrows():
        word = str(row.iloc[1]).strip() if len(row) > 1 else ""
        pos = str(row.iloc[2]).strip() if len(row) > 2 else ""
        meaning = str(row.iloc[3]).strip() if len(row) > 3 else ""
        example = str(row.iloc[4]).strip() if len(row) > 4 else ""

        # የ POS ቅንፍ ማስተካከያ
        pos_display = f" {pos}" if pos else ""

        message += f"🔹 **Word:** {word}{pos_display}\n"
        if meaning and meaning.lower() != "nan":
            message += f"📖 **Meaning:** {meaning}\n"
        if example and example.lower() != "nan":
            message += f"📝 **Example:** {example}\n"
        message += "-----------------------------\n\n"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        print(f"✅ ፖስት (Day {day_number}) 10 ቃላት በቴሌግራም ግሩፕ በተሳካ ሁኔታ ተላክዋል!")
    else:
        print(f"❌ Error Code: {response.status_code}")
        print(f"❌ Full Response: {response.text}")

if __name__ == "__main__":
    send_daily_vocab()

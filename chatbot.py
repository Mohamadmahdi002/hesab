import requests
import streamlit as st

# URL و توکن API
url = 'https://api.one-api.ir/chatbot/v1/gpt3.5-turbo/'
api_token = '587749:6745bc6101f0e'

# تابع برای ارسال پیام به API
def send_message(user_message):
    if not user_message.strip():
        st.warning("لطفاً یک پیام وارد کنید!")
        return

    data = [{"role": "user", "content": user_message}]
    headers = {
        'accept': 'application/json',
        'one-api-token': api_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            api_response = result['result'][0]
            return api_response
        else:
            st.error(f"خطای سرور: {response.status_code}")
    except Exception as e:
        st.error(f"مشکلی در اتصال به سرور پیش آمده است:\n{e}")

# رابط کاربری Streamlit
st.set_page_config(page_title="چت بات محمد مهدی حیری", layout="wide")

# بارگذاری فونت ایران‌سنس
st.markdown("""
    <style>
        @import url('https://cdn.fontcdn.ir/fonts/iransans.css');
        body {
            font-family: 'IranSans', sans-serif;
        }
        .stTextInput input {
            text-align: right;
            direction: rtl;
            font-family: 'IranSans', sans-serif;
        }
        .stButton>button {
            text-align: right;
            direction: rtl;
            font-family: 'IranSans', sans-serif;
        }
        .stTextArea>textarea {
            text-align: right;
            direction: rtl;
            font-family: 'IranSans', sans-serif;
        }
        /* راست‌چین کردن دکمه ارسال */
        .send-button-container {
            text-align: right;
            margin-top: 10px;
        }
        .send-button-container button {
            float: right;
            background-color: #2980B9;
            color: white;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            cursor: pointer;
        }
    </style>
""", unsafe_allow_html=True)

# وسط چین کردن عنوان
st.markdown("<h1 style='text-align:center;'>ربات هوش مصنوعی</h1>", unsafe_allow_html=True)

# عنوان فرم ارسال پیام (وسط‌چین)
st.markdown("<h3 style='text-align:center; color:#2980B9;'>پیام خود را وارد کنید</h3>", unsafe_allow_html=True)

# نمایش چت باکس
if 'messages' not in st.session_state:
    st.session_state.messages = []

# ورودی کاربر (راست‌چین)
user_input = st.text_input("پیام خود را وارد کنید:", "", key="user_input", label_visibility="collapsed")

# قرار دادن دکمه ارسال در موقعیت راست‌چین
send_button = st.button("ارسال 🚀", key="send_button", help="ارسال پیام")

# ارسال پیام و نمایش بلافاصله
if send_button:
    user_message = user_input
    if user_message:
        # نمایش پیام کاربر
        st.session_state.messages.append({
            'sender': 'شما',
            'content': user_message
        })
        
        # ارسال پیام به API و دریافت پاسخ
        bot_response = send_message(user_message)
        if bot_response:
            # نمایش پاسخ ربات
            st.session_state.messages.append({
                'sender': 'ربات هوش مصنوعی:',
                'content': bot_response
            })

# نمایش پیام‌های قبلی به صورت مستقیم
for message in st.session_state.messages:
    if message['sender'] == 'شما':
        # پیام‌های کاربر با افکت شیشه‌ای
        st.markdown(
            f"<div style='padding: 10px; text-align:right; direction:rtl; "
            f"background: rgba(0, 0, 0, 0.1); border-radius: 10px; "
            f"color:white; backdrop-filter: blur(10px);'>{message['sender']} : {message['content']}</div>", 
            unsafe_allow_html=True
        )
    else:
        # پیام‌های ربات با افکت شیشه‌ای
        st.markdown(
            f"<div style='padding: 10px; text-align:right; direction:rtl; "
            f"background: rgba(0, 0, 0, 0.1); border-radius: 10px; "
            f"color:white; backdrop-filter: blur(10px);'>{message['sender']} : {message['content']}</div>", 
            unsafe_allow_html=True
        )

# قرار دادن دکمه ارسال در یک بلوک راست‌چین
st.markdown("<div class='send-button-container'></div>", unsafe_allow_html=True)

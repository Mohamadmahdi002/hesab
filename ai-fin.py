import requests
import pandas as pd
import streamlit as st
from io import StringIO
from datetime import datetime, timedelta
import speech_recognition as sr

# URL و توکن API
url = 'https://api.one-api.ir/chatbot/v1/gpt3.5-turbo/'
api_token = '587749:6745bc6101f0e'

# تابع برای ارسال پیام به API
def send_message(user_message, df):
    data = [{"role": "user", "content": f"{user_message}\n\nاین داده‌ها: {df.head().to_string()}"}]
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
            return "خطای سرور: " + str(response.status_code)
    except Exception as e:
        return f"مشکلی در اتصال به سرور پیش آمده است: {e}"

# بارگذاری فایل CSV
def load_csv(file):
    try:
        df = pd.read_csv(file)
        return df
    except Exception as e:
        return str(e)

# ذخیره داده‌ها به فایل CSV در حافظه
def save_csv(df):
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)  # ذخیره بدون ایندکس
    return csv_buffer.getvalue()

# تبدیل متن به CSV
def text_to_csv(text):
    lines = text.split('\n')
    data = [line.split(',') for line in lines]  # فرض بر این است که داده‌ها با کاما جدا شده‌اند
    df = pd.DataFrame(data)
    return df

# تنظیمات اولیه Streamlit
st.set_page_config(page_title="دستیار هوشمند حسابداری", page_icon=":robot:", layout="centered")
st.title("")  # حذف عنوان پیشفرض Streamlit

# استایل‌گذاری متن
st.markdown("""
    <style>
        .welcome-text {
            font-size: 30px;
            font-weight: bold;
            color: #2980B9;
            text-align: center;
        }
        .footer-text {
            font-size: 15px;
            text-align: center;
            color: #34495E;
            font-style: italic;
        }
        .message-box {
            border-radius: 10px;
            padding: 10px;
            background-color: #F0F3F4;
        }
        .chat-history {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #BDC3C7;
            border-radius: 5px;
            background-color: #ECF0F1;
            max-height: 400px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .chat-message {
            margin-bottom: 20px;
        }
        .warning-text {
            color: red;
            font-size: 14px;
            font-weight: bold;
            text-align: center;
        }
        .header-text {
            font-size: 40px;
            font-weight: bold;
            color: #2980B9;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# خوش آمدگویی و نمایش سازنده
st.markdown('<p class="header-text">دستیار هوشمند حسابداری</p>', unsafe_allow_html=True)
st.markdown('<p class="footer-text">سازنده: محمد مهدی حیدری</p>', unsafe_allow_html=True)

# آپلود فایل CSV
uploaded_file = st.file_uploader("فایل CSV خود را آپلود کنید:", type=["csv"])

# تاریخ و زمان ذخیره آخرین تعامل
if 'last_interaction_time' not in st.session_state:
    st.session_state.last_interaction_time = datetime.now()

# بررسی و حذف تاریخچه پس از 24 ساعت
if datetime.now() - st.session_state.last_interaction_time > timedelta(days=1):
    st.session_state.chat_history = []  # حذف تاریخچه پس از 24 ساعت
    st.session_state.last_interaction_time = datetime.now()

# ایجاد فضای پیام‌ها و تاریخچه گفتگوها
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # ذخیره تاریخچه گفتگوها در session_state

if uploaded_file is not None:
    # بارگذاری داده‌ها
    df = load_csv(uploaded_file)
    if isinstance(df, pd.DataFrame):
        st.write("داده‌های فایل CSV:")
        st.dataframe(df)

        # ورودی پیام
        user_message = st.text_input("پیام خود را وارد کنید:", value=st.session_state.get('last_voice_input', ''))  # قرار دادن ورودی پیشفرض

        # دکمه ضبط صدا
        if st.button("ضبط صدا"):
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                st.write("در حال ضبط... لطفاً صحبت کنید.")
                audio = recognizer.listen(source)
                try:
                    user_message = recognizer.recognize_google(audio, language="fa-IR")
                    st.session_state.last_voice_input = user_message  # ذخیره متن تبدیل شده در session_state
                    st.write(f"متن شما: {user_message}")
                except sr.UnknownValueError:
                    st.error("متاسفانه نمی‌توانم صدای شما را بشنوم.")
                except sr.RequestError:
                    st.error("خطا در اتصال به سرویس تبدیل صدا به متن.")

        # ارسال پیام
        if st.button("ارسال پیام"):
            if user_message.strip():
                # ذخیره پیام کاربر در تاریخچه
                st.session_state.chat_history.append(f"شما: {user_message}")

                # دریافت پاسخ از هوش مصنوعی
                response = send_message(user_message, df)
                st.session_state.chat_history.append(f"ربات: {response}")

                # نمایش تاریخچه گفتگوها
                with st.expander("تاریخچه گفتگوها"):
                    for message in st.session_state.chat_history:
                        st.markdown(f'<div class="chat-message">{message}</div>', unsafe_allow_html=True)

                # اعمال تغییرات در داده‌ها (در اینجا یک ستون جدید اضافه می‌شود)
                df['new_column'] = 'تغییر جدید'

                # نمایش دکمه برای دانلود فایل تغییر یافته
                # این بخش از کد حذف شد

                # پاک کردن ورودی پیام
                st.session_state.user_input = ""  # این متغیر دیگر تغییر نخواهد کرد، حذف شد

            else:
                st.warning("لطفاً یک پیام وارد کنید!")

        # نمایش هشدار درباره حذف تاریخچه پس از 24 ساعت
        st.markdown('<p class="warning-text">توجه: تاریخچه گفتگوها پس از 24 ساعت پاک خواهد شد.</p>', unsafe_allow_html=True)

    else:
        st.error(df)  # نمایش خطا در صورت بارگذاری نادرست

# بخش تبدیل متن به CSV
st.markdown('<p class="header-text">تبدیل متن به CSV</p>', unsafe_allow_html=True)
input_text = st.text_area("متن خود را وارد کنید (جداسازی با کاما):")

if st.button("تبدیل به CSV"):
    if input_text.strip():
        # تبدیل متن به DataFrame
        df_from_text = text_to_csv(input_text)

        # ذخیره داده‌های تبدیل‌شده به CSV
        csv_from_text = save_csv(df_from_text)

        # نمایش دکمه برای دانلود فایل CSV
        st.download_button(
            label="دانلود فایل CSV",
            data=csv_from_text,
            file_name="converted_data.csv",
            mime="text/csv"
        )
    else:
        st.warning("لطفاً متن را وارد کنید.")

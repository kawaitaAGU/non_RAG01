# streamlit_dental_exam_ai.py
import streamlit as st
from PIL import Image
import io
import base64
import openai
import pytesseract

# GPTモデル指定
GPT_MODEL = "gpt-4o-2024-11-20"

# secretsからAPIキーを取得
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.title("📸 歯科医師国家試験 画像からAI解説アプリ")

uploaded_file = st.file_uploader("画像ファイルをアップロードしてください（ドラッグ＆ドロップ対応）", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", use_column_width=True)

    with st.spinner("OCR処理中..."):
        ocr_text = pytesseract.image_to_string(image, lang='jpn')

    st.subheader("📝 抽出された問題文")
    st.text(ocr_text)

    prompt = f"""
以下は歯科医師国家試験の問題です。この問題文と選択肢を読み取り、以下を実行してください：
1. 問題の趣旨を200字以内で解説せよ。
2. 各選択肢について、それぞれが正解かどうかに関わらず、知識的背景や解説を加えよ。
3. この問題と関連する類題を3問作成せよ。それぞれについて、問題文・選択肢・正解・解説を含めよ。
必ずですます調で書いてください。

問題全文：
{ocr_text}
"""

    with st.spinner("GPTによる解析中..."):
        response = openai.ChatCompletion.create(
            model=GPT_MODEL,
            messages=[
                {"role": "system", "content": "あなたは歯科医師国家試験の専門家です。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4096  # 多めに設定
        )
        result = response["choices"][0]["message"]["content"]

    st.subheader("📚 GPTによる解説と類題")
    st.markdown(result)

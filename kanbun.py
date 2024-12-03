import openai
import streamlit as st
import pandas as pd

# ตั้งค่า API key ของ OpenAI
openai.api_key = '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'

# ฟังก์ชันในการสร้างกลอนคันบุน (漢文) โดยใช้ OpenAI API (ChatCompletion)
def generate_kanbun(prompt):
    # ส่งคำขอไปยัง ChatGPT เพื่อสร้างกลอน
    response = openai.ChatCompletion.create(
        model="gpt-4",  # หรือ "gpt-3.5-turbo" ถ้าคุณต้องการใช้ GPT-3.5
        messages=[{"role": "system", "content": "คุณคือผู้แต่งกลอนคันบุน (漢文) ที่มีความเชี่ยวชาญ"},
                  {"role": "user", "content": prompt}],
        max_tokens=100,
        temperature=0.7
    )
    
    kanbun = response['choices'][0]['message']['content'].strip()
    return kanbun

# ฟังก์ชันในการแปล漢文 เป็นภาษาอังกฤษ
def translate_kanbun_to_english(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "คุณคือผู้เชี่ยวชาญด้านการแปล漢文เป็นภาษาอังกฤษ"},
                  {"role": "user", "content": f"แปลข้อความ漢文นี้เป็นภาษาอังกฤษ: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    
    translation = response['choices'][0]['message']['content'].strip()
    return translation

# ฟังก์ชันเพื่อดึงคำศัพท์ที่น่าสนใจจาก漢文
def extract_vocabulary(kanbun):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "คุณคือผู้เชี่ยวชาญด้านคำศัพท์จาก漢文"},
                  {"role": "user", "content": f"ช่วยรวบรวมคำศัพท์ที่น่าสนใจจากข้อความ漢文นี้: {kanbun}"}],
        max_tokens=200,
        temperature=0.7
    )
    
    vocabulary = response['choices'][0]['message']['content'].strip()
    return vocabulary

# ฟังก์ชันที่จัดการการแสดงผลลัพธ์ใน Streamlit
def main():
    st.title("AI แต่งกลอน 漢文 (Kanbun)")

    theme = st.text_input("กรุณาระบุธีมของกลอน (เช่น ธรรมชาติ, ฤดู, ดอกไม้):")

    if st.button("สร้างกลอน"):
        if theme:
            prompt = f"สร้างกลอนคันบุน (漢文) ที่เกี่ยวข้องกับ {theme}"
            kanbun = generate_kanbun(prompt)

            # แปล漢文เป็นภาษาอังกฤษ
            translation = translate_kanbun_to_english(kanbun)

            # รวบรวมคำศัพท์ที่น่าสนใจ
            vocabulary = extract_vocabulary(kanbun)

            st.subheader("กลอนคันบุนที่สร้างขึ้น:")
            st.write(kanbun)

            st.subheader("การแปลเป็นภาษาอังกฤษ:")
            st.write(translation)

            st.subheader("คำศัพท์ที่น่าสนใจจาก漢文:")
            st.write(vocabulary)

            data = {
                "ธีม": [theme],
                "กลอนคันบุน": [kanbun],
                "แปลเป็นภาษาอังกฤษ": [translation],
                "คำศัพท์ที่น่าสนใจ": [vocabulary]
            }
            df = pd.DataFrame(data)
            st.subheader("ข้อมูลในรูปแบบตาราง:")
            st.dataframe(df)
        else:
            st.warning("กรุณาระบุธีมของกลอนเพื่อสร้าง")

if __name__ == "__main__":
    main()
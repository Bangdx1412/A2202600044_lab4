import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Load cấu hình
load_dotenv()

# 2. Đọc nội dung System Prompt từ file .txt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_content = f.read()

# 3. Khởi tạo Gemini
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 4. Tạo tin nhắn gửi đi
messages = [
    SystemMessage(content=system_content),
    HumanMessage(content="Chào bạn, tôi muốn đi Đà Nẵng với 5 triệu đồng vào tuần tới.")
]

# 5. Chạy thử
try:
    response = llm.invoke(messages)
    print("--- PHẢN HỒI CỦA AGENT ---")
    print(response.content)
except Exception as e:
    print("Lỗi:", e)
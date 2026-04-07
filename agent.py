import os
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv

# LangGraph & LangChain
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from tools import search_flights, search_hotels, calculate_budget

load_dotenv()

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State (Trạng thái của Agent)
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM (Gemini) và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
# Kết nối các công cụ vào Model
llm_with_tools = llm.bind_tools(tools_list)

# 4. Định nghĩa Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    
    # Nếu chưa có System Prompt trong lịch sử, hãy thêm vào đầu
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    
    response = llm_with_tools.invoke(messages)
    
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"--- 🛠️ Agent gọi tool: {tc['name']}({tc['args']})")
    else:
        print("--- 💬 Agent trả lời trực tiếp")
        
    return {"messages": [response]}

# 5. Xây dựng Graph (Sơ đồ tư duy)
builder = StateGraph(AgentState)

# Thêm các nút (Nodes)
builder.add_node("agent", agent_node)
tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition) 
builder.add_edge("tools", "agent") 

graph = builder.compile()

# 6. Vòng lặp Chat (Chat loop)
if __name__ == "__main__":
    print("=" * 60)
    print("TravelBuddy - Trợ lý Du lịch Thông minh (Gemini Edition)")
    print("Gõ 'quit', 'exit' hoặc 'q' để thoát")
    print("=" * 60)
    chat_history = []
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        print("\nTravelBuddy đang suy nghĩ...")
        # Chạy Agent với input từ người dùng
        chat_history.append(HumanMessage(content=user_input))
        
        # Gửi toàn bộ lịch sử cho Agent
        result = graph.invoke({"messages": chat_history})
        
        # Cập nhật lại lịch sử từ kết quả trả về (để lưu cả câu trả lời của AI)
        chat_history = result["messages"]
        
        final_message = chat_history[-1]
        if isinstance(final_message.content, list):
                # Tìm phần tử chứa text trong danh sách content
                text_content = next((item['text'] for item in final_message.content if item['type'] == 'text'), "")
                print(f"\nTravelBuddy: {text_content}")
        else:
            print(f"\nTravelBuddy: {final_message.content}")
import os
from langgraph.checkpoint.memory import MemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv

load_dotenv(override=True)

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM (Sử dụng Gemini thay vì OpenAI) và Tools
tools_list = [search_flights, search_hotels, calculate_budget]

# Sử dụng gemini-2.5-flash
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    # Thêm SystemPrompt nếu chưa có trong lịch sử
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
        
    response = llm_with_tools.invoke(messages)

    # === LOGGING ===
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  [Log] Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"  [Log] Trả lời trực tiếp")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

# --- THÊM BỘ NHỚ ---
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 6. Chat loop
# 6. Chat loop
if __name__ == "__main__":
    print("=" * 60)
    print(" TravelBuddy - Trợ lý Du lịch Thông minh (Powered by Gemini) ")
    print(" Gõ 'quit' hoặc 'q' để thoát")
    print("=" * 60)
    
    # Khai báo config chứa thread_id để Agent nhớ ngữ cảnh xuyên suốt cuộc hội thoại
    config = {"configurable": {"thread_id": "phien_chat_01"}}
    
    while True:
        user_input = input("\nBạn: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
            
        print("\nTravelBuddy đang suy nghĩ...")
        # Truyền thêm config vào hàm invoke
        result = graph.invoke({"messages": [("human", user_input)]}, config=config)
        final = result["messages"][-1]
        
        # Xử lý triệt để lỗi in ra dạng List/JSON của Gemini
        if isinstance(final.content, str):
            print(f"\nTravelBuddy: {final.content}")
        elif isinstance(final.content, list):
            text_content = "".join(block.get("text", "") for block in final.content if isinstance(block, dict) and "text" in block)
            print(f"\nTravelBuddy: {text_content}")
        else:
            print(f"\nTravelBuddy: {str(final.content)}")
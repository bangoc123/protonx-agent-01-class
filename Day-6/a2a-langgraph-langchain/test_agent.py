from agent import LangGraphAgent

agent = LangGraphAgent()

response = agent.invoke("Cho tôi thông tin điện thoại?", "user123")
print(response)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class AgentPrompts:
    """Container for all agent-related prompts"""
    
    @staticmethod
    def get_main_prompt() -> ChatPromptTemplate:
        """Returns the main agent prompt template"""
        return ChatPromptTemplate.from_messages([
            ("system", (
                "You're a helpful assistant. When answering a user's question "
                "you should first use one of the tools provided. After using a "
                "tool the tool output will be provided back to you. When you have "
                "all the information you need, you MUST use the final_answer tool "
                "to provide a final answer to the user. Use tools to answer the "
                "user's CURRENT question, not previous questions."
            )),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ])
    
    @staticmethod
    def get_fallback_prompt() -> ChatPromptTemplate:
        """Returns a fallback prompt if needed"""
        return ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant."),
            ("human", "{input}")
        ])
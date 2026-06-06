import streamlit as st
from guards import validate_input
from chatbot import BankingChatbot

st.set_page_config(page_title="SecureBank AI Assistant", layout="wide")

# Hide Deploy button and Hamburger menu
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chatbot" not in st.session_state:
    st.session_state.chatbot = BankingChatbot()
if "last_json" not in st.session_state:
    st.session_state.last_json = None

st.title("🏦 SecureBank AI Customer Service")

st.markdown("Welcome! I can provide information on a variety of banking-related topics including savings accounts, fixed deposits, loans (home, personal, car, education), credit cards, UPI and NEFT/RTGS transactions, interest rates, account policies, and grievance redressal processes. How can I assist you today?")

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input("How can I help you today?"):
    # 1. Display User Message
    st.chat_message("user").markdown(prompt)
    
    # 2. Run Guardrails
    is_safe, error_msg = validate_input(prompt)
    
    if not is_safe:
        with st.chat_message("assistant"):
            st.warning(error_msg)
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    else:
        # 3. Process with Chatbot
        with st.spinner("Thinking..."):
            # Prepare history for the model
            history = []
            # More robust history parsing
            msgs = st.session_state.messages
            for i in range(len(msgs)):
                if msgs[i]["role"] == "user" and i + 1 < len(msgs):
                    if msgs[i+1]["role"] == "assistant":
                        history.append({
                            "user": msgs[i]["content"],
                            "bot": msgs[i+1]["content"]
                        })
            
            response_obj = st.session_state.chatbot.generate_response(prompt, history)
            
            # Update session states
            st.session_state.last_json = response_obj.model_dump()
            
            # 4. Display Assistant Response
            with st.chat_message("assistant"):
                st.markdown(response_obj.advisor_response)
                
                if response_obj.escalation_required:
                    st.error(f"⚠️ Escalation Required: {response_obj.escalation_reason or 'Agent needed.'}")
                
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.messages.append({"role": "assistant", "content": response_obj.advisor_response})

# Footer
st.divider()
st.caption("SecureBank AI can make mistakes. PII is automatically filtered.")
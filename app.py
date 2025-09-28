import streamlit as st
import json
import os
from chatbot_agent import get_ai_response

USER_DB = "users.json"
CHAT_DB = "chats.json"



def load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


users = load_json(USER_DB, {})
chats = load_json(CHAT_DB, {})


st.set_page_config(page_title="Islamic Assistant Chatbot", layout="centered")

st.title("Islamic Assistant Chatbot")
st.caption("Your guide for thoughtful answers, according to Islam. Powered by Gemini 2.5 Flash Lite.")


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None


def register():
    st.subheader("📝 Create Account")
    new_user = st.text_input("Choose a username")
    new_pass = st.text_input("Choose a password", type="password")

    if st.button("Sign Up"):
        if new_user in users:
            st.error(" Username already exists.")
        elif new_user.strip() == "" or new_pass.strip() == "":
            st.error("Username and password cannot be empty.")
        else:
            users[new_user] = new_pass
            chats[new_user] = [
                {"role": "assistant", "content": "As-salamu alaykum! How can I help you today?"}
            ]
            save_json(USER_DB, users)
            save_json(CHAT_DB, chats)
            st.success("Account created! Please login now.")



def login():
    st.subheader("🔐 Login")
    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")

    if st.button("Login"):
        if username_input in users and users[username_input] == password_input:
            st.session_state.authenticated = True
            st.session_state.username = username_input
            st.rerun()
        else:
            st.error("Invalid username or password")

    st.markdown("---")
    if st.button("Create an Account"):
        st.session_state.show_register = True
        st.rerun()



def logout():
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()



def chat_ui():
    username = st.session_state.username
    user_chats = chats.get(username, [])

   
    for msg in user_chats:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])



    if prompt := st.chat_input("Ask your question..."):
        user_chats.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = get_ai_response(prompt)
                st.markdown(ai_response)

        user_chats.append({"role": "assistant", "content": ai_response})

        
        chats[username] = user_chats
        save_json(CHAT_DB, chats)

    logout()



if "show_register" not in st.session_state:
    st.session_state.show_register = False

if not st.session_state.authenticated:
    if st.session_state.show_register:
        register()
    else:
        login()
else:
    chat_ui()

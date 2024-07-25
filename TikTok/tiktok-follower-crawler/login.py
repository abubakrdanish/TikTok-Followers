import streamlit as st

def login(username, password):
    # In a real-world application, use a secure method to verify username and password
    if username == "admin" and password == "password":
        return True
    else:
        return False

def show_login():
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(username, password):
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

# Initialize session state if not already done
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

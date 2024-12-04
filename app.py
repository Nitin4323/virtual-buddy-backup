import streamlit as st
import requests
import os
from dotenv import load_dotenv
from htmlTemplate import css, bot_template, user_template, header
import time

BACKEND_URL = os.getenv("BACKEND_URL","http://localhost:8000")  

def register():
    st.subheader("Register")
    username = st.text_input("Username", key="register_username",disabled=st.session_state.is_login)
    password = st.text_input("Password", type="password", key="register_password",disabled=st.session_state.is_login)
    if st.button("Register",disabled=st.session_state.is_login):
        try :   
            response = requests.post(f"{BACKEND_URL}/register", json={"username": username, "password": password})
            if response.status_code == 200:
                st.success("Registration successful! Please login.")

            else:
                st.error(response.json().get("detail", "Registration failed"))
        except Exception as e :
            st.info("Server Down")

def login():
    st.subheader("Login")
    username = st.text_input("Username", key="login_username",disabled=st.session_state.is_login)
    password = st.text_input("Password", type="password", key="login_password",disabled=st.session_state.is_login)

    if st.button("Login",disabled=st.session_state.is_login):
        try : 
            response = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})
            if response.status_code == 200:
                st.session_state.user_id = response.json()["user_id"]
                st.session_state.is_admin = response.json()["is_admin"]
                st.session_state.is_login = True
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(response.json().get("detail", "Login failed"))
        except Exception as e :
            st.info("Server Down")

        
def create_admin():
    # st.sidebar.subheader("Create Admin")
    with st.sidebar:
        st.subheader("Add admin")
        with st.form("Create Admin", clear_on_submit=True):
            username = st.text_input("Admin Username", key="admin_username")
            password = st.text_input("Admin Password", type="password", key="admin_password")
            submit_button = st.form_submit_button(label="Submit")
            if submit_button:
                st.session_state.chat_animation_effect = False
                print("reached here")
                try :
                    response = requests.post(f"{BACKEND_URL}/create_admin", json={"username": username, "password": password})
                    if response.status_code == 200:
                        st.sidebar.success("Admin created successfully!")
                    else:
                        st.sidebar.error(response.json().get("detail", "Failed to create admin"))
                except Exception as e:
                    st.info(f"Error occured : {e}")

def chat_interface():

    if st.session_state.is_admin:
        st.markdown('<div class="admin-badge">Admin User</div>', unsafe_allow_html=True)

    with st.form(key='user_input_form', clear_on_submit=True):
        user_input = st.text_input("Ask a question:")
        submit = st.form_submit_button(label="Send")

    if submit and user_input:
        with st.spinner("Fetching llm response..."):
            try : 
                response = requests.post(f"{BACKEND_URL}/chat", json={"user_id": 1, "message": user_input})
                if response.status_code == 200 :
                    answer = response.json()['response']
                    print("answer : ",answer)
                    st.session_state.chat_animation_effect = True
                st.session_state['history'].append((user_input, answer))
            except Exception as e : 
                st.info(e)
    
    if st.session_state['history']:
        latest_question, latest_answer = st.session_state['history'][-1]
        st.markdown(user_template.replace("{{MSG}}", latest_question), unsafe_allow_html=True)
        if st.session_state.chat_animation_effect:
            display_response_with_animation(latest_answer)
        else:
            st.write(bot_template.replace("{{MSG}}", latest_answer), unsafe_allow_html=True)

    for idx, (question, answer) in enumerate(reversed(st.session_state['history'][:-1])):
        # st.write(f"**You**: {question}")
        st.write(user_template.replace("{{MSG}}", question), unsafe_allow_html=True)
        st.write(bot_template.replace("{{MSG}}", answer), unsafe_allow_html=True)

def display_response_with_animation(answer):
    displayed_text = ""
    response_container = st.empty()
    for char in answer:
        displayed_text += char
        response_container.markdown(bot_template.replace("{{MSG}}", displayed_text), unsafe_allow_html=True)
        time.sleep(0.05)  

def upload_feature():
    with st.sidebar:
        st.subheader("Upload Files")
        uploaded_files = st.file_uploader(label="Upload file and click on Process",
                                        type=['pdf','docx'],
                                        accept_multiple_files=True)
        st.session_state.chat_animation_effect = False
        if st.button("process"):
            with st.spinner("Processing...."):
                for file in uploaded_files:
                    try :
                        response = requests.post(f"{BACKEND_URL}/upload_pdf",files={"file": (file.name, file, "application/pdf")})
                        if response.status_code == 200:
                            st.success(f"{file.name} uploaded successfully", icon="✅")
                        else:
                            st.error(f"Failed to upload {file.name}", icon="🚨")
                    except Exception as e:
                        st.error(f"Exception occured : {e}")

def file_management_feature():
    with st.sidebar:
        st.subheader("Files to remove")
        try : 
            response = requests.get(f"{BACKEND_URL}/list-files/")
            if response.status_code == 404:
                st.info("No files found in the directory.")

            elif response.status_code == 200:
                files = response.json().get("files", [])
                if files:
                    selected_file = st.multiselect("Select a file to delete", files)
                    
                    if st.button("Delete Selected File"):
                        with st.spinner("Deleting files...."):
                            for file in selected_file :
                                delete_response = requests.delete(f"{BACKEND_URL}/delete-file/", params={"filename": file})
                                # st.session_state.chat_animation_effect = False
                                if delete_response.status_code == 200:
                                    st.success(delete_response.json().get("message", "File deleted successfully."))
                                else:
                                    st.error(delete_response.json().get("detail", "Error deleting file."))
                else:
                    st.info("No files found in the directory.")
            else:
                st.error(f"Error fetching file list: {response.json().get('detail', 'Unknown error')}")
        except Exception as e:
            st.info("Backend is down.")

def main():

    load_dotenv()
    
    st.write(css, unsafe_allow_html=True)
    st.markdown(header,unsafe_allow_html=True)

    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "is_login" not in st.session_state:
        st.session_state.is_login = False


    if 'history' not in st.session_state:
        st.session_state['history'] = []
    if 'chat_animation_effect' not in st.session_state:
        st.session_state.chat_animation_effect=False
    if 'list_file_stop' not in st.session_state:
        st.session_state.list_file_stop=False

    if not st.session_state.is_login:
        choice = st.radio("Choose", ["Login", "New User?"])
        if choice == "New User?":
            register()
        else:
            login() 
    
    else:
        if st.session_state.is_admin:
            upload_feature()
            st.sidebar.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
            file_management_feature()
            st.sidebar.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
            create_admin()

        chat_interface()

        st.sidebar.markdown("<hr style='border: 1px solid #ddd;'>", unsafe_allow_html=True)
        if st.sidebar.button("Logout",key="logout"):
            st.session_state.user_id = None
            st.session_state.is_login = False
            st.session_state.is_admin = False
            login()
            st.rerun()


if __name__=='__main__':
    main()
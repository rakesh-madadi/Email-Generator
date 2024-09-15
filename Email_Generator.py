import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import openai
import os
from dotenv import load_dotenv
load_dotenv()


api_key=os.getenv("OPENAI_API_KEY")

print(api_key)

openai.api_key=api_key

def load_candidates_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)
        if not all(column in df.columns for column in ['Name', 'Email', 'Position']):
            raise ValueError("The Excel file must contain 'Name', 'Email', and 'Position' columns.")
        return df['Name'].tolist(), df.set_index('Name')['Email'].to_dict(), df.set_index('Name')['Position'].to_dict()
    except FileNotFoundError:
        st.error(f"File {file_path} not found. Please upload the correct file.")
        return [], {}, {}
    except Exception as e:
        st.error(f"Failed to load candidates from Excel: {e}")
        return [], {}, {}

# Function to generate email content using OpenAI API
def generate_email_content(candidate_name, candidate_position, interviewer, interview_date, interview_time):
    # Define the chat-based prompt
    messages = [
        {"role": "system", "content": "You are an assistant that writes professional emails."},
        {"role": "user", "content": f"""
        Generate an email invitation for an interview from the company 'Data FactZ' with the address 'Prime Towers, 4th floor, Hyderabad'.
        Candidate: {candidate_name}
        Position: {candidate_position}
        Interviewer: {interviewer}
        Interview Date: {interview_date}
        Interview Time: {interview_time}
        The email should include a polite introduction from 'Data FactZ', details of the interview, and a closing.
        please end the email with regards from the interviewer only use term regards
        please use correct email format 
        Please mention the company address at the end.
        """}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500
        )
        # Get the content of the generated response
        email_body = response.choices[0].message['content'].strip()
        return email_body
    except openai.error.OpenAIError as e:
        st.error(f"Failed to generate email content: {e}")
        return "Failed to generate email content."
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        return "Failed to generate email content."

# Function to send the email using SMTP
def send_email(candidate_name, candidate_email, email_content):
    sender_email = os.getenv("sender_email") 
    password = os.getenv("password") 

    if not sender_email or not password:
        st.error("Missing sender email or password in environment variables.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = candidate_email
    msg['Subject'] = "Interview Invitation"

    msg.attach(MIMEText(email_content, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, candidate_email, msg.as_string())
        server.quit()
        st.success("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        st.error("SMTP Authentication failed. Check your email credentials.")
    except smtplib.SMTPConnectError:
        st.error("Failed to connect to the SMTP server. Check your internet connection.")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Page 1: Candidate and Interviewer Selection
def page_selection():
    st.image('data_factz_logo.png', width=150)
    st.title("Candidate and Interviewer Selection")

    candidates_file = 'candidates.xlsx'
    
    # Load candidate names, emails, and positions from Excel file
    candidate_names, candidate_emails, candidate_positions = load_candidates_from_excel(candidates_file)
    
    if not candidate_names:
        return

    candidate = st.selectbox("Select Candidate", candidate_names)
    interviewers = ['HR-Kishor', 'Manager-Tushar', 'Manager-Vinayak']
    interviewer = st.selectbox("Select Interviewer", interviewers, index=0)

    if st.button("Next"):
        st.session_state['candidate'] = candidate
        st.session_state['interviewer'] = interviewer
        st.session_state['candidate_email'] = candidate_emails[candidate]  
        st.session_state['candidate_position'] = candidate_positions[candidate]
        st.session_state['page'] = 'email_generation'

# Page 2: Email Generation and Sending
def page_email_generation():
    st.image('data_factz_logo.png', width=150)
    st.title("Email Generation")

    try:
        candidate = st.session_state['candidate']
        interviewer = st.session_state['interviewer']
        candidate_email = st.session_state['candidate_email']
        candidate_position = st.session_state['candidate_position']

        st.write(f"Candidate: {candidate}")
        st.write(f"Position: {candidate_position}")
        st.write(f"Interviewer: {interviewer}")
        st.write(f"Email: {candidate_email}")

        interview_date = st.date_input("Interview Date")
        interview_time = st.time_input("Interview Time")

        if st.button("Generate Email"):
            email_content = generate_email_content(candidate, candidate_position, interviewer, interview_date, interview_time)
            st.session_state['email_content'] = email_content
            st.session_state['editable'] = False

        if 'email_content' in st.session_state:
            if not st.session_state.get('editable', False):
                st.subheader("Email Preview")
                st.write(st.session_state['email_content'])
                if st.button("Edit Email"):
                    st.session_state['editable'] = True
            else:
                st.subheader("Edit Email Content")
                editable_email_content = st.text_area("Edit the email content below:", value=st.session_state['email_content'], height=300)
                st.session_state['email_content'] = editable_email_content
                if st.button("Save Changes"):
                    st.session_state['editable'] = False
                    st.success("Changes saved successfully!")

            if st.button("Send Email"):
                send_email(candidate, candidate_email, st.session_state['email_content'])

        else:
            st.warning("Please generate the email first.")
    except KeyError:
        st.error("Session data is missing. Please go back to the selection page.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")

# Streamlit app navigation logic
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'selection'

    if st.session_state['page'] == 'selection':
        page_selection()
    elif st.session_state['page'] == 'email_generation':
        page_email_generation()

if __name__ == "__main__":
    main()

# Email-GeneratorHere's a structured **README.md** file for your GitHub repository, which provides an overview of the project, setup instructions, and usage details:

---

# Shortlisting and Interview Notification System

This Streamlit application simplifies the process of sending interview notification emails. It allows users to select candidates and interviewers, generate professional interview invitation emails using OpenAI's GPT-4, and send them via email through the SMTP server.

## Features
- **Candidate Selection**: Load candidate details (name, email, and position) from an Excel file.
- **Interviewer Selection**: Choose from a predefined list of interviewers.
- **Email Generation**: Automatically generate professional interview invitation emails using the OpenAI GPT-4 API.
- **Email Customization**: Preview and edit generated emails before sending.
- **Email Sending**: Send the generated email to the selected candidate via Gmail SMTP.

## Project Structure
```bash
.
├── app.py              # Main Streamlit application file
├── .env                # Environment variables file (contains OpenAI and SMTP credentials)
├── candidates.xlsx     # Excel file containing candidate details
├── README.md           # This file
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- [Streamlit](https://streamlit.io/)
- An OpenAI account with API access (GPT-4 API)
- Gmail account with [App Password](https://support.google.com/accounts/answer/185833?hl=en) for SMTP access

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/shortlisting-interview-notification-system.git
    cd shortlisting-interview-notification-system
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables**:

    - Create a `.env` file in the project root:
      ```bash
      touch .env
      ```

    - Add the following environment variables to `.env`:
      ```
      OPENAI_API_KEY=your_openai_api_key
      sender_email=your_email@gmail.com
      password=your_gmail_app_password
      ```

4. **Prepare Candidate Data**:
    - Ensure that the `candidates.xlsx` file contains the following columns:
        - `Name`: Candidate's full name
        - `Email`: Candidate's email address
        - `Position`: Job position for which the candidate is being interviewed

### Running the Application

To run the Streamlit app locally, execute the following command:

```bash
streamlit run app.py
```

This will launch the application in your default web browser.

### Usage

1. **Page 1: Candidate and Interviewer Selection**:
    - Upload the `candidates.xlsx` file, and select a candidate and interviewer.
    - Click `Next` to proceed to the email generation page.

2. **Page 2: Email Generation**:
    - Enter the interview date and time.
    - Generate the email invitation using the `Generate Email` button.
    - Preview the generated email and optionally edit the content.
    - Once finalized, click `Send Email` to send the email to the selected candidate.

### Troubleshooting

- **SMTP Authentication Error**: Ensure you are using the correct Gmail app password and have enabled "less secure apps" in your Gmail account settings.
- **OpenAI API Error**: Make sure your API key is valid and you have enough quota for generating responses.

### Future Enhancements

- Integrate more advanced email customization options.
- Add support for other email providers (e.g., Outlook, Yahoo).
- Implement automated scheduling for sending emails.

### License

This project is licensed under the MIT License.

---

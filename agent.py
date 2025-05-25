#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mistralai import Mistral
import base64
import os
import imaplib
import email
from email.header import decode_header

MISTRAL_API_KEY = "ENTER YOUR KEY"
api_key = MISTRAL_API_KEY
client = Mistral(api_key=api_key)

#%%
def encode_pdf(pdf_path):
    """Encode the pdf to base64."""
    try:
        with open(pdf_path, "rb") as pdf_file:
            return base64.b64encode(pdf_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {pdf_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None


def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None
    
#%%
text_model = "mistral-small-latest"
ocr_model = "mistral-ocr-latest"

system = system = """You are an AI Assistant meant to help people with their paperwork. You have document understanding via PDFs and have access to the user email inbox and can extract all the emails recieved by a specific sender.
You will be provided with PDFs and email transcripts, and you must answer any questions related to those documents.
In your working directory there is a target.pdf file which is the paperwork to do, there is also a ./user_data directory that contains PDFs and images you will perform OCR on them to get the relevant data to do the paperwork.

# FETCH EMAILS INSTRUCTIONS
You can access a mail inbox and get all the emails recieved by a specific person by using the `fetch_emails` tool. It sill open a txt concatenating all the emails,
Use this to refine the context of the user query and extract the informations you are asked for.

# OPEN PDFs INSTRUCTIONS
You can open PDFs by using the `open_pdfs` tool. It will open pdfs and apply OCR to them, retrieving the contents. Use those contents to answer the user.
Only PDFs and images are supported; you may encounter an error if they are not; provide that information to the user if required.

# EDIT TXT INSTRUCTIONS
You can create a TXT file by using the `edit_txt` tool. It will open or create a txt document and save your output.

"""

def _perform_ocr(path: str) -> str:
    try:   # Apply OCR to the PDF located in the PATH
        # Getting the base64 string
        print(f"performing ocr on {path}")
        base64_pdf = encode_pdf(path)
        ocr_response = client.ocr.process(
            model="mistral-ocr-latest",
            document={
                "type": "document_url",
                "document_url": f"data:application/pdf;base64,{base64_pdf}" 
            },
            include_image_base64=True
        )
    except Exception:
        try:  # IF PDF OCR fails, try Image OCR
            print(f"performing ocr on {path}")
            base64_image = encode_image(path)
            ocr_response = client.ocr.process(
                model="mistral-ocr-latest",
                document={
                    "type": "image_url",
                    "image_url": f"data:image/jpeg;base64,{base64_image}" 
                },
                include_image_base64=True
            )
        except Exception as e:
            return e  # Return the error to the model if it fails, otherwise return the contents
    return "\n\n".join([f"### Page {i+1}\n{ocr_response.pages[i].markdown}" for i in range(len(ocr_response.pages))])


def open_pdfs(paths: list) -> str:
    if paths[0] == "./user_data":
        paths = os.listdir("./user_data")
        paths = ["./user_data/"+path for path in paths]
    contents = "# Documents"
    for path in paths:
        contents += f"\n\n## PATH: {path}\n{_perform_ocr(path)}"
    return contents

def fetch_emails(sender: str) -> str:
    sender = sender[0] # for some reason the parameter is passed as ["sender"]
    content = ""
    # Connect to the IMAP server
    #imap_server = "imaps.ens-lyon.fr"
    imap_server = "imaps.YOUR DOMAIN"
    #username = "ayoub.dhibi@ens-lyon.fr"
    username = "YOUR USERNAME"
    password = "YOUR PASSWORD "  # Use App Password if 2FA is enabled

    # Create an IMAP4 class with SSL 
    mail = imaplib.IMAP4_SSL(imap_server)

    # Log in to the server
    mail.login(username, password)

    # Select the mailbox you want to search, in this case, the inbox
    mail.select("inbox")

    # Search for specific emails in this case the email sent by "sender"
    status, messages = mail.search(None, f'(FROM "{sender}")')
    # Fetch the list of email IDs
    email_ids = messages[0].split()
    
    ## Fetch the latest email
    #for email_id in email_ids[-1:]:
    
    # Fetch all emails
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, "(RFC822)")
    
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the message into an email object
                msg = email.message_from_bytes(response_part[1])
    
                # Decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # If it's a bytes type, decode to str
                    subject = subject.decode(encoding if encoding else "utf-8")
                content += "\n Subject:" + str(subject)
    
                # Decode the sender's email address
                from_ = msg.get("From")
                content += "\n From:"  + str(from_)
    
                # If the email message is multipart
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
    
                        if "attachment" not in content_disposition:
                            # Get the email body
                            if content_type == "text/plain":
                                body = part.get_payload(decode=True)
                                content += "\n Body:" + str(body.decode())
                else:
                    # The email body is not multipart
                    body = msg.get_payload(decode=True)
                    content += "\n Body:" + str(body.decode())
                    
    # Logout from the server
    mail.logout()
    return content


#%%
tools = [
    {
        "type": "function",
        "function": {
            "name": "open_pdfs",
            "description": "Open PDFs and Images and perform OCR on them.",
            "parameters": {
                "type": "object",
                "properties": {
                    "paths": {
                        "type": "array",
                        "description": "Path to the PDFs or the directory containing them.",
                    }
                },
                "required": ["paths"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "fetch_emails",
            "description": "Get all the emails exchanged between the user and the sender",
            "parameters": {
                "type": "object",
                "properties": {
                    "sender": {
                        "type": "array",
                        "description": "Sender name, the person that sent emails to the user",
                    }
                },
                "required": ["sender"],
            },
        },
    },
]
names_to_functions = {
    'open_pdfs': open_pdfs,
    'fetch_emails': fetch_emails
    
}


#%%
import json
def chatbot(user_input, messages):
    
    messages.append({"role": "user", "content": user_input})
    # Loop Mistral Small tool use until no tool called
    while True:
        response = client.chat.complete(
            model = text_model,
            messages = messages,
            temperature = 0,
            tools = tools
        )
        messages.append({"role":"assistant", "content": response.choices[0].message.content, "tool_calls": response.choices[0].message.tool_calls})

        # If tool called, run tool and continue, else break loop and reply
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]
            function_name = tool_call.function.name
            function_params = json.loads(tool_call.function.arguments)
            function_result = names_to_functions[function_name](**function_params)
            messages.append({"role":"tool", "name":function_name, "content":function_result, "tool_call_id":tool_call.id})
        else:
            break

    return response.choices[0].message.content, messages

    

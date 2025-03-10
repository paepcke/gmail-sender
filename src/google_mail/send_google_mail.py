 # **********************************************************
 #
 # @Author: Andreas Paepcke
 # @Date:   2025-03-10 11:59:34
 # @Last Modified by:   Andreas Paepcke
 # @Last Modified time: 2025-03-10 16:41:16
 #
 # **********************************************************
import base64
import os.path
from pathlib import Path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Module provides the facility to send emails from a fixed 
# GMAIL sender account after proper setup. 
#
# Assumptions:
#    o This application has been registered as an OAuth 2.0 Client.
#    o $HOME/.ssh/MailThroughGoogle contains
#
#          * credentials.json and/or token.json
#          * sender_account.txt 
#
# The credentials.json holds this application's Google secret for
# obtaining an API usage token token.json. The credentials.json are
# used once to obtain token.json. This latter file is passed along
# with every Gmail send request.

class GmailSender:

    # Scopes for which this application should have rights
    SCOPES = ['https://mail.google.com/']
    #SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    home_dir   = Path.home()
    GMAIL_ROOT = home_dir / '.ssh/MailThroughGoogle'
    
    #------------------------------------
    # Constructor
    #-------------------    

    def __init__(self):

        # For convenience:
        gmail_root = GmailSender.GMAIL_ROOT
        
        self.api_token_path = gmail_root / 'token.json'
        self.creds_path     = gmail_root / 'credentials.json'
        
        sender_path = gmail_root / 'send_account.txt'

        try:
            with open(sender_path, 'r') as fd:
                self.sender = fd.read().strip()
        except FileNotFoundError as e:
            err_msg = f"Directory ${gmail_root} must contain token.json or credentials.json, plus sender.txt. The latter is missing"
            raise FileNotFoundError(err_msg)

        self.service = self.get_gmail_service()

    #------------------------------------
    # send_gmail
    #-------------------

    def send_gmail(self, recipient, subject, body):
        message_dict = self.create_message(self.sender,
                                           recipient, 
                                           subject,
                                           body)        
        
        self.send_message_impl(message_dict)


    #------------------------------------
    # create_message
    #-------------------    

    def create_message(self, sender, to, subject, message_text):
        '''
        Reuturns a wire-ready message in form expected
        by the Gmail smtp server

        :param sender: email address of Gmail account from 
            which the msg is sent
        :type sender: str
        :param to: email address of recipient
        :type to: str
        :param subject: email's subject line
        :type subject: str
        :param message_text: body
        :type message_text: str
        :return: a dict with properly encoded, wire-ready
            content. May be passed to send_message_impl
            for sending
        :rtype: dict
        '''
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode('utf-8'))
        return {'raw': raw_message.decode('utf-8')} #important to decode the byte object to string.    

    #------------------------------------
    # send_message_impl
    #-------------------

    def send_message_impl(self, message):
        '''
        Nitty gritty of sending a Gmail message prepared
        in create_message()

        :param message: a wire-ready email message 
        :type message: dict
        :raises RuntimeError: if Gmail rejects or is otherwise
            unhappy with the message
        '''
        try:
            message = (self.service.users().messages().send(userId=self.sender, body=message)
                        .execute())
            # print('Message Id: %s' % message['id'])
            return message
        except Exception as e:
            raise RuntimeError(e)

    #------------------------------------
    # get_gmail_service
    #-------------------
    
    def get_gmail_service(self):
        '''
        Return a Gmail service instance. Used for two 
        phases:

          1. One-time obtaining of a token.json file 
             from a credentials.json file that is associated
             with an application.

          2. Service instantiation using the token.json file
             that is available from phase 1.

        :return: a Gmail service object
        :rtype: object
        '''
        creds = None
        if os.path.exists(self.api_token_path):
            creds = Credentials.from_authorized_user_file(self.api_token_path, GmailSender.SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, GmailSender.SCOPES)
                creds = flow.run_local_server(port=0)
            with open(self.api_token_path, 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

# ------------------------ Main ------------
if __name__ == '__main__':
    # Used only once to obtain token.json. Opens a browser
    # window and allows downloading of token.json. That file
    # must go into whatever GmailSendewr.GMAIL_ROOT is set to:

    sender = GmailSender()
    # Send a message to the account that will
    # be used by this application for future email
    # sending:

    sender.send_gmail(sender.sender, "Obtaining an API token", "Dummy body")
    print("Downloaded token.json.")
    
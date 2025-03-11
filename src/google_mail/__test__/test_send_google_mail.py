 # **********************************************************
 #
 # @Author: Andreas Paepcke
 # @Date:   2025-03-11 12:36:44
 # @Last Modified by:   Andreas Paepcke
 # @Last Modified time: 2025-03-11 13:15:12
 #
 # **********************************************************

from google_mail.send_google_mail import GmailSender

def main():
    GmailSender().send_gmail('paepcke@cs.stanford.edu', 'Test from send_google_mail.py', 'This is the body')

if __name__ == "__main__":
    main()

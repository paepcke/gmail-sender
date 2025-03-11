# gmail-sender
Sends emails programmatically using OAuth2 credentials

The biggest chore is to register the application that uses this
package with Google's labyrinthine OAuth2 machinery. Its Web
pages seem to change often. Below is a very rough outline.

After you accomplished that, and placed the three files,
credentials.json, token.json, and send_account.txt into
$HOME/.ssh/MailThroughGoogle/, it's easy. You import the
GmailSender class, and call


- Sending Gmails from Python:

  Must create an OAuth2 Client to represent your Python application.
  You specify a 'scope', meaning the extent of data that your
  application is allowed to access. Example:

    https://www.googleapis.com/auth/gmail.send

  for sending email.

  All the admin work is via the Google Cloud Console.

  Start at https://console.cloud.google.com/, or google for
  "Google Cloud Console".

    - Create an OAuth2 Client from the console
    - After first creating an OAuth 2.0 Client Id, or
      to make changes to scope, or to get a re-authorization token for
      automatically extending authorization:

        - Go to the Google Cloud console
        - APIs & Services --> Credentials
        - Select your OAuth 2.0 Client ID
        - Left hand nav bar: OAuth consent screen --> Data Access
        - Add or remove scopes. Example for sending email only:
            https://www.googleapis.com/auth/gmail.send

        - Successul registration of your application results in
          a credentials.json file. You use it to obtain a
          token.json file in the OAuth flow:

    - Starting the OAuth initiation flow:
        - Run the software in this repo (gmail-sender). A
          local browser will obtain confirmation from you,
          and then place a token.json file in your source tree.

    - Adding users allowed to use the application

        - Go to Google Cloud Console by googling for it
        - APIs & Services --> OAuth consent screen --> Audience
          Scroll down to "+ Add Users"

    - The gmail-sender software expects credentials.json, token.json,
      and send_account.txt with a one-line gmail account name in
      $HOME/.ssh/MailThroughGoogle. This can be modified in the
      GmailSender class variable.


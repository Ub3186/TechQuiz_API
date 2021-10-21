from functions import webhook
from config import constant

def send_test_webhook():
    format = '''
    `Webhook testing complete!`
    '''
    webhook.send_webhook("Test webhook", format, constant.OK_GREEN)

def send_error_webhook(method, e):
    format = '''
    ```Method:- {method}\nException name:- {name}\nException message:- {message}
    ```
    '''.format(method = method, name = type(e).__name__, message = e)
    webhook.send_webhook("Uncaught Exception", format, constant.ERROR_RED)

def send_user_webhook(method, user):
    format = '''
    `Name :- {username}`
    '''.format(username = user)
    webhook.send_webhook("Account " + method, format, constant.WARN_YELLOW)
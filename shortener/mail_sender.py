from django.core import mail
from django.utils.html import strip_tags


def send_account_activation(email, username, url):
    template = f'''
        <html>
            <head>
            </head>
            <body>
                Здравствуйте, <b>{username}</b>. Вот ваша ссылка для активации аккаунта.<br>
                {url}
            </body>
        </html>
        '''
    mail.send_mail('Подтверждение регистрации',
                   strip_tags(template),
                   'korotynski.alexey@gmail.com',
                   [email],
                   html_message=template)

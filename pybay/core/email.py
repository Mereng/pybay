import abc
import smtplib
import asyncio

import settings


def _get_smtp():
    if settings.config['smtp'].get('ssl'):
        smtp = smtplib.SMTP_SSL(settings.config['smtp']['host'])
    else:
        smtp = smtplib.SMTP(settings.config['smtp']['host'])

    smtp.ehlo()
    smtp.login(settings.config['smtp']['login'], settings.config['smtp']['password'])
    smtp.auth_plain()
    return smtp


def send(email_from, to, subject, message):
    body = ((
        f'From: {email_from}\n' 
        f'To: {to}\n'
        f'Subject: {subject}\n\n'
    ) + message).encode('utf-8')
    _get_smtp().sendmail(email_from, [to], body)


class Notificator:
    subject = None
    from_ = settings.config['smtp']['from']

    def get_subject(self):
        return self.subject

    @abc.abstractmethod
    async def get_emails(self):
        pass

    @abc.abstractmethod
    async def get_message(self):
        pass

    async def _send(self):
        for email in await self.get_emails():
            send(self.from_, email, self.get_subject(), await self.get_message())

    def send(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self._send())

# -*- coding: utf-8 -*-
import time
import threading
import smtplib
from email.mime.text import MIMEText

import requests

from parsers import RegexParser, CSSParser
from SETTINGS import SETTINGS


__author__ = 'ivanenko.danil'

RUN_FIRST_TIME = True
TEXT_CHUNKS = {}
HTML_EMAIL_TEMPLATE = """
    <html>
      <head></head>
      <body>
        <h1>Changes detected</h1>
        {content}
      </body>
    </html>
"""
HTML_EMAIL_CHUNK = """
    <h3>{selector_name}</h3>
    <h4>{selector}</h4>
    <hr/>
"""


def first_run():
    """
    first time run. prepare data structures, compile patterns and collect text_chunks from URL
    """

    request = requests.get(SETTINGS["url_check"])

    # collect all regext chunks
    for selector in SETTINGS["regexp_selectors"]:
        parser = RegexParser(selector["selector"])
        chunk = parser.search(request.text)
        TEXT_CHUNKS[selector["selector"]] = {
            "name": selector["name"],
            "parser": parser,
            "text_chunk": chunk
        }

    # collect all CSS chunks
    for selector in SETTINGS["css_selectors"]:
        parser = CSSParser(selector["selector"])
        chunk = parser.search(request.text)
        TEXT_CHUNKS[selector["selector"]] = {
            "name": selector["name"],
            "parser": parser,
            "text_chunk": chunk
        }

    print "first run complete, now wait"



def time_check_url():
    """
    this function will run every N minites and send email with notification
    """
    request = requests.get(SETTINGS["url_check"])
    print(time.ctime())
    html_parts = []

    # collect webpage parts
    for selector in TEXT_CHUNKS:
        print(selector)
        parser = TEXT_CHUNKS[selector]["parser"]
        TEXT_CHUNKS[selector]["new_text_chunk"] = parser.search(request.text)

        # now check for changes and fill html template
        if TEXT_CHUNKS[selector]["text_chunk"] != TEXT_CHUNKS[selector]["new_text_chunk"]:
            html_parts.append(HTML_EMAIL_CHUNK.format(selector_name=TEXT_CHUNKS[selector]["name"],
                                                      selector=selector))

            TEXT_CHUNKS[selector]["text_chunk"] = TEXT_CHUNKS[selector]["new_text_chunk"]
            print("changes detected")
        else:
            print("no changes detected")

    # if we have changes - send email
    if len(html_parts) > 0:
        msg = MIMEText(HTML_EMAIL_TEMPLATE.format(content="".join(html_parts)), 'html')
        msg['Subject'] = SETTINGS["email_subject"]
        smtpserver = smtplib.SMTP(SETTINGS["smtp_server"], SETTINGS["smtp_port"])

        # check id we need to login
        if len(SETTINGS["smtp_user"]) > 0 and len(SETTINGS["smtp_password"]) > 0:
            smtpserver.login(SETTINGS["smtp_user"], SETTINGS["smtp_password"])

        smtpserver.sendmail("urlwatcher@script", SETTINGS["send_to_emails"], msg.as_string())
        smtpserver.quit()

    # repeat our function once again
    threading.Timer(SETTINGS["time_check"]*60, time_check_url).start()


############################

first_run()
# no need to perform checkings at once, wait for time_check minutes
time.sleep(SETTINGS["time_check"]*60)
time_check_url()

# -*- coding: utf-8 -*-

SETTINGS = {
    # period in minutes
    "time_check": 1,
    "url_check": "http://www.eventbrite.co.uk/e/colour-conference-2016-london-tickets-16596215728?aff=ebrowse",
    #"url_check": "http://127.0.0.1:8000/",

    ## define your regexp or css selectors
    ## "name" - will be used in email, so you can recognize your selector
    ## "selector" - regex or CSS selector

    # define parts of webpage using regexp
    "regexp_selectors": [
        #{"name": "Readable name for email 1", "selector": '<div class="testdate1">(.*)</div>'},
        #{"name": "Readable name for email 2", "selector": '<div id="error_event_quantity_remaining" .*>(.*)</div>'},
    ],

    # define parts of webpage using css
    "css_selectors": [
        {"name": "Readable name for email 3", "selector": "div#panel_when"},
        #{"name": "Readable name for email 3", "selector": "div.testdate2"},
        #{"name": "Readable name for email 3", "selector": "div.testdate3"},
    ],

    # email settings
    "send_to_emails": ["iiiii@mail.com", ],
    "email_subject": "URL watcher notifications",
    "smtp_server": "localhost",
    "smtp_port": 25,
    "smtp_user": "",
    "smtp_password": "",

}


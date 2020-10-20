import requests
from lxml import html

def login_to_feide(username, password, url, org):
    session = requests.Session()
    request = session.get(url)

    AuthState = html.fromstring(request.content).xpath('//input[@name="AuthState"]/@value')[0]
    form_url = html.fromstring(request.content).xpath('//form/@action')[0]

    org_data = {
        'AuthState': AuthState,
        'org': 'ntnu.no'
    }

    login_page = session.get(form_url, params = org_data)


    AuthState = html.fromstring(request.content).xpath('//input[@name="AuthState"]/@value')[0]
    newUrl = login_page.url
    auth_data = {
        'feidename': username,
        'password': password,
        'AuthState': AuthState,
        'org': 'ntnu.no'
    }
    auth_request = session.post(newUrl, auth_data)
    print("Auth request: " + str(auth_request))

    return auth_request, session

def confirm_js(page, session):
    action = html.fromstring(page.content).xpath('//form/@action')[0]
    saml_response = html.fromstring(page.content).xpath('//input[@name="SAMLResponse"]/@value')[0]
    relay_state = html.fromstring(page.content).xpath('//input[@name="RelayState"]/@value')[0]

    auth_confirmation_data = {
        'SAMLResponse': saml_response,
        'RelayState': relay_state
    }

    nojs_auth_confirmation_request = session.post(action, auth_confirmation_data)
    print("Auth confirmation nojs request: " + str(nojs_auth_confirmation_request))

    return nojs_auth_confirmation_request

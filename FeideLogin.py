import requests

def login_to_feide(username, password, url, org):
    # Create session
    session = requests.Session()
    request = session.get(url)

    # Get authentication state
    auth_state = html.fromstring(request.content).xpath('//input[@name="AuthState"]/@value')[0]

    # Select orginization
    form_url = html.fromstring(request.content).xpath('//form/@action')[0]
    org_data = {
        'AuthState': auth_state,
        'org': org
    }
    login_page = session.get(form_url, params = org_data)


    # Complete login by posting username and password
    auth_state = html.fromstring(login_page.content).xpath('//input[@name="AuthState"]/@value')[0]
    login_page_url = login_page.url

    auth_data = {
        'feidename': username,
        'password': password,
        'AuthState': auth_state,
        'org': org
    }
    login_session = session.post(login_page_url, auth_data)

    print("Auth request: " + str(login_session))

    return login_session

def confirm_js(session):
    action = html.fromstring(session.content).xpath('//form/@action')[0]
    saml_response = html.fromstring(session.content).xpath('//input[@name="SAMLResponse"]/@value')[0]
    relay_state = html.fromstring(session.content).xpath('//input[@name="RelayState"]/@value')[0]

    auth_confirmation_data = {
        'SAMLResponse': saml_response,
        'RelayState': relay_state
    }

    nojs_auth_confirmation_request = session.post(action, auth_confirmation_data)
    print("Auth confirmation nojs request: " + str(nojs_auth_confirmation_request))

    return nojs_auth_confirmation_request

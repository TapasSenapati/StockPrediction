import oauth2 as oauth
from linkedin import linkedin
CONSUMER_KEY = 'gkysv9llzkf8'     # This is api_key
CONSUMER_SECRET = 'Rm9u6NYcvcElMN98'   # This is secret_key
USER_TOKEN = '78d34936-8785-42f2-ab99-06464e9f7bfd'   # This is oauth_token
USER_SECRET = '6dcc1417-f136-4422-838f-3b729f56a4f3'   # This is oauth_secret
RETURN_URL = '' # Not required for developer authentication
auth = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET, 
                                USER_TOKEN, USER_SECRET, 
                                RETURN_URL, 
                                permissions=linkedin.PERMISSIONS.enums.values())
app = linkedin.LinkedInApplication(auth)
print app.get_profile()


url = "http://api.linkedin.com/v1/people-search:(people:(id,first-name,last-name,headline,relation-to-viewer:(distance),location:(name,country:(code)),picture-url,site-standard-profile-request:(url),public-profile-url,positions:(title,is-current)),num-results)?company-name=microsoft&keywords=engineering&country-code=gb&start=0&count=100"
consumer = oauth.Consumer( key="gkysv9llzkf8", secret="Rm9u6NYcvcElMN98")
token = oauth.Token( key="78d34936-8785-42f2-ab99-06464e9f7bfd", secret="6dcc1417-f136-4422-838f-3b729f56a4f3")
client = oauth.Client(consumer, token)
resp, content = client.request(url, headers={'x-li-auth-token':'OUT_OF_NETWORK:wHti'})
print resp
print content






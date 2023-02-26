import os

CLIENT_ID = ''
CLIENT_SECRET = ''

if 'FFLOGSAPI_CID' in os.environ:
    CLIENT_ID = os.environ['FFLOGSAPI_CID']
if 'FFLOGSAPI_SECRET' in os.environ:
    CLIENT_SECRET = os.environ['FFLOGSAPI_SECRET']

# 7 days
CACHE_EXPIRY = 86400 * 7

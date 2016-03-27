import string

BLOCKED = ["http://www.facebook.com", "https://www.facebook.com", "https://www.twitter.com""http://www.twitter.com", "http://www.microsoft.com", "http://www.mcafee.com/us/index.html"]

# function to check whether url is blocked or not
def block_check (url):
    if url in BLOCKED:
        print "Found the url in the blocked list - will exit."
        return True     # a blocked url
    else:
        print "Not a blocked url"
        return False

# function to add a url to the blocked list
def add_blocked (url):
    if url in BLOCKED:
        print "Already in list"
        return False
    else:
        BLOCKED.append(url)         # add to list of blocked
        return True

def remove_blocked (url):
    if url in BLOCKED:
        BLOCKED.remove(url)
        return True                 # sucessfully removed
    else:                           # not in list
        return False


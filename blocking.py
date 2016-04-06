import string

BLOCKED = ["http://www.facebook.com/", "http://www.samsung.com/"]

# function to check whether url is blocked or not
def block_check (url):
    if url in BLOCKED:
        print "URL is blocked - will exit."
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


import httplib, thread, socket, proxy_thread, sys, dircache, threading, select, time, tempfile, os, fileinput, filecmp, blocking

BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 32768    # max number of bytes we receive at once
host = 'localhost'
port = 8000

cache = [500]   #the cache

def main(done = 0):

    if (done == 0):
        # allow user to add urls to blocked list
        print "Would you like to add any urls to the blocked list?"
        add = raw_input("Enter the urls one at a time, hitting enter after each.\n To stop entering URLs enter XXX instead.\n")
        while add != "XXX":
            blocking.add_blocked(add)
            add = raw_input("Add another?\n")

        # allow user to remove urls from blocked list
        print "Would you like to remove any urls from the blocked list?"
        for i in range (0, len(blocking.BLOCKED)):
            print blocking.BLOCKED[i], "\t"
        remove = raw_input("Enter the urls one at a time, hitting enter after each.\n To stop entering URLs enter XXX instead.\n")
        while remove != "XXX":
            blocking.remove_blocked(remove)
            remove = raw_input("Remove another?\n")
        done = 1            #means when we go back into main, the blocking stuff wont be done again


    # SOCKET SETUP AND ERROR-HANDLING
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(BACKLOG)
        print 'The proxy server is ready to receive on port ', port
    except socket.error, (value, message):
        if s:
            pass
        s.close()
        print "Could not open socket: ", message
        sys.exit(1)


    while 1:
        is_readable = [s]
        is_writable = [s]
        is_error=[]
        r, q, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:                       # if there is some data available
            client, client_addr = s.accept()
            print "\nNew request received"
            thread.start_new_thread(proxy_thread.proxy_threading, (client, client_addr, cache))
        else:                       # still no data available
            time.sleep(0.5)



    # empty the cache before exiting the program
    for i in range (0, 50):
        os.unlink(cache[i])
    print("Closing connection")
    s.close()

if __name__ == "__main__":
    main()

# the web proxy server should cache each page it receives and check the cache
# for each page that is requeste
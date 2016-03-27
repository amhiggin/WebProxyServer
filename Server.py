import httplib, thread, socket, proxy_thread, sys, dircache, threading, select, time
#********* CONSTANT VARIABLES *********
BACKLOG = 2            # how many pending connections queue will hold
MAX_DATA_RECV = 20000    # max number of bytes we receive at once
host = 'localhost'
port = 8000
# _ports = {'http' : 80, 'https' : 443}         #something i picked up somewhere

def main():

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
        is_writable =[]
        is_error=[]
        r, q, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:                       # if there is some data available
            for i in range(BACKLOG):
                client, client_addr = s.accept()
                print "\nNew request received"
                thread.start_new_thread(proxy_thread.proxy_threading, (client, client_addr))
        else:                       # still no data available
            time.sleep(0.5)

    print("Closing connection")
    s.close()

if __name__ == "__main__":
    main()

# the web proxy server should cache each page it receives and check the cache
# for each page that is requested incase it is already stored locally


# the user needs to be able to block/add urls
# as well as request urls
import httplib, thread, socket, proxy_thread, blocking, sys, ssl, urllib, urllib2, urlparse, httplib, dircache
import threading, select, time
#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 12095    # max number of bytes we receive at once
host = 'localhost'
port = 8000
# _ports = {'http' : 80, 'https' : 443}         #something i picked up somewhere

def worker(num):
    print "Worker: %s " % num
    return


def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(BACKLOG)
        print 'The proxy server is ready to receive on port ', port
    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket: ", message
        sys.exit(1)

    for i in range num_clients:
        is_readable = [s]
        is_writable =[]
        is_error=[]
        r, q, e = select.select(is_readable, is_writable, is_error, 1.0)
        if r:
            conn, client_addr = s.accept()
            thread.start_new_thread(proxy_thread.proxy_threading, (conn, client_addr))
        else:
            time.sleep(0.5)

    print("Closing connection")
    s.close()

if __name__ == "__main__":
    main()










# the web proxy server should cache each page it receives and check the cache
# for each page that is requested incase it is already stored locally



# should have a loop listening for new connections
# that loop should execute every time there is a new connection
# it should be a sub-loop of a bigger loop that keeps running and informing the user as
# to whether there are any threads being executed, and if so, how many
import httplib, thread, socket, proxy_thread, sys, dircache, threading, select, time
#********* CONSTANT VARIABLES *********
BACKLOG = 2            # how many pending connections queue will hold
MAX_DATA_RECV = 12095    # max number of bytes we receive at once
host = 'localhost'
port = 8000
# _ports = {'http' : 80, 'https' : 443}         #something i picked up somewhere

def main():
    num_clients=0


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

    count=0
    while 1:
        is_readable = [s]
        r = select.select(is_readable, 1.0)
        for i in range(BACKLOG):
            if r:
                count=0
                conn, client_addr = s.accept()
                thread.start_new_thread(proxy_thread.proxy_threading, (conn, client_addr))
            else:
                count+=1
                time.sleep(0.5)
                "Waiting ", count

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
import socket, sys, blocking, ssl, urllib, urllib2, urlparse, os

# ********* CONSTANT VARIABLES *********
BACKLOG = 2  # how many pending connections queue will hold
MAX_DATA_RECV = 20000  # max number of bytes we receive at once
DEBUG = False  # set to True to see the debug msgs
FILE_EXISTS = False


def proxy_threading(conn, client_addr):
    request = conn.recv(MAX_DATA_RECV)
    filename = request.split()[1].partition("/")[2]
    fileExist = "false"

    first_line = request.split('\n')[0]
    # get url
    url = first_line.split(' ')[1]
    print "Url is ", url

    # check whether blocked
    blocked = blocking.block_check(url)

    if blocked == True:
        sys.exit(1)
    else:
        # URL not on blocked list

        # check whether exists in cache or not: if it does, send it to the browser
        if os.path.exists(filename):
            print "Cache hit!"
            data = open(filename).readlines()
            conn.send("HTTP/1.0 200 OK\r\n")
            conn.send("Content-Type:text/html\r\n")

            for i in range(0, len(data)):
                conn.send(data[i])
            print "Read from the cache"

        else:
            print "\nNOT CACHED \n"

            http_pos = url.find("://")  # find pos of ://
            if (http_pos == -1):
                temp = url
            else:
                temp = url[(http_pos + 3):]  # get the rest of url

            port_pos = temp.find(":")  # find the port pos (if any)

            # find end of web server
            webserver_pos = temp.find("/")
            if webserver_pos == -1:
                webserver_pos = len(temp)

            webserver = ""
            port = -1
            if (port_pos == -1 or webserver_pos < port_pos):  # default port
                port = 80
                webserver = temp[:webserver_pos]
            else:  # specific port
                port = int((temp[(port_pos + 1):])[:webserver_pos - port_pos - 1])
                print "Port is ", port
                webserver = temp[:port_pos]
                print "Webserver is ", webserver

            print "Connecting to:", webserver, port

            try:
                # create a socket to connect to the web server
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((webserver, port))
                s.send(request)  # send request to webserver
                "Request sent to webserver.. "

                x = 1  # default sentinel value
                while x == 1:
                    # receive data from web server
                    data = s.recv(MAX_DATA_RECV)
                    print "Received data from webserver..."
                    # expect to see HTTP/1.0 200 OK so that we know it connected


                    f = open(filename, 'wb')
                    f.write(data)
                    #THE ABOVE LINE IS INTENDED TO CACHE THE PAGE
                    print "Just cached the page"

                    if (len(data) > 0):
                        # send to browser
                        conn.send(data)
                        print "Sending the data received from webserver to the browser..."
                        x = 2
                    else:
                        print "Could not send to browser - will try again"
                        x = 1
            except socket.error, (value, message):
                if s:
                    s.close()
                if conn:
                    conn.close()
                print "Runtime Error: ", message
                sys.exit(1)

        print "Successfully fetched the page", url

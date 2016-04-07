import socket, sys, blocking, os, Server, ssl

# ********* CONSTANT VARIABLES *********
BACKLOG = 50  # how many pending connections queue will hold
MAX_DATA_RECV = 200000  # max number of bytes we receive at once
DEBUG = False  # set to True to see the debug msgs
FILE_EXISTS = False
prohib = {"/", "?", "@", "!", "=", "+"}


def proxy_threading(conn, client_addr, cache):

    request = conn.recv(MAX_DATA_RECV)
    try:
        file = request.split()[1].partition("/")[2]
        filename =str(file)
        for x in prohib:
            filename = filename.replace("x", "AZBYCX")
        filename = filename.replace("/", "AZBYCX")
        filename+=".dat"
        print "File is ", file
        print "Filename is ", filename
        filepath = os.path.join("C:/Users/Amber/Documents/Cache/" + filename)
        print "Filepath is ", filepath
    except IndexError:
        print "Didn't work...returning to main program"
        Server.main(1)


    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]
    print "Url is ", url

    # check whether blocked
    blocked = blocking.block_check(url)

    if blocked == True:
        print "Blocked"
        Server.main(1)       #return to main program and wait for next
    else:
        # URL not on blocked list

        # check whether exists in cache or not: if it does, send it to the browser
        if os.path.exists(filepath):
            print "Cache hit!", filepath
            f = open(filepath, 'r+') #can read/append
            data = f.read()
            conn.send("HTTP/1.0 200 OK\r\n")
            conn.send("Content-Type:text/html\r\n")

            for i in range(0, len(data)):
                conn.send(data[i])
            print "Read from the cache: saved bandwidth"
            f.close()

        else:
            print "\nNOT CACHED...will put this in the cache \n" # this page will be cached further down the line

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
            else:
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


                    filepath = os.path.join("C:/Users/Amber/Documents/Cache/" + filename)
                    print "Filepath is ", filepath
                    f = open(filepath, 'w+')
                    f.write(data)          # write the received data to the cached file
                    cache+=f
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

        f.close()       #close the file
        print "Successfully fetched the page", url

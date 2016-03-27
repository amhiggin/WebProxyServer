import socket, sys, blocking, ssl, urllib, urllib2, urlparse

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 4096    # max number of bytes we receive at once
DEBUG = False           # set to True to see the debug msgs
FILE_EXISTS = False


def proxy_threading(conn, client_addr):

  print "Received something from ", client_addr, " starting a thread.."
  request = conn.recv(MAX_DATA_RECV)
  print "Received request from browser", request.split(" ")[0]

  first_line = request.split('\n')[0]
  print "First line is ", first_line
  # get url
  url = first_line.split(' ')[1]
  print "Url is ", url

  #check whether blocked
  blocked = blocking.block_check(url)
  if blocked==True:
    sys.exit(1)
  else:
    # find the webserver and port
    http_pos = url.find("://")          # find pos of ://
    if (http_pos==-1):
      temp = url
    else:
      temp = url[(http_pos+3):]       # get the rest of url

    port_pos = temp.find(":")           # find the port pos (if any)

    # find end of web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
      webserver_pos = len(temp)

    webserver=""
    port = -1
    if (port_pos==-1 or webserver_pos < port_pos):      # default port
      port = 80
      print "Default port: ", port
      webserver = temp[:webserver_pos]
      print "Default webserver: ", webserver
    else:       # specific port
      print "A specific port..."
      port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
      print "Port is ", port
      webserver = temp[:port_pos]
      print "Webserver is ", webserver

    print "Connect to:", webserver, port
    print "Lots of debug comments!!"

    try:
      # create a socket to connect to the web server
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect((webserver, port))
      s.send(request)         # send request to webserver
      "Request sent to webserver, ", request

      x=1   #default sentinel value
      while x==1:
        # receive data from web server
        data = s.recv(MAX_DATA_RECV)
        print "Received ", data, " from webserver"
        # expect to see HTTP/1.0 200 OK so that we know it connected

        if (len(data) > 0):
          # send to browser
          conn.send(data)
          print "Sending the data to the browser...", data
          x=2
        else:
          print "Did not send to browser - will try again"
          x=1
    except socket.error, (value, message):
      print "Runtime Error: ", message
      sys.exit(1)

    print "Have successfully fetched the page", url
    return True
  return False
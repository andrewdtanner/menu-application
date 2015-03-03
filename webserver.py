from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("/restaurant"):
        restaurants = session.query(Restaurant).all()
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = "<a href='/restaurant/new'>Make new restaurant</a></br></br>"
        output += "<html><body>"
        for restaurant in restaurants:
          output += restaurant.name
          output += "</br>"
          output += "<a href='/restaurant/%s/edit'>Edit</a>" %restaurant.id
          output += "</br>"
          output += "<a href='/restaurant/%s/delete'>Delete</a>" %restaurant.id
          output += "</br></br>"

        output +="</body></html>"
        self.wfile.write(output)
        return

    except IOError:
      self.send_error(404, 'File Not Found: %s' % self.path)

    if self.path.endswith("/new"):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        output = "<html><body>"
        output += "<h1>Make a new Restaurant</h1>"
        output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new' >"
        output += "<input name='newRestaurantName' type='text' placeholder= 'New Restaurant Name' >"
        output += "<input type='submit' value='Create'>"
        output +="</body></html>"
        self.wfile.write(output)
        return
    if self.path.endswith("/edit"):
        restaurantIDPath = self.path.split("/")[2]
        myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
        if myRestaurantQuery != []:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()
          output = ""
          output += "<html><body>"
          output += "<h1>"
          output += myRestaurantQuery.name
          output += "</h1>"
          output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>" % restaurantIDPath
          output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
          output += "<input type='submit' value='Rename'>"
          output += "</form>"
          output += "</body></html>"
        self.wfile.write(output)

    if self.path.endswith("/delete"):
        restaurantIDPath = self.path.split("/")[2]
        myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
        if myRestaurantQuery != []:
          self.send_response(200)
          self.send_header('Content-type', 'text/html')
          self.end_headers()
          output = ""
          output += "<html><body>"
          output += "<h1>Are you sure you want to delete %s</h1>" %myRestaurantQuery.name
          output += "</h1>"
          output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'>" % restaurantIDPath
          output += "<input type='submit' value='Delete'>"
          output += "</form>"
          output += "</body></html>"
        self.wfile.write(output)




  def do_POST(self):
    if self.path.endswith("/new"):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
        fields=cgi.parse_multipart(self.rfile, pdict)
        messagecontent = fields.get('newRestaurantName')
        newRestaurant = Restaurant(name = messagecontent[0])
        session.add(newRestaurant)
        session.commit()
        self.send_response(301)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', '/restaurant')
        self.end_headers()
    if self.path.endswith("/edit"):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
        fields=cgi.parse_multipart(self.rfile, pdict)
        messagecontent = fields.get('newRestaurantName')
        restaurantIDPath = self.path.split("/")[2]

        myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
        if myRestaurantQuery !=[]:
          myRestaurantQuery.name = messagecontent[0]
          session.add(myRestaurantQuery)
          session.commit()
          self.send_response(301)
          self.send_header('Content-type', 'text/html')
          self.send_header('Location', '/restaurant')
          self.end_headers()

    if self.path.endswith("/delete"):
      ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
      if ctype == 'multipart/form-data':
        fields=cgi.parse_multipart(self.rfile, pdict)
        restaurantIDPath = self.path.split("/")[2]
        print restaurantIDPath
        myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
        print myRestaurantQuery
        if myRestaurantQuery !=[]:
          session.delete(myRestaurantQuery)
          session.commit()
          self.send_response(301)
          self.send_header('Content-type', 'text/html')
          self.send_header('Location', '/restaurant')
          self.end_headers()


def main():
  try:
    port = 8080
    server = HTTPServer(('', port), webServerHandler)
    print "Web Server running on port %s"  % port
    server.serve_forever()
  except KeyboardInterrupt:
    print " ^C entered, stopping web server...."
    server.socket.close()

if __name__ == '__main__':
  main()

def redirect():
  self.send_response(301)
  self.send_header('Content-type', 'text/html')
  self.send_header('Location', '/restaurant')
  self.end_headers()


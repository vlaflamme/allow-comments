import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

default_guestbook_name = 'default_guest'

def guestbook_key(guestbook_name=default_guestbook_name):
    """Constructs a Datastore key for a Guestbook entity.

    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)


class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

class Handler(webapp2.RequestHandler):
        def write(self, *a, **kw):
                self.response.out.write(*a, **kw)

        def render_str(self, template, **params):
                t = jinja_env.get_template(template)
                return t.render(params)

        def render(self, template, **kw):
                self.write(self.render_str(template, **kw))


class MainPage(Handler):
	def get(self):
                self.render("html-toppage.html")

                guestbook_name = self.request.get('guestbook_name',
                                                  default_guestbook_name)
                greetings_query = Greeting.query(
                    ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
                greetings = greetings_query.fetch(10)

                user = users.get_current_user()

                blank_entry = self.request.get('blank_entry')
                
                if user:
                    url = users.create_logout_url(self.request.uri)
                    url_linktext = 'Logout'

                else:
                    url = users.create_login_url(self.request.uri)
                    url_linktext = 'Login to add new or view your old customized notes'

                template_values = {
                    'user': user,
                    'greetings': greetings,
                    'guestbook_name': urllib.quote_plus(guestbook_name),
                    'url': url,
                    'url_linktext': url_linktext,
                    'blank_entry': blank_entry,
                }

                template = JINJA_ENVIRONMENT.get_template('index.html')
                self.response.write(template.render(template_values))

		lessons=["Class Notes"]

		sub_topic=["Networks, HTML Templates, Forms, Webpage"]

                sub_topic_list=['Network - a network is a group of entities that can communicate, even though they are not all directly connected. Must have at least 3 entities.',
                'Network needs to be able to encode and interpret messages (with bits); need a way to route messages; need rules to decide who gets to use the resources.',
                'Latency - used to measure the time it takes for the message to get from the source to the destination (unit of time), e.g. milliseconds.',
                'Bandwidth - amount of information (bits) that can be transmitted per unit of time (milliseconds); bandwidth typically measured as Mbps.',
                'Bit - the smallest unit of information; can choose between two things with 1 bit (e.g. 0 and 1). Use multiple bits to increase the amount of information that can be distinguished; every new bit added doubles how much can be distinguished.',
                'Protocol - a set of rules that tell how two entities talk to each other; on the internet, the client (web browser) and server uses Hypertext Transfer Protocol (HTTP). HTTP is the name of the protocol and defines the rules for this to happen.'
                'Routers figure out the next hops, which are used as a way to direct the message.',
                'Best effort service - in general, there are no rules enforced on the internet in terms of priority on who gets to use the resources.',
                'HTML documents - contains the following sections: doctype; opening and closing HTML tags; the head which contains title, meta-data, java script, css cscript, etc.; and the body tag which contains the content of what appears on the webpage.',
                'URL - Uniform Resource Locator - has 3 main parts: protocol (e.g. HTTP or HTTPS), then host (can be an IP address or the name of the server), then the path (e.g. / )'
                'URLs can have a Query parameter (aka Get parameter) - use the ? followed by name=value (e.g. ?p=1); you can use multiple queries by using an & between each query. These are separate from the path, but included as part of the whole URL.'
                'Cache - something that stores data so you do not have to retrieve it later. It can be used to make data requests faster.'
                'Fragment - is separated from the rest of the URL by a # sign - references a particular part of a webpage you are looking at. This is not sent to the server when you make a request - it just exists in the browser.',
                'Port - when you make a web request to a server, in order to make an internet connection you need the address of the server and the port (e.g. 80 is the default); you can specifiy a port using :port, e.g. :8000'
                'HTTP - the main protocol of the web; used for browser to talk to web servers; a simple text protocol; request line has 3 main parts: method, path, and version; method is the request you are making of the server, e.g. GET, POST); the path is the actual document being requested from the server (this includes the path part after the main server address, and the query) - this would be the relative path; you could use the full path by including the main server address; the version is always HTTP/version number, e.g. HTTP/1.1 or HTTP/1.0.',
                'Headers in an HTTP request line get sent with the request line (name: value). Host header specifies the host part of the URL - this header is required in HTTP 1.1.',
                'User-Agent headers -describes who is making the request, generally your browser, e.g. Chrome. These headers are important so the server can block or slow down a particular agent when it is bombarding a site, etc.',
                'HTTP Responses - server sends back a response to the browser, e.g. the document requested, etc. this is done with the Status Line, which contains HTTP version, status code, and reason phrase which is an english translation of the status code (e.g. HTTP/1.1 200 ok). Common status codes include 300 (ok), 302 (doc is found someplace else), 404 (not found), and 500 (server error). Codes starting with 2 means it worked; with 3 means there is more work to be done technically to find the document; 4 means there is an issue on the browser side; 5 means there is an issue with the server side.',
                'Status line is followed by headers - incl. Date (when request happened), Server (not recommended to use), Content-Type (type of doc being returned, such as html), Content-Length (how long the doc is) etc.',
                'Servers - purpose is to respond to HTTP requests; two types of server responses - static (pre-written file that the server returns, e.g. image) and dynamic (the response is built on the fly by a program (web application) that is running; a web application builds content.'
                'Forms - enables a user to enter information into a website with fields, radio buttons, check boxes, etc.',
                'Validating user input is a critical aspect to any application you code - user input validation not only helps to drive security for the application, but it also helps to ensure the user input will meet the specifications needed by the program to read the input and take any appropriate action on it.',
                'Templates - separate different types of code; make code more readable; enable more secure websites; and enables HTML that is easier to modify. Templates are used as one way to avoid repetition of code - code repetition can cause performance issues, errors in coding, and is a poor approach to coding.',
                'Database - a program that stores and retrieves large amounts of structured data, or the machine running that program, or a group of machines working together to store/ retrieve data.',
                'Database server - special server that runs the database program and stores the data.',
                'Table - contains structured data; columns in a table are the elements stored in the table; the rows contain instances of the elements within the table. Each element is defined as a specific type (e.g. date, integer, string, etc.). Each row normally contains an id which allows you to reference that row. Elements from one table can be used to reference rows in a different table.',
                'Named tuple - allows you to refer to the properties of something by their name.',
                'Downsides of querying data by hand are: error-prone, tedious, and slow. Databases are a better way to handle large amounts of data.',
                'Types of databases - relational (often use SQL to manipulate them), e.g. MySQL which is used by Facebook, sqlite, postgresql, oracle - all free; other databases include Google App Engine Datastore, Amazon Dynamo, NoSQL such as mongo and couch.',
                'SQL - structured query language; language for expressing queries; used on relational database to ask questions of the database; SQL queries contain commands (e.g. SELECT), reference which columns to select (e.g. * means all), tells where to get the data from (e.g. FROM links), criteria or constraint to identify which rows to in the table to return the data (e.g. WHERE id=5), etc.',
                'SQL ORDER parameter - in SQL query ASC means ascending order DESC means decending order.',
                'SQL JOINS - used in SQL statement which involves multiple tables; allows you to join (link) two tables together based on joining (linking) common elements, which scans both tables and only returns the rows where they are equal to each other. JOIN is not often used for WEB programming.',
                'Indexes - allows a non-sequential scan of the table; this significantly improves performance for very large tables. Index makes lookups faster. Hash table lookup stores the indexes and associated element.You need to ensure you keep the hash table updated as you update the database table. Yan have multiple indexes on a single table. SQL command example - "create index hotel_id on hotels(id);".',
                'hashtable is not sorted, but uses constant time lookups. Tree mapping is similar to hashtable but they are sorted; but these lookups are slower.',
                'ACID - Atomicity (all parts of a transaction succeed or fail together), Consistency(the database will always be consistent), Isolation(no transaction can interfere with another transaction) - can accomplish this through locking as one method, Durability(once a transaction is committed, it will not be lost). Database systems will need to trade off between these because it is difficult to have all four in one system.']


                self.render("html-div-lists.html", lessons=lessons,sub_topic=sub_topic, sub_topic_list=sub_topic_list)

class Guestbook(webapp2.RequestHandler):
        def post(self):

                guestbook_name = self.request.get('guestbook_name',
                                                  default_guestbook_name)
                greeting = Greeting(parent=guestbook_key(guestbook_name))

                if users.get_current_user():
                    greeting.author = Author(
                            identity=users.get_current_user().user_id(),
                            email=users.get_current_user().email())
                
                greeting.content = self.request.get('content')

                if greeting.content == "":
                        blank_entry = "Enter notes, and press button below to add"

                else:
                        greeting.put()
                        blank_entry = ""

                query_params = {'guestbook_name': guestbook_name,'blank_entry': blank_entry}
                self.redirect('/?' + urllib.urlencode(query_params))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/sign', Guestbook)
], debug=True)

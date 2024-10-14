import http.server
import socketserver
import json
import sqlite3

# Initialize and set up the SQLite database
def init_db():
    # Create a connection to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('quotes.db')
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()

   # Drop the existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS quotes')

    # Create a table for storing quotes, if it doesn't already exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL,
            color TEXT NOT NULL
        )
    ''')
    
     # Insert some quotes
    cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                   ("To be or not to be", "William Shakespeare", "#FF968A"))
    cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                   ("Life is what happens when you're busy making other plans.", "John Lennon", "#55C8CD"))
    cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                   ("The only thing we have to fear is fear itself.", "Franklin D. Roosevelt", "#FF5733"))
    cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                   ("In the end, we will remember not the words of our enemies, but the silence of our friends.", "Martin Luther King Jr.", "#FFAF6E"))
    cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                   ("The unexamined life is not worth living.", "Socrates", "#7D8BE0"))

    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call this function to initialize the database
init_db()

print("Database and table initialized.")

PORT = 8000

# Define a request handler class that inherits from BaseHTTPRequestHandler
class MyHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/quotes':
            conn = sqlite3.connect('quotes.db')
            cursor = conn.cursor()

            cursor.execute('SELECT id, quote, author, color FROM quotes')
            quotes = cursor.fetchall()

            # Format the result as a list of dictionaries
            quote_list = [{'id': row[0], 'quote': row[1], 'author': row[2], 'color': row[3]} for row in quotes]

            conn.close()
            # Respond with JSON data when the /quotes path is requested
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(quote_list).encode())
        else:
            # Serve static files (index.html, app.js) for any other request
            super().do_GET()

    def do_POST(self):
        if self.path == '/add-quote':  # Ensure this matches the endpoint you're sending the POST to
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)

            # Parse the JSON data
            quote_data = json.loads(post_data)

            # Validate the data and insert into the database (you'll already have this part)
            if 'quote' in quote_data and 'author' in quote_data and 'color' in quote_data:
                conn = sqlite3.connect('quotes.db')
                cursor = conn.cursor()
                
                cursor.execute("INSERT INTO quotes (quote, author, color) VALUES (?, ?, ?)", 
                               (quote_data['quote'], quote_data['author'], quote_data['color']))
                
                conn.commit()
                conn.close()

                self.send_response(201)  # Respond with 201 Created
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Quote added successfully!'}).encode('utf-8'))
            else:
                self.send_response(400)  # Bad request if the necessary fields are not provided
                self.end_headers()
                self.wfile.write(json.dumps({'message': 'Invalid data!'}).encode('utf-8'))


# Set up the server
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()

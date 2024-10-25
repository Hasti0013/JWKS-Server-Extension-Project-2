# Student Name: Hasti Rathod
# Subject: CSCE 3550
# Student ID: 11448416
# EUID- hhr0013
# Project2: Extending JWKS Server

# Import required libraries
from http.server import HTTPServer, BaseHTTPRequestHandler
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from datetime import datetime, timedelta, timezone
from jwt.utils import base64url_encode, bytes_from_int
from calendar import timegm
import sqlite3
import json
import jwt

# Define a custom request handler
class RequestHandler(BaseHTTPRequestHandler):
    JWKS = {"keys": []}  # Initialize storage for JSON Web Keys (JWKs)

    # Handle HTTP PUT requests (Not Allowed)
    def do_PUT(self):
        self.send_response(405)
        self.end_headers()

    # Handle HTTP DELETE requests (Not Allowed)
    def do_DELETE(self):
        self.send_response(405)
        self.end_headers()

    # Handle HTTP PATCH requests (Not Allowed)
    def do_PATCH(self):
        self.send_response(405)
        self.end_headers()

    # Handle HTTP HEAD requests (Not Allowed)
    def do_HEAD(self):
        self.send_response(405)
        self.end_headers()

    # Handle HTTP GET requests
    def do_GET(self):
        if self.path == "/.well-known/jwks.json":
            self.send_response(200)
            self.end_headers()
            curs = db.cursor()

            # Query to retrieve active keys from the database
            select = "SELECT * FROM keys WHERE exp > ?;"
            curs.execute(select, (timegm(datetime.now(tz=timezone.utc).timetuple()),))
            rows = curs.fetchall()

            # Build the JWKs response
            for row in rows:
                expiry = row[2]
                priv_key_bytes = row[1]
                keyID = str(row[0])
                priv_key = load_pem_private_key(priv_key_bytes, None)
                pub_key = priv_key.public_key()

                JWK = {
                    "kid": keyID,
                    "alg": "RS256",
                    "kty": "RSA",
                    "use": "sig",
                    "n": base64url_encode(
                        bytes_from_int(pub_key.public_numbers().n)
                    ).decode("UTF-8"),  # Base64 encoded Modulus
                    "e": base64url_encode(
                        bytes_from_int(pub_key.public_numbers().e)
                    ).decode("UTF-8"),  # Base64 encoded Exponent
                }
                if not expiry <= timegm(datetime.now(tz=timezone.utc).timetuple()):
                    self.JWKS["keys"].append(JWK)

            # Send the JWKs as a JSON response
            self.wfile.write(json.dumps(self.JWKS, indent=1).encode("UTF-8"))
            return
        else:
            self.send_response(405)  # Handle unsupported GET requests
            self.end_headers()
            return

    # Handle HTTP POST requests
    def do_POST(self):
        if (
            self.path == "/auth"
            or self.path == "/auth?expired=true"
            or self.path == "/auth?expired=false"
        ):
            expired = False
            if self.path == "/auth?expired=true":
                expired = True
            self.send_response(200)
            self.end_headers()
            curs = db.cursor()

            # Determine which keys to select based on expiry
            if expired:
                select = "SELECT kid, key, exp FROM keys WHERE exp <= ?;"
            else:
                select = "SELECT * FROM keys WHERE exp > ?;"
            curs.execute(select, (timegm(datetime.now(tz=timezone.utc).timetuple()),))
            key_row = curs.fetchone()

            expiry = key_row[2]
            priv_key_bytes = key_row[1]
            keyID = str(key_row[0])
            jwt_token = jwt.encode(
                {"exp": expiry},
                priv_key_bytes,
                algorithm="RS256",
                headers={"kid": keyID},
            )
            self.wfile.write(bytes(jwt_token, "UTF-8"))
            return
        else:
            self.send_response(405)  # Handle unsupported POST requests
            self.end_headers()
            return

# Initialize the HTTP server on localhost:8080
http_server = HTTPServer(("", 8080), RequestHandler)

# Connect to the SQLite database and ensure the keys table exists
db = sqlite3.connect("totally_not_my_privateKeys.db")
db.execute(
    "CREATE TABLE IF NOT EXISTS keys(kid INTEGER PRIMARY KEY AUTOINCREMENT, key BLOB NOT NULL, exp INTEGER NOT NULL);"
)

# Generate key pairs and store them in the database
print("Generating key pairs... Please hold on...")
for i in range(5):
    priv_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    priv_key_bytes = priv_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    if i % 2 == 0:
        expiry = datetime.now(tz=timezone.utc) + timedelta(0, -3600, 0)
    else:
        expiry = datetime.now(tz=timezone.utc) + timedelta(0, 3600, 0)

    insert = "INSERT INTO keys (key, exp) VALUES(?, ?);"
    db.execute(insert, (priv_key_bytes, timegm(expiry.timetuple())))
db.commit()
print("HTTP Server is up and running on localhost port 8080...")

# Keep the server running indefinitely
try:
    http_server.serve_forever()
except KeyboardInterrupt:  # Gracefully shut down on interrupt
    db.close()
    pass

http_server.server_close()  # Close the server connection

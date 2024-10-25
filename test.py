# Student Name: Hasti Rathod 
# Subject: CSCE 3550 
# Student ID: 11448416 
# EUID- hhr0013 
# Project2: Extending JWKS Serverimport unittest
import requests
import os

total_ran = 0

# Class to test server responses
class ServerTest(unittest.TestCase):
    def test_server_response(self):
        response = requests.get(url="http://localhost:8080")
        # Check if the response indicates the server is running
        if response.status_code:
            response = True
        else:
            response = False
        self.assertEqual(response, True)

    def test_db_presence(self):
        # Verify if the database file exists
        result = os.path.isfile("./totally_not_my_privateKeys.db")
        self.assertEqual(result, True)


# Class to test authentication responses
class AuthTest(unittest.TestCase):
    def test_auth_get_response(self):
        response = requests.get(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert that GET requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_auth_post_response(self):
        response = requests.post(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert that POST requests return OK status
        self.assertEqual(response.status_code, 200)

    def test_auth_patch_response(self):
        response = requests.patch(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert that PATCH requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_auth_put_response(self):
        response = requests.put(
            url="http://localhost:8080/auth",
            auth=("userABC", "password123"),
            data={"test": "data"},
        )
        # Assert that PUT requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_auth_delete_response(self):
        response = requests.delete(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert that DELETE requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_auth_head_response(self):
        response = requests.head(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert that HEAD requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)


# Class to test JWKS responses
class JWKSTest(unittest.TestCase):
    def test_jwks_get_response(self):
        response = requests.get(url="http://localhost:8080/.well-known/jwks.json")
        # Assert that GET requests to JWKS return OK status
        self.assertEqual(response.status_code, 200)

    def test_jwks_post_response(self):
        response = requests.post(url="http://localhost:8080/.well-known/jwks.json")
        # Assert that POST requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_jwks_patch_response(self):
        response = requests.patch(url="http://localhost:8080/.well-known/jwks.json")
        # Assert that PATCH requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_jwks_put_response(self):
        response = requests.put(
            url="http://localhost:8080/.well-known/jwks.json", data={"test": "data"}
        )
        # Assert that PUT requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_jwks_delete_response(self):
        response = requests.delete(url="http://localhost:8080/.well-known/jwks.json")
        # Assert that DELETE requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)

    def test_jwks_head_response(self):
        response = requests.head(url="http://localhost:8080/.well-known/jwks.json")
        # Assert that HEAD requests return Method Not Allowed
        self.assertEqual(response.status_code, 405)


# Class to check response formats
class ResponseTest(unittest.TestCase):
    def test_jwks_response_format(self):
        response = requests.get(url="http://localhost:8080/.well-known/jwks.json")
        # Verify that JWKs are structured correctly
        for JWK in response.json()["keys"]:
            for item in JWK:
                if item == "alg":
                    self.assertEqual(JWK[item], "RS256")  # Check algorithm
                elif item == "kty":
                    self.assertEqual(JWK[item], "RSA")  # Check key type
                elif item == "use":
                    self.assertEqual(JWK[item], "sig")  # Check usage
                elif item == "e":
                    self.assertEqual(JWK[item], "AQAB")  # Check exponent

    def test_auth_response_format(self):
        response = requests.post(
            url="http://localhost:8080/auth", auth=("userABC", "password123")
        )
        # Assert the response is in the format [header].[payload].[signature]
        self.assertRegex(response.text, r".*\..*\..*")


# Load test suites for various classes
basic_suite = unittest.TestLoader().loadTestsFromTestCase(ServerTest)  # Load basic tests
auth_suite = unittest.TestLoader().loadTestsFromTestCase(AuthTest)  # Load auth response tests
jwks_suite = unittest.TestLoader().loadTestsFromTestCase(JWKSTest)  # Load JWKS response tests
response_suite = unittest.TestLoader().loadTestsFromTestCase(ResponseTest)  # Load response formatting tests

# Combine all test suites into a full suite
full_suite = unittest.TestSuite([basic_suite, auth_suite, jwks_suite, response_suite])
unittest.TextTestRunner(verbosity=2).run(full_suite)  # Execute all tests

# Display test coverage information
print("\nTest Coverage = Lines of Code Executed in Tests / Total Lines of Code")
print("Test Coverage = 144 / 155 = {}%".format(int((144 / 155) * 100)))
# Note: My Test Suite does not cover the following lines of code:
#   86-93: Checking if there is an expired tag
#   98-101: Querying for an expired key

"""
Question 1 (20 marks)
Explain the difference between GET and POST requests and show how to make
a POST request to an API using the requests library in Python, including
sending data.

--------------------------------------------------------------------------
GET vs POST
--------------------------------------------------------------------------
GET:
  - Used to RETRIEVE data from a server.
  - Parameters are sent in the URL (query string), e.g. ?id=5&name=andrew
  - Has no request body (or an empty one).
  - Requests can be cached, bookmarked, and stay in browser history.
  - Idempotent and safe: calling it repeatedly does not change server state.
  - Data is visible in the URL, so it is not suitable for sensitive data
    (passwords, tokens, etc.) and has practical length limits.

POST:
  - Used to SEND/submit data to a server, usually to create or update a
    resource.
  - Parameters are sent in the request BODY, not the URL.
  - Not cached or bookmarked by default, and not kept in browser history.
  - Not idempotent: submitting the same POST twice can create two records.
  - Can send much larger and more complex payloads (JSON, files, forms),
    and is the appropriate choice for sensitive data such as login
    credentials, since the body is not exposed in the URL.

In short: GET asks the server for something, POST gives the server
something.
"""

import requests


def make_post_request():
    """Send a POST request with JSON data to an API and return the response."""
    url = "https://jsonplaceholder.typicode.com/posts"

    # Data we want to send to the server
    payload = {
        "title": "Assignment 2",
        "body": "Demonstrating a POST request with the requests library",
        "userId": 1,
    }

    # json=payload automatically serializes the dict to JSON and sets the
    # "Content-Type: application/json" header for us.
    response = requests.post(url, json=payload)

    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

    return response


def make_get_request():
    """Send a GET request for comparison."""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)

    print("Status code:", response.status_code)
    print("Response JSON:", response.json())

    return response


if __name__ == "__main__":
    print("--- GET request ---")
    make_get_request()

    print("\n--- POST request ---")
    make_post_request()

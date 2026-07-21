# PyCurl Wrapper Script (`pycurl.py`)

## 📌 Overview
`pycurl.py` is a lightweight Python wrapper script designed primarily for **security analysis**, **API reverse engineering**, and **traffic inspection / debugging**. It mimics the standard `pycurl` library API while using Python's `requests` library under the hood to manage HTTP/HTTPS requests seamlessly.

---

## 🔑 Key Features
1. **Real-time Request Inspection & Logging**:
   - Automatically outputs the **URL**, **HTTP Method**, **Headers**, **Payload Data**, and **Multipart Post Data** in colorful terminal formatting prior to sending every request. This makes inspecting network activity effortless during reverse engineering or security auditing.
2. **SSL Verification Bypass**:
   - Easily disables SSL certificate verification via the `SSL_VERIFYPEER` option—ideal when proxying traffic through tools like Burp Suite or custom interception proxies.
3. **Full PyCurl API Compatibility**:
   - Provides drop-in compatibility for standard `pycurl` objects, methods, and constants, including `Curl()`, `setopt()`, `perform()`, `getinfo()`, `close()`, `HTTPHEADER`, `POSTFIELDS`, `COOKIE`, `HTTPPOST`, `FORM_FILE`, and more.

---

## 🛠️ How It Works

The wrapper intercepts standard PyCurl calls and translates them into Python `requests` operations:

1. **`Curl` Class Initialization (`__init__`)**:
   - Instantiating `c = pycurl.Curl()` sets up default state variables (`headers`, `data`, `cookie`, `httppost`, `ssl_verify = True`, `method = "GET"`, etc.).

2. **Option Assignment (`setopt`)**:
   - Calls to `c.setopt(option, value)` update internal attributes:
     - `c.URL`: Sets the target endpoint URL.
     - `c.HTTPHEADER`: Parses header lists into key-value structures.
     - `c.COOKIE`: Accepts raw cookie strings and automatically injects them into request headers.
     - `c.POSTFIELDS`: Stores raw, JSON, or form-encoded payloads and sets the HTTP method to `POST`.
     - `c.HTTPPOST`: Handles multipart form fields and file uploads (`c.FORM_FILE`), reading files directly from disk.
     - `c.SSL_VERIFYPEER`: Toggles SSL certificate validation (`ssl_verify = bool(value)`).

3. **Request Execution (`perform`)**:
   - Logs color-coded request details (`SHAJON URL`, `SHAJON HEADERS`, `SHAJON DATA`, etc.) to standard output.
   - Executes `requests.get()` or `requests.post()` according to the configured options and headers.
   - Streams the raw HTTP response body directly to `c.WRITEDATA` (e.g., `io.BytesIO()`) if provided.

4. **Querying Metadata (`getinfo`)**:
   - `c.getinfo(c.RESPONSE_CODE)` returns the HTTP status code, while `c.EFFECTIVE_URL` returns the resolved request URL.

---

## 🚀 Usage Example

```python
import io
import pycurl

# Response buffer
response = io.BytesIO()

# Curl instance
c = pycurl.Curl()
c.setopt(c.URL, "https://httpbin.org/post")
c.setopt(c.WRITEDATA, response)

# Set custom headers & cookie
c.setopt(c.HTTPHEADER, [
    "User-Agent: SecurityTools/1.0",
    "Content-Type: application/json"
])
c.setopt(c.COOKIE, "session=abcdef123456")

# Disable SSL verification (useful for traffic interception proxies)
c.setopt(c.SSL_VERIFYPEER, 0)

# Set POST payload
c.setopt(c.POSTFIELDS, '{"username": "shajon", "action": "login"}')

# Perform request (Prints URL, Headers & Payload to terminal)
c.perform()

# Output response
print(response.getvalue().decode())
c.close()
```
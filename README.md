# Aidar Server

This is a Flask server for the Aidar project. Follow the steps below to set up the environment and run the server.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Setting Up the Environment

1. **Clone the repository:**

   ```bash
   git clone https://github.com/HiralThadeshwar31/aidar-server.git
   ```

2. **Navigate to the project directory:**

   ```bash
   cd aidar-server
   ```

3. **Create a virtual environment:**

   You can create a virtual environment using `venv`:

   ```bash
   python -m venv venv
   ```

4. **Activate the virtual environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Install the required packages:**

   Make sure you have a `requirements.txt` file in your project. If you don't have one, create it and list all necessary packages. Then, run:

   ```bash
   pip install -r requirements.txt
   ```

## Running the Flask Server

Once the environment is set up and the required packages are installed, you can run the Flask server by executing:

```bash
python app.py
```

The server should start, and you can access it at `http://127.0.0.1:5000/` (or whatever host and port your Flask app is configured to use).

## Stopping the Server

To stop the server, you can use `CTRL + C` in the terminal where the server is running.

## Notes

- Make sure to set any required environment variables before running the server, if applicable.
- For detailed usage and endpoints, please refer to the API documentation or code comments.

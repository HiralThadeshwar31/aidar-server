# Aidar Server

This README provides instructions on how to set up and run the Flask server for the Aidar application.

## Prerequisites

Before you start, ensure you have Python installed on your machine.

## Setting Up the Environment

1. **Create a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   Install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

## Starting Redis

### Windows

1. **Download Redis for Windows**:
   - Go to the [Redis for Windows](https://github.com/microsoftarchive/redis/releases) releases page.
   - Download the latest `.zip` file.

2. **Extract and Navigate**:
   - Extract the downloaded `.zip` file.
   - Open a command prompt and navigate to the Redis folder.

3. **Start Redis with `redis-cli`**:
   ```bash
   redis-cli
   ```

### macOS

1. **Install Redis using Homebrew**:
   ```bash
   brew install redis
   ```

2. **Start Redis with `redis-cli`**:
   ```bash
   redis-cli
   ```

## Running the Flask Server

1. **Start Redis** (as described above).
2. **Run the Flask server**:
   ```bash
   python app.py
   ```

3. **Start the Client**:
   - Ensure the client application is set up and running according to its instructions.

Your server should now be running, and you can access it via your web browser or API client.

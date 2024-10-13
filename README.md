
# Aidar Server

## Running the Flask Server

To run the Flask server, follow these steps:

1. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Mac:
     ```bash
     source venv/bin/activate
     ```

3. **Install required packages**:
   Make sure to have your `requirements.txt` file ready and install the necessary packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server**:
   ```bash
   python app.py
   ```

## Installing Redis

### Windows

1. **Download Redis**:
   Visit the [Redis for Windows releases page](https://github.com/microsoftarchive/redis/releases) and download the latest `.msi` installer.

2. **Install Redis**:
   Run the downloaded installer and follow the setup instructions.

3. **Start Redis server**:
   Open a command prompt and run:
   ```bash
   redis-server
   ```

### Mac

1. **Install Homebrew** (if not already installed):
   Open a terminal and run:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Redis**:
   ```bash
   brew install redis
   ```

3. **Start Redis server**:
   ```bash
   brew services start redis
   ```

4. **Verify Redis is running**:
   You can check if Redis is working by running:
   ```bash
   redis-cli ping
   ```
   It should return "PONG".

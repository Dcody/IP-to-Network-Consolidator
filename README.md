# IP Consolidator

A powerful tool for consolidating individual IP addresses from any file format into efficient CIDR networks, with special optimization for network configurations including Cisco ASA.

## Features

- **Smart Analysis**: Multi-threshold analysis to find optimal balance between object count and IP coverage
- **Efficient Consolidation**: Reduce hundreds of individual host objects into optimized CIDR networks
- **Web Interface**: Modern, responsive web UI for easy file upload and analysis
- **Visual Analytics**: Interactive charts showing Pareto frontier and score distribution
- **Network-Ready Output**: Generate network configuration files ready for deployment

## Web Interface

The project now includes a modern web interface built with Flask that provides:

- **Drag & Drop File Upload**: Easy file upload with visual feedback
- **Real-time Analysis**: Instant processing and results display
- **Interactive Charts**: Visual representation of consolidation results
- **Download Generation**: Generate and download network configuration files
- **Responsive Design**: Works on desktop and mobile devices

## Installation & Setup (Step-by-Step Guide)

### Prerequisites - What You Need First

**You need these things installed on your computer:**

1. **Python** (version 3.7 or newer)
   - Go to [python.org](https://python.org)
   - Download the latest version for your operating system
   - **IMPORTANT**: During installation, check the box that says "Add Python to PATH"

2. **A text editor** (like Notepad++, VS Code, or even regular Notepad)

3. **A web browser** (Chrome, Firefox, Safari, or Edge)

### Step 1: Get the Application Files

**Option A: Download as ZIP (Easiest)**
1. Click the green "Code" button on this page
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer (like `C:\IP_Consolidator`)

**Option B: Using Git (If you have Git installed)**
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to where you want the files:
   ```bash
   cd C:\
   ```
3. Download the files:
   ```bash
   git clone [repository-url]
   ```

### Step 2: Open Command Prompt/Terminal

**Windows:**
1. Press `Windows + R` on your keyboard
2. Type `cmd` and press Enter
3. Navigate to your project folder:
   ```bash
   cd C:\IP_Consolidator
   ```

**Mac/Linux:**
1. Open Terminal
2. Navigate to your project folder:
   ```bash
   cd /path/to/IP_Consolidator
   ```

### Step 3: Install Python Dependencies

**What this does:** This downloads all the extra software the application needs to work.

1. In your Command Prompt/Terminal, type this command and press Enter:
   ```bash
   pip install -r requirements.txt
   ```

2. **Wait for it to finish** - you'll see lots of text scrolling by. This is normal!

3. **If you get an error** saying "pip not found":
   - Make sure Python is installed correctly
   - Try this command instead:
   ```bash
   python -m pip install -r requirements.txt
   ```

### Step 4: Set Up Security (Optional but Recommended)

**What this does:** This makes your application more secure by setting up a secret password.

1. **Generate a secret key** (this is like a password for your app):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **Copy the long string** that appears (it will look like: `a1b2c3d4e5f6...`)

3. **Create a configuration file:**
   - In your project folder, find the file called `env.example`
   - Right-click on it and select "Copy"
   - Right-click in the same folder and select "Paste"
   - Rename the copied file from `env.example - Copy` to `.env`
   - **Note:** The file should be named exactly `.env` (with the dot at the beginning)

4. **Edit the .env file:**
   - Right-click on the `.env` file
   - Select "Open with" → "Notepad" (or your text editor)
   - Find the line that says: `SECRET_KEY=your_secure_secret_key_here_64_characters_long`
   - Replace `your_secure_secret_key_here_64_characters_long` with the long string you copied in step 1
   - Save the file

### Step 5: Run the Application

1. **In your Command Prompt/Terminal**, make sure you're in the project folder, then type:
   ```bash
   python app.py
   ```

2. **You should see something like this:**
   ```
   * Running on http://0.0.0.0:5000
   * Debugger PIN: 123-456-789
   ```

3. **Keep this window open** - the application is now running!

### Step 6: Use the Application

1. **Open your web browser** (Chrome, Firefox, etc.)

2. **Go to this address:**
   ```
   http://localhost:5000
   ```

3. **You should see the IP Consolidator webpage!**

### Step 7: Stop the Application

**When you're done using the application:**

1. **Go back to the Command Prompt/Terminal** window where the app is running
2. **Press `Ctrl + C`** (Windows) or `Cmd + C` (Mac)
3. **You'll see the application stop** and return to the command prompt

### Troubleshooting Common Problems

**Problem: "python not found"**
- **Solution:** Python isn't installed or isn't in your PATH
- **Fix:** Reinstall Python and make sure to check "Add Python to PATH"

**Problem: "pip not found"**
- **Solution:** Try using `python -m pip` instead of just `pip`

**Problem: "Port 5000 is already in use"**
- **Solution:** Something else is using port 5000
- **Fix:** Either stop the other application or change the port in your `.env` file

**Problem: Can't access the website**
- **Solution:** Make sure the Command Prompt/Terminal shows the app is running
- **Fix:** Check that you typed `http://localhost:5000` correctly

**Problem: "Permission denied" errors**
- **Solution:** You might not have permission to write to the folder
- **Fix:** Run Command Prompt as Administrator (Windows) or use `sudo` (Mac/Linux)

### What Each File Does

- **`app.py`** - The main application file (this is what you run)
- **`requirements.txt`** - List of Python packages the app needs
- **`env.example`** - Template for configuration settings
- **`.env`** - Your actual configuration settings (you create this)
- **`templates/`** - The webpage designs
- **`uploads/`** - Where uploaded files are stored (created automatically)

### Security Notes

- **Never share your `.env` file** - it contains your secret key
- **The application is only accessible from your computer** by default
- **If you want others to access it**, you'll need to configure your firewall and network settings

## Usage Guide (How to Use the Application)

### What This Application Does

This application helps you **consolidate IP addresses** from files. Think of it like organizing a messy drawer:
- **Before**: You have 100 individual socks scattered everywhere
- **After**: You have 5 organized groups of socks

In networking terms:
- **Before**: You have 100 individual IP addresses like `192.168.1.1`, `192.168.1.2`, `192.168.1.3`, etc.
- **After**: You have 1 network group like `192.168.1.0/24` (which includes all IPs from 192.168.1.1 to 192.168.1.254)

### Step-by-Step Usage Instructions

#### Step 1: Prepare Your File

**What files can you use?**
- Any text file with IP addresses
- Network configuration files
- Log files
- CSV files
- Even files you created yourself

**Example file content:**
```
192.168.1.1
192.168.1.2
192.168.1.3
10.0.0.1
10.0.0.2
```

#### Step 2: Upload Your File

1. **Make sure the application is running** (you should see the webpage at `http://localhost:5000`)

2. **On the webpage, you'll see a big upload area** that says "Drag & Drop your file here"

3. **Upload your file** using one of these methods:
   - **Method A (Drag & Drop)**: Click and drag your file from your computer folder onto the upload area
   - **Method B (Browse)**: Click the "Choose File" button and select your file

4. **You'll see a green message** saying your file was selected

5. **Click the "Analyze Configuration" button**

#### Step 3: Wait for Analysis

1. **You'll see a progress bar** showing the analysis is running
2. **This might take a few seconds** to a few minutes depending on your file size
3. **Don't close the browser** or the Command Prompt/Terminal window

#### Step 4: View Results

**When analysis is complete, you'll see:**

1. **Summary Cards** at the top showing:
   - Total IPs found
   - Number of thresholds tested
   - Number of optimal solutions found
   - Best score achieved
   - Recommended threshold

2. **Two Charts**:
   - **Objects vs Missing IPs**: Shows the trade-off between efficiency and coverage
   - **Score Distribution**: Shows how well each threshold performed

3. **Detailed Results Table** showing each threshold tested

#### Step 5: Choose Your Output Format

**At the top of the results page, you'll see "Output Format" options:**

1. **Cisco ASA Configuration**: Creates a file ready to paste into a Cisco ASA firewall
2. **Raw IP Addresses**: Creates a simple list of the consolidated IP addresses

#### Step 6: Generate and Download

1. **In the results table**, find the row with the threshold you want to use
2. **Click the "Generate" button** in that row
3. **Your file will automatically download** to your computer's Downloads folder
4. **The button will briefly show "Downloaded"** to confirm success

### Understanding the Results

#### What is a "Threshold"?

A threshold is like a **tolerance level** for how much extra space you're willing to include:
- **0% threshold**: Only include exactly the IPs you have (very precise, but might create many small groups)
- **25% threshold**: Include up to 25% more IPs than you have (good balance)
- **50% threshold**: Include up to 50% more IPs (creates larger groups, fewer total groups)

#### What is the "Recommended Threshold"?

The application automatically calculates which threshold gives you the **best balance** between:
- **Fewer network objects** (easier to manage)
- **Not including too many extra IPs** (staying efficient)

#### What are "Pareto Solutions"?

These are the **optimal solutions** - the ones that can't be improved in one area without making another area worse. Think of it like finding the best car:
- You want good gas mileage AND good performance
- You can't have both at maximum, so you find the best compromise

### Example Walkthrough

**Let's say you have a file with these IPs:**
```
192.168.1.1
192.168.1.2
192.168.1.3
192.168.1.5
192.168.1.6
192.168.1.7
192.168.1.9
192.168.1.10
```

**After analysis, you might get:**
- **0% threshold**: 8 individual IPs (no consolidation)
- **25% threshold**: 2 network groups (192.168.1.0/29 and 192.168.1.8/31)
- **50% threshold**: 1 network group (192.168.1.0/24)

**The recommended threshold might be 25%** because it gives you good consolidation without including too many extra IPs.

### Tips for Best Results

1. **Use the recommended threshold** unless you have specific requirements
2. **Larger files work better** - the more IPs you have, the more benefit you'll see
3. **Check the charts** to understand the trade-offs
4. **Try different thresholds** if you're not happy with the results
5. **Use ASA format** if you're working with Cisco firewalls
6. **Use Raw format** if you just need a simple list

### Common Questions

**Q: Why does it include extra IPs?**
A: To create efficient network groups (CIDR blocks), it sometimes needs to include IPs you don't have. This is normal and expected.

**Q: Which threshold should I use?**
A: Start with the recommended threshold. If you need fewer groups, try a higher threshold. If you need more precision, try a lower threshold.

**Q: Can I use this for IPv6 addresses?**
A: Currently, this application only works with IPv4 addresses.

**Q: What if my file has errors?**
A: The application will show you an error message. Check that your file contains valid IP addresses and try again.

## Security

### Production Deployment

For production deployment, ensure you:

1. **Set a secure secret key**:
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Add to your .env file
   SECRET_KEY=your_generated_key_here
   ```

2. **Use HTTPS**: Configure SSL/TLS certificates for secure communication

3. **Set proper file permissions**: Ensure the `uploads/` directory has appropriate permissions

4. **Configure firewall**: Only allow necessary ports (typically 443 for HTTPS)

### Security Features

- **Content Security Policy (CSP)**: Prevents XSS and other injection attacks
- **Path traversal protection**: Prevents directory traversal attacks
- **File upload validation**: Validates file types and sizes
- **Input sanitization**: All user inputs are validated and sanitized
- **Secure headers**: X-Frame-Options, X-Content-Type-Options, etc.



## Input Format

The tool can process any file containing IPv4 addresses and CIDR networks. It automatically detects and extracts IP addresses from:

- Network configuration files
- Log files
- CSV files
- Text files
- Any other file format with IP addresses

### Supported File Types:
- `.txt`, `.cfg`, `.conf` - Configuration files
- `.csv` - Comma-separated values
- `.log` - Log files
- `.dat`, `.lst` - Data files
- `.ip`, `.hosts` - IP lists

### Example Input Formats:

**ASA Configuration:**
```
network-object host 192.168.1.1
network-object host 192.168.1.2
```

**Log File:**
```
2024-01-01 10:00:00 Connection from 10.0.0.1
2024-01-01 10:01:00 Connection from 10.0.0.2
```

**CSV File:**
```
ip,description
192.168.1.1,Server A
192.168.1.2,Server B
```

**Plain Text with CIDR:**
```
192.168.1.1
192.168.1.0/24
10.0.0.1
10.0.0.0/16
```

**Mixed Format:**
```
192.168.1.1
192.168.2.0/24
10.0.0.1
172.16.0.0/12
```

## Output

The tool generates:

1. **Analysis Summary**: Detailed breakdown of consolidation results
2. **Pareto Frontier**: Optimal solutions balancing objects vs. missing IPs
3. **Network Configuration**: Ready-to-deploy network object definitions

### Sample Output

```
! Generated with 25% missing threshold
! === Object definitions ===
object network 192.168.1.0
 subnet 192.168.1.0 255.255.255.0

! === Group member list ===
network-object object 192.168.1.0
```

## How It Works

1. **Extract IPs**: Parses configuration files for individual host IPs
2. **Consolidate**: Groups IPs into CIDR networks using different thresholds
3. **Analyze**: Computes Pareto frontier for optimal trade-offs
4. **Score**: Normalized scoring system to rank solutions
5. **Generate**: Creates network-compatible output files

## Thresholds

The tool tests multiple thresholds (0%, 10%, 20%, 25%, 30%, 35%, 40%, 45%, 50%) to find the optimal balance between:

- **Objects Defined**: Number of network objects created
- **Missing IPs**: Additional IPs included in the consolidation
- **Expansion**: Percentage of extra IPs added

## Files

- `app.py` - Flask web application
- `templates/` - HTML templates for the web interface
- `core_consolidation.py` - Core consolidation logic
- `analysis.py` - Analysis and optimization functions
- `output_generator.py` - Network output generation
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.7+
- Flask 2.3.3+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the tool.

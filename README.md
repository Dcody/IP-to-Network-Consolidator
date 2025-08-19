# 🌐 IP Consolidator

<div align="center">

<div style="background-color: #ff6b6b; color: white; padding: 20px; border-radius: 10px; margin: 20px 0; border: 3px solid #d63031;">

## ⚠️ **IMPORTANT WARNING** ⚠️

### 🎮 **This is a TOY PROJECT for educational purposes only!**

**🚫 DO NOT use this in production environments**  
**🚫 DO NOT use this for real network security**  
**🚫 DO NOT use this in enterprise environments**

This project was created for learning and experimentation. It lacks proper security measures, error handling, and production-ready features.

**Use at your own risk!**

</div>

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Toy%20Project-orange.svg?style=for-the-badge)

**A powerful tool for consolidating individual IP addresses from any file format into efficient CIDR networks, with special optimization for network configurations including Cisco ASA.**

[🚀 Quick Start](#installation--setup) • [📊 Features](#-features) • [🌐 Web Interface](#-web-interface) • [📖 Usage](#-usage-guide)

</div>

---

<div align="center">
  <img src="https://img.shields.io/badge/Network%20Optimization-IP%20Consolidation-007ACC?style=for-the-badge&logo=cisco&logoColor=white" alt="Network Optimization">
  <img src="https://img.shields.io/badge/Web%20Interface-Modern%20UI-FF6B6B?style=for-the-badge&logo=flask&logoColor=white" alt="Web Interface">
  <img src="https://img.shields.io/badge/File%20Support-Multiple%20Formats-28A745?style=for-the-badge&logo=file&logoColor=white" alt="File Support">
</div>

## 🚀 Features

<div align="center">

| 🔍 **Smart Analysis** | ⚡ **Efficient Consolidation** | 🌐 **Web Interface** |
|----------------------|-------------------------------|---------------------|
| Multi-threshold analysis to find optimal balance between object count and IP coverage | Reduce hundreds of individual host objects into optimized CIDR networks | Modern, responsive web UI for easy file upload and analysis |

| 📊 **Visual Analytics** | 🔧 **Network-Ready Output** | 📁 **Multi-Format Support** |
|------------------------|----------------------------|---------------------------|
| Interactive charts showing Pareto frontier and score distribution | Generate network configuration files ready for deployment | Supports txt, cfg, conf, csv, log, dat, lst, ip, hosts files |

</div>

## 🌐 Web Interface

<div align="center">

| 🎯 **Drag & Drop Upload** | ⚡ **Real-time Analysis** | 📊 **Interactive Charts** |
|---------------------------|---------------------------|---------------------------|
| Easy file upload with visual feedback | Instant processing and results display | Visual representation of consolidation results |

| 📥 **Download Generation** | 📱 **Responsive Design** | 🔒 **Security Features** |
|---------------------------|-------------------------|-------------------------|
| Generate and download network configuration files | Works on desktop and mobile devices | File validation, path traversal protection, CSP headers |

</div>

## 🛠️ Installation & Setup

### 📋 Prerequisites

<div align="center">

| 🐍 **Python** | 📝 **Text Editor** | 🌐 **Web Browser** |
|---------------|-------------------|-------------------|
| Version 3.7 or newer | Notepad++, VS Code, or regular Notepad | Chrome, Firefox, Safari, or Edge |

</div>

1. **🐍 Python** (version 3.7 or newer)
   - Go to [python.org](https://python.org)
   - Download the latest version for your operating system
   - **IMPORTANT**: During installation, check the box that says "Add Python to PATH"

### 📥 Step 1: Get the Application Files

<div align="center">

| 📦 **Option A: Download as ZIP** | 🔧 **Option B: Using Git** |
|----------------------------------|----------------------------|
| **Easiest method** | **For advanced users** |

</div>

**📦 Option A: Download as ZIP (Easiest)**
1. Click the green "Code" button on this page
2. Select "Download ZIP"
3. Extract the ZIP file to a folder on your computer (like `C:\IP_Consolidator`)

**🔧 Option B: Using Git (If you have Git installed)**
1. Open Command Prompt (Windows) or Terminal (Mac/Linux)
2. Navigate to where you want the files:
   ```bash
   cd C:\
   ```
3. Download the files:
   ```bash
   git clone https://github.com/Dcody/IP-to-Network-Consolidator.git
   ```

### 💻 Step 2: Open Command Prompt/Terminal

<div align="center">

| 🪟 **Windows** | 🍎 **Mac/Linux** |
|----------------|------------------|
| Press `Windows + R`, type `cmd`, press Enter | Open Terminal application |

</div>

**🪟 Windows:**
1. Press `Windows + R` on your keyboard
2. Type `cmd` and press Enter
3. Navigate to your project folder:
   ```bash
   cd C:\IP_Consolidator
   ```

**🍎 Mac/Linux:**
1. Open Terminal
2. Navigate to your project folder:
   ```bash
   cd /path/to/IP_Consolidator
   ```

### 📦 Step 3: Install Python Dependencies

<div align="center">

| ⚡ **Primary Command** | 🔄 **Alternative Command** |
|----------------------|---------------------------|
| `pip install -r requirements.txt` | `python -m pip install -r requirements.txt` |

</div>

1. In your Command Prompt/Terminal, type this command and press Enter:
   ```bash
   pip install -r requirements.txt
   ```

2. **⏳ Wait for it to finish** - you'll see lots of text scrolling by. This is normal!

3. **❌ If you get an error** saying "pip not found":
   - Make sure Python is installed correctly
   - Try this command instead:
   ```bash
   python -m pip install -r requirements.txt
   ```

### 🔒 Step 4: Set Up Security (Optional but Recommended)

<div align="center">

| 🔑 **Generate Key** | 📋 **Copy String** | ⚙️ **Configure** |
|-------------------|-------------------|-----------------|
| Create a secure secret key | Copy the generated string | Add to environment file |

</div>

1. **🔑 Generate a secret key** (this is like a password for your app):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

2. **📋 Copy the long string** that appears (it will look like: `a1b2c3d4e5f6...`)

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

### 🚀 Step 5: Run the Application

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

4. **Open your web browser** and go to: `http://localhost:5000`

### 🛑 Stop the Application

**When you're done using the application:**
1. **Go back to the Command Prompt/Terminal** window where the app is running
2. **Press `Ctrl + C`** (Windows) or `Cmd + C` (Mac)
3. **You'll see the application stop** and return to the command prompt

### 🔧 Troubleshooting Common Problems

| ❌ **Problem** | 💡 **Solution** | 🔧 **Fix** |
|---------------|----------------|------------|
| "python not found" | Python isn't installed or isn't in your PATH | Reinstall Python and make sure to check "Add Python to PATH" |
| "pip not found" | Try using `python -m pip` instead of just `pip` | Use `python -m pip install -r requirements.txt` |
| "Port 5000 is already in use" | Something else is using port 5000 | Either stop the other application or change the port in your `.env` file |
| Can't access the website | Make sure the Command Prompt/Terminal shows the app is running | Check that you typed `http://localhost:5000` correctly |
| "Permission denied" errors | You might not have permission to write to the folder | Run Command Prompt as Administrator (Windows) or use `sudo` (Mac/Linux) |

## 📖 Usage Guide

### 🎯 What This Application Does

This application helps you **consolidate IP addresses** from files. Think of it like organizing a messy drawer:
- **Before**: You have 100 individual IP addresses like `192.168.1.1`, `192.168.1.2`, `192.168.1.3`, etc.
- **After**: You have 1 network group like `192.168.1.0/24` (which includes all IPs from 192.168.1.1 to 192.168.1.254)

### 📋 Step-by-Step Usage Instructions

#### 📁 Step 1: Prepare Your File

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

#### 📤 Step 2: Upload Your File

1. **Make sure the application is running** (you should see the webpage at `http://localhost:5000`)

2. **On the webpage, you'll see a big upload area** that says "Drag & Drop your file here"

3. **Upload your file** using one of these methods:
   - **Method A (Drag & Drop)**: Click and drag your file from your computer folder onto the upload area
   - **Method B (Browse)**: Click the "Choose File" button and select your file

4. **You'll see a green message** saying your file was selected

5. **Click the "Analyze Configuration" button**

#### ⏳ Step 3: Wait for Analysis

1. **You'll see a progress bar** showing the analysis is running
2. **This might take a few seconds** to a few minutes depending on your file size
3. **Don't close the browser** or the Command Prompt/Terminal window

#### 📊 Step 4: View Results

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

#### 📥 Step 5: Generate and Download

1. **In the results table**, find the row with the threshold you want to use
2. **Click the "Generate" button** in that row
3. **Your file will automatically download** to your computer's Downloads folder
4. **The button will briefly show "Downloaded"** to confirm success

### 🧠 Understanding the Results

#### 📊 What is a "Threshold"?

A threshold is like a **tolerance level** for how much extra space you're willing to include:
- **0% threshold**: Only include exactly the IPs you have (very precise, but might create many small groups)
- **25% threshold**: Include up to 25% more IPs than you have (good balance)
- **50% threshold**: Include up to 50% more IPs (creates larger groups, fewer total groups)

#### 🎯 What is the "Recommended Threshold"?

The application automatically calculates which threshold gives you the **best balance** between:
- **Fewer network objects** (easier to manage)
- **Not including too many extra IPs** (staying efficient)

#### ⚖️ What are "Pareto Solutions"?

These are the **optimal solutions** - the ones that can't be improved in one area without making another area worse. Think of it like finding the best car:
- You want good gas mileage AND good performance
- You can't have both at maximum, so you find the best compromise

### 📝 Example Walkthrough

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

### 💡 Tips for Best Results

1. **Use the recommended threshold** unless you have specific requirements
2. **Larger files work better** - the more IPs you have, the more benefit you'll see
3. **Check the charts** to understand the trade-offs
4. **Try different thresholds** if you're not happy with the results
5. **Use ASA format** if you're working with Cisco firewalls
6. **Use Raw format** if you just need a simple list

### ❓ Common Questions

| ❓ **Question** | 💡 **Answer** |
|----------------|---------------|
| **Why does it include extra IPs?** | To create efficient network groups (CIDR blocks), it sometimes needs to include IPs you don't have. This is normal and expected. |
| **Which threshold should I use?** | Start with the recommended threshold. If you need fewer groups, try a higher threshold. If you need more precision, try a lower threshold. |
| **Can I use this for IPv6 addresses?** | Currently, this application only works with IPv4 addresses. |
| **What if my file has errors?** | The application will show you an error message. Check that your file contains valid IP addresses and try again. |

## 📁 Input & Output Formats

### 📄 Supported File Types

| 📝 **File Type** | 🔧 **Description** |
|------------------|-------------------|
| `.txt`, `.cfg`, `.conf` | Configuration files |
| `.csv` | Comma-separated values |
| `.log` | Log files |
| `.dat`, `.lst` | Data files |
| `.ip`, `.hosts` | IP lists |

### 📥 Example Input Formats

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

### 📤 Sample Cisco ASA Output

```
! Generated with 25% missing threshold
! === Object definitions ===
object network 192.168.1.0
 subnet 192.168.1.0 255.255.255.0

! === Group member list ===
network-object object 192.168.1.0
```

## 🔧 How It Works

1. **🔍 Extract IPs**: Parses configuration files for individual host IPs
2. **⚡ Consolidate**: Groups IPs into CIDR networks using different thresholds
3. **📊 Analyze**: Computes Pareto frontier for optimal trade-offs
4. **🎯 Score**: Normalized scoring system to rank solutions
5. **📤 Generate**: Creates network-compatible output files

## 🔒 Security Features

<div align="center">

| 🛡️ **Content Security Policy** | 🚫 **Path Traversal Protection** | ✅ **File Upload Validation** |
|-------------------------------|--------------------------------|-----------------------------|
| Prevents XSS and other injection attacks | Prevents directory traversal attacks | Validates file types and sizes |

| 🧹 **Input Sanitization** | 🔒 **Secure Headers** | 🔑 **Secret Key Management** |
|---------------------------|---------------------|----------------------------|
| All user inputs are validated and sanitized | X-Frame-Options, X-Content-Type-Options, etc. | Secure secret key handling with environment variables |

</div>

## 🧹 File Cleanup System

The application includes an intelligent delayed file cleanup system with retry mechanism:

### ⏰ **Delayed Cleanup with Retry**
- Generated files are scheduled for cleanup with a 30-second initial delay
- Each generated file has a unique filename to prevent conflicts and ensure proper cleanup
- After the delay, if the file is still in use (being downloaded), the system retries every 30 seconds
- Maximum retry period of 5 minutes (10 retries × 30 seconds)
- This ensures files are cleaned up as soon as possible after downloads complete

### 🔄 **Retry Logic**
- **Initial Delay**: Waits 30 seconds before first cleanup attempt
- **Retry Attempts**: Every 30 seconds if file is in use
- **Success**: File is deleted as soon as it's no longer in use
- **Timeout**: Stops retrying after 10 attempts (5 minutes total)
- **Error Handling**: Distinguishes between "file in use" and other errors

### 🚀 Production Deployment

For production deployment, ensure you:

1. **🔑 Set a secure secret key**:
   ```bash
   # Generate a secure key
   python -c "import secrets; print(secrets.token_hex(32))"
   
   # Add to your .env file
   SECRET_KEY=your_generated_key_here
   ```

2. **🔒 Use HTTPS**: Configure SSL/TLS certificates for secure communication

3. **📁 Set proper file permissions**: Ensure the `uploads/` directory has appropriate permissions

4. **🔥 Configure firewall**: Only allow necessary ports (typically 443 for HTTPS)

## 📋 Project Structure

| 📄 **File** | 🔧 **Purpose** |
|-------------|----------------|
| `app.py` | Flask web application |
| `templates/` | HTML templates for the web interface |
| `core_consolidation.py` | Core consolidation logic |
| `analysis.py` | Analysis and optimization functions |
| `output_generator.py` | Network output generation |
| `requirements.txt` | Python dependencies |
| `env.example` | Template for configuration settings |
| `.env` | Your actual configuration settings (you create this) |
| `uploads/` | Where uploaded files are stored (created automatically) |

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Please don't submit issues, feature requests, or pull requests to improve the tool.

---

<div align="center">

### 🌟 **Star this repository if you find it useful!**

[![GitHub stars](https://img.shields.io/github/stars/Dcody/IP-to-Network-Consolidator?style=social)](https://github.com/Dcody/IP-to-Network-Consolidator)
[![GitHub forks](https://img.shields.io/github/forks/Dcody/IP-to-Network-Consolidator?style=social)](https://github.com/Dcody/IP-to-Network-Consolidator)
[![GitHub issues](https://img.shields.io/github/issues/Dcody/IP-to-Network-Consolidator)](https://github.com/Dcody/IP-to-Network-Consolidator/issues)

---

**Made as fast as possible for network administrators and security professionals**

<div align="center">
  <img src="https://img.shields.io/badge/Python-Flask-FF6B6B?style=for-the-badge&logo=python&logoColor=white" alt="Python Flask">
  <img src="https://img.shields.io/badge/Web%20Development-Modern%20UI-28A745?style=for-the-badge&logo=web&logoColor=white" alt="Web Development">
</div>

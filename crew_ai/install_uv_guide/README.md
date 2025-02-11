 
---

### **How to Install `uv` on Windows**

1. **Run the Installation Command:**
   Open **PowerShell** as an administrator and run the following command:
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/0.5.21/install.ps1 | iex"
   ```
   This will download and install `uv` to `C:\Users\<YourUsername>\.local\bin`.

   Example output:
   ```
   Downloading uv 0.5.21 (x86_64-pc-windows-msvc)
   Installing to C:\Users\arman\.local\bin
     uv.exe
     uvx.exe
   everything's installed!
   ```

2. **Add `uv` to Your PATH:**
   After installation, you need to add the installation directory to your system's `PATH` so you can use `uv` from anywhere.

   #### **Option 1: Temporarily Add to PATH (for the current session only):**
   Run this command in PowerShell:
   ```powershell
   $env:Path = "C:\Users\arman\.local\bin;$env:Path"
   ```
   This will allow you to use `uv` immediately in the current session.

   #### **Option 2: Permanently Add to PATH (for all future sessions):**
   Follow these steps:
   - Open the Start menu and search for **Environment Variables**.
   - Click on **Edit the system environment variables**.
   - In the **System Properties** window, click the **Environment Variables** button.
   - Under **System variables**, find the `Path` variable and click **Edit**.
   - Click **New** and add the following path:
     ```
     C:\Users\arman\.local\bin
     ```
   - Click **OK** to save the changes.

3. **Verify the Installation:**
   Restart your PowerShell session and run the following command to check if `uv` is installed correctly:
   ```powershell
   uv --version
   ```
   If everything is set up correctly, it will display the version of `uv` installed.

---
 
 

# **How to Install Packages in DeepLearning.AI's Jupyter Notebook**  

Jupyter Notebook environments on platforms like **DeepLearning.AI** sometimes restrict direct package installations. If you encounter errors such as `pip: not found` or `ModuleNotFoundError`, follow these steps to install and use packages correctly.

---

## **Step 1: Ensure `pip` is Installed and Up-to-Date**  

Some Jupyter environments may not have `pip` available by default. Run the following code in a new cell to install or update `pip`:  

```python
import sys
import subprocessHey, Cortana. 

# Ensure pip is installed
subprocess.check_call([sys.executable, "-m", "ensurepip"])

# Upgrade pip to the latest version
subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
```

### **Verify Installation**  
Now, check if `pip`   are available:  

```python
import pip 
print("Pip version:", pip.__version__)
```

---

## **Step 2: Install Packages Using `%pip install`**  

Instead of `!pip install`, use `%pip install` inside Jupyter Notebook. This ensures that the package is installed in the correct environment.

```python
%pip install groq
```

### **Why Use `%pip install` Instead of `!pip install`?**  
- `%pip install` ensures that Jupyter uses the same Python environment that the notebook is running in.  
- `!pip install` might install packages in a different environment, leading to import errors.  

---

## **Step 3: Restart the Kernel**  

After installing a package, **restart the kernel** for changes to take effect.  

- Click on **Kernel** → **Restart Kernel** in the Jupyter Notebook menu.  
- Alternatively, you can run this in a code cell:  

```python
import os
os._exit(00)
```

---

## **Step 4: Verify Installation**  

After restarting the kernel, import the package and check its version to confirm successful installation:  

```python
import groq as gr
print("groq version:", gr.__version__)
```

---
 

## **Conclusion**  
To install packages in DeepLearning.AI's Jupyter Notebook:  
✅ Ensure `pip` is installed and updated.  
✅ Use `%pip install package_name` inside Jupyter.  
✅ Restart the kernel after installation.  
✅ Verify installation with `import package_name`.  

Following these steps should help you successfully install and use any package in your Jupyter Notebook! 🚀  

 
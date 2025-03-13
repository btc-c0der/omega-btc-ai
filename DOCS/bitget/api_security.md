```python
import os
import json
import configparser

def demonstrate_api_key_security():
    """
    Demonstrates secure ways to handle API keys and passphrases in a Python script:
    1. Using Environment Variables
    2. Using a Secure Configuration File

    This script does not actually call any APIs, it just shows how to *retrieve*
    API credentials securely for use in your scripts.
    """

    print("--- Demonstrating Secure API Key Handling ---")

    # --- 1. Using Environment Variables ---
    print("\n--- 1. Using Environment Variables ---")
    print("Retrieving API Key, Secret Key, and Passphrase from environment variables...")

    api_key_env = os.environ.get("MY_API_KEY")
    secret_key_env = os.environ.get("MY_SECRET_KEY")
    passphrase_env = os.environ.get("MY_PASSPHRASE")

    if api_key_env and secret_key_env and passphrase_env:
        print("Successfully retrieved API credentials from environment variables!")
        print(f"API Key (from env): {api_key_env[:4]}... (showing first 4 chars for security)") # Show only first few chars
        print(f"Secret Key (from env): {secret_key_env[:4]}... (showing first 4 chars for security)")
        print(f"Passphrase (from env): {passphrase_env[:4]}... (showing first 4 chars for security)")
    else:
        print("Error: Could not retrieve all API credentials from environment variables.")
        print("Please ensure you have set the environment variables: MY_API_KEY, MY_SECRET_KEY, MY_PASSPHRASE")
        print("Example (in your terminal before running the script):")
        print("export MY_API_KEY=your_api_key_value")
        print("export MY_SECRET_KEY=your_secret_key_value")
        print("export MY_PASSPHRASE=your_passphrase_value")

    print("\n--- Explanation of Environment Variables ---")
    print("Environment variables are a secure way to store sensitive information because:")
    print(" - They are *not* hardcoded in your script, preventing accidental exposure in code repositories.")
    print(" - They are configured *outside* of your code, typically at the system or process level.")
    print(" - They can be set differently for different environments (development, testing, production).")
    print(" - They are often more easily managed in deployment pipelines and CI/CD systems.")


    # --- 2. Using a Secure Configuration File (example with configparser for INI-style files) ---
    print("\n--- 2. Using a Secure Configuration File ---")
    config = configparser.ConfigParser()
    config_file_path = 'config.ini'  # You can name it something more specific and secure

    print(f"Attempting to load configuration from: {config_file_path}")

    try:
        config.read(config_file_path)
        api_key_config = config['API_CREDENTIALS']['API_KEY']
        secret_key_config = config['API_CREDENTIALS']['SECRET_KEY']
        passphrase_config = config['API_CREDENTIALS']['PASSPHRASE']

        print("Successfully loaded API credentials from configuration file!")
        print(f"API Key (from config file): {api_key_config[:4]}... (showing first 4 chars)")
        print(f"Secret Key (from config file): {secret_key_config[:4]}... (showing first 4 chars)")
        print(f"Passphrase (from config file): {passphrase_config[:4]}... (showing first 4 chars)")

    except (configparser.Error, KeyError) as e:
        print(f"Error loading configuration from file: {e}")
        print(f"Please ensure you have a '{config_file_path}' file in the same directory as your script.")
        print(f"Example '{config_file_path}' file content (do *not* commit this to public repos):")
        print("[API_CREDENTIALS]")
        print("API_KEY = your_api_key_value")
        print("SECRET_KEY = your_secret_key_value")
        print("PASSPHRASE = your_passphrase_value")


    print("\n--- Explanation of Secure Configuration Files ---")
    print("Configuration files (when used securely) are beneficial because:")
    print(" - They keep sensitive data out of your main code, making it cleaner and easier to share (without credentials).")
    print(" - You can use file system permissions to restrict access to the configuration file, limiting who can read the credentials.")
    print(" - Configuration files can be easily managed and modified without changing the code itself.")
    print(" - For better security, configuration files containing secrets should:")
    print("    - **NOT be committed to version control systems (like Git).** Add them to `.gitignore` or similar.")
    print("    - Be stored outside of the web-accessible directory if deploying web applications.")
    print("    - Have restricted file permissions so only necessary processes or users can read them.")


    print("\n--- Important Security Best Practices ---")
    print(" - **Choose ONE method (Environment Variables OR Secure Config Files) and be consistent.**")
    print(" - **Never hardcode API keys or secrets directly in your Python code.**")
    print(" - **Treat API keys and passphrases like passwords.** Keep them confidential.")
    print(" - **Use strong, randomly generated API keys and passphrases.**")
    print(" - **Regularly rotate your API keys and passphrases**, especially if they might have been compromised.")
    print(" - **For production systems, consider using more advanced secret management solutions** like HashiCorp Vault, AWS Secrets Manager, Google Secret Manager, Azure Key Vault, etc., for even stronger security and auditing capabilities.")


if __name__ == "__main__":
    demonstrate_api_key_security()
```

**To use this script and demonstrate secure API key handling:**

1.  **Install `configparser` (if you don't have it):**
    ```bash
    pip install configparser
    ```

2.  **Set Environment Variables (for demonstration of method 1):**
    *   **In your terminal (before running the script):**
        ```bash
        export MY_API_KEY=your_api_key_value_env_example
        export MY_SECRET_KEY=your_secret_key_value_env_example
        export MY_PASSPHRASE=your_passphrase_value_env_example
        ```
        *(Replace `your_api_key_value_env_example`, etc., with example values – these don't need to be real API keys for this demonstration)*

3.  **Create a Configuration File (`config.ini`) (for demonstration of method 2):**
    *   Create a file named `config.ini` in the same directory as your Python script.
    *   Add the following content to `config.ini` (replace the example values):

        ```ini
        [API_CREDENTIALS]
        API_KEY = your_api_key_value_config_file_example
        SECRET_KEY = your_secret_key_value_config_file_example
        PASSPHRASE = your_passphrase_value_config_file_example
        ```

    *   **Important Security Step:** In a real project, you should **add `config.ini` to your `.gitignore` file** (if you are using Git) to prevent accidentally committing it to your version control repository.

4.  **Run the Python script:**
    ```bash
    python your_script_name.py
    ```

**Explanation of the Script:**

*   **Environment Variables Demonstration:**
    *   `os.environ.get("MY_API_KEY")`, etc., retrieves the values of environment variables named `MY_API_KEY`, `MY_SECRET_KEY`, and `MY_PASSPHRASE`.
    *   It checks if these variables are set. If they are, it prints a masked version of the credentials (showing only the first 4 characters for security) and explains the benefits of environment variables. If not set, it provides instructions on how to set them.

*   **Secure Configuration File Demonstration:**
    *   `configparser.ConfigParser()` is used to parse an INI-style configuration file (`config.ini`).
    *   `config.read(config_file_path)` attempts to read the configuration file.
    *   `config['API_CREDENTIALS']['API_KEY']`, etc., accesses the values from the `[API_CREDENTIALS]` section and the keys `API_KEY`, `SECRET_KEY`, and `PASSPHRASE` in the configuration file.
    *   It includes basic error handling for file reading and key access. If successful, it prints masked credentials from the configuration file and explains the advantages of secure configuration files.  If there's an error, it gives instructions on creating a sample `config.ini` file.

*   **Security Best Practices:** The script concludes with a summary of important security best practices for handling API keys and sensitive information in your code.

This script serves as a practical demonstration of how to implement secure API key handling using environment variables and secure configuration files in Python.  Remember to choose the method that best suits your project and always prioritize security when working with sensitive credentials.
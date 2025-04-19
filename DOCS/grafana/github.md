
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


```python
import requests
import json
import time
import os  # For environment variables

def get_github_repo_metrics_for_grafana(repo_owner, repo_name, github_token=None):
    """
    Retrieves GitHub repository metrics using the GitHub API and formats them
    into a JSON structure suitable for Grafana.

    Args:
        repo_owner (str): The owner/organization of the repository (e.g., "your-org").
        repo_name (str): The name of the repository (e.g., "your-repo").
        github_token (str, optional): Your GitHub Personal Access Token.
                                      Highly recommended to avoid rate limiting,
                                      especially for frequent polling or public repos.
                                      Can also be set as environment variable GITHUB_TOKEN.

    Returns:
        str: JSON string containing GitHub repository metrics for Grafana.
             Returns None if there's an error retrieving data from GitHub API.
    """

    api_url_base = "https://api.github.com/repos"
    repo_url = f"{api_url_base}/{repo_owner}/{repo_name}"

    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    elif os.environ.get("GITHUB_TOKEN"): # Check for token in environment variable
        headers['Authorization'] = f'token {os.environ.get("GITHUB_TOKEN")}'

    metrics = {}
    timestamp = int(time.time())

    try:
        # 1. Repository Details
        repo_response = requests.get(repo_url, headers=headers)
        repo_response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        repo_data = repo_response.json()

        metrics['repo_info'] = {
            'stars_count': repo_data.get('stargazers_count'),
            'forks_count': repo_data.get('forks_count'),
            'watchers_count': repo_data.get('watchers_count'),
            'open_issues_count': repo_data.get('open_issues_count'),
            'open_pull_requests_count': repo_data.get('open_issues_count'), # Assuming PRs are also considered issues
            'subscribers_count': repo_data.get('subscribers_count'),
            'size_kb': repo_data.get('size'), # Repository size in KB
            'created_at': repo_data.get('created_at'),
            'updated_at': repo_data.get('updated_at'),
            # Add more repo details from repo_data as needed
        }

        # 2. Contributors Count
        contributors_url = f"{repo_url}/contributors"
        contributors_response = requests.get(contributors_url, headers=headers)
        contributors_response.raise_for_status()
        contributors_data = contributors_response.json()
        metrics['contributors_count'] = len(contributors_data)

        # 3. Commit Activity (Last year - weekly commits)
        commit_activity_url = f"{repo_url}/stats/commit_activity"
        commit_activity_response = requests.get(commit_activity_url, headers=headers)
        commit_activity_response.raise_for_status()
        commit_activity_data = commit_activity_response.json()

        total_commits_last_year = 0
        if commit_activity_data:
            for week_data in commit_activity_data:
                total_commits_last_year += sum(week_data['days']) # Sum of commits for each day in a week

        metrics['commit_activity'] = {
            'total_commits_last_year': total_commits_last_year,
            # You could break down by weekly commits if needed in Grafana, but total is often sufficient.
        }

        # Structure for Grafana
        grafana_data = {
            "metrics": metrics,
            "timestamp": timestamp
        }

        return json.dumps(grafana_data, indent=2)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from GitHub API: {e}")
        return None


if __name__ == "__main__":
    # Configuration - Customize these values
    github_repo_owner = 'your-org-or-username'  # Replace with the repository owner (e.g., 'grafana')
    github_repo_name = 'your-repo-name'       # Replace with the repository name (e.g., 'grafana')
    github_personal_access_token = None # "YOUR_GITHUB_TOKEN" # Or set as environment variable GITHUB_TOKEN

    grafana_json_output = get_github_repo_metrics_for_grafana(
        repo_owner=github_repo_owner,
        repo_name=github_repo_name,
        github_token=github_personal_access_token
    )

    if grafana_json_output:
        print(grafana_json_output)
    else:
        print("Failed to retrieve GitHub repository metrics.")


# --- How to use this with Grafana ---

# 1. Install required library:
#    pip install requests

# 2. Run this script:
#    python your_script_name.py

#    This will print a JSON output to your console.

# 3. Integrate with Grafana:

#    a) Using a File Data Source (Simplest for testing):
#       - Redirect the script output to a file (e.g., github_metrics.json):
#         python your_script_name.py > github_metrics.json
#       - In Grafana, add a "JSON API" or "Simple JSON" data source.
#       - Configure the data source to read from your 'github_metrics.json' file (you'll likely need a web server to serve the file).
#       - **Not recommended for production** as it's file-based and not real-time.

#    b) Using a Pushgateway (for Prometheus Data Source):
#       - Install and run a Prometheus Pushgateway.
#       - Modify this script to push metrics to the Pushgateway using the Prometheus client library for Python.
#       - In Grafana, add a Prometheus data source pointing to your Prometheus server (which scrapes the Pushgateway).

#    c) Using a Custom Exporter (for Prometheus Data Source - Best for Production):
#       - Turn this script into a proper Prometheus exporter that exposes metrics on an HTTP endpoint. Use a Prometheus client library (e.g., `prometheus_client` for Python).
#       - Run the exporter as a service.
#       - In Grafana, add a Prometheus data source pointing to your Prometheus server (which scrapes your exporter endpoint).

#    d) Using Telegraf (Data Collection Agent):
#       - Install and configure Telegraf.
#       - Use the `exec` input plugin in Telegraf to run this script periodically.
#       - Use the `http_json` input plugin in Telegraf to parse the JSON output.
#       - Use an output plugin in Telegraf to send the metrics to a time-series database that Grafana can use.

#    e) **Using Grafana's "JSON API" Data Source directly to a webserver endpoint:**
#       - Create a simple web server (e.g., using Flask or FastAPI) that runs this Python script
#         and serves the JSON output at an HTTP endpoint.
#       - In Grafana, add a "JSON API" data source and point it to the URL of your web server endpoint.
#       - This is a relatively straightforward way to get real-time data into Grafana without Prometheus if you
#         are comfortable setting up a basic web server.

# Choose the integration method that best suits your needs. For more frequent updates and production,
# Prometheus-based (b or c), Telegraf (d) or a direct JSON API endpoint (e) are better choices than file-based (a).
```

**Explanation:**

1.  **Import Libraries:**
    *   `requests`: To make HTTP requests to the GitHub API.
    *   `json`: To format data as JSON for Grafana.
    *   `time`: To get timestamps.
    *   `os`: To access environment variables (for GitHub token).

2.  **`get_github_repo_metrics_for_grafana` Function:**
    *   **Arguments:** Takes `repo_owner`, `repo_name`, and `github_token` (optional) as input.
    *   **API Base URL:** Defines `api_url_base` for GitHub API.
    *   **Repo URL:** Constructs the specific API URL for the repository.
    *   **Headers for Authentication:**
        *   Checks for `github_token` argument.
        *   If not provided as argument, checks for `GITHUB_TOKEN` environment variable.
        *   If a token is found, adds `Authorization` header to requests to avoid rate limits. **Highly recommended.**
    *   **Metrics Dictionary:** Initializes `metrics` dictionary to store results.
    *   **Timestamp:** Gets current timestamp.
    *   **Error Handling (`try...except`):** Encloses the API calls in a `try...except` block to catch potential `requests.exceptions.RequestException` errors (network issues, API errors, etc.).
    *   **1. Repository Details:**
        *   Constructs `repo_url`.
        *   Uses `requests.get()` to fetch repository data from the `/repos/{owner}/{repo}` endpoint.
        *   `repo_response.raise_for_status()`: Checks for HTTP errors (4xx, 5xx).
        *   Parses JSON response using `repo_response.json()`.
        *   Extracts key metrics from `repo_data` and stores them in `metrics['repo_info']`:
            *   `stars_count` (Stargazers)
            *   `forks_count`
            *   `watchers_count`
            *   `open_issues_count` (Open issues - assuming Pull Requests are counted as issues in `open_issues_count` - could be refined to separate PRs if needed)
            *   `subscribers_count` (Watchers/Subscribers)
            *   `size_kb` (Repository size in KB)
            *   `created_at` (Creation timestamp)
            *   `updated_at` (Last update timestamp)
            *   **You can add more metrics from `repo_data` as needed. See GitHub API Repo endpoint documentation.**
    *   **2. Contributors Count:**
        *   Constructs `contributors_url`.
        *   Fetches contributor data from `/repos/{owner}/{repo}/contributors`.
        *   Gets contributor count by taking the `len()` of the `contributors_data` list.
    *   **3. Commit Activity:**
        *   Constructs `commit_activity_url`.
        *   Fetches commit activity data from `/repos/{owner}/{repo}/stats/commit_activity`.
        *   Calculates `total_commits_last_year` by summing up the commit counts for each week in the last year (from the API response).
    *   **Structure for Grafana:** Creates `grafana_data` dictionary with `"metrics"` and `"timestamp"`.
    *   **Return JSON:** Returns JSON string using `json.dumps()`.
    *   **Error Handling:** If any `requests.exceptions.RequestException` occurs, prints an error message and returns `None`.

3.  **`if __name__ == "__main__":` Block (Example Usage):**
    *   **Configuration:**
        *   Sets `github_repo_owner`, `github_repo_name`, and `github_personal_access_token` (you **must** replace placeholders).
        *   **Important:** It's highly recommended to set `github_personal_access_token` or set it as an environment variable `GITHUB_TOKEN`.  Otherwise, you will likely hit GitHub API rate limits quickly, especially for public repositories.
    *   **Call `get_github_repo_metrics_for_grafana`:** Calls the function with configured parameters.
    *   **Print Output:** Prints JSON output to console if successful, error message if not.

4.  **"How to use this with Grafana" Comments:**
    *   Provides instructions for integrating with Grafana, similar to the Redis script, outlining options: File, Pushgateway, Exporter, Telegraf, and **Direct JSON API Endpoint via Webserver**.
    *   The "Direct JSON API Endpoint" option (e) is added as a relatively simple way to get real-time data into Grafana if you're willing to set up a basic web server.

**To Use:**

1.  **Install `requests` library:**
    ```bash
    pip install requests
    ```

2.  **Get a GitHub Personal Access Token:**
    *   Go to your GitHub Settings -> Developer settings -> Personal access tokens -> Generate new token.
    *   Give it a descriptive name.
    *   You usually don't need to select any scopes for public repository metrics. For private repositories, you might need `repo` scope.
    *   Copy the generated token.
    *   **Set it as `github_personal_access_token` variable in the script OR set it as an environment variable `GITHUB_TOKEN`.**  Environment variable is generally more secure.

3.  **Customize Configuration:**
    *   Modify `github_repo_owner` and `github_repo_name` in the `if __name__ == "__main__":` block.
    *   Set your `github_personal_access_token` or environment variable.

4.  **Run the script:**
    ```bash
    python your_script_name.py
    ```
    This will print the JSON output to your console.

5.  **Integrate with Grafana:**
    *   Choose an integration method from the comments in the script.
    *   **For a relatively quick setup, using a "JSON API" data source with a simple web server (option e) or using Telegraf (option d) might be good starting points.**  For more robust production, Prometheus-based solutions (b or c) are recommended.

**Important Considerations:**

*   **GitHub API Rate Limits:**  Using a Personal Access Token is crucial to avoid hitting API rate limits, especially if you plan to poll frequently. Without a token, you'll be limited to very few requests per hour.
*   **Error Handling:** The script includes basic error handling, but you might want to enhance it for production use (e.g., logging, more specific error messages).
*   **Metrics Selection:** The script retrieves a set of common repository metrics. You can easily customize it to fetch more metrics available from the GitHub API based on your monitoring needs.  Refer to the GitHub API documentation for the `/repos/{owner}/{repo}` endpoint and related endpoints for available metrics.
*   **UI Output (Clarification):** The script itself outputs JSON text to the console. To visualize this data in a UI (like Grafana), you need to integrate it with Grafana using one of the methods described in the comments. The script provides the *data* that will be displayed in the Grafana UI, but it's not a UI itself.
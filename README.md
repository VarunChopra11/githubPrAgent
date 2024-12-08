# GitHub Pull Request Analyzer

This project provides a service for analyzing GitHub Pull Requests (PRs) using Azure's deployed GPT-4-o-mini model. The primary goal is to process and analyze PR changes programmatically to assist developers with code reviews, suggestions, or understanding complex PRs more effectively. The service is accessible via an API backend.

---

## Project Approach

The project employs the following approach:

- **Prompt Engineering**: The service constructs a prompt for the GPT-4-o-mini model using the changes from a GitHub Pull Request. This prompt is designed to guide the model to analyze the PR and provide meaningful insights or feedback.

- **Task Management**: Celery and Redis are used to queue and manage tasks for efficient processing, ensuring scalability and robustness.

- **API Endpoints**:
  - Submit a PR for analysis.
  - Check the status of an analysis task.
  - Retrieve the results of an analysis task.

- **Deployed Service**: The application is deployed at [`https://githubpragent.onrender.com/docs`](https://githubpragent.onrender.com/docs) for easy access. Users can also run it locally or via Docker.

---

## Features

- Analyze both public and private repositories (requires GitHub token for private repositories).
- Track the status of analysis tasks.
- Retrieve detailed insights on the analyzed Pull Request.
- User-friendly API documentation available at `/docs`.

---

## How to Use

### Option 1: Use the Deployed Service

The service is deployed at [https://githubpragent.onrender.com](https://githubpragent.onrender.com).

1. Visit [`https://githubpragent.onrender.com/docs`](https://githubpragent.onrender.com/docs) to explore the API documentation.

2. Submit a POST request to the `/analyze-pr` endpoint with the following example JSON:

   ```json
   {
       "repo_url": "https://github.com/your/repo",
       "pr_number": 123,
       "github_token": "your_personal_access_token(optional_for_public_repos)"
   }
   ```

   - Replace `repo_url`, `pr_number`, and `github_token` with your specific values.
   - The `github_token` is optional for public repositories.

3. Use the returned `task_id` to:
   - Check task status: `/status/{task_id}`
   - Retrieve task results: `/results/{task_id}`

### Option 2: Run Locally

#### Clone the Repository

```bash
git clone https://github.com/varunchopra11/githubPrAgent.git
cd githubPrAgent
```

#### Install Dependencies

Create a virtual environment and install the required dependencies:

```bash
python -m venv myenv
source myenv/bin/activate  # Use myenv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Run the Application

```bash
python -m app.main
```

Access the service at [`http://localhost:8000/docs`](http://localhost:8000/docs).

### Option 3: Use Docker

Setup .env file in project's root directory.

#### Build the Docker Image

```bash
docker build -t githubagent .
```

#### Run the Container

```bash
docker run -d -p 8000:8000 --env-file .env githubagent
```

This setup ensures that your project runs with environment variables from the `.env` file and binds to port 8000. Access the service at [`http://localhost:8000/docs`](http://localhost:8000/docs).

---

## Environment Variables

The application uses environment variables defined in a `.env` file for configuration. Ensure your `.env` file includes:

```plaintext
AZURE_ENDPOINT=<your_azure_endpoint>
AZURE_API_KEY=<your_azure_api_key>
REDIS_URL=<your_redis_url>
```

---

## API Endpoints Overview

1. **Analyze PR**: `POST /analyze-pr`
   - **Input**: Repository URL, PR number, optional GitHub token.
   - **Output**: `task_id` for tracking analysis.

2. **Get Task Status**: `GET /status/{task_id}`
   - **Input**: `task_id`
   - **Output**: Current status of the analysis task.

3. **Get Task Results**: `GET /results/{task_id}`
   - **Input**: `task_id`
   - **Output**: Results of the analysis.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your proposed changes.

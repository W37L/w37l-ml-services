# W37L ML Service API

## Overview
The W37L ML Service API is designed to provide machine learning functionalities for a decentralized social media platform. This service handles tasks such as profanity detection, hashtag generation, and recommendation systems, using a FastAPI framework with a strong emphasis on modularity and maintainability through dependency injection.

## Prerequisites
To run this ML Service, you will need:
- Python 3.8 or higher
- FastAPI
- Uvicorn (ASGI server)
- Dependencies as listed in the `requirements.txt` file

## Configuration
Before running the service, ensure your environment is set up with the necessary configurations:

```bash
export MLSERVICE_STORAGE_DIR=<path_to_storage_directory>
export ML_Service_LOG_LEVEL=INFO
```

## Installation

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/W37L/W37L-ML-Service.git
cd W37L-ML-Service
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Running the API

Start the ML service using Uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

This command runs the service on localhost at port 8000 with live reloading enabled.

## API Endpoints

The ML Service API provides several endpoints for machine learning tasks:

### Profanity Check
- **POST /MLService/checkProfanity**
  Check text for profanity and return results.

### Hashtag Generation
- **GET /MLService/getHashtag**
  Generate hashtags based on the provided text.

### Trending Topics
- **GET /MLService/getTrendingTopics**
  Fetch current trending topics.

### User Recommendations
- **GET /MLService/recommendationUser**
  Get user recommendations based on preferences.

### Post Recommendations
- **GET /MLService/recommendationPost**
  Get post recommendations tailored to user interests.

## CORS Middleware
The API is configured with CORS middleware to allow requests from all origins, which is suitable for development. For production, it is recommended to restrict origins to secure the API.

## Deployment
For production environments, ensure that the `MLSERVICE_STORAGE_DIR` and logging levels are configured appropriately. It is also recommended to run the service behind a secure reverse proxy like Nginx.

## Testing
You can test the API by accessing the live instance at `http://ml.w37l.com:8000`. This instance runs in a Docker container and includes Swagger UI for an interactive API documentation and testing experience. Use Swagger to view detailed information about each endpoint, including parameters and required data formats, or use Postman to send requests and analyze responses.

To test using Swagger:
1. Open a web browser and navigate to `http://ml.w37l.com:8000/docs`.
2. Explore the available API endpoints.
3. Execute API calls directly from the Swagger UI by entering required parameters and executing the request.

For Postman:
1. Open Postman and configure the request URL to `http://ml.w37l.com:8000/<endpoint>`.
2. Set the appropriate HTTP method and headers.
3. Send the request and view the response directly in Postman.


## Contributing
Contributions to the ML Service API are welcome! Please fork the repository, create a new branch for your features, and submit a pull request.


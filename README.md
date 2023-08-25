
# Microservices E-commerce

Welcome to the Microservices E-commerce ! This project showcases a refined microservices architecture implemented using FastAPI, serving as an illustration of best practices in modern application development.

## High-Level Architecture

Our application orchestrates the following order microservice responsible for managing customer orders, dynamic product location assignment, and seamless inter-service communication.:


## Setup and Running

To get the application up and running:

1. Install Python (version >= 3.7) and pip if not already present.
2. Clone this repository: `https://github.com/Matt-Murungi/microservice-setup.git`
3. Navigate to each microservice directory and ensure dependency installation:
   ```
   pienv install -r requirements.txt
   ```
4. Launch the microservice via `uvicorn`:
   ```
   uvicorn order_service.main:app
      ```
5. Launch the swagger doc to view the documentation for the implemented endpoints.
      ```
      http://127.0.0.1:8000/docs
      ```

## Considerations

Data Integrity Assurance: Asynchronous communication enforces eventual consistency across services.
Strengthening Resilience: Rigorous error handling and validation mechanisms elevate application robustness.
Security Measures: Security measures, including authentication and authorization, underscore production readiness.
Potential for Scaling: Docker containerization aligns with scalability goals, simplifying scaling and deployment.

## Authors
Murungi Matthew

## License

This project is licensed under the MIT License.
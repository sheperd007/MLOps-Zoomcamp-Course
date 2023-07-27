The project aims to develop an efficient deep learning model for detecting SARS-CoV-2 infection using CT-scan images. Leveraging GitLab CI/CD, Docker Swarm, MLflow, Evidently, and pytest, we ensure seamless development, testing, and deployment of the model. The entire workflow guarantees reproducibility, transparency, and efficient model evaluation.

Objectives:

Data Collection: Gather a comprehensive dataset of SARS-CoV-2 CT-scan images from Kaggle, ensuring diverse and balanced samples.

Model Development: Implement a Deep Residual Network (ResNet) architecture, taking advantage of its skip connections to facilitate efficient learning and avoid vanishing gradient issues. Optimize the model for image classification tasks using transfer learning techniques.

GitLab CI/CD Setup: Establish a robust continuous integration and continuous deployment pipeline using GitLab CI/CD. Automated testing, version control, and code review ensure consistent model development.

Docker Swarm Deployment: Deploy the entire project, including the model and MLflow server, using Docker Swarm to ensure scalability, load balancing, and easy management of containers in a cluster environment.

MLflow Integration: Integrate MLflow to track model experiments, parameters, and metrics, providing clear insights into the model's performance and facilitating model versioning and comparisons.

Evidently for Model Evaluation: Employ Evidently to analyze and visualize model performance metrics and interpretability. Gain a comprehensive understanding of model bias, fairness, and robustness.

Unit Testing with pytest: Implement unit tests using pytest to validate the correctness and consistency of model components, data preprocessing, and utility functions.

FastAPI Deployment: Deploy the trained ResNet model using FastAPI, building a RESTful API for easy inference and model access. The API will enable integration with various healthcare systems and applications.

Impact:
The successful completion of this project will contribute significantly to the fight against COVID-19 by providing an accurate and efficient diagnostic tool based on CT-scan images. The use of modern DevOps practices, such as GitLab CI/CD and Docker Swarm, will enable seamless collaboration and automated deployment. MLflow and Evidently will enhance model transparency, explainability, and reproducibility, while pytest ensures code reliability through automated testing.

Future Scope:
The project can be extended to include more advanced deep learning architectures, such as attention-based models or transformers. Additionally, continuous improvement through transfer learning on new COVID-19 data can enhance model generalization and accuracy. Collaboration with healthcare organizations can facilitate real-world validation and deployment of the model in clinical settings, potentially leading to significant public health benefits.

# Deployment
Unfortunately, I didn't have access to any kind of cloud storage and computing system. so I built the Project Top of a Swarm Cluster.
1. you Need to Lunch a Docker Cluster with Evidently, Prefect, Mlflow, and a Traefik as a reverse proxy and a Gitlab Runner Instance.
2. you need to register the gitlab runner on gitlab.com and add this repository to gitlab.
3. you should define variables like EVIDENTLY inside Gitlab variables so that gitlab CI/CD can access them.
4. run the CI/CD flow. it will deploy the model on Swarm Cluster.

Traefik use case : https://collabnix.com/how-to-use-traefik-v2-as-a-reverse-proxy-for-docker/
it has been used for deploying multiple projects. just for showing scalability of platform.

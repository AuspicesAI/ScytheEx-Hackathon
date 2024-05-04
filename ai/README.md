# ScythEx/ai

## Table of Contents

- [Project Status](#project-status)

  - [Current State](#current-state)
  - [Ongoing Development](#ongoing-development)
  - [Maintenance](#maintenance)
  - [Future Plans](#future-plans)

- [Badges](#badges)
- [Setting Up the Environment](#setting-up-the-environment)
  - [Poetry Environment Setup](#Poetry-environment-setup)
- [Repository Structure](#repository-structure)
- [Project Workflow](#project-workflow)
  - [Input and Output](#input-and-output)
    - [Input](#input)
    - [Output](#output)
- [Authors and Acknowledgment](#authors-and-acknowledgment)

## Project Status

This section provides an overview of the current status of the project, including development progress, maintenance updates, and future plans.

### Current State

> [!Warning]
> **Model Selection Caution**<br>The use of Logistic Regression as the model in this project was primarily driven by the limited timeframe of the hackathon. This approach bypasses the comprehensive model evaluation usually recommended, which involves testing multiple models to identify the best performer under varied scenarios.

> [!Warning]
> **Data Completeness Caution**<br>The dataset currently employed in this project is in a preliminary phase and not comprehensive. We are actively working on expanding this dataset with more extensive feature engineering, additional data points, and a broader spectrum of malware samples. The dataset's final iteration is expected to differ significantly from its current form.

### Ongoing Development

> [!Important]
> **Model Optimization**<br>Ongoing development efforts are focused on evaluating a range of predictive models beyond Logistic Regression.These improvements aim to adhere to best practices in model selection and are expected to enhance performance significantly.

> [!Important]
> **Data Enhancement**<br>The current dataset is undergoing substantial expansion and refinement through advanced feature engineering and by increasing the volume and diversity of malware samples included. These enhancements will ensure a more robust dataset, better suited for training highly accurate models.

> [!Important]
> **Code Refactoring of `main.py`**<br>We are planning substantial enhancements to the `main.py` file to align with software engineering best practices. This includes restructuring the code into modular Python modules, which will improve maintainability, scalability, and readability.

### Maintenance

> [!Important]
> As ScytheEx is in the early development phase, regular updates will be made to the environment and codebase. These updates will address any emerging issues and add new features as they are developed

### Future Plans

- **Advanced AI Model Implementation**: Plans include incorporating a sophisticated Mistral model to enhance the unit test generation and code analysis capabilities.
- **Deployment Strategy**: While the current focus is on foundational development, there are plans to deploy Zenith on a scalable and reliable cloud platform in the future.
- **Code Fixing Model**: After the initial launch of Zenith, we will be adding the code fixing feature. Which actually fixes the actual code based on the unit tests.

## Badges

<h2 align="left">
  <img alt="Py`Torch" src="https://img.shields.io/badge/-poetry-white?style=for-the-badge&logo=poetry"> <img alt="Python" src="https://img.shields.io/badge/-Python%20-yellow?style=for-the-badge&logo=python" /> <img alt="AnaPoetry" src="https://img.shields.io/badge/-MLFlow-white?style=for-the-badge&logo=mlflow"> <img alt="VS code" src="https://img.shields.io/badge/-Visual%20Studio%20Code-blue?style=for-the-badge&logo=visualstudiocode"> <img alt="Jupyter" src="https://img.shields.io/badge/-Jupyter-white?style=for-the-badge&logo=jupyter"> <img alt="Pandas" src="https://img.shields.io/badge/-Pandas-darkblue?style=for-the-badge&logo=pandas"> <img alt="PyTorch" src="https://img.shields.io/badge/-Redis-black?style=for-the-badge&logo=redis">

  </h2>

## Setting Up the Environment

### Poetry Environment Setup

To set up the Poetry environment for this project, go through the following steps:

- Go to ScytheEx/ai directory
- Run the following script to set up the environment:

  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

- This script will prepare TestGenAI environment using Poetry, and other verifications/installations for the environment.

## Repository Structure

```bash
Zenith/
│
├── .gitlab-ci.yml               # CI/CD pipeline configuration
├── Dockerfile                   # Docker configuration for containerization
├── README.md                    # Project overview, setup, usage, and contribution guide
├── pyproject.toml               # Poetry configuration for Python dependencies
├── poetry.lock                  # Locked dependencies for consistent builds
├── main.py                      # Main file that runs in production
│
├── data/                        # Data files (excluded from version control)
│   └── README.md                # Data format, structure, and management guidelines
│
├── models/                      # AI models and related resources
│   └── Neris_LogReg_model.pkl   # Final Model used in production
│
├── notebooks/                   # Jupyter notebooks for model development
│   ├── LogRegNerisProcessing.ipynb # Experimental file to build the final Logistic Regression Model
│   └── XGBNerisProcessing.ipynb  # Experimental file to build the initial XGBoost model
│
└── internal_lib/                # A private library, will probably be removed later. and new modules will be added for `main.py`
    ├── __init__.py              # Module initialization
    └── [model modules]          # Individual model logic files
               # Logging guidelines and analysis

```

## Project Workflow

Packets from the network get forwarded to the model via Redis DB in Real-time, Once retrieved, the data is processed to match the data that was shown to the model during training. A Logistic Regression model predicts the status of the packet e.g "Botnet" or "Background", The Prediciton along side some chosen packet data is uploaded to the Redis DB to be sent tot he UI and Back-end

### Input and Output

#### Input

- **Automated Packet Retrieval**: Packets from the network get forwarded to the model via Redis DB in Real-time
- **Processing**: Once retrieved, the data is processed to match the data that was shown to the model during training.

#### Output

- **Packet Status Prediction**: A Logistic Regression model predicts the status of the packet e.g "Botnet" or "Background"
- **Upload to Redis**: The Prediciton along side some chosen packet data is uploaded to the Redis DB to be sent tot he UI and Back-end

## Authors and acknowledgment

- **Yousinator** - _CEO/Head of AI_ - [Yousinator](https://yousinator.github.io) - _The AI code and the AI application in general_

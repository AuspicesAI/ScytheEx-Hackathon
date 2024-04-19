# Zenith

## Table of Contents

- [Project Status](#project-status)

  - [Current State](#current-state)
  - [Ongoing Development](#ongoing-development)
  - [Maintenance](#maintenance)
  - [Future Plans](#future-plans)

- [Description](#description)
  - [Overview](#overview)
  - [Features](#features)
  - [Purpose and Use Cases](#purpose-and-use-cases)
  - [Technologies Used](#technologies-used)
  - [Motivation](#motivation)
- [Badges](#badges)
- [Visuals](#visuals)
- [Setting Up the Environment](#setting-up-the-environment)
  - [Poetry Environment Setup](#Poetry-environment-setup)
- [Repository Structure](#repository-structure)
- [Project Workflow](#project-workflow)
  - [Input and Output](#input-and-output)
    - [Input](#input)
    - [Output](#output)
  - [Testing and Validation](#testing-and-validation)
- [Authors and Acknowledgment](#authors-and-acknowledgment)

  ## Project Status

This section provides an overview of the current status of the project, including development progress, maintenance updates, and future plans.

### Current State

- **Version**: Version 0.1
- **Last Update**: 11/2/2023
- **Stability**: The project is still in the initiation proccess, so it isn't stable
- **Known Issues**: Poetry environment OpenSSL doesn't work

### Ongoing Development

- **In Progress**: The focus is now on starting the core development of Zenith's features, including integrating the AI models and developing the CLI and UI interfaces.
- **Upcoming Features**: Code Analysis Model

### Maintenance

- **Regular Updates**: As Zenith is in the early development phase, regular updates will be made to the environment and codebase. These updates will address any emerging issues and add new features as they are developed.

### Future Plans

- **Advanced AI Model Implementation**: Plans include incorporating a sophisticated Mistral model to enhance the unit test generation and code analysis capabilities.
- **Deployment Strategy**: While the current focus is on foundational development, there are plans to deploy Zenith on a scalable and reliable cloud platform in the future.
- **Code Fixing Model**: After the initial launch of Zenith, we will be adding the code fixing feature. Which actually fixes the actual code based on the unit tests.

## Description

### Overview

The AuspicesAI Zenith is an advanced CLI tool designed to automate the creation of unit tests for software code. Utilizing advanced AI algorithms via the Mistral API, Zenith reads and analyzes source code to intelligently generate corresponding unit tests. This streamlines the testing process, enhances code reliability, and integrates seamlessly into the software development workflow through its intuitive CLI and user-friendly UI.

### Features

- **Automated Test Generation**: Employs AI to automatically generate unit tests for specific pieces of code.
- **AI-Powered Analysis**: Uses advanced AI algorithms, accessed through the Mistral API, for in-depth understanding of code structure and functionality.
- **Suggested Solutions**: Provides code fixes and suggestions for premium users if generated tests uncover potential issues.
- **Code Fixing (Future Versions)**: Future iterations of Zenith will actively rectify identified code issues, offering an even more advanced level of automation.
- **CLI and UI Integration**: Zenith offers a versatile CLI for seamless integration with development pipelines, and a user-friendly UI for easy interaction and result visualization.

### Purpose and Use Cases

Zenith is particularly beneficial for developers and teams aiming to expedite their testing process, especially in large-scale projects where manual test writing is a significant bottleneck. The tool’s automation capabilities free developers to concentrate on more complex tasks, thereby boosting overall productivity.

### Technologies Used

Developed in Python, Zenith harnesses the power of the Mistral API for AI capabilities and employs Poetry for environment management. Its robust CLI tool facilitates easy integration and automation in various development environments, while the UI provides a clear and interactive way for users to manage and review test results.

### Motivation

Developed to address the challenge of time-consuming manual test writing, aiming to enhance efficiency and code quality in software development projects.

## Badges

<h2 align="left">
  <img alt="Py`Torch" src="https://img.shields.io/badge/-poetry-white?style=for-the-badge&logo=poetry"> <img alt="Python" src="https://img.shields.io/badge/-Python%20-yellow?style=for-the-badge&logo=python" /> <img alt="AnaPoetry" src="https://img.shields.io/badge/-MLFlow-white?style=for-the-badge&logo=mlflow"> <img alt="VS code" src="https://img.shields.io/badge/-Visual%20Studio%20Code-blue?style=for-the-badge&logo=visualstudiocode"> <img alt="Jupyter" src="https://img.shields.io/badge/-Jupyter-white?style=for-the-badge&logo=jupyter"> <img alt="Pandas" src="https://img.shields.io/badge/-Pandas-darkblue?style=for-the-badge&logo=pandas"> <img alt="PuTorch" src="https://img.shields.io/badge/-Pytorch-white?style=for-the-badge&logo=pytorch">

  </h2>

## Visuals

Depending on what you are making, it can be a good idea to include screenshots or even a video (you'll frequently see GIFs rather than actual videos). Tools like ttygif can help, but check out Asciinema for a more sophisticated method.

## Setting Up the Environment

### Poetry Environment Setup

To set up the Poetry environment for this project, go through the following steps:

- Go to zenith/TestGenAI directory
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
│
├── data/                        # Data files (excluded from version control)
│   └── README.md                # Data format, structure, and management guidelines
│
├── docs/                        # Comprehensive project documentation
│   ├── Architecture.md          # Detailed architecture diagrams and descriptions
│   ├── API_Documentation.md     # API endpoints and usage documentation
│   ├── SetupGuide.md            # Setup and installation instructions
│   └── UserGuide.md             # Detailed user guide and examples
│
├── models/                      # AI models and related resources
│   └── README.md                # Model descriptions and performance metrics
│
├── notebooks/                   # Jupyter notebooks for model development
│   ├── CodeAnalysis/
│   │   ├── PromptFineTuning.ipynb
│   │   ├── FineTuning.ipynb
│   │   └── PromptEngineering.ipynb
│   ├── TestGeneration/
│   │   ├── PromptFineTuning.ipynb
│   │   ├── FineTuning.ipynb
│   │   └── PromptEngineering.ipynb
│   └── CodeSuggestion/
│   │   ├── PromptFineTuning.ipynb
│       ├── FineTuning.ipynb
│       └── PromptEngineering.ipynb
│
├── input/                       # Initial input files and model prompts
│   ├── prompts/                 # Model-specific prompts
│   │   ├── CodeAnalysis.txt
│   │   ├── TestGeneration.txt
│   │   └── CodeSuggestion.txt
│   └── initial_code_file.py     # Initial code file for processing
│
├── output/                      # Output files post-processing
│   ├── CodeAnalysis_result.txt  # Result from Code Analysis model
│   └── CodeSuggestion_result.txt # Result from Code Suggestion model
│
├── src/                         # Application source code
│   ├── main.py                  # Main application entry point
│   └── [additional modules]     # Other source files and modules
│
├── tests/                       # Automated tests
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── README.md                # Testing guidelines and best practices
│
├── zenith_models/               # Core prediction logic modules
│   ├── __init__.py              # Module initialization
│   └── [model modules]          # Individual model logic files
│
├── .gitignore                   # Specifies untracked files to ignore
├── logs/                        # Application logs
│   └── README.md                # Logging guidelines and analysis
├── config/                      # Configuration files and environment variables
│   └── README.md                # Configuration management instructions
└── scripts/                     # Utility scripts for deployment and maintenance
    └── README.md                # Description and usage of each script

```

## Project Workflow

Zenith automates unit testing in software development through a sophisticated AI-driven approach. Users interact with Zenith via a dedicated CLI tool, which handles file operations and process management seamlessly.

### Input and Output

#### Input

- **Automated File Retrieval**: Users provide the source code for unit testing through Zenith's CLI tool. The tool automatically retrieves the source code file from the user's repository.
- **Processing**: Once retrieved, the source code is processed using Zenith's proprietary AI models. These models are designed to analyze the code's structure and functionality, laying the groundwork for test generation.

#### Output

- **Unit Test Generation**: The AI-driven Test Generation model automatically creates unit tests tailored to the input source code.
- **Code Suggestions**: For users with premium access, Zenith offers additional value by generating code improvement suggestions, particularly helpful if potential issues are identified during testing.
- **Automated File Delivery**: The generated unit tests and any code suggestions are automatically delivered back to the user's repository via the CLI tool.

### Workflow Overview

- **Initiation**: Users start the process by issuing a command through Zenith's CLI tool, specifying the target source code file in their repository.
- **Automated Processing**: Zenith's backend processes kick in:
  - **Code Analysis**: The AI models analyze the input code.
  - **Test Generation**: Relevant and comprehensive unit tests are automatically generated.
  - **Code Suggestions**: For premium plans, actionable code improvement suggestions are generated.
- **Output Delivery**: The CLI tool automatically uploads the generated unit tests and suggestions back to the user's repository.
- **Review and Integration**: Users can review the outputs directly in their repository and integrate them into their development workflow.

### Testing and Validation

To ensure the reliability and correctness of the application, follow these testing and validation steps:

1. **Unit Testing**

   - Run the unit tests provided in the `tests/` directory to ensure that each component of the application is working correctly.
   - Use the following command to run all unit tests:

     ```bash
     pytest
     ```

2. **Output Validation**

   - Manually review the generated unit tests in the `outputs/` directory to ensure they match the expected format and cover the necessary aspects of the input code.
   - Optionally, integrate these unit tests into your existing codebase and run them to validate their functionality.

3. **Feedback and Iteration**
   - Collect feedback on the output quality from users or team members.
   - Iterate on the application's logic based on feedback to improve the quality of the generated unit tests.

## Authors and acknowledgment

- **Yousinator** - _CEO/AI R&D Lead_ - [Yousinator](https://yousinator.github.io) - _The LLM code and the application in general_
- **smadi0x86** - _COO/Security E&R Lead_ - [smadi0x86](https://github.com/smadi0x86) - Infrastructure, DevSecOps and architecture

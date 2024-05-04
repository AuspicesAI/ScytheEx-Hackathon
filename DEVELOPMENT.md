# ScytheEx Development Guide

## Introduction

Welcome to the ScytheEx development guide. This document provides a structured approach for developers contributing to ScytheEx, a sophisticated cybersecurity tool designed for real-time network traffic analysis and threat detection. Here, you will find detailed instructions on setting up your development environment, a checklist of tasks categorized by project component, and guidelines for coding and contributions.

> [!Important]
> These are few of the features that are planned to be implemented, you can also suggest new features and work on them. Open an issue and discuss the feature you want to implement.

## Setting Up Your Development Environment

To contribute effectively, set up your development environment according to the specifications in the `README.md`. Additionally, ensure you have the following tools configured:

- **Integrated Development Environment (IDE)**: We recommend using PyCharm or Visual Studio Code with Python and TypeScript extensions installed.
- **Code Linters**: Use Flake8 for Python and ESLint for TypeScript to maintain code quality.
- **Version Control**: Contributions should be managed through Git. Familiarity with basic Git operations is essential.

## Feature Development Checklist

Development tasks are categorized by project modules to streamline the contribution process.

### AI and Analytics (ai/)

- **Automate Malware PCAP Data Handling**:
  - Develop a script to periodically download malware PCAP files from trusted sources.
  - Create a parser to extract relevant features from PCAP files for AI training.
  - Automate the retraining process of AI models with new datasets to adapt to evolving threats.

### Backend Services (backend/)

- **Dynamic Configuration Implementation**:

  - Build a system in `backend/core/` for dynamically loading and applying changes from `config.toml` without system restarts.
  - Ensure components like `redis_publisher.py` and `redis_subscriber.py` adapt to configuration changes in real-time.

### Web and Visualization (frontend/)

- **Dashboard Enhancements**:
  - Upgrade the dashboard to effectively display real-time data on traffic and threats.
  - Implement user-customizable features for visualizing reports and alerts.

### Threat Intelligence (backend/intelligence/)

- **Integrate Threat Intelligence Feeds**:
  - Enable configuration of custom and default threat intelligence sources through `config.toml`.
  - Utilize external APIs like VirusTotal and Hybrid Analysis to enhance detection capabilities.

### Configuration and Deployment

- **Kubernetes and Helm**:
  - Setup Helm charts for deploying ScytheEx on Kubernetes clusters.
  - ScytheEx should be deployed as daemonset on all nodes in the cluster.

## Testing

- Develop and run comprehensive tests for all new features or updates using `pytest` for backend and AI components, and `jest` for frontend testing.
- Ensure all tests pass before submitting pull requests.

## Code Style and Contribution Guidelines

- Follow PEP8 standards for Python code and adhere to best practices for TypeScript.
- Document all changes comprehensively; use clear, descriptive commit messages.

## Continuous Integration

- Implement CI workflows with GitHub Actions to automate tests, lint checks, and builds upon new commits and pull requests.

## Documentation

- Keep all project documentation current to reflect feature changes or additions.
- Maintain high-quality inline and API documentation for ease of maintenance and future development.

## Future Directions

- **ScytheEx Kubernetes Operator**: Develop a Kubernetes operator which will cordon and drain nodes when a threat is detected, automating the mitigation process.
- **Machine Learning Enhancements**: Implement advanced machine learning models that can detect malware execution patterns related to operating system internals (e.g., CPU usage, registry changes).
- **Real-Time Threat Response**: Integrate automated threat response mechanisms to mitigate threats as they are detected, enhancing system resilience.
- **Static & Dynamic Malware Analysis**: Expand capabilities to analyze malware executables both statically and dynamically to understand their behavior and impact on the system.
- **Trending Malware Techniques Analysis**: Begin collection and analysis of emerging malware techniques like DLL Side-Loading and Process Injection to better train the model in recognizing these threats.

## License

All contributions to this project must comply with the terms outlined in the LICENSE file. For more details, refer to the full license documentation.

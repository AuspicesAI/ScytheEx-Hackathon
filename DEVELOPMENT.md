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

Huge changes coming soon...

## Future Directions

- **ScytheEx Kubernetes Operator**: Develop a Kubernetes operator which will cordon and drain nodes when a threat is detected, automating the mitigation process.
- **Machine Learning Enhancements**: Implement advanced machine learning models that can detect malware execution patterns related to operating system internals (e.g., CPU usage, registry changes).
- **Real-Time Threat Response**: Integrate automated threat response mechanisms to mitigate threats as they are detected, enhancing system resilience.
- **Static & Dynamic Malware Analysis**: Expand capabilities to analyze malware executables both statically and dynamically to understand their behavior and impact on the system.
- **Trending Malware Techniques Analysis**: Begin collection and analysis of emerging malware techniques like DLL Side-Loading and Process Injection to better train the model in recognizing these threats.

## License

All contributions to this project must comply with the terms outlined in the LICENSE file. For more details, refer to the full license documentation.

![ScytheEx Logo](https://github.com/AuspicesAI/ScytheEx/assets/75253629/edfcdbb7-cdec-49b6-aacb-314bcc9faeda)

![ScytheEx Banner](https://github.com/AuspicesAI/ScytheEx/assets/75253629/226966e1-0d2e-400c-a94b-e6cdac9e4e3e)

## Overview

ScytheEx is an advanced cybersecurity tool designed for real-time network traffic monitoring and threat analysis. Initially developed as a Linux service daemon and capable of deployment on Kubernetes bare metal, this versatile solution extends its functionality across various operating systems.

ScytheEx integrates AI-driven analytics to detect activities post-attack, adhering to the philosophy that despite advanced protective measures like EDR or AV, malware may still execute on the system. The tool operates at this post-execution level to identify malicious activities and generate YARA rules, providing continuous feeds to enhance other detection tools and technologies.

> [!Warning]
> ScytheEx project is still in an early stage which means that any feature changes are very welcome. Also note that anything can break, stable release is still not close.

### Main Features

- AI-powered network traffic analysis.
- Real-time threat detection and mitigation.
- Background process management for continuous monitoring.
- Integrated threat intelligence.
- Robust mitigation strategies including IP blacklisting.
- Customizable configuration to fit your business need.
- HTTP Server for visualization.
- Support for Kubernetes deployments.
- 3rd Party APIs usage (e.g: Virus Total, Hybrid-Analysis)

## Workflow

![image](https://github.com/AuspicesAI/ScytheEx/assets/75253629/6edbdb92-ce46-4d8e-885f-5bfba04139da)

## Setup Instructions

![Kubernetes Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/11bdfe89-175d-4e1c-87df-2ec29fe5a32e)

### Kubernetes Deployment using Helm

> [!Important]
> By default, **ScytheEx** runs as a daemonset on Kubernetes and is not fully tested which may break; Kubernetes admins can customize the deployment as needed.

1. **Prepare Your Environment**:

   - Ensure Kubernetes cluster is set up and `kubectl` is configured.
   - Install Helm on your system.

2. **Deploy ScytheEx**:
   - Clone the repository and navigate to the Helm chart directory.
   - Modify the values in `values.yaml` as necessary, particularly the network interfaces and Redis settings.
   - Run `helm install scytheex ./scytheex-chart` to deploy to your Kubernetes cluster.

![Debian Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/cddd869a-1080-45d9-8668-dc05b0d41ea6)

### Debian-Based Linux Host Setup

1. **Installation**:

   - Use the following command to install ScytheEx directly:
     ```bash
     curl -sSL https://raw.githubusercontent.com/AuspicesAI/ScytheEx/main/setup/debian_linux.sh | sudo bash
     ```
   - This script will clone the ScytheEx repository, install Python dependencies, set up the environment, and configure ScytheEx as a systemd service.

2. **Enable Service**:
   - Run `systemctl enable scytheex` to enable the ScytheEx service to automatically start at boot time.

![Windows Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/e8cc8fba-903a-4f18-886b-4dab1ab8eeb7)

### Windows Host Setup

> [!Warning]
> Still not tested, will probably break.

1. **Download and Install**:

   - Download the latest release from the [ScytheEx Repository](https://github.com/AuspicesAI/ScytheEx/releases).
   - Ensure Python is installed on your system. If not, download and install it from [Python's official site](https://www.python.org/downloads/).
   - Open a command prompt as Administrator and navigate to the directory where ScytheEx is downloaded.
   - Install required Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configure and Run**:
   - Open the `config.toml` file located in your ScytheEx installation directory.
   - Manually adjust the network interface settings under the appropriate section to correspond with your system.
   - Run `setup_windows.bat` to configure and start ScytheEx as a service. Make sure to run the command prompt as Administrator.

## How to Contribute

Interested in contributing to ScytheEx? Please read our [CONTRIBUTE.md](https://github.com/AuspicesAI/ScytheEx/CONTRIBUTE.md) and [DEVELOPMENT.md](https://github.com/AuspicesAI/ScytheEx/DEVELOPMENT.md) for guidelines on how to get involved in this project.

## License

This project is licensed under the Apache License 2.0. For more details, see the LICENSE file in the root directory of this project.

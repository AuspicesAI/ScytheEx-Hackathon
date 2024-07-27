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

### Workflow

![image](https://github.com/AuspicesAI/ScytheEx/assets/75253629/1d448ae9-8872-4b2e-bf1b-b5cf30c0492d)

## Setup Instructions

![Kubernetes Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/11bdfe89-175d-4e1c-87df-2ec29fe5a32e)

### Kubernetes Deployment using Helm

> [!Important]
> By default, **ScytheEx** runs as a daemonset on Kubernetes and is not fully tested which may break; Kubernetes admins can customize the deployment as needed.

Huge changes coming...

![Debian Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/cddd869a-1080-45d9-8668-dc05b0d41ea6)

### Debian-Based Linux Host Setup

Huge changes coming...

![Windows Setup](https://github.com/AuspicesAI/ScytheEx/assets/75253629/e8cc8fba-903a-4f18-886b-4dab1ab8eeb7)

### Windows Setup

Huge changes coming...

## How to Contribute

Interested in contributing to ScytheEx? Please read our [CONTRIBUTE.md](CONTRIBUTE.md) and [DEVELOPMENT.md](DEVELOPMENT.md) for guidelines on how to get involved in this project.

## License

This project is licensed under the GNU General Public License v3.0. For more details, see the LICENSE file in the root directory of this project.

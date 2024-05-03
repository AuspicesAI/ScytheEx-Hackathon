![image](https://github.com/AuspicesAI/ScytheEx/assets/75253629/edfcdbb7-cdec-49b6-aacb-314bcc9faeda)

## Overview

ScytheEx is an advanced cybersecurity tool designed for real-time network traffic monitoring and threat analysis. Initially developed as a Linux service daemon and capable of deployment on Kubernetes bare metal, this versatile solution extends its functionality across various operating systems.

ScytheEx integrates AI-driven analytics to detect activities post-attack, adhering to the philosophy that despite advanced protective measures like EDR or AV, malware may still execute on the system. The tool operates at this post-execution level to identify malicious activities and generate YARA rules, providing continuous feeds to enhance other detection tools and technologies.

> [!Warning]
> ScytheEx project is still in an early stage which means that any feature changes are very welcome.

### Main Features

- AI-powered network traffic analysis.
- Real-time threat detection and mitigation.
- Background process management for continuous monitoring.
- Integrated threat intelligence.
- Robust mitigation strategies including IP blacklisting.
- Customizable configuration to fit your business need.
- HTTP Server for visualization.
- Support kubernetes deployments.
- 3rd Party APIs usage (e.g: virus total, hybrid-analysis)

## Setup Instructions

![Kubernetes](https://github.com/AuspicesAI/ScytheEx/assets/75253629/11bdfe89-175d-4e1c-87df-2ec29fe5a32e)

### Kubernetes Deployment using Helm

> [!Important]
> by default **ScytheEx** runs as a daemonset on kubernetes and is not fully tested which may break, kubernetes admins can customize the deployment as needed.

1. **Prepare Your Environment**:

   - Ensure Kubernetes cluster is set up and `kubectl` is configured.
   - Install Helm on your system.

2. **Deploy ScytheEx**:
   - Clone the repository and navigate to the Helm chart directory.
   - Modify the values in `values.yaml` as necessary, particularly the network interfaces and Redis settings.
   - Run `helm install scytheex ./scytheex-chart` to deploy to your Kubernetes cluster.

![Debian](https://github.com/AuspicesAI/ScytheEx/assets/75253629/cddd869a-1080-45d9-8668-dc05b0d41ea6)

### Debian-Based Linux Host Setup

1. **Installation**:

   - Use the following command to install ScytheEx directly:
     ```bash
     curl -sSL https://raw.githubusercontent.com/AuspicesAI/ScytheEx/main/setup/debian_linux.sh | sudo bash
     ```
   - This script will clone the ScytheEx repository, install Python dependencies, set up the environment, and configure ScytheEx as a systemd service.

2. **Enable Service**:
   - Run `systemctl enable scytheex` to enable ScytheEx service to automatically start at boot time.

![Windows](https://github.com/AuspicesAI/ScytheEx/assets/75253629/e8cc8fba-903a-4f18-886b-4dab1ab8eeb7)

### Windows Host Setup

1. **Download and Install**:

   - Download the latest release from [ScytheEx Repository](https://github.com/AuspicesAI/ScytheEx/releases).
   - Ensure Python is installed on your system. If not, download and install it from [Python's official site](https://www.python.org/downloads/).
   - Open a command prompt as Administrator and navigate to the directory where ScytheEx is downloaded.
   - Install required Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configure and Run**:

   - Open the `config.toml` file located in your ScytheEx installation directory.
   - Manually adjust the network interface settings under the appropriate section to correspond with your system.
   - Run `setup_windows.bat` to configure and start ScytheEx as a service. Make sure to run the command prompt as Administrator:
     ```bash
     setup_windows.bat
     ```

   **Note**: Configuration of network settings and service setup may require specific permissions or adjustments depending on your system's security settings.

## Configuration (`config.toml`)

The configuration file `config.toml` found in `/config` directory is central to customizing and controlling the behavior of the ScytheEx system. Below are details about each configurable section and setting:

### `[ScytheEx]`

- `network_interface`: Specify the network interface on which ScytheEx will capture traffic (e.g., `"eth0"` for Linux, `"Ethernet"` for Windows).
- `use_threat_intel`: Enable to use real-time threat intelligence (uncomment and set to `true` to enable).
- `threat_intel_sources`: URLs of threat intelligence feeds (uncomment and list sources to enable).
- `log_directory`: The directory where logs will be stored.
- `traffic_logs_path`: File path for storing traffic logs.
- `error_logs_path`: File path for storing error logs.
- `visualization_server`: URL of the visualization server if used (uncomment and set URL to enable).
- `number_of_processes`: Number of worker processes for handling tasks.
- `remote_logging_enabled`: Enable to log remotely (uncomment and set to `true` to enable).
- `remote_logging_server`: URL of the remote logging server (uncomment and set URL to enable).
- `user_whitelist`: List of IP addresses that are allowed unrestricted access.
- `show_debug_messages`: Set to `true` to enable verbose logging for debugging purposes.

### `[redis_traffic]`

- `redis_traffic_host`: Hostname or IP address of the Redis server used for real-time data.
- `redis_traffic_port`: Port number for the Redis server handling real-time data.
- `redis_traffic_db_index`: Database index for the Redis server used for real-time data.
- SSL settings (commented out by default):
  - `ssl`: Enable SSL for secure connection (set to `true` to enable).
  - `ssl_cert_reqs`: SSL certificate requirements.
  - `ssl_ca_certs`: Path to the CA certificate.
  - `ssl_certfile`: Path to the SSL certificate.
  - `ssl_keyfile`: Path to the SSL key.

### `[redis_results]`

- `host`: Hostname or IP address of the Redis server used for storing AI analysis results.
- `port`: Port number for the Redis server handling AI results.
- `db_index`: Database index for the Redis server used for AI results.
- Similar SSL settings as `[redis_traffic]` (commented out by default).

### `[security]`

- `enable_encryption`: Enable encryption for sensitive data within the application (set to `true` to enable).
- `encryption_key_path`: Path to the encryption key file.

### `[performance]`

- `memory_optimization`: Enable to optimize memory usage (set to `true` to enable).
- `cpu_priority`: Set the CPU priority level (e.g., `"high"`, `"normal"`).

## System Workflow

Detailed steps from initial data capture through to AI analysis and front-end interaction:

1. **Data Capture**: Captures real-time network traffic and parses data using custom packet analysis techniques.
2. **Redis Integration**: Utilizes dual Redis setups for handling real-time data flow and AI analysis results efficiently.
3. **AI Analysis**: Periodically processes data to identify potential threats using advanced machine learning algorithms.
4. **Threat Response**: Implements automated responses based on analysis, such as updating firewall rules or isolating affected network segments.
5. **Front-end Monitoring**: Provides a real-time dashboard for monitoring network status and alerts.
6. **Continuous Updates**: Regularly updates AI models and system configurations to adapt to new threats and improve accuracy.

## Future Enhancements

- **Mitigation Strategies**: Automated system responses based on threat severity.
- **Threat Intelligence**: Integration with real-time threat intelligence feeds to enhance detection capabilities.
- **Kubernetes Response**: Future feature to cordon off and drain infected Kubernetes nodes, preventing the spread of malware and automatically redistributing workloads.

## License

This project is licensed under the Apache License 2.0. For more details, see the LICENSE file in the root directory of this project.

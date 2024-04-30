![image](https://github.com/AuspicesAI/ScytheEx/assets/75253629/edfcdbb7-cdec-49b6-aacb-314bcc9faeda)

## Main Features Checklist
 - [ ] AI Model for Network Analysis
 - [ ] UI
 - [x] Running as Background Process
 - [ ] Mitigation logic
 - [ ] IP Blacklist
 - [ ] Threat Intelligence [Optional]

## Overview

ScytheEx is an advanced cybersecurity tool designed for real-time network traffic monitoring and threat analysis. Initially developed as a Linux service daemon and capable of deployment on Kubernetes bare metal, this versatile solution extends its functionality across various operating systems. 

ScytheEx integrates AI-driven analytics to detect activities post-attack, adhering to the philosophy that despite advanced protective measures like EDR or AV, malware may still execute on the system. The tool operates at this post-execution level to identify malicious activities and generate YARA rules, providing continuous feeds to enhance other detection tools and technologies.

## Task Checklist

- [ ] Front-end Setup
- [x] Back-end Setup
- [ ] AI Model Development
- [x] AI Running File Implementation
- [x] Data Parsing from Network Packets
- [x] Demonstration of an Attack Scenario
- [x] Redis Database Setup
- [ ] Integrating Front-end with Redis Database
- [x] Integrating AI Model with Redis Database
- [x] Integrating Traffic Analysis with Redis Database
- [ ] Adding Mitigation Logic (Optional)
- [ ] Incorporating Threat Intelligence Fields (Optional)
- [ ] Documentation of All Components

## System Workflow

### 1. Front-end Initialization

- The React-based front-end is served to users, providing a dashboard for monitoring network traffic, alerts, and analytics.
- Users can interact with the UI to customize settings or initiate specific analyses.

### 2. Back-end and Traffic Monitoring

- The back-end, written in C++, captures real-time network traffic data from the operating system.
- This component parses the network packets to extract relevant data fields as specified (e.g., protocol, service, state).

### 3. Data Storage with Redis

- Extracted data from the back-end is pushed to a Redis database, which acts as a real-time data store.
- Redis is configured to handle high-throughput and low-latency operations to ensure timely analysis.

### 4. AI Model Analysis

- The Python-based AI model periodically retrieves network traffic data from Redis.
- The model analyzes the data, applying machine learning algorithms to detect anomalies or potential threats based on predefined rules and metrics.

### 5. Result Processing and Response

- Analysis results are pushed back to another Redis instance or the same with different data structuring, which might include threat levels, types of attacks detected, and other relevant metrics.
- Depending on the results, automated mitigation strategies may be triggered (if implemented).

### 6. Front-end Updates and User Interaction

- The front-end continuously polls or listens for updates from Redis to display the latest analysis and alerts.
- Users can view detailed reports, adjust system settings, or manually intervene in response to specific threats.

### 7. Ongoing Monitoring and Updates

- The system constantly monitors network traffic, with AI models adapting to new data and evolving threats.
- System updates and new threat intelligence can be rolled out to enhance detection and response capabilities.

### 8. Logging and Auditing

- All actions, from traffic logging to alert responses, are documented for auditing and improvement purposes.
- Logs are crucial for understanding past incidents and refining system performance and security measures.

## Optional Components

### Mitigation Logic

- If a threat is detected, automated or suggested mitigation responses can be activated to protect the system.

### Threat Intelligence Integration

- Real-time data can be enriched with external threat intelligence feeds to improve detection accuracy.

## License

This project is licensed under the Apache License 2.0. For more details, see the LICENSE file in the root directory of this project.

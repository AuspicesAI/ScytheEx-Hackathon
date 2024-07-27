-- Schema for Agents
CREATE TABLE IF NOT EXISTS agents (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active'
);

-- Schema for Events
CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    agent_id INTEGER REFERENCES agents(id) ON DELETE CASCADE,
    event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type VARCHAR(50),
    event_data TEXT
);

-- Schema for Alerts
CREATE TABLE IF NOT EXISTS alerts (
    id SERIAL PRIMARY KEY,
    event_id INTEGER REFERENCES events(id) ON DELETE CASCADE,
    alert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    alert_type VARCHAR(50),
    alert_message TEXT,
    resolved BOOLEAN DEFAULT FALSE
);

-- Schema for Configurations
CREATE TABLE IF NOT EXISTS configurations (
    id SERIAL PRIMARY KEY,
    key VARCHAR(255) UNIQUE NOT NULL,
    value TEXT NOT NULL
);

-- Sample Configuration Data
INSERT INTO configurations (key, value) VALUES ('server_port', '8080');
INSERT INTO configurations (key, value) VALUES ('log_level', 'info');
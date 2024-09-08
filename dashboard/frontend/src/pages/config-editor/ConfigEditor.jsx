import React, { useState } from "react";
import { CustomCheckbox, TextInput, Dropdown } from "./ConfigEditorComponents";

const defaultConfig = {
  ScytheEx: {
    network_interface: "eth0",
    use_threat_intel: false,
    threat_intel_sources: [],
    log_directory: "./scytheex",
    traffic_logs_path: "./scytheex/traffic.log",
    error_logs_path: "./scytheex/error.log",
    visualization_server: "",
    number_of_processes: 4,
    remote_logging_enabled: false,
    remote_logging_server: "",
    user_whitelist: ["192.168.1.10", "192.168.1.11"],
    show_debug_messages: false,
    blacklist_generation_rules: [],
  },
  redis_traffic: {
    redis_traffic_host: "0.tcp.eu.ngrok.io",
    redis_traffic_port: 16944,
    redis_traffic_db_index: 0,
    ssl: false,
    ssl_cert_reqs: "",
    ssl_ca_certs: "",
    ssl_certfile: "",
    ssl_keyfile: "",
  },
  redis_results: {
    host: "localhost",
    port: 6380,
    db_index: 0,
    ssl: false,
    ssl_cert_reqs: "",
    ssl_ca_certs: "",
    ssl_certfile: "",
    ssl_keyfile: "",
  },
  security: {
    enable_encryption: false,
    encryption_key_path: "",
  },
  performance: {
    memory_optimization: false,
    cpu_priority: "normal",
  },
};

const ConfigEditor = () => {
  const [config, setConfig] = useState(defaultConfig);

  const handleChange = (section, key, value) => {
    setConfig((prevConfig) => ({
      ...prevConfig,
      [section]: {
        ...prevConfig[section],
        [key]: value,
      },
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission
    console.log(config);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl text-center font-bold mb-4">
        ScytheEX Configuration
      </h1>
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* ScytheEx Section */}
        <section>
          <h2 className="text-2xl font-semibold mb-6">ScytheEx</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TextInput
              label="Network Interface"
              type="text"
              value={config.ScytheEx.network_interface}
              onChange={(e) =>
                handleChange("ScytheEx", "network_interface", e.target.value)
              }
            />
            <TextInput
              label="Log Directory"
              type="text"
              value={config.ScytheEx.log_directory}
              onChange={(e) =>
                handleChange("ScytheEx", "log_directory", e.target.value)
              }
            />
            <TextInput
              label="Traffic Logs Path"
              type="text"
              value={config.ScytheEx.traffic_logs_path}
              onChange={(e) =>
                handleChange("ScytheEx", "traffic_logs_path", e.target.value)
              }
            />
            <TextInput
              label="Error Logs Path"
              type="text"
              value={config.ScytheEx.error_logs_path}
              onChange={(e) =>
                handleChange("ScytheEx", "error_logs_path", e.target.value)
              }
            />
            <TextInput
              label="Number of Processes"
              type="number"
              value={config.ScytheEx.number_of_processes}
              onChange={(e) =>
                handleChange("ScytheEx", "number_of_processes", e.target.value)
              }
            />
            <TextInput
              label="User Whitelist"
              type="text"
              value={config.ScytheEx.user_whitelist.join(", ")}
              onChange={(e) =>
                handleChange(
                  "ScytheEx",
                  "user_whitelist",
                  e.target.value.split(", ").map((v) => v.trim())
                )
              }
            />
            <TextInput
              label="Blacklist Generation Rules"
              type="text"
              value={config.ScytheEx.blacklist_generation_rules.join(", ")}
              onChange={(e) =>
                handleChange(
                  "ScytheEx",
                  "blacklist_generation_rules",
                  e.target.value.split(", ").map((v) => v.trim())
                )
              }
            />
            <CustomCheckbox
              label="Use Threat Intel"
              checked={config.ScytheEx.use_threat_intel}
              onChange={(e) =>
                handleChange("ScytheEx", "use_threat_intel", e.target.checked)
              }
            />
          </div>
          <hr className="my-6 border-gray-300" />
        </section>

        {/* redis_traffic Section */}
        <section>
          <h2 className="text-xl font-semibold mb-6">Redis Traffic</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TextInput
              label="Host"
              type="text"
              value={config.redis_traffic.redis_traffic_host}
              onChange={(e) =>
                handleChange(
                  "redis_traffic",
                  "redis_traffic_host",
                  e.target.value
                )
              }
            />
            <TextInput
              label="Port"
              type="number"
              value={config.redis_traffic.redis_traffic_port}
              onChange={(e) =>
                handleChange(
                  "redis_traffic",
                  "redis_traffic_port",
                  e.target.value
                )
              }
            />
            <TextInput
              label="DB Index"
              type="number"
              value={config.redis_traffic.redis_traffic_db_index}
              onChange={(e) =>
                handleChange(
                  "redis_traffic",
                  "redis_traffic_db_index",
                  e.target.value
                )
              }
            />
          </div>
          <hr className="my-6 border-gray-300" />
        </section>

        {/* redis_results Section */}
        <section>
          <h2 className="text-xl font-semibold mb-6">Redis Results</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <TextInput
              label="Host"
              type="text"
              value={config.redis_results.host}
              onChange={(e) =>
                handleChange("redis_results", "host", e.target.value)
              }
            />
            <TextInput
              label="Port"
              type="number"
              value={config.redis_results.port}
              onChange={(e) =>
                handleChange("redis_results", "port", e.target.value)
              }
            />
            <TextInput
              label="DB Index"
              type="number"
              value={config.redis_results.db_index}
              onChange={(e) =>
                handleChange("redis_results", "db_index", e.target.value)
              }
            />
          </div>
          <hr className="my-6 border-gray-300" />
        </section>

        {/* security Section */}
        <section>
          <h2 className="text-xl font-semibold mb-6">Security</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <CustomCheckbox
              label="Enable Encryption"
              checked={config.security.enable_encryption}
              onChange={(e) =>
                handleChange("security", "enable_encryption", e.target.checked)
              }
            />
          </div>
          <hr className="my-6 border-gray-300" />
        </section>

        {/* performance Section */}
        <section>
          <h2 className="text-xl font-semibold mb-6">Performance</h2>
          <Dropdown
            label="CPU Priority"
            value={config.performance.cpu_priority}
            options={[
              { value: "low", label: "Low" },
              { value: "normal", label: "Normal" },
              { value: "high", label: "High" },
            ]}
            onChange={(e) =>
              handleChange("performance", "cpu_priority", e.target.value)
            }
          />
        </section>

        <button
          type="submit"
          className="bg-primary-pink text-white px-4 py-2 rounded hover:bg-gray-900"
        >
          Save Changes
        </button>
      </form>
    </div>
  );
};

export default ConfigEditor;

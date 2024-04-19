# Zenith Models Module Documentation

## Using the Module in Other Directories

```python
import importlib.util
import sys

# Define the package name and path to its __init__.py file
package_name = "zenith_models"
package_path = "zenith_models/__init__.py"  # Adjust this path as needed

# Create a module spec
spec = importlib.util.spec_from_file_location(package_name, package_path)
# Load the module from spec
zenith_models = importlib.util.module_from_spec(spec)
sys.modules[package_name] = zenith_models
spec.loader.exec_module(zenith_models)

# Example usage
model_instance = zenith_models.TestGenerationModel()
```

`After importing zenith_models like this, you can use its contents (e.g., classes or functions defined in code_analysis.py, test_generation.py, etc.) in your script`

`Make sure that the path ../zenith_models/__init__.py correctly points to the __init__.py file of the zenith_models package from the location of your script. If your script is deeper in the directory structure, you might need to adjust the relative path accordingly.`

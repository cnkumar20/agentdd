from copilotkit import Copilot

# Initialize a copilot
copilot = Copilot()

# Add your tools and configure the copilot
copilot.add_tool(my_custom_tool)

# Run the copilot
response = copilot.run("Your task description here")
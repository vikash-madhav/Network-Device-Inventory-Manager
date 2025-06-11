**🌐 Python Network Device Inventory Manager**
A robust command-line application built with Python to manage and track network device inventory. This tool is designed to help network engineers maintain an accurate record of their network assets, including hostnames, IP addresses, vendors, and OS versions, with data persistence and basic reporting capabilities.

**✨ Features**
This inventory manager provides a comprehensive set of functionalities for efficient device management:

**Add New Devices:**

Interactive prompts for Host Name, Vendor, OS Version, and IP Address.

Unique Hostname Validation: Ensures no two devices share the same hostname.

Robust IP Address Validation: Checks for correct IPv4 format (4 octets, dot-separated) and ensures each octet is within the 0-255 range.

Unique IP Address Validation: Prevents duplicate IP addresses in the inventory.

Non-Empty Field Checks: Guarantees that Host Name, Vendor, and OS Version are not left blank.

Confirmation Step: Prompts for user confirmation before adding a new device.

**Display All Devices:**

Lists all devices currently in the inventory with their full details.

Provides a clear "No devices" message if the inventory is empty.

**Display Specific Device:**

Offers flexible search options: by Host Name or IP Address.

Displays all recorded details for the matching device.

Provides feedback if the device is not found.

**Update Existing Device:**

Allows updating individual fields (Host Name, Vendor, OS Version, IP Address) for a selected device.

Re-applies all relevant validation rules (unique hostname, valid/unique IP, non-empty fields) during updates.

Confirmation Step: Prompts for user confirmation to save changes, with an option to discard modifications.

**Delete Devices:**

Enables removal of devices from the inventory by Host Name.

Includes a confirmation step to prevent accidental deletions.

**Data Persistence (JSON):**

Automatically saves the entire inventory to a network_devices.json file after every addition, update, or deletion.

Automatically loads the inventory from network_devices.json when the program starts, ensuring your data is retained across sessions.

Includes error handling for missing or corrupted JSON files.

**Basic Reports:**

Generates a summary of the inventory, including:

Total number of devices.

Count of devices grouped by Vendor.

Count of devices grouped by OS Version.

**User-Friendly CLI:**

Clear, interactive menu system for easy navigation.

Informative messages and error handling to guide the user.

**🚀 How to Run**
To get this project up and running on your local machine:

**Clone the repository:**

git clone https://github.com/vikash-madhav/network-device-inventory-manager.git


**Navigate to the project directory:**

cd network-device-inventory-manager

**Run the Python script:**

python network_inventory.py 


The program will start and present you with the main menu.

🛠️ Technologies Used
Python3

json (built-in Python module for JSON handling)

collections.Counter (from Python's standard library for efficient counting)


**💡 Future Enhancements**
**Here are some ideas for how this project could be expanded:**

**Network Automation Integration:** Integrate with libraries like Netmiko or Nornir to fetch device configurations or status directly from network devices.

**Advanced Reporting:** Add more sophisticated reporting features, such as filtering by specific criteria (e.g., devices older than a certain OS version, devices from a specific vendor).

**Web Interface:** Develop a simple web-based user interface using frameworks like Flask or Django for a more modern user experience.

**Export/Import:** Allow exporting the inventory to other formats like CSV or Excel, and importing data from them.

**Error Logging:** Implement a dedicated logging mechanism to record program events, errors, and user actions.

**Multi-User Support:** Introduce basic user authentication and authorization.

✍️ Author
Vikash Madhav Sridhar
LinkedIn: https://www.linkedin.com/in/vikash-madhav/
https://vikash-madhav.github.io/

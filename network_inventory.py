import json # helps us save and load data
from collections import Counter # good for counting things easily

# --- Global Stuff ---
# This list will hold all our network devices while the program is running.
network_devices = []
DATA_FILE = 'network_devices.json' # This is the file where our inventory data lives

# --- Data Saving/Loading Functions ---

def load_devices():
    """Loads device data from our JSON file."""
    global network_devices # gotta tell Python we're changing the global list
    try:
        with open(DATA_FILE, 'r') as f: # opening the file to read from it
            network_devices = json.load(f) # pulling the data out of the JSON file
        print(f"Loaded {len(network_devices)} devices from {DATA_FILE}.")
    except FileNotFoundError: # what if the file isn't there yet?
        print("No old inventory file found. Starting fresh!")
        network_devices = [] # make sure the list is empty if no file
    except json.JSONDecodeError: # what if the file is messed up JSON?
        print(f"Error reading {DATA_FILE}. It might be broken. Starting empty.")
        network_devices = [] # clear the list if the file is corrupted

def save_devices():
    """Saves the current device data to our JSON file."""
    try:
        with open(DATA_FILE, 'w') as f: # opening the file to write to it (overwrites existing!)
            json.dump(network_devices, f, indent=4) # putting our device list into the file, with nice spacing
        print(f"Saved {len(network_devices)} devices to {DATA_FILE}.")
    except Exception as e: # catching any other weird errors while saving
        print(f"Oops, something went wrong saving devices: {e}")

# --- Helper Function for IP Validation ---

def check_octet_validity(octet_number):
    """Checks if a number is a valid part of an IP address (0-255)."""
    if 0 <= octet_number <= 255: # checking the range
        return True
    else:
        return False

# --- IP Address Validation Function ---
def get_validated_ip_address(current_device=None):
    """
    Asks for an IP address and makes sure it's valid and not a duplicate.

    If we're updating a device, 'current_device' tells it to ignore that device's own IP.
    """
    while True: # keep asking until we get a good IP or the user cancels
        ip_address_string = input("Enter the IP address (e.g., 192.168.1.10) or 'cancel': ").strip()

        if ip_address_string.lower() == 'cancel':
            return 'cancel' # user wants out

        octets_list = ip_address_string.split('.') # break IP into its four parts
        is_ip_valid_format_and_range = True # start assuming it's good

        if len(octets_list) != 4: # needs exactly 4 parts
            print("Error: IP address needs exactly 4 parts separated by dots.")
            is_ip_valid_format_and_range = False
        else:
            for octet_string in octets_list:
                try:
                    octet_int = int(octet_string) # try turning text into a number
                    if not check_octet_validity(octet_int): # use our helper to check the number
                        print(f"Error: '{octet_string}' isn't between 0 and 255.")
                        is_ip_valid_format_and_range = False
                        break # stop checking if one part is bad
                except ValueError: # what if they typed "a" instead of a number?
                    print(f"Error: '{octet_string}' isn't a valid number.")
                    is_ip_valid_format_and_range = False
                    break # stop if it's not a number

        if not is_ip_valid_format_and_range: # if any checks failed
            print("Invalid IP address format or range. Try again.")
            continue # ask for IP again

        # Now, check if this IP is already used by another device
        is_duplicate = False
        for device_dict in network_devices:
            # this part makes sure we don't say a device's current IP is a duplicate of itself during an update
            if device_dict['ip_address'] == ip_address_string and \
               (current_device is None or device_dict is not current_device):
                print(f"Error: This IP address is already used by '{device_dict.get('hostname', 'N/A')}'.")
                is_duplicate = True
                break

        if is_duplicate:
            print("Please enter a different IP address.")
            continue # ask for IP again
        else:
            print("IP address looks good and is unique.")
            return ip_address_string # finally, return the good IP

# --- Add New Device Function ---
def add_new_device():
    print("\n--- Add New Device ---")

    # Get a unique hostname
    while True:
        host_name = input("Enter the Host Name (or 'cancel'): ").strip()
        if host_name.lower() == 'cancel':
            print("Device addition cancelled.")
            return
        if not host_name: # can't be empty
            print("Host Name cannot be empty. Try again.")
            continue
        is_duplicate_hostname = False
        for device_dict in network_devices:
            if device_dict['hostname'].lower() == host_name.lower(): # check existing hostnames
                print(f"Error: Host Name '{host_name}' already exists.")
                is_duplicate_hostname = True
                break
        if is_duplicate_hostname:
            print("Please enter a different Host Name.")
            continue
        else:
            print(f"Host Name '{host_name}' is unique.")
            break

    # Get a non-empty vendor
    while True:
        vendor = input("Enter the Vendor: ").strip()
        if not vendor:
            print("Vendor cannot be empty. Enter a value.")
            continue
        break

    # Get a non-empty OS version
    while True:
        os_version = input("Enter the Operating System Version: ").strip()
        if not os_version:
            print("OS Version cannot be empty. Enter a value.")
            continue
        break

    # Get a validated IP address using our special function
    ip_address_string = get_validated_ip_address()
    if ip_address_string == 'cancel': # if user cancelled IP input
        print("Device addition cancelled.")
        return

    # Put all device details into a dictionary
    device_details = {
        "hostname": host_name,
        "vendor": vendor,
        "os_version": os_version,
        "ip_address": ip_address_string
    }

    # --- Confirmation before adding ---
    print(f"\n--- Confirm New Device Details ---")
    print(f"Host Name: {device_details['hostname']}")
    print(f"Vendor: {device_details['vendor']}")
    print(f"OS Version: {device_details['os_version']}")
    print(f"IP Address: {device_details['ip_address']}")
    confirm = input("Add this device to the inventory? (yes/no): ").strip().lower()

    if confirm == 'yes': # if user says yes, add it
        network_devices.append(device_details)
        print(f"\nDevice '{host_name}' (IP: {ip_address_string}) added successfully!")
    else: # if user says no
        print("Device addition cancelled by user.")

# --- Display All Devices Function ---
def display_all_devices():
    """Shows all devices currently in the inventory."""
    if not network_devices: # check if the list is empty
        print("\nNo devices in the inventory yet.\n")
    else:
        print("\n-------------------------------------------------")
        print(f"\nHere are all the devices in the inventory: \n")
        for i, device_dict in enumerate(network_devices): # loop through devices to print them
            print(f"--- Device {i+1} ---") # adding a number for each device
            print(f"Host Name: {device_dict['hostname']}")
            print(f"Vendor: {device_dict['vendor']}")
            print(f"OS Version: {device_dict['os_version']}")
            print(f"IP Address: {device_dict['ip_address']}")
            print("----------------------------")

# --- Display Specific Device Function ---
def display_specific_device():
    """Lets you search for and display one device by hostname or IP."""
    print("\n--- Display Specific Device ---")
    if not network_devices: # can't search if nothing's there
        print("The inventory is empty. No devices to search for.")
        return

    while True: # loop until user finds a device or cancels
        print("\nHow do you want to find the device?")
        print("1. By Host Name")
        print("2. By IP Address")
        print("3. Back to Main Menu")
        search_choice = input("Enter your choice (1/2/3): ").strip()

        if search_choice == '3': # user wants to go back
            print("Going back to main menu.")
            return

        search_by_hostname = False
        search_by_ip = False

        if search_choice == '1':
            search_by_hostname = True
        elif search_choice == '2':
            search_by_ip = True
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            continue # ask for search type again

        search_term = ""
        if search_by_hostname:
            search_term = input("Enter the Host Name to find (or 'cancel'): ").strip()
        elif search_by_ip:
            search_term = input("Enter the IP Address to find (e.g., 192.168.1.10) (or 'cancel'): ").strip()

        if search_term.lower() == 'cancel': # user wants to cancel search
            print("Search cancelled. Going back to main menu.")
            return

        found_device = None
        for device_dict in network_devices: # loop through all devices to find a match
            if search_by_hostname:
                if device_dict['hostname'].lower() == search_term.lower(): # case-insensitive hostname search
                    found_device = device_dict
                    break
            elif search_by_ip:
                if device_dict['ip_address'] == search_term: # IP needs exact match
                    found_device = device_dict
                    break

        if found_device: # if we found it
            print(f"\n--- Details for Device: {found_device['hostname']} ---")
            print(f"  Vendor: {found_device['vendor']}")
            print(f"  OS Version: {found_device['os_version']}")
            print(f"  IP Address: {found_device['ip_address']}")
            print("-------------------------------------------")
            break # exit the search loop
        else: # if not found
            if search_by_hostname:
                print(f"Device with Host Name '{search_term}' not found. Try again.")
            elif search_by_ip:
                print(f"Device with IP Address '{search_term}' not found. Try again.")
            # loop continues to ask for another search term

# --- Update Existing Device Function ---
def update_device():
    """Allows you to change details of an existing device."""
    print("\n--- Update Existing Device ---")
    returned_changes_saved = False # this tells the main program if we actually saved anything

    while True: # loop to find the device first
        device_update_hostname = input("\nEnter the Host Name of the device to update (or 'cancel'): ").strip()

        if device_update_hostname.lower() == 'cancel':
            print("\nGoing back to main menu.")
            return False # no changes made

        found_device = None # reset for each search attempt
        for device_dict in network_devices: # loop to find the device by hostname
            if device_dict['hostname'].lower() == device_update_hostname.lower():
                found_device = device_dict
                break

        if found_device: # if we found the device
            print(f"Device found: {found_device['hostname']}")
            print("Current details:")
            print(f"  Vendor: {found_device['vendor']}")
            print(f"  OS Version: {found_device['os_version']}")
            print(f"  IP Address: {found_device['ip_address']}")
            print("----------------------------")

            changes_made_in_session = False # track if anything was changed in this session

            while True: # sub-menu to choose what to update
                print("\nWhat do you want to change?")
                print("1. Host Name")
                print("2. Vendor")
                print("3. OS Version")
                print("4. IP Address")
                print("5. Save Changes and Go Back")
                print("6. Discard Changes and Go Back")
                device_detail_choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

                if device_detail_choice == "1":
                    while True: # loop for new hostname input
                        new_host_name = input(f"Enter the new Host Name (current: {found_device['hostname']}): ").strip()
                        if not new_host_name:
                            print("Host Name can't be empty. Try again.")
                            continue
                        is_duplicate_hostname = False
                        for device_dict in network_devices:
                            # make sure the new hostname isn't used by another device
                            if device_dict['hostname'].lower() == new_host_name.lower() and device_dict is not found_device:
                                print(f"Error: Host Name '{new_host_name}' already exists.")
                                is_duplicate_hostname = True
                                break
                        if is_duplicate_hostname:
                            print("Please enter a different Host Name.")
                            continue
                        else:
                            if found_device['hostname'].lower() != new_host_name.lower(): # check if it's actually different
                                found_device['hostname'] = new_host_name
                                print(f"Host Name updated to: {new_host_name}")
                                changes_made_in_session = True # remember we made a change
                            else:
                                print("Host Name is the same. No change needed.")
                            break

                elif device_detail_choice == "2":
                    while True: # loop for new vendor input
                        new_vendor = input(f"Enter the new Vendor (current: {found_device['vendor']}): ").strip()
                        if not new_vendor:
                            print("Vendor can't be empty. Enter a value.")
                            continue
                        if found_device['vendor'].lower() != new_vendor.lower(): # check if actually different
                            found_device['vendor'] = new_vendor
                            print(f"Vendor updated to: {new_vendor}")
                            changes_made_in_session = True
                        else:
                            print("Vendor is the same. No change needed.")
                        break

                elif device_detail_choice == "3":
                    while True: # loop for new OS version input
                        new_os_version = input(f"Enter the new OS Version (current: {found_device['os_version']}): ").strip()
                        if not new_os_version:
                            print("OS Version can't be empty. Enter a value.")
                            continue
                        if found_device['os_version'].lower() != new_os_version.lower(): # check if actually different
                            found_device['os_version'] = new_os_version
                            print(f"OS Version updated to: {new_os_version}")
                            changes_made_in_session = True
                        else:
                            print("OS Version is the same. No change needed.")
                        break

                elif device_detail_choice == "4":
                    old_ip = found_device['ip_address']
                    print(f"Current IP Address: {old_ip}")
                    new_ip_address = get_validated_ip_address(current_device=found_device) # use our IP validation function

                    if new_ip_address == 'cancel':
                        print("IP update cancelled.")
                        continue # stay in this update sub-menu
                    
                    if found_device['ip_address'] != new_ip_address: # check if IP actually changed
                        found_device['ip_address'] = new_ip_address
                        print(f"IP Address updated to: {new_ip_address}")
                        changes_made_in_session = True
                    else:
                        print("IP Address is the same. No change needed.")
                    
                elif device_detail_choice == "5": # Save Changes and Go Back
                    if changes_made_in_session: # if we actually changed anything
                        print("\n--- Confirm Changes ---")
                        print("Updated details for this device:")
                        print(f"  Host Name: {found_device['hostname']}")
                        print(f"  Vendor: {found_device['vendor']}")
                        print(f"  OS Version: {found_device['os_version']}")
                        print(f"  IP Address: {found_device['ip_address']}")
                        confirm_save = input("Are you sure you want to save these changes? (yes/no): ").strip().lower()
                        if confirm_save == 'yes':
                            print(f"Changes for {found_device['hostname']} confirmed and will be saved.")
                            returned_changes_saved = True # tell the main program to save
                        else:
                            print("Changes NOT saved by user. Going back to main menu.")
                        break # exit this sub-menu
                    else: # if no changes were made
                        print("No changes were made. Going back to main menu.")
                        break # exit this sub-menu

                elif device_detail_choice == "6": # Discard Changes and Go Back
                    print("All changes discarded. Going back to main menu.")
                    # changes in memory are ignored because returned_changes_saved is still False
                    break # exit this sub-menu

                else:
                    print("Invalid choice. Enter a valid option (1/2/3/4/5/6).")
            
            break # exit the loop for finding the device, since we're done updating it

        else: # if the device wasn't found by hostname
            print(f"Device '{device_update_hostname}' not found. Try again.")

    print("--- Update Finished ---")
    return returned_changes_saved # tell main program whether to save or not

# --- Delete Device Function ---
def delete_device():
    print("\n--- Delete Existing Device ---")

    while True: # loop to keep asking until a device is deleted or user cancels
        hostname_to_delete = input("Enter the Host Name of the device to delete (or 'cancel'): ").strip()

        if hostname_to_delete.lower() == 'cancel':
            print("Deletion cancelled. Going back to main menu.")
            return # exit the function

        device_found = False # flag to track if we found it
        index_to_delete = -1 # where the device is in our list

        for index, device_dict in enumerate(network_devices): # loop to find the device
            if device_dict['hostname'].lower() == hostname_to_delete.lower():
                device_found = True
                index_to_delete = index # save its position
                break # found it, stop looping

        if device_found: # if we found the device
            found_device = network_devices[index_to_delete] # get the actual device dictionary
            print(f"\n--- Found Device: {found_device['hostname']} ---")
            print("Current details:")
            print(f"  Vendor: {found_device['vendor']}")
            print(f"  OS Version: {found_device['os_version']}")
            print(f"  IP Address: {found_device['ip_address']}")
            print("----------------------------")

            confirmation = input(f"Really delete '{found_device['hostname']}' (IP: {found_device['ip_address']})? (yes/no): ").strip().lower()

            if confirmation == 'yes': # if user says yes
                del network_devices[index_to_delete] # remove it from the list
                print(f"Device '{found_device['hostname']}' successfully deleted.")
                break # exit the main delete loop
            else: # if user says no
                print("Deletion cancelled by user.")
                break # exit the main delete loop
        else: # if device not found
            print(f"Device with Host Name '{hostname_to_delete}' not found. Try again.")

    print("--- Delete Finished ---")

# --- Generate Reports Function ---
def generate_reports():
    """Generates simple statistics about the inventory."""
    print("\n--- Network Device Inventory Reports ---")

    if not network_devices: # if no devices
        print("Inventory is empty. No reports to make.")
        return

    # 1. Total devices
    total_devices = len(network_devices)
    print(f"\nTotal number of devices: {total_devices}")

    # 2. Devices grouped by Vendor
    print("\n--- Devices by Vendor ---")
    vendors = [device['vendor'] for device in network_devices] # get all vendor names
    vendor_counts = Counter(vendors) # count how many of each vendor
    if vendor_counts:
        for vendor, count in vendor_counts.most_common(): # print them from most to least common
            print(f"- {vendor}: {count} device(s)")
    else:
        print("No vendor data.")


    # 3. Devices grouped by OS Version
    print("\n--- Devices by OS Version ---")
    os_versions = [device['os_version'] for device in network_devices] # get all OS versions
    os_version_counts = Counter(os_versions) # count how many of each OS
    if os_version_counts:
        for os_version, count in os_version_counts.most_common(): # print them from most to least common
            print(f"- {os_version}: {count} device(s)")
    else:
        print("No OS version data.")

    print("\n--- End of Reports ---")

# --- Main Program Logic ---
def main_program():
    """The main loop for our inventory management application."""
    load_devices() # load any saved devices when the program starts

    while True: # keep showing the menu until user quits
        print("\nWelcome, what would you like to do today?\n")
        print("------------------------------------------------------------------------------------")
        print("1. Add New Device")
        print("2. Display All Devices")
        print("3. Display Specific Device")
        print("4. Update Device")
        print("5. Delete Device")
        print("6. Generate Reports")
        print("7. Exit")
        choice = input("\nEnter your choice (1/2/3/4/5/6/7): ").strip() # get user's choice

        if choice == "1":
            print("\nAdding a new device...\n")
            add_new_device() # call the add function
            save_devices() # save after adding (or cancelling add)
        elif choice == "2":
            print("\nDisplaying all devices...\n")
            display_all_devices() # call the display all function
        elif choice == "3":
            print("\nDisplaying a specific device...\n")
            display_specific_device() # call the display specific function
        elif choice == "4":
            print("\nUpdating a device...\n")
            if update_device(): # call update, if it returns True (changes saved)
                save_devices() # then save the changes
        elif choice == "5":
            print("\nDeleting a device...\n")
            delete_device() # call the delete function
            save_devices() # save after deleting (or cancelling delete)
        elif choice == "6":
            print("\nGenerating reports...\n")
            generate_reports() # call the reports function
        elif choice == "7":
            print("\nExiting the program. Goodbye!\n")
            save_devices() # save one last time before closing
            break # exit the main loop
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

# --- Start the program when the script runs ---
if __name__ == "__main__":
    main_program()

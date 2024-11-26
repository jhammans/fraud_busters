import csv


def write_to_csv(data, filename, mode="w"):
    """Function to write data to a CSV file"""
    # Validate mode
    if mode not in ["w", "a"]:
        raise ValueError("Mode must be 'w' for write or 'a' for append.")

    if not data:
        print("No data to write")
        return

    # Assuming the data is a list of dictionaries
    with open(filename, mode=mode, newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        if mode == "w":
            writer.writeheader()  # Write the header only in write mode
        writer.writerows(data)
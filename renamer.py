import os

# Define the directory containing the files
directory = "assets/bottom"

# Iterate over files in the directory
for filename in os.listdir(directory):
    if filename.startswith("Layer"):
        fileraw, file_extension = os.path.splitext(filename)
        # Extract the number part from the filename
        try:
            layer_number = int(fileraw.split("Layer")[1])
            if layer_number >= 0:
                # Construct the new filename
                new_filename = f"Layer {layer_number+77}.png"
                # Rename the file
                os.rename(
                    os.path.join(directory, filename),
                    os.path.join(directory, new_filename),
                )
                print(f"Renamed {filename} to {new_filename}")
                # os.remove(os.path.join(directory, filename))
        except ValueError:
            # Skip files that don't have a valid number after 'Layer'
            continue

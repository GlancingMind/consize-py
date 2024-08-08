import subprocess
import tempfile
import os

def open_editor_with_content(initial_content):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
        # Write the initial content to the temporary file
        temp_file.write(initial_content.encode('utf-8'))
        temp_file.close()  # Close the file to ensure it's saved

        # Open the text editor (you can change 'nano' to your preferred editor)
        editor = os.environ.get('EDITOR', 'nano')  # Default to 'nano' if EDITOR is not set
        subprocess.run([editor, temp_file.name])

        # Read the content of the file after the editor is closed
        with open(temp_file.name, 'r', encoding='utf-8') as f:
            final_content = f.read()

    # Clean up the temporary file
    os.remove(temp_file.name)

    return final_content

# Example usage
if __name__ == "__main__":
    initial_content = "Edit this text and save the file.\n"
    result = open_editor_with_content(initial_content)
    print("Final content after editing:")
    print(result)

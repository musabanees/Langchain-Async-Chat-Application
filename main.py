import os
import chatapplication

def main():

    base = "backend/chatapplication"

    directories = [
        "api",
        "agent",
        "streaming"
    ]

    files = {
        "__init__.py": "",
        "api/routes.py": "",
        "api/__init__.py": "",
        "agent/__init__.py": "",
        "agent/executor.py": "",
        "agent/tools.py": "",
        "agent/prompts.py": "",
        "streaming/__init__.py": "",
        "streaming/token_generator.py": ""
    }

    # Create base directories
    os.makedirs(base, exist_ok=True)

    # Create subdirectories
    for d in directories:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # Create files
    for filepath, content in files.items():
        full_path = os.path.join(base, filepath)
        with open(full_path, "w") as f:
            f.write(content)

    print("Project structure created successfully!")



if __name__ == "__main__":
    # main()
    print(chatapplication.__name__)

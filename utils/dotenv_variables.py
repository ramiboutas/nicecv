import os

import dotenv  # pip install python-dotenv


def change_env_variable(key, value):
    # change a virtual environment variable
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    os.environ[key] = value

    # Write changes to .env file.
    dotenv.set_key(dotenv_file, key, os.environ[key])

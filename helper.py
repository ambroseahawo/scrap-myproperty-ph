import os

LOGS_FOLDER_NAME = "logs"


def setup_project_folders():
    # fmt: off
    try:os.mkdir(str(LOGS_FOLDER_NAME))
    except:pass

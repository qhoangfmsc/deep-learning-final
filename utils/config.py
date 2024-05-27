from pydantic import BaseSettings


class ProjectConfig(BaseSettings):
    # Size frame
    WIDTH: int = 1280
    HEIGHT: int = 720
    SIZE: tuple = (1280, 720)

    # Some basic color
    BLUE: tuple = (0, 0, 255)
    GREEN: tuple = (0, 255, 0)
    RED: tuple = (255, 0, 0)
    WHITE: tuple = (230, 230, 230)

    MAIN_ICON_PATH: str = r".\public\x-ray.ico"
    INFO_ICON_PATH: str = r".\public\info.ico"
    INFO_PDF_PATH: str = r".\public\info.pdf"

    SIZE_MAIN: str = r"1280x720"

    MODEL_PATH1: str = r"model\best_model_CNN.h5"
    MODEL_PATH2: str = r"model\best_model_CNN_LSTM.h5"
    MODEL_PATH3: str = r"model\best_model_CNN_RNN.h5"


project_config = ProjectConfig()

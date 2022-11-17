from dataclasses import dataclass
from pathlib import Path


@dataclass
class Project:
    """
    This class represents our project.
    It stores useful information about the structure
    """

    module_dir: Path = Path(__file__).parent
    project_dir: Path = Path(__file__).parents[1]

    config_dir = module_dir / "config"
    main_config_file = config_dir / "config.yml"

    data_dir = project_dir / "data"
    log_dir = project_dir / "log"

    export_dir = project_dir / "exports"

    def __post_init__(self) -> None:

        # create the directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.log_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)
        self.export_dir.mkdir(exist_ok=True)


if __name__ == "__main__":
    project = Project()

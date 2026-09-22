from pathlib import Path
from peppi_py import read_slippi


def load_replay(path, skip_frames=True):
    replay_path = Path(path)

    if not replay_path.exists():
        raise FileNotFoundError(
            f"Replay file does not exist: {replay_path}"
        )

    if replay_path.suffix.lower() != ".slp":
        raise ValueError(
            "The selected file must be a Slippi .slp replay."
        )

    return read_slippi(
        str(replay_path),
        skip_frames=skip_frames
    )
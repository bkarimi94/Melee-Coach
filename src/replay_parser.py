from pathlib import Path

from peppi_py import read_slippi


def load_replay(path, skip_frames=True):
    """
    Load a Slippi replay file.

    Parameters
    ----------
    path:
        Path to the .slp replay file.

    skip_frames:
        If True, only basic replay information is loaded.
        If False, full frame-by-frame gameplay data is loaded.

    Returns
    -------
    A peppi-py Game object.
    """

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
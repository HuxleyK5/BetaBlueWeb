"""Stable launcher with release-friendly crash reporting."""

import logging
import traceback

from game.main import main
from game.config import USER_DATA_ROOT


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:
        report = traceback.format_exc()
        USER_DATA_ROOT.mkdir(parents=True, exist_ok=True)
        crash_path = USER_DATA_ROOT / "crash.log"
        logging.basicConfig(filename=crash_path, level=logging.ERROR)
        logging.error("Uncaught Pokemon Beta Blue error\n%s", report)
        print(report)
        print(f"A crash report was written to {crash_path}.")
        raise SystemExit(1)

"""Save recognition events to CSV using only the Python standard library."""

import csv
from datetime import datetime
import logging
from pathlib import Path
import time


class EventLogger:
    def __init__(self, csv_path=None, cooldown_seconds=10):
        if cooldown_seconds < 0:
            raise ValueError("cooldown_seconds must be zero or greater")
        self.csv_path = (Path(csv_path) if csv_path is not None
                         else Path(__file__).with_name("detection_events.csv"))
        self.cooldown_seconds = cooldown_seconds
        self.last_logged = {}

    def log_event(self, person_name, confidence_score, camera_name):
        """Return True if saved, or False during cooldown or on a file error.

        Cooldowns are per name and camera, and reset when the program restarts.
        All Unknown detections on a camera share one cooldown.
        """
        key = (person_name, camera_name)
        now = time.monotonic()
        previous = self.last_logged.get(key)
        if previous is not None and now - previous < self.cooldown_seconds:
            return False

        detected_at = datetime.now().astimezone()
        status = "Unknown" if person_name == "Unknown" else "Authorized"
        try:
            # a+ preserves existing records and also creates a missing file.
            with self.csv_path.open("a+", newline="", encoding="utf-8") as file:
                file.seek(0, 2)
                writer = csv.writer(file)
                if file.tell() == 0:
                    writer.writerow([
                        "person_name", "detection_date", "detection_time",
                        "recognition_status", "confidence_score", "camera_name",
                    ])
                writer.writerow([
                    person_name, detected_at.strftime("%Y-%m-%d"),
                    detected_at.strftime("%H:%M:%S%z"), status,
                    confidence_score, camera_name,
                ])
        except (OSError, csv.Error) as error:
            logging.error("Could not save detection event to %s: %s",
                          self.csv_path, error)
            return False

        # Failed writes must not start a cooldown, so they can be retried.
        self.last_logged[key] = now
        return True

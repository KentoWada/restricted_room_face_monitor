# Restricted Room Face Monitor

Restricted Room Face Monitor is a face recognition system for rooms that only a small, named group of people should ever enter, such as a server room, a storeroom or a vault. It watches a camera, recognizes a small group of enrolled people by name, and marks everyone else as Unknown. At the moment it works on a laptop webcam. Later the camera source will be swapped for an external IP camera.

## Current status

Phase 1 of the methodology is working. The program reads frames from a camera, detects faces, compares each face against the enrolled people, and draws a green box with a name for a match or a red box labelled Unknown otherwise. The score shown next to each name is the cosine similarity between the live face and the closest enrolled photo.

Not done yet: the audio alert is being written separately in `alerts.py` and is not connected to `main.py`. RTSP camera streams, ONVIF discovery, the event log, the web dashboard and night mode are later phases.

## Setup

You need Python 3 and a webcam. The project was developed on Python 3.14 on Linux. Create a virtual environment inside the project folder and install the dependencies:

```
python -m venv env
source env/bin/activate
pip install opencv-python insightface onnxruntime numpy
```

On the fish shell, use `source env/bin/activate.fish` for the activation line. On Windows, use `env\Scripts\activate`.

The first time the program runs, InsightFace downloads its model files (a few hundred MB), so the first start is slow and needs internet. After that it works offline. You may see a `FutureWarning` about `estimate` being deprecated. It comes from inside InsightFace and can be ignored.

## How to use it

### 1. Enroll people

Each authorized person gets a folder inside `images/`, named after them. The folder name becomes the label shown on screen. Run the capture script:

```
python pic_taker.py
```

It asks for the person's name and how many pictures to take. Click the video window, then press S to take a picture and Q to quit. Take several pictures per person with different head angles and lighting, because the system compares a live face against every stored photo and keeps the best score. Only one face should be in view when you press S. Running the script again for the same name adds more photos and never overwrites the old ones.

The result looks like this:

```
images/
    John/
        0.jpg
        1.jpg
    Peter/
        0.jpg
```

You can also copy photos into a person's folder by hand. Any `.jpg`, `.jpeg` or `.png` file is used, as long as it contains exactly one face. Photos with no face or several faces are skipped, and a message says which file was skipped.

To check that enrollment works on its own, run:

```
python enroller.py
```

It prints each person's name and how many usable photos were found.

### 2. Run the recognizer

```
python main.py
```

A window opens showing the camera. Enrolled people get a green box and their name. Anyone else gets a red box labelled Unknown. Press Q in the video window to quit. If `images/` contains no usable photos, the program stops and says so.

## How it works

`grab_frame.py` provides a generator called `frames` that yields camera frames one at a time and reconnects automatically if a stream drops. `detector.py` loads the InsightFace model and finds faces in a frame. Each detected face comes with an embedding, a list of 512 numbers that describes the face. `enroller.py` reads every photo in `images/<name>/`, turns each into an embedding, and returns a dictionary that maps each name to a list of embeddings. `recognize.py` compares a live embedding against every stored one using a dot product, which for these normalized vectors equals the cosine of the angle between them. A score near 1 means the same person and a score near 0 means unrelated faces. If the best score is below `THRESHOLD`, the face is labelled Unknown. `main.py` ties everything together and draws the result. `pic_taker.py` is the helper for capturing enrollment photos. `alerts.py` plays the audio alert and is still being finished.

To save processing time, the detector runs on every third frame (`PROCESS_EVERY` in `main.py`) and the boxes from the last run are reused in between.

## Settings you may want to change

The camera is chosen by `SOURCE` at the top of `main.py`. The value 0 means the first webcam. Later it will be an RTSP address such as `"rtsp://user:password@192.168.1.50:554/stream1"`, and it can also be the path of a video file for testing.

The strictness of recognition is `THRESHOLD` in `recognize.py`, currently 0.45. This value is provisional. Raising it makes the system stricter, so an authorized person is more likely to be flagged as Unknown, and lowering it makes it easier for a stranger to be accepted. For a vault door the safer failure is the first one. The final value will be chosen in Phase 6 by measuring real scores across many photos.

## Privacy

Enrolled photos are face data. They stay on the local machine and nothing is sent to any cloud service. The `images/` folder should not be committed to the repository or shared outside the team. Add `images/`, `env/`, `__pycache__/` and `sounds/` to `.gitignore`.

## Known limitations

The system does not defend against spoofing, so a photo or video of an enrolled person held up to the camera could be accepted. This is a stated non-goal in the concept paper and is left as future work. Recognition also depends on lighting and angle, and a covered or turned away face is simply not detected.

## Roadmap

Following the methodology in the concept paper: Phase 2 replaces the webcam with an RTSP IP camera stream and tests recovery from a dropped connection. Phase 3 adds ONVIF camera discovery and a camera registry. Phase 4 adds the timestamped event log with snapshots and real-time notifications for unknown faces. Phase 5 adds the manually armed night mode. Phase 6 measures accuracy and false positive and false negative rates and documents limitations.


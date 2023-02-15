# Rocket League Score Timestamps

## Description
 
Extract timestamps from a video of rocket league gameplay whenever the user's team scores a goal, then output them into a text file. Also works for twitch vods.

## Limitations

This application currently only successfully proccesses **1280x720 60fps mp4** videos. Any other resolution, fps, or file type will not work.

Only works for up to 9 goals per game. Timestamps will not be given for the user's 10th goal and beyond.

The application and effectiveness of the model may also be limited by the user's UI scale in the Rocket League settings. I'm not completely sure of this though.

## **Usage**

1. Clone the repository.

```shell
git clone https://github.com/ColeBallard/RL-score-timestamps
```

2. Install the latest version of python. [Downloads.](https://www.python.org/downloads/)

3. Run the 'install.bat' file. **You only have to do this once.**

4. Run the 'run.bat' file.

5. Select your mp4 files.

## Contribution

If you have an idea or want to report a bug, please create an issue.

## **[Contact](https://coleb.io/contact)**

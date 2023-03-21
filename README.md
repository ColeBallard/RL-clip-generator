# Rocket League Clip Generator

## Description
 
Extract timestamps from a video of rocket league gameplay whenever the user's team scores a goal, then generates a clip based off the timestamp. Also works for twitch vods.

## Limitations

This application currently only successfully proccesses **60fps mp4** videos in 3 resolutions: 
- 1920 x 1080
- 1920 x 810
- 1280 x 720

Any other resolution, fps, or file type **WILL NOT WORK**.

Only works for up to 9 goals per game. Clips may not be generated for the user's 10th goal and beyond.

The application and effectiveness of the model is also limited by the user's UI scale in their Rocket League settings. I'm currently working on an option where the user can select the gameplay/vods corresponding UI scale.

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

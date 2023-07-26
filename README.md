# Publication

[1] "An Empirical Study of Functional Bugs in Android Apps" by Yiheng Xiong, Mengqian Xu, Ting Su, Jingling Sun, Jue Wang, He Wen, Geguang Pu, Jifeng He and Zhendong Su. In Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis (ISSTA 2023).
```
@inproceedings{functionalbugs2023,
  title={An Empirical Study of Functional Bugs in Android Apps},
  author={Xiong, Yiheng and Xu, Mengqian and Su, Ting and Sun, Jingling and Wang, Jue and Wen, He and Pu, Geguang and He, Jifeng and Su, Zhendong},
  booktitle={Proceedings of the 32nd ACM SIGSOFT International Symposium on Software Testing and Analysis},
  pages={1319--1331},
  year={2023},
  doi = {10.1145/3597926.3598138},
  series = {ISSTA 2023}
}
```

*You can find more about our work on testing/analyzing Android apps at this [website](https://tingsu.github.io/files/mobile-app-analysis.html)*.

# Replication Package
This repository contains all the artifacts (including the dataset and the tool Regdroid) in our study.

## Directory Structure

    home
        |
        | --- Dataset:                      The bug list of 399 bug reports
        | --- RegDroid:                     The source code of RegDroid
             |
             | --- start.py:                The entry of RegDroid, which accepts the parameters
             | --- regdroid.py              The main module of RegDroid
             | --- executor.py              The execution module of RegDroid
## Dataset

view the bug list in [Dataset](Dataset)
or Download all the data from [this link](https://1drv.ms/u/s!AqF-Z1v5QCuxgir6NaCpCtUC7ouX?e=PD1jVs)


## RegDroid

### Getting Started

#### Download

```
git clone https://github.com/Android-Functional-bugs-study/home.git
```

#### Requirements

- Android SDK: API26+
- python 3.8
- We use some libraries (e.g., uiautomator2, androguard, cv2) provided by python, you can add them as prompted, for example:

```
pips install uiautomator2
```

#### Setting up

You can create an emulator before running RegDroid. See [this link](https://stackoverflow.com/questions/43275238/how-to-set-system-images-path-when-creating-an-android-avd) for how to create avd using [avdmanager](https://developer.android.com/studio/command-line/avdmanager).
The following sample command will help you create an emulator, which will help you to start using RegDroid quickly：

```
sdkmanager "system-images;android-26;google_apis;x86"
avdmanager create avd --force --name Android8.0 --package 'system-images;android-26;google_apis;x86' --abi google_apis/x86 --sdcard 512M --device "pixel_xl"
```

Next, you can start two identical emulators and assign their port numbers with the following commands:

```
emulator -avd Android8.0 -read-only -port 5554
emulator -avd Android8.0 -read-only -port 5556
```

#### Run

If you have downloaded our project and configured the environment, you only need to enter ``download_path/tool/RegDroid`` to execute our sample app with the following command:

```
python3 start.py -app_path ./App/AmazeFileManager-3.7.1.apk -emulator_path  path_to_emulator -app_path ./App/AmazeFileManager-3.7.2.apk  -append_device emulator-5554 -append_device emulator-5556 -output  3.7.1-3.7.2  -testcase_count 1 -event_num 20
```

Here,

``-app_path``: the file path of APK

``-emulator_path ``: the path to the emulator

``-append_device``: the serial number of devices used in the test, which can be obtained by executing "adb devices" in the terminal.

``-output``: the output directory under /Tool/Output/app_package_name/

``-testcase_count`` The number of rounds that you want to test.

``-event_num`` The number of events in per round of test.

#### Detailed Description

##### Description of Output Files

* The output path of the tool is in ``/Too/Output/``.
* The result files of each app are classified and stored in ``/Too/Output/``.
* Open the folder of an app, and you will see the result files of each strategy for this app are stored by category.
* Open the folder corresponding regression test result, and you will see an ``error_realtime.txt`` file, a ``wrong_realtime.txt`` file, and many numbered folders corresponding to each round of test results.
* Open a numbered folder, and you can see a ``read_trace.txt`` file, a ``trace.txt`` file, an ``i_trace.html`` file, and a folder named ``screen``.
* Open the ``screen`` folder, and you can see the screenshot of each step and the corresponding interface layout information file.
* Next, I will introduce the content and use of each file.

###### error_realtime.txt

This file records the sequences that trigger the defects, which start with ``Start::x::run_count::y`` (x means the x-th error and Y means the error was captured during the y-th round of execution), and end with ``End::``

###### wrong_realtime.txt

This file records the sequences that trigger the suspected defects.

###### read_trace.txt

This file records the execution sequence of RegDroid, which is easy for RegDroid users to read.

###### trace.txt

This file records the execution sequence of RegDroid, which can be read and replayed by RegDroid.

###### i_trace.html

This file records the sequence of screenshots after each step, which is arranged horizontally. The events executed at each step are marked on the screenshot. After opening the file in the browser, there is a drag bar at the bottom, which can drag horizontally to view the whole sequence. When the error is captured, the screenshot is marked with a red frame. When the two interfaces are different, the screen capture is marked with a yellow frame.

# People-Counter
This program count incoming and outcoming people, who crooss by hall.
I find many examples in video, how count people who crossing hall or doors, 
but didn`t find examples code. I decided write little program, 
which been counting incoming and outcoming people.
I use OpenCV and Python 2.7

## Installing

So, begining you need install all dependensies:

```
pip install --trusted-host pypi.python.org -r requirements.txt
```
Use "import" for importing this library in your projects.

## Usage

For running program write in command line 

```
python PeopleCounterMain.py test2.mp4 -w 800
```

It is possible to test it with different videos and 
you can specifiy video frame width for

```sh
$ python PeopleCounterMain.py --help
usage: PeopleCounterMain.py [-h] [-w WIDTH] source

Count passing people from the selected video source

positional arguments:
  source                the directory of the image which will be opened

optional arguments:
  -h, --help            show this help message and exit
  -w WIDTH, --width WIDTH
                        video frame width of the video source
```

## How it works
If you want chenge video or set stream from rtsp camera change line

```
camera = cv2.VideoCapture("test2.mp4") # set here your video
```

This example use mechanism computer the absolute difference between the current frame and
first frame, so I compare two frame and if chenges exist i find where. If area bigest more than 
1200 I draw rectange around object which been chenged, if less than contour is too small, ignore it.

  

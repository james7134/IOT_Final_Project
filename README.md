# IOT_Final_Project
auto-turner

## Set up your Raspberry Pi
Make sure you have set up your Raspberry Pi. If not, you can follow the "Set_up.pdf" above to get ready to use.

## Overview
  A lot of people like to play guitar, violin and piano in their free
time. However, when we learn to play the instruments, it takes time to
turn the sheet music page from page.</br> 
  As a result, I want to develop an IoT device which can turn the
page automatically by sensing where the paragraph of music is
playing.</br> 
 This is device will pick out the 「dominant frequency 」of the
audio when we play the chords.

## Compoents
Raspberry Pi 3 Model B * 1</br>
Servo  Motor * 1</br>
N20 Motor * 1</br>
N20 Tire * 1</br>
Battery 1.5v * 4 </br>
Battery case * 1</br>
Breadboard * 1</br>
Wires * 15</br>

## Technologies implementation
**Sight-Reader**
* Step 1</br>
Get your hands on the sounds coming from the user’s microphone. 
```python
$ navigator.getUserMedia(
  // details about the 'user media' that we want access to
  {audio: true},

  // the user media, as a 'stream'
  stream => {
    // this is a stream of audio coming from the user's microphone
    // we will do things with this in just a moment...
  },

  // handling an error
  err => console.log(err)
);
```

* Step 2</br>
-There is an "audio context" that is at the center of everything you do with the audio you’re working with.</br>
-The audio contex that is source of audio would be the stream from the user’s mic.</br>
-Then we connect a thing called an ‘analyser’ which would give us some data about the audio. 

```python
const audioContext = new window.AudioContext();
const analyser = audioContext.createAnalyser();

navigator.getUserMedia(
  {audio: true},
  stream => audioContext.createMediaStreamSource(stream).connect(analyser),
  err => console.log(err)
);
```

* Step 3</br>
 Turn that rather abstract "stream" into an array of numbers.
 ```python
const audioContext = new window.AudioContext();
const analyser = audioContext.createAnalyser();

navigator.getUserMedia(
  {audio: true},
  stream => audioContext.createMediaStreamSource(stream).connect(analyser),
  err => console.log(err)
);

const dataArray = new Uint8Array(analyser.frequencyBinCount);

setTimeout(() => {
  analyser.getByteTimeDomainData(dataArray);
  console.log(dataArray);
}, 300);
```

* Step 4</br>
Loop through the array and spit it out onto a canvas.
 ```python
const audioContext = new window.AudioContext();
const analyser = audioContext.createAnalyser();

navigator.getUserMedia(
  {audio: true},
  stream => audioContext.createMediaStreamSource(stream).connect(analyser),
  err => console.log(err)
);

const dataArray = new Uint8Array(analyser.frequencyBinCount);

const canvasContext = refs.canvas.getContext('2d'); // a canvas I have in my HTML
canvasContext.fillStyle = 'firebrick';

setTimeout(() => {
  analyser.getByteTimeDomainData(dataArray);

  dataArray.forEach((item, i) => {
    canvasContext.fillRect(i, item, 1, 1);
  });
}, 300);
```

* Step 5</br>
1.The Web Audio API is recording at 44.1 kHz.</br>
2.The pitch of a note is defined by how many waves there are in one second.</br>
3.If 87 whatevers long. There are 44,100 whatevers in a second. Which means there would be 507 of these wobbles in one   second (44100 / 87). In other words, the pitch of this sound is 507 Hz. </br>

```python

const audioContext = new window.AudioContext();
const analyser = audioContext.createAnalyser();
const pitchSamples = [];
let audioReady = false;

navigator.getUserMedia(
  {audio: true},
  stream => {
    audioContext.createMediaStreamSource(stream).connect(analyser);
    audioReady = true;
  },
  err => console.log(err)
);

const dataArray = new Uint8Array(analyser.frequencyBinCount);

const canvasContext = refs.canvas.getContext('2d');
canvasContext.fillStyle = 'firebrick';

const drawWave = () => { // this gets called via requestAnimationFrame, so runs roughly every 16ms
  analyser.getByteTimeDomainData(dataArray);

  let lastPos = 0;
  dataArray.forEach((item, i) => {
    if (item > 128 && lastItem <= 128) { // we have crossed below the mid point
      const elapsedSteps = i - lastPos; // how far since the last time we did this
      lastPos = i;

      const hertz = 1 / (elapsedSteps / 44100);
      pitchSamples.push(hertz); // an array of every pitch encountered
    }

    canvasContext.fillRect(i, item, 1, 1); // point in the wave

    lastItem = item;
  });
};

const renderAudio = () => {
  requestAnimationFrame(renderAudio);

  if (!audioReady) return;

  canvasContext.clearRect(0, 0, 1024, 300);

  drawWave();
};

renderAudio(); // kick the whole thing off

setInterval(() => {
  renderKey(pitchSamples); // defined elsewhere, will get the average pitch and render a key
}, 250);
```

* Step 6</br>
Rendering a key(four times/sec)
```python
class SmartArray {
  constructor() {
    this.dataArray = [];
  }

  push(item) {
    this.dataArray.push(item);
  }

  get mode() {
    if (!this.dataArray.length) return 0;

    const counts = {};
    let mode = null;
    let max = 0;

    this.dataArray.forEach(item => {
      const value = Math.round(item * 10) / 10;

      counts[value] = (counts[value] || 0) + 1;

      if (counts[value] > max) {
        max = counts[value];
        mode = value;
      }
    });

    return mode;
  }

  get avg() {
    return this.dataArray.reduce((result, time) => {
        return result + time;
      }, 0) / this.dataArray.length;
  }

  get median() {
    if (!this.dataArray.length) return 0;
    const midPoint = Math.floor(this.dataArray.length / 2);
    return this.dataArray[midPoint];
  }

  empty() {
    this.dataArray.length = 0;
  }
}
```

* Step 7</br>
Draw a piano

```python
const COLORS = {
  EBONY: 'ebony',
  IVORY: 'ivory',
};

const SHIFTS = {
  LEFT: 'LEFT',
  MIDDLE: 'MIDDLE',
  RIGHT: 'RIGHT',
};

function getKeyDeets(keyPos) {
  const key = keyPos % 12;
  let shift;
  let color;

  if (key === 2 || key === 7) {
    shift = SHIFTS.RIGHT;
    color = COLORS.EBONY;
  } else if (key === 5 || key === 10) {
    shift = SHIFTS.LEFT;
    color = COLORS.EBONY;
  } else if (key === 0) {
    shift = SHIFTS.MIDDLE;
    color = COLORS.EBONY;
  } else {
    shift = null;
    color = COLORS.IVORY;
  }
  return {shift, color};
}

class Piano {
  render() {
    // key dimensions from http://www.rwgiangiulio.com/construction/manual/
    const {KEYS, refs} = SP_APP; // KEYS is an array of the 88 piano keys
    const pianoEl = refs.piano; // 'refs' are element references. 'piano' is an SVG wrapper
    const ns = 'http://www.w3.org/2000/svg';

    let left = 0;
    const blackKeyGroup = document.createElementNS(ns, 'g');
    const whiteKeyGroup = document.createElementNS(ns, 'g');

    KEYS.forEach(key => {
      const keyRect = document.createElementNS(ns, 'rect');
      const keyDeets = getKeyDeets(key.pos);
      let x = left;
      let height = 125;
      let width = 22;

      if (keyDeets.color === COLORS.EBONY) {
        height -= 45;
        width = 11;

        if (keyDeets.shift === SHIFTS.LEFT) {
          x = left - 7;
        } else if (keyDeets.shift === SHIFTS.MIDDLE) {
          x = left - 5;
        } else if (keyDeets.shift === SHIFTS.RIGHT) {
          x = left - 3;
        } else {
          console.warn('SHIFT was not set');
        }
      } else {
        left += 22;
        const keyText = document.createElementNS(ns, 'text');
        keyText.textContent = key.pos;

        keyText.setAttribute('x', x + width / 2);
        keyText.setAttribute('y', 10);
        keyText.setAttribute('text-anchor', 'middle');
        whiteKeyGroup.appendChild(keyText);
      }

      keyRect.setAttribute('rx', 2);
      keyRect.setAttribute('x', x);
      keyRect.setAttribute('y', 14);
      keyRect.setAttribute('width', width);
      keyRect.setAttribute('height', height);
      keyRect.setAttribute('data-ref', `key_${key.pos}`); // so I can access it with SP_APP.refs.key_22, for example
      keyRect.setAttribute('piano-key', true);
      keyRect.classList.add('piano-key');
      keyRect.classList.add(`piano-key--${keyDeets.color}`);

      if (keyDeets.color === COLORS.EBONY) {
        blackKeyGroup.appendChild(keyRect);
      } else {
        whiteKeyGroup.appendChild(keyRect);
      }
    });

    pianoEl.appendChild(whiteKeyGroup);
    pianoEl.appendChild(blackKeyGroup);
  }
}
```

* Step 8</br>
Let the key of piano can light up
```python
const renderKey = key => {
  const keyEls = document.querySelectorAll('[piano-key]');

  for (let keyEl of keyEls) {
    keyEl.style.fill = '';
    keyEl.classList.remove('piano-key--lit');
  }

  const pressedKeyEl = SP_APP.refs[`key_${key.pos}`];
  pressedKeyEl.classList.add('piano-key--lit');
};
```
* Step 9</br>
For using this Reader-</br>
1.open the terminal</br>
2.cd to the pageage of this reader</br>
`
$ cd C:\Users\MSI\Desktop\iot\sight-reader-master
`
</br>3.
`
$ npm install
`
</br>4.
`
$ npm run-script build
`
</br>5.
`
$ node index
`
</br>6.Go to the http://localhost:8080 with your browser</br>

**Page-turner**
![image](https://github.com/james7134/IOT_Final_Project/blob/main/page-turner/S__52051992.jpg?raw=true)
</br>
* Step 1</br>
Set up the page turner</br>
L298N Driver</br>
1.The left-blue wire connnect to the N20 Motor +</br>
2.The left-white wire connnect to the N20 Motor -</br>
3.The green wire connect to the power supply +</br>
4.The yellow wire connect to the power supply -</br>
5.The purple wire connect to the Ground on the pi</br>
6.The red wire connect to the 5v Power on the pi</br>
7.The gray wire connect to the pin 16</br>
8.The right-blue wire connect to the pin 18</br>
9.The right-white wire connect to the pin 22</br>
![image](https://github.com/james7134/IOT_Final_Project/blob/main/page-turner/S__52051996.jpg?raw=true)
</br>

* Step 2</br>
Set up Servo  motor</br>
1.The red wire connnect to 5v Power on the pi</br>
2.The orange one connnect to pin 11</br>
3.The brown one connnect to Ground</br>
![image](https://github.com/james7134/IOT_Final_Project/blob/main/page-turner/S__52051993.jpg?raw=true)
</br>

* Step 3</br>
Now you can use the page turner with the code below.
```python
# Import libraries
import sys
import RPi.GPIO as GPIO          
import time

in1 = 16
in2 = 18
en = 22
ser_1=11


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(22,GPIO.OUT)
GPIO.output(16,GPIO.LOW)
GPIO.output(18,GPIO.LOW)
GPIO.setup(11,GPIO.OUT)
p=GPIO.PWM(22,500)
servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

p.ChangeDutyCycle(100)


while(1)
    time.sleep(2)
    GPIO.output(16,GPIO.HIGH)
    GPIO.output(18,GPIO.LOW)

    time.sleep(2)

    GPIO.output(16,GPIO.LOW)
    GPIO.output(18,GPIO.LOW)

    #start PWM running, but with value of 0 (pulse off)
    servo1.start(2)
    servo1.ChangeDutyCycle(16)

    time.sleep(2)
    servo1.ChangeDutyCycle(2)

    #Clean things up at the end
servo1.stop()
GPIO.cleanup()
```

![image](https://github.com/james7134/IOT_Final_Project/blob/main/page-turner/Hnet-image.gif?raw=true)

**PiCamera-Digit-Recognizer-master**</br>
Beacuse the speed of Raspberry Pi is too slow, i choose to use my computer as a sensor for listening the audio. In additon to this, i didn't find out the way to let the web-api to set the result to Raspberry Pi. As a result, i use Picamera to caught the result of web-api on computer and make pi turn the page. </br>

* Step 1</br>
Set up the dependencies</br>

</br>1. Install Tensorflow</br>
`
pip install tensorflow
`
</br>2. Install keras</br>
`
pip install keras 
`
</br>3. Install Open-CV 3.3</br>
Here is a good tutorial for installing Open-Cv</br>
https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/
</br>4. Install the picamera with Numpy optimizations.</br>
`
pip install "picamera[array]"
`
</br>

* Step 2</br>
Algorithm Steps</br>
1. Read the image</br>
First step is to obviously put an image before the camera. This will be scaled later since the CNN (convolutional neural network) expect images of a certain size.</br>
2.Convert to gray scale</br>
The acquired image is then converted to gray-scale by using the scipy function call. Coincidentally you can only use opencv for the image manipulations but you have to remember all the function names. Also another point , there are some very subtle differences between scipy and open-cv when it comes to certain functions.</br>

3. Scale image range</br>
Here the image is converted from a floating point format to a uint8 range [0, 255]</br>

4. Thresholding</br>
To obtain a nice black and white image, thresholding is done via the Otsu method. This is the magic sauce step since doing thresholding manually will have one enter the values one by one.</br>

5. Resize image</br>
The image is resized to a 28 by 28 pixel array. This is then flattened to a linear array of size (28x28)</br>

6. Invert image</br>
MNIST DNN accepts images as 28x28 pixels, drawn as white on black background. So we have to invert the image.</br>

7. Feed into trained neural network</br>
This is the last step. Here we are loading the deep neural network weights and feed the image to the network. It takes 2-3 seconds to come up with a prediction.</br></br>

* Step 3</br>
If the Digit-Recognizer match the reult to the right key and correct timwline, if will make the turner turn the page 
```python
# 1. read image
# 2. convert to gray scale
# 3. convert to uint8 range
# 4. threshold via otsu method
# 5. resize image
# 6. invert image to balck background
# 7. Feed into trained neural network 
# 8. print answer

# from skimage.io import imread
#from skimage.transform import resize
import numpy as np
#from skimage import data, io
#from matplotlib import pyplot as plt
from skimage import img_as_ubyte		#convert float to uint8
from skimage.color import rgb2gray
import cv2
import datetime
import argparse
import imutils
import time
from time import sleep
from imutils.video import VideoStream
from keras.models import load_model
import turner as tu

model=load_model('mnist_trained_model.h5')		#import CNN model weight

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())
 
# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

def ImagePreProcess(im_orig):
  time_position = 0       #timeline position
  key_position = 0        #key which should turn the page
  time_point = 0          #
	im_gray = rgb2gray(im_orig)				#convert original to gray image
	#io.imshow(im_gray)
	#plt.show()
	img_gray_u8 = img_as_ubyte(im_gray)		# convert grey image to uint8
	#cv2.imshow("Window", img_gray_u8)
	#io.imshow(img_gray_u8)
	#plt.show()
	#Convert grayscale image to binary
	(thresh, im_bw) = cv2.threshold(img_gray_u8, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
	#cv2.imshow("Window", im_bw)
	#resize using opencv
	img_resized = cv2.resize(im_bw,(28,28))
	#cv2.imshow("Window", img_resized)
	############################################################
	#resize using sciikit
	#im_resize = resize(im,(28,28), mode='constant')
	#io.imshow(im_resize) 
	#plt.show()
	#cv2.imshow("Window", im_resize)
	##########################################################
	#invert image
	im_gray_invert = 255 - img_resized
	#cv2.imshow("Window", im_gray_invert)
	####################################
	im_final = im_gray_invert.reshape(1,28,28,1)
	# the below output is a array of possibility of respective digit
	ans = model.predict(im_final)
  
	# choose the digit with greatest possibility as predicted dight
	ans = ans[0].tolist().index(max(ans[0].tolist()))
  
        #determine where to turn the page
	if ans == key_position &&  time_point == time_position:
       		 tu()
        else
   		 ans++
    		 time_position++
    
def main():
	# loop over the frames from the video stream
	while True:
		try:
			# grab the frame from the threaded video stream and resize it
			# to have a maximum width of 400 pixels
			frame = vs.read()
			frame = imutils.resize(frame, width=400)
		 
			# draw the timestamp on the frame
			timestamp = datetime.datetime.now()
			ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
			cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
				0.35, (0, 0, 255), 1)
		 
			# show the frame
			cv2.imshow("Frame", frame)
			key = cv2.waitKey(1) & 0xFF
		 
			# if the `q` key was pressed, break from the loop
			if key == ord("q"):
				break
				# do a bit of cleanup
				cv2.destroyAllWindows()
				vs.stop()
			elif key == ord("t"):
				cv2.imwrite("num.jpg", frame)  
				im_orig = cv2.imread("num.jpg")
				ImagePreProcess(im_orig)
			else:
				pass
				
		except KeyboardInterrupt:
			# do a bit of cleanup
			cv2.destroyAllWindows()
			vs.stop()
			
			

if __name__=="__main__":
	main()

```
* Step  4</br>
-Open your terminal and</br>
`
$ python PiCameraApp.py
`
</br>
-Turn your Picamrea to the console of the web-api</br>
![image]()


## References</br>
* https://www.youtube.com/watch?v=xHDT4CwjUQE&ab_channel=ExplainingComputers</br>
* https://www.youtube.com/watch?v=wkZW9Hgrnao&ab_channel=ExplainingComputers</br>
* https://www.youtube.com/watch?v=2bganVdLg5Q&ab_channel=MakerTutor</br>
* https://developer.mozilla.org/en-US/docs/Web/API/AnalyserNode</br>
* https://developer.mozilla.org/en-US/docs/Web/API/Streams_API<br>
* https://www.hackster.io/dhq/ai-digit-recognition-with-picamera-2c017f#toc-program-explanation-5</br>

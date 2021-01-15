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
Server Motor * 1</br>
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
3.Whwn 87 whatevers long. There are 44,100 whatevers in a second. Which means there would be 507 of these wobbles in one   second (44100 / 87). In other words, the pitch of this sound is 507 Hz. </br>

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

* Step 7/br>
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
**Page-turner**
* Step 1</br>
The 

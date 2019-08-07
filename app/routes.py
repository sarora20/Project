from app import app
import flask
from flask import Flask, render_template, request, jsonify
import socket
import threading
import time
import random




#pd socket host/port
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 9001        # The port used by the server

#lists for scale offsets for key changes (arpeggiating)
majorOffsets = [0,4,7,12,16,19,24]
minorOffsets = [0,3,7,12,15,19,24]

#IP overload prevention dictionary
ipDict = {}
whitelistIP = ['137.22.183.192', '127.0.0.1','137.22.5.44']

key = 1
harmonyTrue = 1
midiGenType = 0
tempcounter = 0
#global variables sent to pd in noteout() msg
midi = 60
duration = 500
channel = 1
volume = 90
baselineVolume = 0
baselineMidi = 36
baselineDuration = 1000
baselineChannel = 4

#global array for the sequencer

sequencerArray = [[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7]]



def checkIP():
    global ipDict
    global whitelistIP
    testIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if testIP in whitelistIP:
        return True
    else:
        if testIP not in ipDict:
            ipDict[testIP] = time.time()
            return True
        else:
            if time.time()-ipDict[testIP] >= 2.0:
                ipDict[testIP] = time.time()
                return True
            else:
                return False

def is_ip_whitelisted():
    global whitelistIP
    testIP = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if testIP in whitelistIP:
        return True
    else:
        return False

def sequencerMidi():
    global sequencerArray



#pd socket connect
def noteout():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        #msg sent to unpack
        t = 0
        while True:
            global key
            global midi
            global harmonyTrue
            global baselineMidi
            global baselineVolume
            global baselineDuration
            global baselineChannel
            global midiGenType
            global sequencerArray
            global duration

            if midiGenType == 0:
                #random midi gen
                if key == 1:
                    tempMidi = 62
                    offsetIndex = random.randint (0,6)
                    midi = tempMidi + majorOffsets[offsetIndex]
                elif key == 2:
                    tempMidi = 58
                    offsetIndex = random.randint (0,6)
                    midi = tempMidi + minorOffsets[offsetIndex]

                if harmonyTrue % 2 == 0:
                    baselineMidi = midi - 7
                    baselineDuration = duration
                    baselineVolume = volume
                elif harmonyTrue % 2 == 1:
                    baselineVolume = 0


                msg = str(midi) + " " + str(duration) + " " + str(channel + 1) + " " + str(volume) + \
                " " + str(baselineVolume)+ " " + str(baselineMidi) + " " + str(baselineDuration) + " " + str(baselineChannel) +" ;"
                s.send(msg.encode('utf-8'))

                time.sleep(duration/1000)


            #sequencer
            else:

                tempDuration = duration
                midiRoot = 60
                majorSequencerOffsets = [0,2,4,5,7,9,11]
                minorSequencerOffsets = [0,2,3,5,7,8,10]
                sequencerMidiSend = []
                for r in sequencerArray:
                    if r[t] != 7:
                        if key == 1:
                            midiRoot = 60
                            sequencerMidiSend.append(midiRoot + majorSequencerOffsets[int(r[t])])
                        elif key == 2:
                            midiRoot = 58
                            sequencerMidiSend.append(midiRoot + minorSequencerOffsets[int(r[t])])
                for i in sequencerMidiSend:
                    msg = str(i) + " " + str(tempDuration) + " " + str(channel + 1) + " " + str(volume) + \
                    " " + str("0")+ " " + str(baselineMidi) + " " + str(baselineDuration) + " " + str(baselineChannel) +" ;"
                    s.send(msg.encode('utf-8'))

                time.sleep(tempDuration/1000)
                t = (t+1) % 8




                #sequencer midi gen


















#creating a new thread to handle the infinite msg output

class musicThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        noteout()

thread1 = musicThread(1, "Thread-1")
thread1.start()



@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/major_key')
def major_key():
    if checkIP():
        global key
        key = 1
        return "major"
    else:
        return "wait"
@app.route('/minor_key')
def minor_key():
    if checkIP():
        global key
        key = 2
        return "minor"
    else:
        return "wait"
@app.route('/increase_volume')
def increase_volume():
    global volume
    if checkIP():
        if volume <= 127:
            volume += 8
            return "increasevolume"
        else:
            pass
            return "increasevolume"
    else:
        return "wait"


@app.route('/decrease_volume')
def decrease_volume():
    global volume
    if checkIP():
        if volume >= 30:
            volume -= 8
            return "decreasevolume"
        else:
            pass
            return "decreasevolume"
    else:
        return "wait"


@app.route('/increase_tempo')
def increase_tempo():
    global duration
    if checkIP():
        if duration >= 200:
            duration = (duration / 8) * 7
            return "increasetempo"
        else:
            pass
            return "increasetempo"
    else:
        return "wait"


@app.route('/decrease_tempo')
def decrease_tempo():
    global duration
    if checkIP():
        if duration <= 5000:
            duration = (duration * 8) / 7
            return "decreasetempo"
        else:
            pass
            return "decreasetempo"
    else:
        return "wait"


@app.route("/add_bassline")
def add_baseline():
    global harmonyTrue
    if checkIP():
        harmonyTrue += 1
        return "toggleharmony"
    else:
        return "wait"


@app.route('/change_instrument')
def change_instrument():
    global channel
    if checkIP():
        channel = ((channel+1)%3)
        return "intrunment"
    else:
        return "wait"

@app.route('/toggle_midi')
def toggle_midi():
    global midiGenType
    global tempcounter
    if is_ip_whitelisted():
        tempcounter += 1
        if tempcounter % 2 == 1:
            midiGenType = 1
        else:
            midiGenType = 0
        print (midiGenType)
        return "toggle"
    else:
        return "Not Administrator"

@app.route('/clearSequencer')
def clear_sequencer():
    global sequencerArray
    if is_ip_whitelisted():
        sequencerArray = [[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7]]
        return "cleared"
    else:
        return "Not Administrator"

@app.route ('/sequence_action')
def sequenceAction():
    global sequencerArray

    sequencerOffsets = [6,5,4,3,2,1,0]

    data = (request.args)
    print (data)

    if data['ischecked'] == '1':
        #midiData = midi + sequencerMajorOffsets[int(data['row'])]
        sequencerArray [int(data['row'])][int(data['column'])] = sequencerOffsets[int(data['row'])]
    else:
        #midiData = 0
        sequencerArray [int(data['row'])][int(data['column'])] = 7


    return "sequencer"



@app.route ('/request_array')
def requestArray():
    global sequencerArray
    return jsonify(sequencerArray)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port="5000")

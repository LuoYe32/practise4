import json, os
import pyttsx3, vosk, pyaudio, requests
tts = pyttsx3.init()
voices = tts.getProperty('voices')
tts.setProperty('voices', 'ru')
for voice in voices:
    if voice.name == 'Microsoft David Desktop - English (UnitedStates)':
        tts.setProperty('voice', voice.id)
model = vosk.Model('vosk-model-small-ru-0.4')
record = vosk.KaldiRecognizer(model, 16000)
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16,
                 channels=1,
                 rate=16000,
                 input=True,
                 frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if record.AcceptWaveform(data) and len(data) > 0:
            answer = json.loads(record.Result())
            if answer['text']:
                yield answer['text']


def speak(say):
    tts.say(say)
    tts.runAndWait()

f = False
print('start')
pwd = ''
for text in listen():
    if text == 'закрыть':
        quit()
    elif text == 'следующий':
        f = True
        req = requests.get('http://numbersapi.com/random/math/?json')
        data = req.json()
        pwd = data['number']
        pwd1 = data['text']
        print(pwd)
    elif text == 'факт':
        if f:
            print(pwd1)
        else:
            print('нет фактов')
    elif text == 'прочитать':
        if f:
            speak(pwd1)
        else:
            speak('нечего читать')
    elif text == 'записать':
        if f:
            with open('result.txt', 'a', encoding="utf-8") as f:
                f.write(pwd1)
                f.write('\n')
                speak('записано')
        else:
            speak('нечего записывать')
    elif text == 'удалить':
        if f:
            with open('result.txt', 'r', encoding="utf-8") as f:
                if os.stat('result.txt').st_size:
                    lines = f.readlines()
                    lines = lines[:-1]
                    with open('result.txt', 'w', encoding="utf-8") as f:
                        f.write(str(*lines))
                    speak('удалено')
                else:
                    speak('нечего удалять')
        else:
            speak('нечего удалять')
    else:
        print(text)

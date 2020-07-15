import speech_recognition as sr

r = sr.Recognizer()

# capture data

demo = sr.AudioFile("data/sound.wav")
with demo as source:
	audio = r.record(source)

print(type(audio))

# recognizing speech in the audio

r.recognize_google(audio)
r.recognize_google(augio, language="pl-PL")

# recording segment of audio

with demo as source:
	audio = r.record(source, offset=4, duration=3)

r.recognize_google(audio)

# dealing with noise
with demo as source:
	r.adjust_for_ambient_noise(source)
	audio = r.record(source, offset=2.5, duration=3)
r.recognize_google(audio)

with demo as source:
	r.adjust_for_ambient_noise(source, duration=0.515)
	audio = r.record(source, offset=2.5, duration=3)
r.recognize_google(audio)

# MICROPHONES

mic = sr.Microphone()
sr.Microphone.list_microphone_names()

# or

mic = sr.Microphone(device_index=3)


# capturing microphone input

with mic as source:
	audio = r.listen(source)

r.recognize_google(audio)

with mic as source:
	r.adjust_for_ambient_noise(source)
	audio = r.listen(source)
r.recognize_google(audio)

# ARTICLE FROM
# https://data-flair.training/blogs/python-speech-recognition-ai/
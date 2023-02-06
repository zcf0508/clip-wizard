
import json
from typing import Dict, List
from uuid import uuid1

import whisper

from server import db
from server.models.task import Task

from .enums import ModelDevice, ModelSize

vad_model = None


def run_transcribe(speech_timestamps, audio, lang, whisper_model, task_id):
    try:
        task = Task.query.filter_by(uuid=task_id).first()
        if not task:
            task.status = 3
            task.err = 'task not found'
            db.session.commit()
            return
        res = []
        for seg in speech_timestamps:
            r = whisper_model.transcribe(
                audio[int(seg['start']) : int(seg['end'])],
                task='transcribe',
                language=lang,
            )
            r['origin_timestamp'] = seg
            res.append(r)
        print(res)
        task.res = json.dumps(res)
        task.status = 2
        db.session.commit()
    except BaseException as e:
        print(e)
        task.status = 3
        task.err = str(e)
        db.session.commit()
        

class Transcribe():
    sampling_rate = 16000
    size = ModelSize['base']
    device = ModelDevice['cpu']
    lang = 'zh'

    def __init__(self, input: str, size: str, device: str, lang: str, vad=True):
        print(input, size, device, lang, vad)
        self.input = input
        self.audio = whisper.load_audio(self.input, sr=self.sampling_rate)
        self.speech_timestamps: List[Dict[str, int]] = []
        self.size = size
        self.device = device
        self.whisper_model: whisper.Whisper = None
        self.lang = lang
        self.vad = vad
        self.vad_model = None
    
    def setup(self):
        self.whisper_model = whisper.load_model(self.size, self.device)
        self.speech_timestamps = [{"start": 0, "end": len(self.audio)}]
        if self.vad:
            self._voice_activity_detection()
        else:
            self.speech_timestamps = [{"start": 0, "end": len(self.audio)}]

    def _voice_activity_detection(self):
        # TODO: Implement voice activity detection
        self.speech_timestamps = [{"start": 0, "end": len(self.audio)}]
        pass

    def run(self):
        self.setup()
        if len(self.speech_timestamps) == 0:
            return False, None
        
        task_id = str(uuid1())
        task = Task(task_id, self.input)
        try:
            db.session.add(task)
            db.session.commit()

            from multiprocessing import Process
            Process(
                target=run_transcribe, 
                args=(self.speech_timestamps, self.audio, self.lang, self.whisper_model, task_id)
            ).start()

        except BaseException as e:
            task.status = 3
            task.err = str(e)
            db.session.commit()
            print(e)
        return True, task_id


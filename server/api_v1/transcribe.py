import json

from flask import jsonify, request

from server.utils.transcribe import ModelDevice, ModelSize, Transcribe

from . import api_v1


@api_v1.route("/transcribe", methods=['POST'])
def transcribe():
    input = request.get_json().get("input", None)
    size = request.get_json().get("size", ModelSize['small'])
    device = request.get_json().get("device", ModelDevice['cpu'])
    lang = request.get_json().get("lang", 'zh')
    vad = request.get_json().get("vad", True)

    if not input:
        return jsonify({
            "code": -1,
            "msg": "Missing input",
            "data": None
        })
    try:
        status, uuid = Transcribe(input, size, device, lang, vad).run()
        return jsonify({
            "code": 0,
            "msg": "OK",
            "data": {
                "status": status,
                "uuid": uuid,
            }
        })
    except BaseException as e:
        print(e)
        return jsonify({
            "code": -444,
            "msg": "Unknown error",
            "data": None
        })

@api_v1.route("/transcribe_report", methods=['GET'])
def transcribe_report():
    uuid = request.args.get("uuid", None) # e9a558ff-a5e2-11ed-91eb-04d4c4009b25
    if not uuid:
        return jsonify({
            "code": -1,
            "msg": "Missing uuid",
            "data": None
        })
    from server.models.task import Task
    task = Task.query.filter_by(uuid=uuid).first()
    if not task:
        return jsonify({
            "code": -2,
            "msg": "Task not found",
            "data": None
        })
    return jsonify({
        "code": 0,
        "msg": "OK",
        "data": {
            "status": task.status,
            "err": task.err,
            "result": json.loads(task.result) if task.result else None,
        },
    })


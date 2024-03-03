import json


def parse(s):
    try:
        j = json.loads(s)
        name = j['name']
        subject = j['subject']
        termsofstudying = j['termsofstudying']
        matnr = j['matnr']
        assert isinstance(name, str) and isinstance(subject, str) \
               and isinstance(termsofstudying, str) and isinstance(matnr, str)
        return name, subject, termsofstudying, matnr
    except Exception:
        return None

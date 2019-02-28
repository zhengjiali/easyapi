from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .models import *
from api.test_views import *
import json
from api.models import *
from utils.send_email import send_email
# from django.contrib.auth.models import User

@shared_task
def execute(task_id):
    t = task.objects.get(id=int(task_id))
    p = t.plan
    env = t.runtime_env
    user = t.user
    for case in p.cases.all():
        if case.validation == '':
            valids = json.loads('{}')
        else:
            valids = json.loads(case.validation)
        try:
            r = test_case(env.id, case)
            result_id = save_result(r, case, task_id, env.id)
            if len(valids.keys()) > 0:
                verify(result_id, valids)
        except Exception as e:
            result_id = save_exception(e, case, task_id, env.id)
            continue

    t.status = 1
    t.save()
    if user.email:
        send_email(user.email,"done")
    return t.status

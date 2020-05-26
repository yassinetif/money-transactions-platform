from django_q.tasks import AsyncTask
from apps.shared.repository.shared_repository import SharedRepository
def run(to, text):
    task = AsyncTask('apps.services.controller.sms_controller.send_otp_sms_task', to, text, group='sms',
                     hook='apps.services.tasks.sms_task.hook')
    task.run()


def hook(task):
    SharedRepository.save_notification('SMS', task.args[1], task.args[0], task.result)

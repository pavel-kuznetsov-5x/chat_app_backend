from fcm_django.models import FCMDevice


def send_message(user, message):
    device = FCMDevice.objects.filter(user_id=user.id).first()
    if device:
        print("message sent")
        device.send_message(data={"test": "test"})

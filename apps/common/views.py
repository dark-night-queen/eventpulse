# Standard Library imports
from django.http import JsonResponse

# App imports
from apps.common.kafka.producer import KafkaProducer


def health(request):
    return JsonResponse({"status": "ok"}, status=200)


def test_event(request):
    try:
        producer = KafkaProducer()
        producer.send_message(
            topic="events",
            key="user-42",
            message={
                "event": "user.created",
                "team_id": 42,
                "payload": {"name": "Shreya"},
            },
        )
        producer.flush()
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "event sent!"})

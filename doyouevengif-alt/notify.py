import json
import os
import sys
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTIFICATIONS_FILE = os.path.join(BASE_DIR, 'notifications.json')


def get_notifications():
    if os.path.exists(NOTIFICATIONS_FILE):
        try:
            with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def get_unread_count():
    return sum(
        1 for n in get_notifications()
        if not n.get("read", False)
    )


def add_notification(message):
    notifications = get_notifications()

    new_id = max(
        [n.get("id", 0) for n in notifications],
        default=0
    ) + 1

    notifications.append({
        "id": new_id,
        "message": message,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "read": False,
        "avatar": "/faviconn.png"
    })

    with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            notifications,
            f,
            indent=2,
            ensure_ascii=False
        )

    return notifications


def mark_as_read(notification_id):
    notifications = get_notifications()

    for n in notifications:
        if n.get("id") == notification_id:
            n["read"] = True
            break

    with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(
            notifications,
            f,
            indent=2,
            ensure_ascii=False
        )

    return notifications


def clear_all():
    with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, indent=2, ensure_ascii=False)

    return []


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Usage: python notify.py "Your notification message"')
        sys.exit(1)

    # Everything after "notify.py" becomes the message.
    message = " ".join(sys.argv[1:])

    result = add_notification(message)

    print(f"✅ Notification added! Total: {len(result)}")

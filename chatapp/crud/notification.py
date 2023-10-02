from sqlalchemy.orm import Session
from chatapp.models.notification import Notification

def create_notification(db: Session, notification_data: dict):
    notification = Notification(**notification_data)
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification

def get_notification(db: Session, notification_id: int):
    return db.query(Notification).filter(Notification.id == notification_id).first()

def get_notifications(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Notification).offset(skip).limit(limit).all()

def update_notification(db: Session, notification_id: int, notification_data: dict):
    notification = get_notification(db, notification_id)
    if notification is None:
        return None
    for key, value in notification_data.items():
        setattr(notification, key, value)
    db.commit()
    db.refresh(notification)
    return notification

def delete_notification(db: Session, notification_id: int):
    notification = get_notification(db, notification_id)
    if notification is None:
        return False
    db.delete(notification)
    db.commit()
    return True

def get_notifications_by_user(db: Session, user_id: int):
    return db.query(Notification).filter(Notification.recipient_id == user_id).all()


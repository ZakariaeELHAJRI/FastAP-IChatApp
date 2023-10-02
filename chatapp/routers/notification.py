from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from chatapp.database import get_db
from chatapp.crud.notification import create_notification, get_notification, get_notifications, update_notification, delete_notification, get_notifications_by_user
from chatapp.models.notification import Notification
from dependencies.auth import User, get_current_user
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
router = APIRouter()

@router.post("/notifications/")
def create_new_notification(notification_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return create_notification(db, notification_data)

@router.get("/notifications/{notification_id}")
def get_single_notification(notification_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        notification = get_notification(db, notification_id)
        if notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    except Exception as e:
        logging.error(f"Error in get_single_notification: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
@router.get("/notifications/")
def get_all_notifications(skip: int = 0, limit: int = 10, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_notifications(db, skip, limit)

@router.put("/notifications/{notification_id}")
def update_existing_notification(notification_id: int, notification_data: dict, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = update_notification(db, notification_id, notification_data)
    if notification is None:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notification

@router.delete("/notifications/{notification_id}")
def delete_existing_notification(notification_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    notification = delete_notification(db, notification_id)
    if notification is False:
        raise HTTPException(status_code=404, detail="Notification not found")
    return {"message": "Notification deleted successfully"}

@router.get("/notifications-by-user/{user_id}")
def get_notifications_by_u(user_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        notifications = get_notifications_by_user(db, user_id)
        if not notifications:
            raise HTTPException(status_code=404, detail="Notifications not found")
        custom_notifications = [
            {
                "id": notification.id,
                "sender_id": notification.sender_id,
                "first_name_sender" :db.query(User).filter(User.id == notification.sender_id).first().firstname,
                "last_name_sender" :db.query(User).filter(User.id == notification.sender_id).first().lastname,
                "recipient_id": notification.recipient_id,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at,
            }
            for notification in notifications
        ]
        return custom_notifications
    except Exception as e:
        logging.error(f"Error in get_notifications_by_user: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
        

@router.put("/mark-notification-as-read/{user_id}")
def mark_notification_as_read(user_id: int, db: Session = Depends(get_db)):
    try:
        notifications = get_notifications_by_user(db, user_id)
        print("notifications before :", notifications)  
        if not notifications:
            raise HTTPException(status_code=404, detail="Notifications not found")

        for notification in notifications:
            if not notification.is_read:
                notification.is_read = True

        db.commit()
        print("notifications:", notifications)  
        return notifications
    except Exception as e:
        logging.error(f"Error in mark_notification_as_read: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

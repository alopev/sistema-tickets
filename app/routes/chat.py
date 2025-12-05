from flask import request
from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from app.models import ChatMessage, User

# Dictionary to track online users: {user_id: session_id}
online_users = {}

@socketio.on('connect')
def handle_connect():
    if current_user.is_authenticated:
        # Add user to online users
        online_users[current_user.id] = request.sid
        print(f'User {current_user.username} connected with sid {request.sid}')
        
        # Broadcast updated online users list to all clients
        emit_online_users()
        
        # Broadcast individual status change to all other clients
        emit_user_status_change(current_user.id, current_user.username, True)
        
        # Send unread counts to current user
        unread_counts = get_unread_counts(current_user.id)
        emit('unread_counts', unread_counts)
    else:
        print('Anonymous user connected')

@socketio.on('disconnect')
def handle_disconnect():
    if current_user.is_authenticated:
        user_id = current_user.id
        username = current_user.username
        
        # Remove user from online users
        if user_id in online_users:
            del online_users[user_id]
            print(f'User {username} disconnected')
            
            # Broadcast updated online users list
            emit_online_users()
            
            # Broadcast individual status change to all other clients
            emit_user_status_change(user_id, username, False)

@socketio.on('get_online_users')
def handle_get_online_users():
    """Send list of online users to requesting client"""
    emit_online_users()

@socketio.on('private_message')
def handle_private_message(data):
    """Handle private message between two users"""
    if not current_user.is_authenticated:
        return
    
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    
    if not receiver_id or not content:
        return
    
    # Save message to database
    message = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    # Prepare message data
    message_data = {
        'id': message.id,
        'sender_id': current_user.id,
        'sender_name': current_user.username,
        'receiver_id': receiver_id,
        'content': content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Send to sender (confirmation)
    emit('new_message', message_data, room=request.sid)
    
    # Send to receiver if online, otherwise send email
    if receiver_id in online_users:
        receiver_sid = online_users[receiver_id]
        emit('new_message', message_data, room=receiver_sid)
    else:
        # Receiver is offline, send email notification
        receiver = User.query.get(receiver_id)
        if receiver:
            from app.email import send_chat_notification_email
            # Truncate message for preview
            message_preview = content[:100] + '...' if len(content) > 100 else content
            send_chat_notification_email(current_user, receiver, message_preview)

@socketio.on('get_chat_history')
def handle_get_chat_history(data):
    """Get chat history between current user and another user"""
    if not current_user.is_authenticated:
        return
    
    other_user_id = data.get('user_id')
    if not other_user_id:
        return
    
    # Get messages between these two users
    messages = ChatMessage.query.filter(
        db.or_(
            db.and_(ChatMessage.sender_id == current_user.id, ChatMessage.receiver_id == other_user_id),
            db.and_(ChatMessage.sender_id == other_user_id, ChatMessage.receiver_id == current_user.id)
        )
    ).order_by(ChatMessage.timestamp.asc()).all()
    
    # Mark messages as read
    for msg in messages:
        if msg.receiver_id == current_user.id and not msg.read:
            msg.read = True
    db.session.commit()
    
    # Format messages
    history = [{
        'id': msg.id,
        'sender_id': msg.sender_id,
        'sender_name': msg.sender.username,
        'receiver_id': msg.receiver_id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'read': msg.read
    } for msg in messages]
    
    emit('chat_history', {'messages': history, 'other_user_id': other_user_id})

@socketio.on('mark_as_read')
def handle_mark_as_read(data):
    """Mark messages from a specific user as read"""
    if not current_user.is_authenticated:
        return
    
    sender_id = data.get('sender_id')
    if not sender_id:
        return
    
    # Mark all unread messages from this sender as read
    ChatMessage.query.filter_by(
        sender_id=sender_id,
        receiver_id=current_user.id,
        read=False
    ).update({'read': True})
    db.session.commit()

def emit_online_users():
    """Broadcast list of ALL users (online and offline) to all connected clients"""
    # Get ALL users
    all_users = User.query.all()
    
    # Create a list for each connected user
    for user_id, session_id in online_users.items():
        user_list = []
        for user in all_users:
            # Don't include the user themselves in their own list
            if user.id != user_id:
                user_list.append({
                    'id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'profile_picture': user.get_profile_picture(),
                    'is_online': user.id in online_users  # Mark if user is online
                })
        
        # Sort: online users first, then by username
        user_list.sort(key=lambda x: (not x['is_online'], x['username']))
        
        # Send to this specific user
        emit('online_users', {'users': user_list}, room=session_id)

def emit_user_status_change(user_id, username, is_online):
    """Broadcast individual user status change to all connected clients"""
    from datetime import datetime
    emit('user_status_changed', {
        'user_id': user_id,
        'username': username,
        'is_online': is_online,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }, broadcast=True)

def get_unread_counts(user_id):
    """Get count of unread messages for a user from each sender"""
    unread_counts = db.session.query(
        ChatMessage.sender_id, db.func.count(ChatMessage.id)
    ).filter(
        ChatMessage.receiver_id == user_id,
        ChatMessage.read == False
    ).group_by(ChatMessage.sender_id).all()
    
    return {sender_id: count for sender_id, count in unread_counts}

def global_user(user_id):
    from bot import DB
    return DB.child("UserConfig").child(str(user_id))
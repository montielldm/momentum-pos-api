from app.users.models import User

def user_serializer(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "lastname": user.lastname,
        "document_type": user.document_type,
        "document": user.document,
        "email": user.email,
        "telephone": user.telephone,
        "created_at": user.created_at,
        "avatar": user.avatar,
        "status": user.status,
        "company": user.company.company_name,
    }
from app.customers.models import Customer

def customer_serializer(customer: Customer) -> dict:
    return {
        "id": customer.id,
        "name": customer.name,
        "type_identification": customer.type_identification,
        "identification": customer.identification,
        "phone": customer.phone,
        "email": customer.email
    }
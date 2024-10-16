from gradio_client import Client

client = Client("Youssef-Hatem/Banking-churn")
result = client.predict(
    credit_score=502,
    gender="Male",
    tenure=2,
    balance=3,
    age=42,
    products_number=3,
    credit_card="Yes",
    active_member="Yes",
    estimated_salary=3,
    country="France",
    api_name="/predict",
)
print(result)

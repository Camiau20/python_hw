from fastapi import FastAPI, Query
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()


DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"


engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)

app = FastAPI()

@app.get("/orders")
def get_orders(start_date: datetime, end_date: datetime):
    session = Session()

    #
    orders = session.query(Order).filter(
        Order.created_at >= start_date,
        Order.created_at <= end_date
    ).all()

    
    orders_data = []
    overall_total = 0
    for order in orders:
        order_total = 0
        order_details = []
        for detail in order.details:
            product_total = detail.price * detail.quantity
            order_details.append({
                'product_name': detail.product.name,
                'quantity': detail.quantity,
                'price': detail.price,
                'total': product_total
            })
            order_total += product_total

        orders_data.append({
            'order_id': order.id,
            'total': order_total,
            'details': order_details
        })
        overall_total += order_total

    session.close()

    return {
        'orders': orders_data,
        'overall_total': overall_total
    }
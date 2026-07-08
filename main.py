from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from model import CustomerModel
from schema import CustomerUpdate, CustomerResponse

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.put("/customers/{customer_id}", response_model=CustomerResponse, status_code=status.HTTP_200_OK)
def update_customer(customer_id: int, customer_update: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(CustomerModel).filter(
        CustomerModel.id == customer_id
    ).first()

    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )

    customer.full_name = customer_update.full_name
    customer.phone = customer_update.phone
    customer.address = customer_update.address

    db.commit()
    db.refresh(customer)

    return customer
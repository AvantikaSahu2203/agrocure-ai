import logging
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.medicine import Medicine
from app.models.inventory import StoreInventory
from app.models.store import Store
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.db.base import Base
from app.db.session import engine

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Check if we have a user to own the store
        user = db.query(User).filter(User.email == "farmer@agrocure.com").first()
        if not user:
            from app.core.security import get_password_hash
            user = User(
                email="farmer@agrocure.com",
                hashed_password=get_password_hash("password"),
                full_name="Farmer Joe",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            logger.info(f"Created Default User: {user.email}")

        # 1. Create a Store if not exists
        store = db.query(Store).filter(Store.name == "AgroCure Official Store").first()
        if not store:
            store = Store(
                name="AgroCure Official Store",
                owner_id=user.id,
                description="Official partner store for AgroCure",
                address="123 Agro Tech Park, Pune",
                city="Pune",
                state="Maharashtra",
                rating=4.8
            )
            db.add(store)
            db.commit()
            db.refresh(store)
            logger.info(f"Created Store: {store.name}")
        else:
            logger.info(f"Store exists: {store.name}")

        # 2. Create Medicines
        medicines_data = [
            {
                "name": "Amistar Top",
                "description": "Broad spectrum fungicide for control of diseases in various crops.",
                "category": "Fungicide",
                "manufacturer": "Syngenta",
                "image_url": "https://agribegri.com/product_images/b_1000_2245_16_02_2024_11_29_57.jpg"
            },
            {
                "name": "Coragen",
                "description": "Insecticide for control of pests in various crops.",
                "category": "Insecticide",
                "manufacturer": "FMC",
                "image_url": "https://krishibazaar.in/wp-content/uploads/2020/03/Coragen-1.jpg"
            },
            {
                "name": "Urea 46%",
                "description": "High nitrogen fertilizer for vegetative growth.",
                "category": "Fertilizer",
                "manufacturer": "IFFCO",
                "image_url": "https://5.imimg.com/data5/SELLER/Default/2022/9/MQ/OF/DA/47407758/urea-fertilizer.jpg"
            },
            {
                "name": "Neem Oil",
                "description": "Organic pesticide for eco-friendly farming.",
                "category": "Organic",
                "manufacturer": "AgroPure",
                "image_url": "https://m.media-amazon.com/images/I/71J1rJ2+uOL.jpg"
            }
        ]

        for med_data in medicines_data:
            medicine = db.query(Medicine).filter(Medicine.name == med_data["name"]).first()
            if not medicine:
                medicine = Medicine(**med_data)
                db.add(medicine)
                db.commit()
                db.refresh(medicine)
                logger.info(f"Created Medicine: {medicine.name}")
            
            # 3. Add to Inventory
            inventory_item = db.query(StoreInventory).filter(
                StoreInventory.store_id == store.id,
                StoreInventory.medicine_id == medicine.id
            ).first()
            
            if not inventory_item:
                inventory_item = StoreInventory(
                    store_id=store.id,
                    medicine_id=medicine.id,
                    quantity=100,
                    unit_price=500.0 if "Amistar" in med_data["name"] else 250.0
                )
                db.add(inventory_item)
                db.commit()
                logger.info(f"Added to Inventory: {medicine.name}")

    except Exception as e:
        logger.error(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()

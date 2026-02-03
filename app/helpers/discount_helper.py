from datetime import datetime
from typing import Optional
from decimal import Decimal


class DiscountHelper:
    @staticmethod
    def validate_discount(discount_type: str, discount_value: Decimal):
        if discount_type not in ["PERCENT", "FLAT"]:
            raise ValueError("Invalid discount type")

        if discount_value <= 0:
            raise ValueError("Discount value must be greater than zero")

        if discount_type == "PERCENT" and discount_value > 100:
            raise ValueError("Percentage discount cannot exceed 100%")
    @staticmethod
    def is_discount_active(start_date: Optional[datetime],
        end_date: Optional[datetime],
        now: Optional[datetime] = None)-> bool:
        now = now or datetime.utcnow()
        
        if start_date and now < start_date:
            return False
        if end_date and now > end_date:
            return False
        return True
    
    @staticmethod
    def calculate_price(price:  Decimal,
        discount_type: str,
        discount_value:  Decimal)-> Decimal:
        
        if discount_type == "PERCENT":
            return price * (Decimal("1") - discount_value / Decimal("100"))
        
        if discount_type == "FLAT":
           return max(price - discount_value, Decimal("0"))
        
        return price
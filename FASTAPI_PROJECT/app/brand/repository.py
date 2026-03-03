from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from typing import Optional, List
from .models import Brand


COMPARISON_MAP = {
    "eq":         lambda col, val: col == val,
    "neq":        lambda col, val: col != val,
    "contains":   lambda col, val: col.ilike(f"%{val}%"),
    "startswith": lambda col, val: col.ilike(f"{val}%"),
    "endswith":   lambda col, val: col.ilike(f"%{val}"),
    "gt":         lambda col, val: col > val,
    "gte":        lambda col, val: col >= val,
    "lt":         lambda col, val: col < val,
    "lte":        lambda col, val: col <= val,
}


def get_all_brands(
    db: Session,
    filters: Optional[List[dict]] = None,
    order_ascending: Optional[bool] = None,
    order_property: Optional[str] = None,
    page_index: Optional[int] = None,
    page_size: Optional[int] = None,
):
    query = db.query(Brand)

    # Apply Filters
    if filters:
        for f in filters:
            prop = f.get("property")
            comparison = f.get("comparison", "eq").lower()
            value = f.get("value")

            column = getattr(Brand, prop, None)
            if column is not None and comparison in COMPARISON_MAP:
                query = query.filter(COMPARISON_MAP[comparison](column, value))

    # Apply Ordering
    if order_property:
        column = getattr(Brand, order_property, None)
        if column is not None:
            query = query.order_by(asc(column) if order_ascending is not False else desc(column))

    # Apply Pagination
    if page_index and page_size:
        offset = (page_index - 1) * page_size
        query = query.offset(offset).limit(page_size)

    return query.all()


def get_brand_by_id(db: Session, brand_id: int):
    return db.query(Brand).filter(Brand.brandId == brand_id).first()


def create_brand(db: Session, brand_data: dict):
    brand = Brand(**brand_data)
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


def update_brand(db: Session, brand_id: int, brand_data: dict):
    brand = get_brand_by_id(db, brand_id)
    if not brand:
        return None
    for key, value in brand_data.items():
        setattr(brand, key, value)
    db.commit()
    db.refresh(brand)
    return brand


def delete_brand(db: Session, brand_id: int):
    brand = get_brand_by_id(db, brand_id)
    if not brand:
        return None
    db.delete(brand)
    db.commit()
    return True
# ERD - Olist SQL Business Analysis

This ERD reflects the normalized source-style schema used for the SQL analysis.

```mermaid
erDiagram
    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--o{ ORDER_ITEMS : contains
    ORDERS ||--o{ ORDER_PAYMENTS : paid_by
    ORDERS ||--o{ ORDER_REVIEWS : reviewed_by
    PRODUCTS ||--o{ ORDER_ITEMS : appears_in
    SELLERS ||--o{ ORDER_ITEMS : sells
    PRODUCT_CATEGORY_TRANSLATION ||--o{ PRODUCTS : translates

    CUSTOMERS {
        varchar customer_id PK
        varchar customer_unique_id
        integer customer_zip_code_prefix
        text customer_city
        char customer_state
    }

    ORDERS {
        varchar order_id PK
        varchar customer_id FK
        text order_status
        timestamp order_purchase_timestamp
        timestamp order_approved_at
        timestamp order_delivered_carrier_date
        timestamp order_delivered_customer_date
        timestamp order_estimated_delivery_date
    }

    ORDER_ITEMS {
        varchar order_id PK, FK
        integer order_item_id PK
        varchar product_id FK
        varchar seller_id FK
        timestamp shipping_limit_date
        numeric price
        numeric freight_value
    }

    ORDER_PAYMENTS {
        varchar order_id PK, FK
        integer payment_sequential PK
        text payment_type
        integer payment_installments
        numeric payment_value
    }

    ORDER_REVIEWS {
        varchar review_id PK
        varchar order_id PK, FK
        integer review_score
        text review_comment_title
        text review_comment_message
        timestamp review_creation_date
        timestamp review_answer_timestamp
    }

    PRODUCTS {
        varchar product_id PK
        text product_category_name FK
        integer product_name_lenght
        integer product_description_lenght
        integer product_photos_qty
        integer product_weight_g
        integer product_length_cm
        integer product_height_cm
        integer product_width_cm
    }

    PRODUCT_CATEGORY_TRANSLATION {
        text product_category_name PK
        text product_category_name_english
    }

    SELLERS {
        varchar seller_id PK
        integer seller_zip_code_prefix
        text seller_city
        char seller_state
    }

    GEOLOCATION {
        integer geolocation_zip_code_prefix
        numeric geolocation_lat
        numeric geolocation_lng
        text geolocation_city
        char geolocation_state
    }
```

## Modeling Notes

- `customers.customer_id` is order-level customer identity; `customer_unique_id` is the person-level identity used for repeat customer analysis.
- `order_items` is the main revenue fact table. One order can have multiple items and sellers.
- `order_payments` can contain multiple payment rows per order, so payment analysis is kept separate from item-revenue analysis to avoid duplicated joins.
- `geolocation` is included as source data but not joined by default because ZIP prefixes can repeat many times. Aggregate it to ZIP prefix first before using it in analysis.

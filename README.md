# Vendor-management-system
This system will handle vendor profiles, track purchase orders, and calculate vendor performance metrics.


# Vendor Management System Setup Guide

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-repository/vendor-management-system.git
   cd vendor-management-system
   ```

2. **Install required packages**

   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup**

   Ensure you have a database set up and configured. Update the `DATABASES` configuration in `settings.py` according to your database credentials.

4. **Run Migrations**

   ```bash
   python manage.py migrate
   ```

5. **Start the Development Server**

   ```bash
   python manage.py runserver
   ```

   This will start the server on `http://127.0.0.1:8000/`.

## API Usage

The system provides several APIs to manage vendors, purchase orders, and calculate performance metrics.

### Vendor APIs

- **List and Create Vendors**
  - **GET** `/api/vendors/`: List all vendors.
  - **POST** `/api/vendors/`: Create a new vendor.
```bash
  payload
    {
        "vendor_code": "unique-id",
        "name": "kush",
        "contact_details": "unique-no.",
        "address": "value",
        "on_time_delivery_rate": 0.0,
        "quality_rating_avg": 0.0,
        "average_response_time": 0.0,
        "fulfillment_rate": 0.0,
        "ontime_deliver_order": 0
    }
```
- **Update, Retrieve, and Delete Vendor**
  - **GET** `/api/vendors/<vendor_code>/`: Retrieve a vendor.
  - **PUT/PATCH** `/api/vendors/<vendor_code>/`: Update a vendor.
  - **DELETE** `/api/vendors/<vendor_code>/`: Delete a vendor.

- **Vendor Performance**
  - **GET** `/api/vendors/<vendor_code>/performance/`: Get performance metrics for a vendor.

### Purchase Order APIs

- **List and Create Purchase Orders**
  - **GET** `/api/purchase_orders/`: List all purchase orders.
  - **POST** `/api/purchase_orders/`: Create a new purchase order.
  payload
  {
    "po_number": "unique-id",
    "order_date": null,
    "delivery_date": null,
    "items": {
        //details for the order exapmle color, size, name 
    },
    "quantity": value,
    "status": "",
    "quality_rating": 0.0,
    "issue_date": null,
    "acknowledgment_date": null,
    "vendor": "unique-id of vendor"
}

- **Update, Retrieve, and Delete Purchase Order**
  - **GET** `/api/purchase_orders/<po_number>/`: Retrieve a purchase order.
  - **PUT/PATCH** `/api/purchase_orders/<po_number>/`: Update a purchase order.
  - **DELETE** `/api/purchase_orders/<po_number>/`: Delete a purchase order.

- **Additional Purchase Order Actions**
  - **PATCH** `/api/purchase_orders/<po_number>/acknowledge/`: Acknowledge a purchase order.
  - **PATCH** `/api/purchase_orders/<po_number>/delivery/`: Record delivery of a purchase order.
  - **PATCH** `/api/purchase_orders/<po_number>/rating/`: Rate the quality of a purchase order.

## Conclusion

This system allows for comprehensive management of vendors and purchase orders while providing insights into vendor performance. Follow the above steps to set up and start using the system.



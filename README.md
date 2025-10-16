# Restaurant Web App – Project Plan (MVP Scope)

## 1) Brief Description
A lightweight restaurant web application where customers can **browse the menu**, **add items to a cart**, and **place an order** for **dine-in or pickup** as a **guest or logged-in user**.  
Staff can **view incoming orders** and **update their status** through a basic dashboard.  
**Out of scope for MVP**: order history pages, menu item customization, inventory/stock management, nutrition labels, online payment.

**Tech stack:** Django, PostgreSQL , HTML/CSS.

---

## 2) ERD
```mermaid
---
title: Restaurant app ERD
---
erDiagram
    User {
        int user_id PK
        varchar(50) username
        varchar(1) user_type
        varchar(50) password
        varchar(50) email
        int phone
    }
    Order {
        int order_id PK
        int user_id FK
        varchar(1) status
        varchar(1) order_type
        int party
        datetime reservation_time
        int table_no
        varchar(50) address
    }
    MenuItem {
        int menu_item_id PK
        varchar(50) name
        varchar(50) ingredients
        boolean is_available
        float unit_price
        int portions
        varchar(2) allergen
    }
    OrderItem {
        int order_item_id PK
        int menu_item_id FK
        int order_id FK
        int quantity
    }
    UserAddress {
        int user_id FK
        varchar(25) building
        varchar(25) street
        varchar(25) region
        varchar(25) city
    }
    User ||--|{ UserAddress : has
    User ||--o{ Order : makes
    Order ||--|{ OrderItem : contains
    OrderItem ||--|| MenuItem : contains
```````
---

## 3) User Stories

### Guest Customer
- As a guest, I want to **browse the menu by category** so I can quickly see available dishes.
- As a guest, I want to **login or signup for an account**.
- As a guest, I want to **view information about the restaurant**.

### Registered Customer
- As a registered user, I want to **log in** so my basic details auto-fill at checkout.
- As a registered user, I want my **profile (name/address)** to be saved so checkout is faster next time.
- As a registered user, I want to **add/remove items from my order and adjust quantities**.
- As a registered user, I want to **submit my order and get confirmation that my order was recieved**.
- As a registered user, I want to **view and edit my submitted orders that are still pending** (under development).

### Staff User (under development)
- As a staff member, I want to **see a list of incoming orders** so I can prepare them efficiently.
- As a staff member, I want to **view an order’s details** so I know what to prepare.
- As a staff member, I want to **update order status** (received → preparing → ready → completed).

### Manager/Admin
- As a manager, I want to **manage menu items and categories** via Django Admin so I can keep the menu current.
- As a manager, I want to **activate/deactivate items** so unavailable dishes don’t appear to customers.

---

## 4) MVP Scope & Non-Goals

**Included**
- Menu browsing
- Logged-in order submission
- Order creation (Order + OrderItems) with price snapshots
- Staff dashboard (under development)
- Basic responsive styling
- Django Admin for menu management
- Order history pages (under development)

**Excluded (Stretch)**
- Menu item customization/options
- Inventory/stock management & dynamic availability
- Nutrition labels
- Payments, emails, real-time updates, reports

---

## 5) Routes (Proposed)
- `/` — Home (CTA to Menu)
- `/about/` — About page
- `/login/` — Login page
- `/signup/` — Signup page
- `/profile/` — User profile
- `/order/menu/` — Categories & items
- `/order/review/` — View/update cart (before submission)
- `/orders/confirmation/<int:order_id>` — Order confirmation page
- `/staff/` — Staff page (under development)


---

## 6) Acceptance Criteria (MVP)
- **Menu:** Only `is_active` items are visible.
- **Review:** Add/remove and quantity updates work; subtotals recalc correctly.
- **Confirm:** Creates `Order` + `OrderItem` records; generates short `confirmation_number`.
- **Auth/Permissions:** Customers can order only as logged-in user. Users can only access their own order history.
- **UX:** Mobile-friendly layout; success messages.

---

## 7) Timeline (7 Days)

**Day 1:** Project setup, base templates, models for Category/MenuItem, Django Admin, seed data.  
**Day 2:** Menu list/detail, add-to-cart, cart page with quantity update & remove, subtotal calc.  
**Day 3:** Submission flow → create Order/OrderItems, confirmation with `order_code`.  
**Day 4:** Staff dashboard (list/detail), status transitions, basic auth/permissions.  
**Day 5:** Styling & UX polish; tax/total computation; validation & messages.  
**Day 6:** Tests (models/services), a couple of view tests; fixtures; README updates.  
**Day 7:** Buffer, QA pass.

---

## 8) Stretch Goals (Post-MVP)
- **Order history** for registered users; simple loyalty points tally.
- **Menu customization** (OptionGroups/Choices with price deltas; OrderItemOption).
- **Nutrition labels** per order item (ingredient macros & snapshot).
- **Inventory** (Ingredient stock ledger + auto-hide items).
- **Real-time** staff updates, email receipts, online payments, reports.

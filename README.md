# Restaurant Web App – Project Plan (MVP Scope)

## 1) Brief Description
A lightweight restaurant web application where customers can **browse the menu**, **add items to a cart**, and **place an order** for **dine-in or pickup** as a **guest or logged-in user**.  
Staff can **view incoming orders** and **update their status** through a basic dashboard.  
**Out of scope for MVP**: order history pages, menu item customization, inventory/stock management, nutrition labels, online payment.

**Tech stack:** Django, PostgreSQL , HTML/CSS.

---

## 2) ERD
![ERD](https://github.com/malekbadarin/Capstone-Project/blob/main/Restaurant%20app%20ERD.png?raw=true)

**Relationships (high-level)**
- MenuCategory **1..N** MenuItem  
- Order **1..N** OrderItem
- OrderItem **1..** MenuItem
- User **0..N** Order (guest orders allowed)
- User **0..N** CustomerProfile (users can be staff)

---

## 3) User Stories

### Guest Customer
- As a guest, I want to **browse the menu by category** so I can quickly see available dishes.
- As a guest, I want to **add/remove items to a cart and change quantities** so I can build my order.
- As a guest, I want to **checkout without creating an account** so I can order quickly.
- As a guest, I want to **choose dine-in or pickup** during checkout so the restaurant prepares accordingly.
- As a guest, I want to **see a clear confirmation with an order code** so I can reference my order at the counter.

### Registered Customer
- As a registered user, I want to **log in** so my basic details auto-fill at checkout.
- As a registered user, I want my **profile (name/phone)** to be saved so checkout is faster next time.
- *(No order history in MVP—future stretch.)*

### Staff User
- As a staff member, I want to **see a list of incoming orders** so I can prepare them efficiently.
- As a staff member, I want to **view an order’s details** so I know what to prepare.
- As a staff member, I want to **update order status** (received → preparing → ready → completed) so front-of-house knows what’s next.

### Manager/Admin
- As a manager, I want to **manage menu items and categories** via Django Admin so I can keep the menu current.
- As a manager, I want to **activate/deactivate items** so unavailable dishes don’t appear to customers.

---

## 4) MVP Scope & Non-Goals

**Included**
- Menu browsing (categories & items)
- Session-based cart (no “saved carts”)
- Guest & logged-in checkout (simple form: contact name, phone, order type)
- Order creation (Order + OrderItems) with price snapshots
- Staff dashboard (list, filter by status, update status)
- Basic responsive styling
- Django Admin for menu management

**Excluded (Stretch)**
- Order history pages
- Menu item customization/options
- Inventory/stock management & dynamic availability
- Nutrition labels
- Payments, emails, real-time updates, reports

---

## 5) Routes (Proposed)
- `/` — Home (CTA to Menu)
- `/menu/` — Categories & items
- `/cart/` — View/update cart
- `/checkout/` — Checkout form (guest or logged-in)
- `/orders/<code>/confirmation/` — Order confirmation page
- `/staff/orders/` — Staff order list (auth required)
- `/staff/orders/<id>/` — Staff order detail + status update (auth required)

---

## 6) Acceptance Criteria (MVP)
- **Menu:** Only `is_active` items are visible; categories render in sort order.
- **Cart:** Add/remove and quantity updates work; subtotals recalc correctly.
- **Checkout:** Creates `Order` + `OrderItem` records; stores `unit_price_snapshot`; generates short `order_code`.
- **Staff:** Orders appear on a dynamic view; status transitions are persisted and visible on order detail.
- **Auth/Permissions:** Staff routes require authenticated staff user; customers can order as guest or logged-in user.
- **UX:** Mobile-friendly layout; clear error/empty states; success flash messages.

---

## 7) Timeline (7 Days)

**Day 1:** Project setup, base templates, models for Category/MenuItem, Django Admin, seed data.  
**Day 2:** Menu list/detail, add-to-cart (session), cart page with quantity update & remove, subtotal calc.  
**Day 3:** Checkout flow → create Order/OrderItems, confirmation with `order_code`.  
**Day 4:** Staff dashboard (list/detail), status transitions, basic auth/permissions.  
**Day 5:** Styling & UX polish; tax/total computation; validation & messages.  
**Day 6:** Tests (models/services), a couple of view tests; fixtures; README updates.  
**Day 7:** Buffer, QA pass, screenshots/GIF for demo.

---

## 8) Stretch Goals (Post-MVP)
- **Order history** for registered users; simple loyalty points tally.
- **Menu customization** (OptionGroups/Choices with price deltas; OrderItemOption).
- **Nutrition labels** per order item (ingredient macros & snapshot).
- **Inventory** (Ingredient stock ledger + auto-hide items).
- **Real-time** staff updates, email receipts, online payments, reports.

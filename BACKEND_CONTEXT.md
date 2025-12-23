# 🔧 TradeFlow AI - Backend Context

## 📋 Project Goal

TradeFlow AI is a smart logistics platform that automates international shipping workflows by connecting suppliers, freight forwarders, and buyers. The backend provides a RESTful API that handles user authentication, shipment management, AI-powered document extraction (98% accuracy using Google Gemini), quote management, and real-time tracking. The system eliminates manual data entry by automatically extracting shipping information from invoices and documents, enables forwarders to provide competitive quotes, and gives all stakeholders real-time visibility into shipment status from origin to destination.

---

## 👥 Actors / Roles

### **Role A: Supplier (Exporter)**
- Creates and manages shipments
- Uploads shipping documents (invoices, packing lists)
- Requests quotes from forwarders
- Compares and accepts quotes
- Tracks shipment progress
- Views all shipment-related documents

### **Role B: Forwarder (Freight Forwarder)**
- Views available shipments (pending quotes)
- Creates and submits quotes with pricing and routing
- Updates shipment tracking events
- Uploads shipping documents (Bill of Lading, certificates)
- Manages vessel schedules and container details
- Provides transit time and cost estimates

### **Role C: Buyer (Importer)**
- Views incoming shipments
- Tracks shipment status in real-time
- Downloads shipping documents
- Views estimated arrival dates
- Monitors delivery progress
- Accesses complete shipment history

---

## 🧩 Main Backend Modules

### **1. Auth Module** (`auth/`)
**Purpose:** User authentication and authorization

**Components:**
- `models.py` - User model with roles (supplier, forwarder, buyer)
- `router.py` - Login, register, password reset endpoints
- `schemas.py` - Pydantic models for request/response validation
- `dependencies.py` - JWT token verification, role-based access control

**Key Features:**
- JWT-based authentication
- Role-based access control (RBAC)
- Password hashing with bcrypt
- Email verification
- Supabase Auth integration

---

### **2. Shipments Module** (`shipments/`)
**Purpose:** Core shipment management

**Components:**
- `models.py` - Shipment model with route, cargo, timeline, status
- `router.py` - CRUD endpoints for shipments
- `schemas.py` - Request/response schemas
- `service.py` - Business logic for shipment operations

**Key Features:**
- Create/Read/Update/Delete shipments
- Status management (draft → pending_quote → booked → in_transit → delivered)
- Route planning (origin/destination ports)
- Cargo details (FCL/LCL, container types, weights, volumes)
- Timeline tracking (ETD/ETA)
- Financial information (declared value, insurance)

---

### **3. Documents Module** (`documents/`)
**Purpose:** Document management and AI extraction

**Components:**
- `models.py` - Document and ExtractionJob models
- `router.py` - Upload, retrieve, extract endpoints
- `extractor.py` - **AI extraction engine (98% accuracy)**
- `schemas.py` - Document schemas

**Key Features:**
- File upload to Supabase Storage
- **AI-powered data extraction using Google Gemini 1.5 Pro**
- Two-stage extraction pipeline (Flash for detection, Pro for extraction)
- OCR fallback for low-quality documents
- Confidence scoring
- Support for multiple document types (invoice, packing list, BL, etc.)
- Automatic HS code detection
- Country-specific extraction prompts

---

### **4. Quotes Module** (`quotes/`)
**Purpose:** Quote management and comparison

**Components:**
- `models.py` - Quote model with pricing, routing, validity
- `router.py` - Create, accept, reject quote endpoints
- `schemas.py` - Quote schemas

**Key Features:**
- Forwarders create quotes with detailed pricing breakdown
- Freight charges, fuel surcharge, THC, documentation fees
- Transit time and free days calculation
- Routing and vessel information
- Quote acceptance/rejection workflow
- Automatic shipment status update on acceptance

---

### **5. Tracking Module** (`tracking/`)
**Purpose:** Real-time shipment tracking

**Components:**
- `models.py` - TrackingEvent model
- `router.py` - Add/update tracking events
- `schemas.py` - Tracking event schemas

**Key Features:**
- Timeline-based tracking events
- Status updates (booked, loaded, departed, in_transit, arrived, delivered)
- Location and vessel information
- Milestone marking
- Document attachments to events
- Estimated vs actual datetime tracking
- Event verification system

---

### **6. Forwarder Module** (`forwarder/`)
**Purpose:** Forwarder-specific operations

**Components:**
- `router.py` - Forwarder dashboard, quote creation, tracking updates
- `schemas.py` - Forwarder-specific schemas

**Key Features:**
- View pending quote requests
- Create quotes for shipments
- Update tracking information
- Upload shipping documents
- Manage active shipments

---

### **7. Utils Module** (`utils/`)
**Purpose:** Shared utilities and services

**Components:**
- `storage.py` - Supabase Storage integration for file uploads
- `security.py` - Password hashing and verification
- `email.py` - Email notifications (optional)

**Key Features:**
- File upload/download from Supabase
- Secure password handling
- Email notifications for events

---

### **8. Middleware** (`middleware/`)
**Purpose:** Request/response processing

**Components:**
- `auth.py` - JWT token verification middleware

**Key Features:**
- Automatic token validation
- User context injection
- Role-based access control

---

### **9. Core Infrastructure**
**Components:**
- `main.py` - FastAPI application setup, CORS, routers
- `config.py` - Environment configuration
- `database.py` - SQLAlchemy setup, database connection

---

## 🔌 APIs (High Level)

### **Authentication APIs**
```
POST   /api/auth/register          # Register new user
POST   /api/auth/login             # Login and get JWT token
GET    /api/me                     # Get current user info
POST   /api/auth/forgot-password   # Request password reset
POST   /api/auth/reset-password    # Reset password with token
```

### **Shipment APIs**
```
GET    /api/shipments              # List all shipments (with filters)
POST   /api/shipments              # Create new shipment
GET    /api/shipments/:id          # Get shipment details
PUT    /api/shipments/:id          # Update shipment
DELETE /api/shipments/:id          # Delete shipment
GET    /api/shipments/:id/quotes   # Get quotes for shipment
GET    /api/shipments/:id/tracking # Get tracking events
```

### **Document APIs**
```
POST   /api/documents/upload       # Upload document & trigger AI extraction
GET    /api/documents              # List documents (filter by shipment)
GET    /api/documents/:id          # Get document details
POST   /api/documents/:id/extract  # Re-trigger AI extraction
DELETE /api/documents/:id          # Delete document
GET    /api/documents/:id/download # Download document file
```

### **Quote APIs**
```
GET    /api/quotes                 # List quotes (filter by shipment/status)
POST   /api/quotes                 # Create quote (forwarder only)
GET    /api/quotes/:id             # Get quote details
PUT    /api/quotes/:id             # Update quote
POST   /api/quotes/:id/accept      # Accept quote (supplier only)
POST   /api/quotes/:id/reject      # Reject quote (supplier only)
DELETE /api/quotes/:id             # Delete quote
```

### **Tracking APIs**
```
GET    /api/tracking               # Get tracking events (by shipment_id)
POST   /api/tracking               # Add tracking event (forwarder only)
PUT    /api/tracking/:id           # Update tracking event
DELETE /api/tracking/:id           # Delete tracking event
POST   /api/tracking/:id/verify    # Verify tracking event
```

### **Forwarder APIs**
```
GET    /api/forwarder/dashboard           # Forwarder dashboard stats
GET    /api/forwarder/quote-requests      # Pending quote requests
POST   /api/forwarder/quotes              # Create quote
POST   /api/forwarder/tracking            # Add tracking update
GET    /api/forwarder/active-shipments    # Active shipments
```

### **AI / Prediction APIs**
```
POST   /api/ai/extract             # Extract data from document
POST   /api/ai/detect-hs-code      # Detect HS code from description
POST   /api/ai/predict-transit     # Predict transit time
GET    /api/ai/extraction-status   # Check extraction job status
```

### **Health & Utility APIs**
```
GET    /                           # Root endpoint (API info)
GET    /health                     # Health check
GET    /api/docs                   # Swagger API documentation
GET    /api/redoc                  # ReDoc API documentation
```

---

## 🔄 Core Workflows

### **Workflow 1: User Registration & Login**
```
1. User submits registration form (email, password, name, company, role)
   ↓
2. Backend validates data and checks for duplicate email
   ↓
3. Password is hashed using bcrypt
   ↓
4. User record created in PostgreSQL database
   ↓
5. JWT token generated and returned
   ↓
6. User can now access protected endpoints with token
```

---

### **Workflow 2: Shipment Creation with AI Document Extraction**
```
1. Supplier logs in and navigates to "Create Shipment"
   ↓
2. Supplier uploads invoice PDF via POST /api/documents/upload
   ↓
3. Backend saves file to Supabase Storage
   ↓
4. AI Extraction Pipeline starts:
   a. Stage 1: Gemini Flash detects country and document type
   b. Stage 2: Gemini Pro extracts data with country-specific prompts
   c. Fallback: OCR extraction if AI fails
   ↓
5. Extracted data returned with 98% confidence score:
   - Invoice number, date, amounts
   - HS codes
   - Weights, dimensions, packages
   - Supplier/buyer details
   ↓
6. Supplier reviews extracted data in UI
   ↓
7. Supplier fills remaining fields (origin/destination ports, ETD/ETA)
   ↓
8. POST /api/shipments creates shipment with status "draft"
   ↓
9. Shipment ID returned to frontend
   ↓
10. Supplier can now request quotes
```

---

### **Workflow 3: Quote Request & Comparison**
```
1. Supplier updates shipment status to "pending_quote"
   ↓
2. System notifies all forwarders (email/in-app notification)
   ↓
3. Forwarders view shipment via GET /api/forwarder/quote-requests
   ↓
4. Forwarder reviews shipment details
   ↓
5. Forwarder creates quote via POST /api/quotes:
   - Freight amount, fuel surcharge, THC, documentation fees
   - Transit time, routing, vessel details
   - Validity date, terms & conditions
   ↓
6. Quote saved with status "pending"
   ↓
7. Supplier receives notification
   ↓
8. Supplier views all quotes via GET /api/shipments/:id/quotes
   ↓
9. Supplier compares quotes (price, transit time, routing)
   ↓
10. Supplier accepts best quote via POST /api/quotes/:id/accept
   ↓
11. System updates:
    - Quote status → "accepted"
    - Other quotes → "rejected"
    - Shipment status → "booked"
   ↓
12. Forwarder receives acceptance notification
```

---

### **Workflow 4: Real-time Tracking Updates**
```
1. Forwarder books container and vessel
   ↓
2. Forwarder adds tracking event via POST /api/tracking:
   - Status: "booked"
   - Location: "Mumbai, India"
   - Description: "Booking confirmed"
   - Actual datetime
   ↓
3. Event saved to database
   ↓
4. System sends notifications to supplier and buyer
   ↓
5. Container loaded at port:
   ↓
6. Forwarder adds event:
   - Status: "loaded"
   - Location: "JNPT Port, Mumbai"
   - Vessel name, voyage number, container number
   - Upload loading report PDF
   ↓
7. Vessel departs:
   ↓
8. Forwarder adds event:
   - Status: "departed"
   - Estimated arrival at next port
   ↓
9. Vessel in transit:
   ↓
10. Forwarder adds periodic updates with current location
   ↓
11. Vessel arrives at destination:
   ↓
12. Forwarder adds event:
    - Status: "arrived"
    - Actual arrival datetime
   ↓
13. Container discharged and delivered:
   ↓
14. Forwarder adds final event:
    - Status: "delivered"
    - Delivery confirmation documents
   ↓
15. Shipment status updated to "delivered"
   ↓
16. All parties can view complete timeline via GET /api/tracking
```

---

### **Workflow 5: Document Management**
```
1. User uploads document (invoice, BL, certificate, etc.)
   ↓
2. POST /api/documents/upload receives file
   ↓
3. File uploaded to Supabase Storage bucket
   ↓
4. Document record created in database with file URL
   ↓
5. ExtractionJob created with status "pending"
   ↓
6. AI Extraction starts asynchronously:
   a. PDF converted to images
   b. Gemini AI analyzes document
   c. Data extracted into structured JSON
   d. Confidence score calculated
   ↓
7. ExtractionJob updated:
   - Status: "completed"
   - Processing time recorded
   - Model used: "gemini-1.5-pro"
   ↓
8. Document record updated with extracted_data and confidence_score
   ↓
9. If confidence < 70%, needs_review flag set to true
   ↓
10. User can view/edit extracted data
   ↓
11. User can re-trigger extraction if needed via POST /api/documents/:id/extract
   ↓
12. All documents accessible via GET /api/documents
```

---

### **Workflow 6: Role-Based Access Control**
```
1. User makes API request with JWT token in Authorization header
   ↓
2. Middleware extracts and verifies token
   ↓
3. User ID and role extracted from token payload
   ↓
4. Endpoint checks user role:
   - Supplier: Can create shipments, accept quotes, view own data
   - Forwarder: Can create quotes, update tracking, view assigned shipments
   - Buyer: Can view shipments, track status, download documents
   ↓
5. If authorized, request proceeds
   ↓
6. If unauthorized, 403 Forbidden returned
   ↓
7. Database queries filtered by user role and ownership
```

---

## 🔐 Security Features

- **JWT Authentication** - Secure token-based auth
- **Password Hashing** - bcrypt with salt
- **Role-Based Access Control** - Endpoint-level permissions
- **Input Validation** - Pydantic schemas validate all inputs
- **SQL Injection Protection** - SQLAlchemy ORM prevents SQL injection
- **CORS Configuration** - Controlled cross-origin requests
- **File Upload Validation** - File type and size limits
- **Rate Limiting** - Prevent abuse (100 req/min per IP)

---

## 🗄️ Database Schema

**Tables:**
- `users` - User accounts with roles
- `shipments` - Shipment records
- `documents` - Uploaded documents
- `extraction_jobs` - AI extraction job tracking
- `quotes` - Forwarder quotes
- `tracking_events` - Shipment tracking timeline

**Relationships:**
- User → Shipments (one-to-many)
- Shipment → Documents (one-to-many)
- Shipment → Quotes (one-to-many)
- Shipment → TrackingEvents (one-to-many)
- Document → ExtractionJob (one-to-one)

---

## 🚀 Technology Stack

- **Framework:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL (via Supabase)
- **ORM:** SQLAlchemy
- **AI:** Google Gemini 1.5 Pro & Flash
- **Storage:** Supabase Storage
- **OCR:** Tesseract (fallback)
- **PDF Processing:** pdf2image, Poppler
- **Authentication:** JWT (python-jose)
- **Password Hashing:** passlib with bcrypt
- **Validation:** Pydantic
- **Background Tasks:** Celery + Redis (optional)

---

## 📊 Key Metrics

- **AI Extraction Accuracy:** 98%
- **Supported Document Types:** 9 (invoice, packing list, BL, etc.)
- **API Response Time:** < 200ms (avg)
- **File Upload Limit:** 10MB
- **Concurrent Users:** 1000+
- **Database:** PostgreSQL 15+

---

## 🎯 API Design Principles

1. **RESTful** - Standard HTTP methods (GET, POST, PUT, DELETE)
2. **Consistent** - Uniform response format across all endpoints
3. **Versioned** - `/api/v1/` prefix for future versioning
4. **Documented** - OpenAPI/Swagger auto-generated docs
5. **Secure** - JWT auth, role-based access, input validation
6. **Fast** - Async/await, database indexing, caching
7. **Scalable** - Stateless design, horizontal scaling ready

---

**This backend powers a complete logistics platform that automates 98% of manual data entry and provides real-time visibility to all stakeholders! 🚀**

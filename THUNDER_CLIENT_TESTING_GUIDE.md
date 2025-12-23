# 🌩️ Thunder Client Testing Guide - TradeFlow AI

## 📋 Table of Contents
1. [Setup Instructions](#setup-instructions)
2. [Testing Workflow](#testing-workflow)
3. [API Endpoints Overview](#api-endpoints-overview)
4. [Common Test Scenarios](#common-test-scenarios)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup Instructions

### Step 1: Install Thunder Client
1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Thunder Client"
4. Click Install

### Step 2: Import the Collection
1. Open Thunder Client in VS Code (click the Thunder Client icon in the sidebar)
2. Click on "Collections" tab
3. Click the "Menu" (three dots) → "Import"
4. Select the file: `thunder-client-collection.json`
5. The collection "TradeFlow AI - Complete API Collection" will be imported

### Step 3: Start Your Backend Server
Before testing, make sure your backend is running:

#### Option A: Using Docker (Recommended)
```bash
cd "c:\Users\sridh\OneDrive\Desktop\Track Eye\trade-flow-ai"
docker compose up -d
```

#### Option B: Using Python Directly
```bash
cd "c:\Users\sridh\OneDrive\Desktop\Track Eye\trade-flow-ai"
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Verify Server is Running
Open your browser and navigate to:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/

---

## 🔄 Testing Workflow

### Complete Testing Flow (Recommended Order)

#### 1️⃣ **Authentication Flow**
Test these in order:

1. **Register User (Supplier)**
   - Creates a supplier account
   - Returns `access_token` (automatically saved to environment)
   
2. **Register User (Forwarder)**
   - Creates a forwarder account for quote testing
   
3. **Login**
   - Login with supplier credentials
   - Token is auto-saved to `{{access_token}}`
   
4. **Get Current User**
   - Verify authentication is working
   - Check user details

#### 2️⃣ **Shipments Flow**

1. **Create Shipment**
   - Creates a new shipment
   - `shipment_id` is auto-saved to environment
   
2. **List All Shipments**
   - View all shipments (with pagination)
   
3. **Get Shipment by ID**
   - View specific shipment details
   - Uses `{{shipment_id}}` from environment
   
4. **Update Shipment**
   - Modify shipment status or details
   
5. **Delete Shipment** (Optional)
   - Remove a shipment

#### 3️⃣ **Documents Flow**

1. **Upload Document**
   - Upload invoice/packing list/etc.
   - Select a PDF/image file
   - `document_id` is auto-saved
   - AI extraction happens automatically
   
2. **List Documents**
   - View all documents for a shipment
   
3. **Get Document by ID**
   - View document details and extracted data
   
4. **Trigger Re-extraction**
   - Re-run AI extraction if needed

#### 4️⃣ **Quotes Flow**

**Note:** Login as forwarder first to create quotes!

1. **Create Quote (Forwarder)**
   - Forwarder creates a quote for shipment
   - `quote_id` is auto-saved
   
2. **List Quotes**
   - View all quotes for a shipment
   
3. **Get Quote by ID**
   - View specific quote details
   
4. **Accept Quote** (Supplier)
   - Login as supplier
   - Accept the quote
   - Shipment status changes to "booked"
   
5. **Reject Quote** (Optional)
   - Reject a quote with reason

#### 5️⃣ **Tracking Flow**

1. **Add Tracking Event**
   - Add shipment status updates
   - Examples: "loaded", "departed", "in_transit", "arrived"
   
2. **List Tracking Events**
   - View shipment journey timeline

#### 6️⃣ **Carriers API Flow**

1. **Search Carrier Schedules**
   - Find available sailing schedules
   
2. **Get Rate Quote**
   - Get freight rate quotes
   
3. **AI Rate Prediction**
   - Get AI-predicted future rates
   
4. **Create Carrier Booking**
   - Book with a carrier
   - `booking_id` is auto-saved
   
5. **Track Carrier Shipment**
   - Get real-time tracking from carrier

#### 7️⃣ **Customs (ICEGATE) Flow**

1. **ICEGATE - Authenticate**
   - Login to ICEGATE system
   - `icegate_token` is auto-saved
   
2. **ICEGATE - Calculate Duty**
   - Calculate import/export duties
   
3. **ICEGATE - File Bill of Entry**
   - Submit customs declaration
   - `bill_id` is auto-saved
   
4. **ICEGATE - Upload Documents**
   - Upload supporting documents
   
5. **ICEGATE - Get Bill Status**
   - Check customs clearance status

---

## 📊 API Endpoints Overview

### 🔐 Authentication Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get token |
| GET | `/api/me` | Get current user info |

### 📦 Shipments Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/shipments` | List all shipments |
| POST | `/api/shipments` | Create new shipment |
| GET | `/api/shipments/{id}` | Get shipment details |
| PUT | `/api/shipments/{id}` | Update shipment |
| DELETE | `/api/shipments/{id}` | Delete shipment |

### 📄 Documents Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/documents/upload` | Upload document with AI extraction |
| GET | `/api/documents` | List documents |
| GET | `/api/documents/{id}` | Get document details |
| POST | `/api/documents/{id}/extract` | Re-run AI extraction |
| DELETE | `/api/documents/{id}` | Delete document |

### 💰 Quotes Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/quotes` | List quotes |
| POST | `/api/quotes` | Create quote (forwarder) |
| GET | `/api/quotes/{id}` | Get quote details |
| POST | `/api/quotes/{id}/accept` | Accept quote (supplier) |
| POST | `/api/quotes/{id}/reject` | Reject quote |

### 📍 Tracking Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tracking` | List tracking events |
| POST | `/api/tracking` | Add tracking event |
| PUT | `/api/tracking/{id}` | Update tracking event |
| DELETE | `/api/tracking/{id}` | Delete tracking event |

### 🚢 Carriers API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/carriers/schedules/search` | Search sailing schedules |
| POST | `/api/carriers/rates/quote` | Get rate quote |
| POST | `/api/carriers/rates/predict` | AI rate prediction |
| POST | `/api/carriers/bookings` | Create booking |
| GET | `/api/carriers/tracking/{id}` | Track shipment |

### 🛃 Customs (ICEGATE) Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/customs/icegate/authenticate` | ICEGATE login |
| POST | `/api/customs/icegate/bills` | File bill of entry |
| GET | `/api/customs/icegate/bills/{id}/status` | Get bill status |
| POST | `/api/customs/icegate/duty/calculate` | Calculate duty |
| POST | `/api/customs/icegate/bills/{id}/documents` | Upload documents |

---

## 🎯 Common Test Scenarios

### Scenario 1: Complete Shipment Lifecycle

```
1. Register as Supplier → Login
2. Create Shipment
3. Upload Invoice Document (AI extracts data)
4. Register as Forwarder → Login
5. Create Quote for Shipment
6. Login as Supplier
7. Accept Quote
8. Login as Forwarder
9. Add Tracking Events (booked → loaded → departed → in_transit → arrived)
10. Check Shipment Status
```

### Scenario 2: Carrier Integration

```
1. Login as Supplier
2. Search Carrier Schedules (Mumbai → LA)
3. Get Rate Quote
4. Get AI Rate Prediction
5. Create Carrier Booking
6. Track Carrier Shipment
```

### Scenario 3: Customs Clearance

```
1. Login as Supplier
2. Create Shipment
3. ICEGATE Authenticate
4. Calculate Duty
5. File Bill of Entry
6. Upload Supporting Documents
7. Check Bill Status
```

---

## 🔧 Environment Variables

The collection uses these environment variables (auto-populated):

| Variable | Description | Auto-saved? |
|----------|-------------|-------------|
| `base_url` | API base URL | Manual |
| `access_token` | JWT auth token | ✅ Yes |
| `shipment_id` | Current shipment ID | ✅ Yes |
| `document_id` | Current document ID | ✅ Yes |
| `quote_id` | Current quote ID | ✅ Yes |
| `tracking_event_id` | Current event ID | ✅ Yes |
| `booking_id` | Carrier booking ID | ✅ Yes |
| `bill_id` | Customs bill ID | ✅ Yes |
| `icegate_token` | ICEGATE auth token | ✅ Yes |

### How to View/Edit Environment Variables:
1. Click "Env" tab in Thunder Client
2. Select "Local Development"
3. View or manually edit variables

---

## 🐛 Troubleshooting

### Issue: "Connection Refused" or "Network Error"
**Solution:**
- Ensure backend server is running on port 8000
- Check: http://localhost:8000/docs
- Verify Docker containers are up: `docker compose ps`

### Issue: "401 Unauthorized"
**Solution:**
- Run the "Login" request first
- Check if `access_token` is saved in environment
- Token might be expired - login again

### Issue: "404 Not Found"
**Solution:**
- Check if the endpoint URL is correct
- Ensure you're using the right HTTP method (GET/POST/PUT/DELETE)
- Verify the resource ID exists (e.g., `shipment_id`)

### Issue: "422 Validation Error"
**Solution:**
- Check request body format
- Ensure all required fields are provided
- Verify data types (string, number, boolean)

### Issue: "500 Internal Server Error"
**Solution:**
- Check backend logs: `docker compose logs app`
- Database might not be initialized
- Check environment variables in `.env` file

### Issue: Document Upload Fails
**Solution:**
- Ensure file size is < 10MB
- Supported formats: PDF, JPG, PNG
- Check if `shipment_id` exists
- Verify Supabase storage is configured

### Issue: ICEGATE Endpoints Return Errors
**Solution:**
- These are simulated endpoints
- Check if you have valid ICEGATE credentials
- Ensure ICEGATE service is configured in `.env`

---

## 📝 Testing Checklist

Use this checklist to ensure all APIs are working:

### Authentication ✅
- [ ] Register Supplier
- [ ] Register Forwarder
- [ ] Login
- [ ] Get Current User

### Shipments ✅
- [ ] Create Shipment
- [ ] List Shipments
- [ ] Get Shipment by ID
- [ ] Update Shipment
- [ ] Delete Shipment

### Documents ✅
- [ ] Upload Document
- [ ] List Documents
- [ ] Get Document Details
- [ ] Trigger Re-extraction

### Quotes ✅
- [ ] Create Quote (Forwarder)
- [ ] List Quotes
- [ ] Get Quote by ID
- [ ] Accept Quote (Supplier)
- [ ] Reject Quote

### Tracking ✅
- [ ] Add Tracking Event
- [ ] List Tracking Events

### Carriers API ✅
- [ ] Search Schedules
- [ ] Get Rate Quote
- [ ] AI Rate Prediction
- [ ] Create Booking
- [ ] Track Shipment

### Customs (ICEGATE) ✅
- [ ] Authenticate
- [ ] Calculate Duty
- [ ] File Bill of Entry
- [ ] Upload Documents
- [ ] Get Bill Status

---

## 🎨 Tips for Effective Testing

1. **Use the Recommended Order**: Follow the testing workflow above for best results

2. **Check Response Status Codes**:
   - 200: Success
   - 201: Created
   - 204: No Content (Delete)
   - 400: Bad Request
   - 401: Unauthorized
   - 404: Not Found
   - 422: Validation Error
   - 500: Server Error

3. **Monitor Environment Variables**: Watch the "Env" tab to see auto-saved IDs

4. **Use Tests Tab**: Thunder Client can run assertions on responses

5. **Save Responses**: Right-click response → "Save Response" for documentation

6. **Collection Runner**: Use "Run All" to test entire collection at once

7. **Export Results**: Export test results for reporting

---

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc
- **Backend Context**: See `BACKEND_CONTEXT.md`
- **API Reference**: See `API_REFERENCE.md`
- **Docker Guide**: See `DOCKER_GUIDE.md`

---

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review backend logs: `docker compose logs -f app`
3. Check database connection: `docker compose ps postgres`
4. Verify environment variables in `.env` file
5. Ensure all services are healthy: `docker compose ps`

---

**Happy Testing! 🚀**

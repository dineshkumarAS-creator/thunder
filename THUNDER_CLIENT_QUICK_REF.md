# 🌩️ Thunder Client - Quick Reference Card

## 🚀 Quick Start (3 Steps)

### 1. Import Collection
```
Thunder Client → Collections → Menu (⋮) → Import → Select: thunder-client-collection.json
```

### 2. Start Backend
```bash
cd "c:\Users\sridh\OneDrive\Desktop\Track Eye\trade-flow-ai"
docker compose up -d
# OR
uvicorn main:app --reload
```

### 3. Test APIs
```
Open Thunder Client → Select Collection → Start Testing!
```

---

## 📋 Essential Test Flow

### Quick 5-Minute Test
```
1. 🔐 Auth → Register User (Supplier)
2. 🔐 Auth → Login
3. 📦 Shipments → Create Shipment
4. 📦 Shipments → List All Shipments
5. ✅ Done! Your API is working!
```

### Complete Test (15 minutes)
```
1. Register Supplier & Forwarder
2. Login as Supplier
3. Create Shipment
4. Upload Document
5. Login as Forwarder
6. Create Quote
7. Login as Supplier
8. Accept Quote
9. Add Tracking Events
10. Check Everything Works!
```

---

## 🔑 Environment Variables (Auto-saved)

| Variable | Where it's saved |
|----------|------------------|
| `access_token` | After Login |
| `shipment_id` | After Create Shipment |
| `document_id` | After Upload Document |
| `quote_id` | After Create Quote |
| `booking_id` | After Create Booking |
| `bill_id` | After File Bill of Entry |

**View/Edit:** Thunder Client → Env Tab → Local Development

---

## 🎯 Most Used Endpoints

### Authentication
```
POST /api/auth/register    → Register
POST /api/auth/login       → Login (saves token)
GET  /api/me               → Get user info
```

### Shipments
```
GET  /api/shipments        → List all
POST /api/shipments        → Create (saves ID)
GET  /api/shipments/{id}   → Get details
PUT  /api/shipments/{id}   → Update
```

### Documents
```
POST /api/documents/upload → Upload (saves ID)
GET  /api/documents        → List all
```

### Quotes
```
POST /api/quotes           → Create (forwarder)
POST /api/quotes/{id}/accept → Accept (supplier)
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| ❌ Connection refused | Start backend: `docker compose up -d` |
| ❌ 401 Unauthorized | Run "Login" request first |
| ❌ 404 Not Found | Check if resource ID exists |
| ❌ 422 Validation Error | Check request body format |
| ❌ 500 Server Error | Check logs: `docker compose logs app` |

---

## 📊 Response Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | ✅ Success | All good! |
| 201 | ✅ Created | Resource created |
| 204 | ✅ No Content | Delete successful |
| 400 | ❌ Bad Request | Check request format |
| 401 | ❌ Unauthorized | Login first |
| 404 | ❌ Not Found | Check resource ID |
| 422 | ❌ Validation Error | Fix request body |
| 500 | ❌ Server Error | Check backend logs |

---

## 🔗 Useful Links

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/
- **Full Guide:** `THUNDER_CLIENT_TESTING_GUIDE.md`
- **API Reference:** `API_REFERENCE.md`

---

## 💡 Pro Tips

1. **Always login first** before testing protected endpoints
2. **Check Env tab** to see auto-saved IDs
3. **Use Collection Runner** to test all at once
4. **Monitor backend logs** for debugging
5. **Save responses** for documentation

---

## 📁 Collection Structure

```
TradeFlow AI Collection
├── 🔐 Authentication (4 requests)
├── 📦 Shipments (5 requests)
├── 📄 Documents (4 requests)
├── 💰 Quotes (5 requests)
├── 📍 Tracking (2 requests)
├── 🚢 Carriers API (5 requests)
└── 🛃 Customs/ICEGATE (5 requests)

Total: 30+ API endpoints ready to test!
```

---

**Need detailed help?** See `THUNDER_CLIENT_TESTING_GUIDE.md`

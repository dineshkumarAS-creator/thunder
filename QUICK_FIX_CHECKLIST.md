# ✅ Quick Fix Checklist - TradeFlow AI

## 🔴 CRITICAL FIXES (Must Do First)

### 1. Create `utils/security.py`
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
```

### 2. Create `quotes/` Module
- [ ] `quotes/__init__.py` (empty)
- [ ] `quotes/models.py` (Quote model)
- [ ] `quotes/router.py` (API endpoints)
- [ ] `quotes/schemas.py` (Pydantic schemas)

### 3. Create `tracking/` Module
- [ ] `tracking/__init__.py` (empty)
- [ ] `tracking/models.py` (TrackingEvent model)
- [ ] `tracking/router.py` (API endpoints)
- [ ] `tracking/schemas.py` (Pydantic schemas)

### 4. Create `documents/router.py`
- [ ] Document upload endpoint
- [ ] AI extraction trigger
- [ ] Document retrieval

### 5. Create `shipments/service.py`
- [ ] ShipmentService class
- [ ] CRUD operations

### 6. Create `forwarder/schemas.py`
- [ ] QuoteCreate schema
- [ ] QuoteResponse schema
- [ ] TrackingUpdate schema

### 7. Create `.env` File
```env
SUPABASE_URL=your-url
SUPABASE_KEY=your-key
DATABASE_URL=your-db-url
JWT_SECRET_KEY=your-secret
GEMINI_API_KEY=your-gemini-key
```

## 🟡 IMPORTANT FIXES (Do Next)

### 8. Fix Windows Compatibility
**File:** `forwarder/router.py` line 222

**Change from:**
```python
temp_path = f"/tmp/{uuid.uuid4()}_{file.filename}"
```

**Change to:**
```python
import tempfile
temp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}_{file.filename}")
```

### 9. Add Missing Import
**File:** `forwarder/router.py` top of file

**Add:**
```python
import uuid
```

## 🟢 OPTIONAL IMPROVEMENTS

### 10. Add __init__.py Files
- [ ] `auth/__init__.py`
- [ ] `documents/__init__.py`
- [ ] `shipments/__init__.py`
- [ ] `forwarder/__init__.py`
- [ ] `middleware/__init__.py`
- [ ] `utils/__init__.py`

### 11. Install Prerequisites (Windows)
```powershell
# Install Tesseract OCR
choco install tesseract

# Install Poppler
choco install poppler

# Or download manually and add to PATH
```

## 📊 Progress Tracker

- [ ] **Step 1-7:** Critical fixes (0/7 complete)
- [ ] **Step 8-9:** Important fixes (0/2 complete)
- [ ] **Step 10-11:** Optional improvements (0/2 complete)

**Total Progress:** 0/11 (0%)

---

## 🚀 Quick Start After Fixes

```powershell
# 1. Install dependencies
python -m pip install -r requirements.txt

# 2. Run the application
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 3. Open API docs
# http://localhost:8000/api/docs
```

---

**Status:** ⚠️ **NOT READY TO RUN**  
**After completing items 1-7:** ✅ **READY TO RUN**

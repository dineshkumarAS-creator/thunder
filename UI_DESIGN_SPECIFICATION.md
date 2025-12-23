# 🎨 TradeFlow AI - Complete UI Design Specification

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [How the System Works](#how-the-system-works)
3. [User Roles & Workflows](#user-roles--workflows)
4. [UI Components Needed](#ui-components-needed)
5. [Page-by-Page Breakdown](#page-by-page-breakdown)
6. [Design System](#design-system)
7. [Technical Stack](#technical-stack)
8. [API Integration](#api-integration)

---

## 🚀 Project Overview

**TradeFlow AI** is a smart logistics platform that uses AI to automate international shipping workflows. It connects three types of users:
- **Suppliers** (Exporters who ship goods)
- **Forwarders** (Freight forwarders who provide shipping quotes)
- **Buyers** (Importers who receive goods)

### Key Features
- ✅ **98% Accurate Document Extraction** - AI automatically reads invoices, packing lists, and shipping documents
- ✅ **Real-time Shipment Tracking** - Track containers from origin to destination
- ✅ **Automated Quote Management** - Get and compare quotes from multiple forwarders
- ✅ **Multi-role Dashboard** - Different views for suppliers, forwarders, and buyers
- ✅ **Document Management** - Upload, extract, and manage shipping documents

---

## 🔄 How the System Works

### Complete User Journey

#### **1. Supplier Creates Shipment**
```
Supplier logs in → Creates new shipment → Uploads invoice/packing list 
→ AI extracts data (HS code, weight, dimensions, etc.) 
→ System auto-fills shipment form → Supplier reviews and submits
→ Shipment goes to "Pending Quote" status
```

#### **2. Forwarders Provide Quotes**
```
Forwarder logs in → Sees available shipments (pending quotes)
→ Views shipment details → Creates quote (freight cost, transit time, routing)
→ Submits quote → Supplier receives notification
```

#### **3. Supplier Accepts Quote**
```
Supplier reviews multiple quotes → Compares prices and transit times
→ Accepts best quote → Shipment status changes to "Booked"
→ Forwarder receives confirmation
```

#### **4. Tracking Updates**
```
Forwarder updates tracking events (Booked → In Transit → Arrived → Delivered)
→ All parties can see real-time status
→ Documents (BL, certificates) attached to tracking events
→ Automated notifications sent
```

### Data Flow Architecture

```
┌─────────────────┐
│   User Upload   │
│   (PDF/Image)   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  Gemini AI Extraction   │
│  (98% Accuracy)         │
│  - Invoice data         │
│  - HS codes             │
│  - Weights/dimensions   │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Database Storage       │
│  (PostgreSQL)           │
│  - Shipments            │
│  - Documents            │
│  - Quotes               │
│  - Tracking Events      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│  Real-time Dashboard    │
│  (React UI)             │
└─────────────────────────┘
```

---

## 👥 User Roles & Workflows

### **Role 1: Supplier (Exporter)**

**Main Tasks:**
1. Create new shipments
2. Upload shipping documents
3. Review AI-extracted data
4. Request quotes from forwarders
5. Compare and accept quotes
6. Track shipment progress
7. View shipment history

**Dashboard Widgets:**
- Active shipments count
- Pending quotes count
- In-transit shipments
- Recent activity feed
- Quick actions (New Shipment, Upload Document)

---

### **Role 2: Forwarder (Freight Forwarder)**

**Main Tasks:**
1. View available shipments (pending quotes)
2. Create and submit quotes
3. Update tracking information
4. Upload shipping documents (BL, certificates)
5. Manage vessel schedules
6. View quote history (accepted/rejected)

**Dashboard Widgets:**
- Pending quote requests
- Active shipments
- Quote acceptance rate
- Revenue this month
- Recent shipments

---

### **Role 3: Buyer (Importer)**

**Main Tasks:**
1. View incoming shipments
2. Track shipment status
3. Download shipping documents
4. View estimated arrival dates
5. Communicate with supplier/forwarder

**Dashboard Widgets:**
- Incoming shipments
- In-transit count
- Expected arrivals this week
- Recent deliveries
- Document library

---

## 🧩 UI Components Needed

### **1. Authentication Components**

#### Login Page
- Email/password fields
- "Remember me" checkbox
- "Forgot password" link
- Role selector (Supplier/Forwarder/Buyer)
- Social login options (optional)

#### Registration Page
- Multi-step form:
  - **Step 1:** Basic info (Name, Email, Password)
  - **Step 2:** Company details (Company name, GSTIN, Country)
  - **Step 3:** Role selection
  - **Step 4:** Verification (Email OTP)

---

### **2. Dashboard Components**

#### Top Navigation Bar
- Logo
- Search bar (global search for shipments)
- Notifications bell (with badge count)
- User profile dropdown
  - Profile settings
  - Company settings
  - Logout

#### Sidebar Navigation
**Supplier Menu:**
- 📊 Dashboard
- 📦 Shipments
  - All Shipments
  - Pending Quotes
  - In Transit
  - Delivered
- 📄 Documents
- 💰 Quotes
- ⚙️ Settings

**Forwarder Menu:**
- 📊 Dashboard
- 📋 Quote Requests
- 📦 Active Shipments
- 🚢 Tracking Updates
- 📄 Documents
- ⚙️ Settings

**Buyer Menu:**
- 📊 Dashboard
- 📦 Incoming Shipments
- 📍 Track Shipments
- 📄 Documents
- ⚙️ Settings

#### Dashboard Cards (Widgets)
- **Stat Card** - Shows count with icon and trend
- **Activity Feed** - Recent actions timeline
- **Quick Actions** - Large buttons for common tasks
- **Chart Widget** - Line/bar charts for analytics
- **Table Widget** - Recent items in table format

---

### **3. Shipment Management Components**

#### Shipment List Page
**Features:**
- Data table with columns:
  - Shipment Number
  - Origin → Destination
  - Status badge
  - ETD/ETA dates
  - Cargo type
  - Actions (View, Edit, Delete)
- Filters:
  - Status filter (Draft, Pending Quote, Booked, etc.)
  - Date range picker
  - Port filter
  - Cargo type filter
- Search bar
- Pagination
- Bulk actions
- Export to Excel/CSV

#### Create/Edit Shipment Form
**Multi-step wizard:**

**Step 1: Basic Information**
- Shipment number (auto-generated)
- Origin port (searchable dropdown)
- Destination port (searchable dropdown)
- Incoterm (FOB, CIF, CFR, etc.)
- Cargo type (FCL, LCL, Air)
- Container type (20GP, 40HC, etc.)
- Container quantity

**Step 2: Goods Details**
- Goods description (textarea)
- HS Code (searchable input with suggestions)
- Gross weight (kg)
- Net weight (kg)
- Volume (CBM)
- Total packages
- Package type (Cartons, Pallets, etc.)

**Step 3: Timeline**
- Preferred ETD (date picker)
- Preferred ETA (date picker)

**Step 4: Documents**
- Drag-and-drop file upload
- Document type selector
- AI extraction preview
- Edit extracted data

**Step 5: Review & Submit**
- Summary of all entered data
- Edit buttons for each section
- Submit button

#### Shipment Detail Page
**Layout:**
- **Header Section:**
  - Shipment number (large)
  - Status badge
  - Action buttons (Edit, Request Quote, Cancel)
  
- **Tab Navigation:**
  - **Overview Tab:**
    - Basic info cards
    - Route map visualization
    - Timeline (ETD → ETA)
  
  - **Documents Tab:**
    - Document cards with thumbnails
    - Upload new document button
    - View/Download actions
    - AI extraction data viewer
  
  - **Quotes Tab:**
    - Quote comparison table
    - Accept/Reject buttons
    - Quote details modal
  
  - **Tracking Tab:**
    - Timeline view of events
    - Add tracking event (forwarder only)
    - Map view (optional)
  
  - **Activity Tab:**
    - Audit log of all changes
    - User actions history

---

### **4. Document Management Components**

#### Document Upload Component
- **Drag-and-drop zone**
- **File browser button**
- **Supported formats:** PDF, JPG, PNG
- **Max file size:** 10MB
- **Progress bar** during upload
- **Preview thumbnail** after upload

#### AI Extraction Viewer
- **Two-column layout:**
  - **Left:** Document preview (PDF viewer or image)
  - **Right:** Extracted data in editable form
- **Confidence score indicator** (color-coded)
- **Field-by-field editing**
- **Save/Discard buttons**

#### Document Card
- Document icon (based on type)
- File name
- Upload date
- Uploaded by (user name)
- File size
- Actions:
  - View
  - Download
  - Delete
  - Re-extract (if AI failed)

---

### **5. Quote Management Components**

#### Quote Request Form (Supplier)
- Select shipment (dropdown)
- Additional requirements (textarea)
- Preferred forwarders (multi-select)
- Urgency level
- Submit button

#### Create Quote Form (Forwarder)
**Sections:**
- **Freight Charges:**
  - Freight amount (USD)
  - Fuel surcharge
  - THC charges
  - Documentation charges
  - Other charges
  - **Total** (auto-calculated)

- **Service Details:**
  - Transit time (days)
  - Free days at destination
  - Validity date

- **Routing:**
  - Port rotation (textarea)
  - Vessel name
  - Voyage number

- **Container Details:**
  - Container type
  - Container quantity

- **Terms:**
  - Remarks (textarea)
  - Terms & conditions (textarea)

#### Quote Comparison Table
**Columns:**
- Forwarder name
- Total cost
- Transit time
- Validity
- Routing
- Actions (View Details, Accept, Reject)

**Features:**
- Sort by price/transit time
- Highlight best value
- Expand row for full details

#### Quote Detail Modal
- All quote information in readable format
- Forwarder contact info
- Accept/Reject buttons
- Download as PDF

---

### **6. Tracking Components**

#### Tracking Timeline
**Visual timeline showing:**
- Booking confirmed
- Container loaded
- Vessel departed
- In transit
- Vessel arrived
- Container discharged
- Customs clearance
- Delivered

**Each event shows:**
- Status icon
- Date/time
- Location
- Description
- Attached documents
- Added by (user)

#### Add Tracking Event Form (Forwarder)
- Status dropdown
- Location input
- Vessel name
- Voyage number
- Container number
- Description (textarea)
- Estimated datetime
- Actual datetime
- Upload documents
- Mark as milestone checkbox

#### Tracking Map (Optional)
- Interactive map showing route
- Markers for key locations
- Current vessel position (if available)

---

### **7. Settings Components**

#### Profile Settings
- Profile photo upload
- Name
- Email (read-only)
- Phone
- Change password section

#### Company Settings
- Company name
- GSTIN
- Country
- Address
- Company logo upload

#### Notification Settings
- Email notifications toggle
- SMS notifications toggle
- Notification preferences:
  - New quote received
  - Quote accepted/rejected
  - Tracking updates
  - Document uploaded

---

### **8. Reusable UI Components**

#### Buttons
- Primary button (solid)
- Secondary button (outline)
- Danger button (red)
- Icon button
- Loading button (with spinner)

#### Form Inputs
- Text input
- Textarea
- Number input
- Date picker
- Time picker
- Dropdown/Select
- Multi-select
- Searchable select
- File upload
- Checkbox
- Radio button
- Toggle switch

#### Data Display
- Table (with sorting, filtering, pagination)
- Card
- Badge/Tag
- Status indicator
- Progress bar
- Stat card
- Timeline
- Tabs
- Accordion

#### Feedback
- Toast notifications
- Alert banners
- Modal dialogs
- Confirmation dialogs
- Loading spinners
- Empty states
- Error states

#### Navigation
- Breadcrumbs
- Pagination
- Stepper (for multi-step forms)

---

## 📄 Page-by-Page Breakdown

### **Public Pages**

#### 1. Landing Page
**Sections:**
- Hero section with CTA
- Features showcase
- How it works (3-step process)
- Testimonials
- Pricing (optional)
- Footer

#### 2. Login Page
- Left: Branding/illustration
- Right: Login form

#### 3. Register Page
- Multi-step registration wizard

---

### **Supplier Pages**

#### 1. Dashboard (`/dashboard`)
- Welcome message
- Stats cards (4 cards)
- Recent shipments table
- Activity feed
- Quick actions

#### 2. Shipments List (`/shipments`)
- Filter bar
- Shipments table
- Create new button

#### 3. Create Shipment (`/shipments/new`)
- Multi-step form wizard

#### 4. Shipment Details (`/shipments/:id`)
- Tabbed interface
- All shipment information

#### 5. Documents (`/documents`)
- Document library
- Upload new document

#### 6. Quotes (`/quotes`)
- All quotes table
- Filter by status

#### 7. Settings (`/settings`)
- Profile and company settings

---

### **Forwarder Pages**

#### 1. Dashboard (`/dashboard`)
- Stats cards
- Pending quote requests
- Active shipments
- Revenue chart

#### 2. Quote Requests (`/quote-requests`)
- Available shipments table
- Create quote button

#### 3. Create Quote (`/quotes/new/:shipmentId`)
- Quote form

#### 4. Active Shipments (`/shipments`)
- Shipments table
- Update tracking button

#### 5. Add Tracking Event (`/tracking/add/:shipmentId`)
- Tracking event form

---

### **Buyer Pages**

#### 1. Dashboard (`/dashboard`)
- Incoming shipments
- Expected arrivals
- Recent deliveries

#### 2. Shipments (`/shipments`)
- Incoming shipments table

#### 3. Track Shipment (`/shipments/:id/track`)
- Tracking timeline
- Map view

#### 4. Documents (`/documents`)
- Document library

---

## 🎨 Design System

### **Color Palette**

#### Primary Colors
```css
--primary-50: #EFF6FF;
--primary-100: #DBEAFE;
--primary-200: #BFDBFE;
--primary-300: #93C5FD;
--primary-400: #60A5FA;
--primary-500: #3B82F6; /* Main brand color */
--primary-600: #2563EB;
--primary-700: #1D4ED8;
--primary-800: #1E40AF;
--primary-900: #1E3A8A;
```

#### Status Colors
```css
--success: #10B981; /* Green - Delivered, Accepted */
--warning: #F59E0B; /* Orange - Pending, In Transit */
--danger: #EF4444;  /* Red - Cancelled, Rejected */
--info: #3B82F6;    /* Blue - Booked, Processing */
--gray: #6B7280;    /* Gray - Draft, Inactive */
```

#### Neutral Colors
```css
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-400: #9CA3AF;
--gray-500: #6B7280;
--gray-600: #4B5563;
--gray-700: #374151;
--gray-800: #1F2937;
--gray-900: #111827;
```

### **Typography**

#### Font Family
```css
--font-primary: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

#### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

#### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### **Spacing**
```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-5: 1.25rem;  /* 20px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-10: 2.5rem;  /* 40px */
--space-12: 3rem;    /* 48px */
```

### **Border Radius**
```css
--radius-sm: 0.25rem;  /* 4px */
--radius-md: 0.5rem;   /* 8px */
--radius-lg: 0.75rem;  /* 12px */
--radius-xl: 1rem;     /* 16px */
--radius-full: 9999px; /* Pill shape */
```

### **Shadows**
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

---

## 💻 Technical Stack

### **Frontend**
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **Routing:** React Router v6
- **State Management:** 
  - Zustand (global state)
  - React Query (server state)
- **UI Library:** 
  - Tailwind CSS
  - Shadcn/ui components
  - Headless UI
- **Forms:** React Hook Form + Zod validation
- **Tables:** TanStack Table (React Table v8)
- **Charts:** Recharts or Chart.js
- **Date Picker:** React DatePicker
- **File Upload:** React Dropzone
- **PDF Viewer:** React PDF
- **Icons:** Lucide React or Heroicons
- **Notifications:** React Hot Toast

### **Backend API**
- **Base URL:** `http://localhost:8000/api`
- **Authentication:** JWT Bearer tokens
- **Format:** JSON

---

## 🔌 API Integration

### **Authentication Endpoints**

#### Register
```typescript
POST /api/auth/register
Body: {
  email: string;
  password: string;
  name: string;
  company_name: string;
  role: 'supplier' | 'forwarder' | 'buyer';
  phone?: string;
  gstin?: string;
  country?: string;
}
Response: {
  access_token: string;
  user: User;
}
```

#### Login
```typescript
POST /api/auth/login
Body: {
  email: string;
  password: string;
}
Response: {
  access_token: string;
  user: User;
}
```

#### Get Current User
```typescript
GET /api/me
Headers: { Authorization: 'Bearer <token>' }
Response: {
  user_id: string;
  role: string;
}
```

---

### **Shipment Endpoints**

#### Get All Shipments
```typescript
GET /api/shipments
Query: {
  status?: string;
  page?: number;
  limit?: number;
}
Response: {
  items: Shipment[];
  total: number;
  page: number;
  pages: number;
}
```

#### Create Shipment
```typescript
POST /api/shipments
Body: {
  origin_port: string;
  destination_port: string;
  incoterm: string;
  cargo_type: string;
  container_type: string;
  container_qty: number;
  goods_description: string;
  hs_code?: string;
  gross_weight_kg: number;
  net_weight_kg: number;
  volume_cbm: number;
  total_packages: number;
  package_type: string;
  preferred_etd: string;
  preferred_eta: string;
}
Response: Shipment
```

#### Get Shipment by ID
```typescript
GET /api/shipments/:id
Response: Shipment
```

#### Update Shipment
```typescript
PUT /api/shipments/:id
Body: Partial<Shipment>
Response: Shipment
```

---

### **Document Endpoints**

#### Upload Document
```typescript
POST /api/documents/upload
Body: FormData {
  file: File;
  shipment_id: string;
  type: 'invoice' | 'packing_list' | 'commercial_invoice' | ...;
}
Response: {
  document: Document;
  extracted_data: any;
  confidence_score: number;
}
```

#### Get Documents
```typescript
GET /api/documents
Query: {
  shipment_id?: string;
}
Response: Document[]
```

#### Trigger AI Extraction
```typescript
POST /api/documents/:id/extract
Response: {
  extracted_data: any;
  confidence_score: number;
}
```

---

### **Quote Endpoints**

#### Get Quotes
```typescript
GET /api/quotes
Query: {
  shipment_id?: string;
  status?: string;
}
Response: Quote[]
```

#### Create Quote (Forwarder)
```typescript
POST /api/quotes
Body: {
  shipment_id: string;
  freight_amount_usd: number;
  fuel_surcharge?: number;
  thc_charges?: number;
  documentation_charges?: number;
  other_charges?: number;
  transit_time_days: number;
  validity_date: string;
  routing: string;
  vessel_name?: string;
  voyage_number?: string;
  container_type: string;
  container_quantity: number;
  remarks?: string;
  terms_and_conditions?: string;
}
Response: Quote
```

#### Accept Quote (Supplier)
```typescript
POST /api/quotes/:id/accept
Response: Quote
```

#### Reject Quote (Supplier)
```typescript
POST /api/quotes/:id/reject
Response: Quote
```

---

### **Tracking Endpoints**

#### Get Tracking Events
```typescript
GET /api/tracking
Query: {
  shipment_id: string;
}
Response: TrackingEvent[]
```

#### Add Tracking Event (Forwarder)
```typescript
POST /api/tracking
Body: {
  shipment_id: string;
  status: string;
  location: string;
  description: string;
  vessel_name?: string;
  voyage_number?: string;
  container_number?: string;
  estimated_datetime?: string;
  actual_datetime?: string;
  is_milestone?: boolean;
}
Response: TrackingEvent
```

---

## 📱 Responsive Design

### **Breakpoints**
```css
--screen-sm: 640px;   /* Mobile landscape */
--screen-md: 768px;   /* Tablet */
--screen-lg: 1024px;  /* Desktop */
--screen-xl: 1280px;  /* Large desktop */
--screen-2xl: 1536px; /* Extra large */
```

### **Mobile Considerations**
- Collapsible sidebar on mobile
- Bottom navigation for mobile
- Touch-friendly buttons (min 44px)
- Swipeable cards
- Simplified tables (card view on mobile)
- Responsive forms (single column on mobile)

---

## 🎯 Key User Flows

### **Flow 1: Supplier Creates Shipment with AI Extraction**
1. Click "New Shipment" button
2. Upload invoice PDF
3. AI extracts data (loading indicator)
4. Review extracted data (editable fields)
5. Fill remaining fields
6. Submit shipment
7. Redirect to shipment detail page

### **Flow 2: Forwarder Provides Quote**
1. View "Pending Quote Requests" on dashboard
2. Click on shipment
3. Review shipment details
4. Click "Create Quote"
5. Fill quote form
6. Submit quote
7. See success message

### **Flow 3: Supplier Accepts Quote**
1. View shipment detail page
2. Go to "Quotes" tab
3. Compare quotes in table
4. Click "View Details" on preferred quote
5. Review quote in modal
6. Click "Accept Quote"
7. Confirm in dialog
8. See shipment status change to "Booked"

### **Flow 4: Forwarder Updates Tracking**
1. View active shipment
2. Go to "Tracking" tab
3. Click "Add Event"
4. Fill tracking form
5. Upload documents (optional)
6. Submit event
7. See event appear in timeline

---

## 🔔 Notifications

### **Real-time Notifications**
- New quote received
- Quote accepted/rejected
- Tracking update added
- Document uploaded
- Shipment status changed

### **Notification UI**
- Bell icon with badge count
- Dropdown panel with recent notifications
- Mark as read functionality
- "View all" link to notifications page

---

## 🎨 UI/UX Best Practices

### **Design Principles**
1. **Clarity** - Clear labels, obvious actions
2. **Consistency** - Same patterns throughout
3. **Feedback** - Loading states, success/error messages
4. **Efficiency** - Minimize clicks, smart defaults
5. **Accessibility** - WCAG 2.1 AA compliance

### **Accessibility**
- Keyboard navigation
- Screen reader support
- Color contrast (4.5:1 minimum)
- Focus indicators
- Alt text for images
- ARIA labels

### **Performance**
- Lazy loading for images
- Code splitting
- Optimistic UI updates
- Skeleton loaders
- Debounced search
- Pagination for large lists

---

## 📦 Component Library Structure

```
src/
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx
│   │   ├── RegisterForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── dashboard/
│   │   ├── StatCard.tsx
│   │   ├── ActivityFeed.tsx
│   │   └── QuickActions.tsx
│   ├── shipments/
│   │   ├── ShipmentList.tsx
│   │   ├── ShipmentForm.tsx
│   │   ├── ShipmentDetail.tsx
│   │   └── ShipmentCard.tsx
│   ├── documents/
│   │   ├── DocumentUpload.tsx
│   │   ├── DocumentCard.tsx
│   │   ├── AIExtractionViewer.tsx
│   │   └── PDFViewer.tsx
│   ├── quotes/
│   │   ├── QuoteForm.tsx
│   │   ├── QuoteComparison.tsx
│   │   ├── QuoteCard.tsx
│   │   └── QuoteDetailModal.tsx
│   ├── tracking/
│   │   ├── TrackingTimeline.tsx
│   │   ├── TrackingEventForm.tsx
│   │   └── TrackingMap.tsx
│   ├── ui/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Select.tsx
│   │   ├── Table.tsx
│   │   ├── Modal.tsx
│   │   ├── Card.tsx
│   │   ├── Badge.tsx
│   │   ├── Tabs.tsx
│   │   └── ...
│   └── layout/
│       ├── Navbar.tsx
│       ├── Sidebar.tsx
│       ├── Footer.tsx
│       └── PageLayout.tsx
├── pages/
│   ├── auth/
│   ├── dashboard/
│   ├── shipments/
│   ├── documents/
│   ├── quotes/
│   ├── tracking/
│   └── settings/
├── hooks/
│   ├── useAuth.ts
│   ├── useShipments.ts
│   ├── useDocuments.ts
│   ├── useQuotes.ts
│   └── useTracking.ts
├── services/
│   ├── api.ts
│   ├── auth.service.ts
│   ├── shipment.service.ts
│   ├── document.service.ts
│   ├── quote.service.ts
│   └── tracking.service.ts
├── stores/
│   ├── authStore.ts
│   └── uiStore.ts
├── types/
│   ├── shipment.types.ts
│   ├── document.types.ts
│   ├── quote.types.ts
│   └── tracking.types.ts
└── utils/
    ├── formatters.ts
    ├── validators.ts
    └── constants.ts
```

---

## 🚀 Getting Started with UI Development

### **Step 1: Setup Project**
```bash
npm create vite@latest tradeflow-ui -- --template react-ts
cd tradeflow-ui
npm install
```

### **Step 2: Install Dependencies**
```bash
npm install react-router-dom zustand @tanstack/react-query
npm install react-hook-form zod @hookform/resolvers
npm install axios
npm install tailwindcss @tailwindcss/forms
npm install lucide-react
npm install react-hot-toast
npm install date-fns
npm install react-dropzone
npm install @tanstack/react-table
```

### **Step 3: Setup Tailwind**
```bash
npx tailwindcss init -p
```

### **Step 4: Create Folder Structure**
Follow the component library structure above.

### **Step 5: Start Development**
```bash
npm run dev
```

---

## 📊 Priority Order for Development

### **Phase 1: Core (Week 1-2)**
1. ✅ Authentication (Login/Register)
2. ✅ Dashboard layout (Navbar, Sidebar)
3. ✅ Basic routing
4. ✅ API integration setup

### **Phase 2: Shipments (Week 3-4)**
1. ✅ Shipment list page
2. ✅ Create shipment form
3. ✅ Shipment detail page
4. ✅ Document upload

### **Phase 3: AI & Documents (Week 5)**
1. ✅ AI extraction viewer
2. ✅ Document management
3. ✅ PDF viewer

### **Phase 4: Quotes (Week 6)**
1. ✅ Quote form (forwarder)
2. ✅ Quote comparison (supplier)
3. ✅ Accept/reject flow

### **Phase 5: Tracking (Week 7)**
1. ✅ Tracking timeline
2. ✅ Add tracking events
3. ✅ Real-time updates

### **Phase 6: Polish (Week 8)**
1. ✅ Notifications
2. ✅ Settings pages
3. ✅ Mobile responsiveness
4. ✅ Testing & bug fixes

---

## 🎉 Summary

This UI will provide:
- **3 distinct user experiences** (Supplier, Forwarder, Buyer)
- **20+ pages** with full functionality
- **50+ reusable components**
- **Complete CRUD operations** for all entities
- **Real-time updates** and notifications
- **AI-powered document extraction** interface
- **Responsive design** for all devices
- **Professional, modern design** with excellent UX

The system connects the entire logistics workflow from shipment creation to delivery tracking, with AI automation reducing manual data entry by 98%.

---

**Ready to build?** Start with Phase 1 and work your way through! 🚀

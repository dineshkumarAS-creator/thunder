# 🔌 TradeFlow AI - Complete API Reference & Data Models

## 📋 Table of Contents
1. [API Overview](#api-overview)
2. [Authentication](#authentication)
3. [Data Models](#data-models)
4. [API Endpoints](#api-endpoints)
5. [Error Handling](#error-handling)
6. [Code Examples](#code-examples)

---

## 🌐 API Overview

### Base URL
```
Development: http://localhost:8000/api
Production: https://api.tradeflow.ai/api
```

### Authentication
All protected endpoints require JWT Bearer token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

### Response Format
All responses are in JSON format:
```json
{
  "data": { ... },
  "message": "Success",
  "status": 200
}
```

### Pagination
List endpoints support pagination:
```
GET /api/shipments?page=1&limit=20
```

Response includes:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "pages": 5,
  "limit": 20
}
```

---

## 🔐 Authentication

### Register User
```typescript
POST /api/auth/register

Request Body:
{
  "email": "john@example.com",
  "password": "SecurePass123!",
  "name": "John Doe",
  "company_name": "ABC Trading Co.",
  "role": "supplier", // "supplier" | "forwarder" | "buyer"
  "phone": "+1234567890",
  "gstin": "29ABCDE1234F1Z5", // Optional, for Indian companies
  "country": "IN" // ISO 2-letter code
}

Response (201 Created):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "supplier",
    "company_name": "ABC Trading Co.",
    "is_verified": false,
    "created_at": "2024-12-13T10:30:00Z"
  }
}
```


### Login
```typescript
POST /api/auth/login

Request Body:
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}
Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "john@example.com",
    "name": "John Doe",
    "role": "supplier"
  }
}
```

### Get Current User
```typescript
GET /api/me
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "role": "supplier",
  "email": "john@example.com",
  "name": "John Doe"
}
```

---

## 📦 Data Models

### User Model
```typescript
interface User {
  id: string; // UUID
  email: string;
  name: string;
  company_name: string;
  phone?: string;
  role: "supplier" | "forwarder" | "buyer";
  gstin?: string; // Indian tax ID
  country: string; // ISO 2-letter code
  address?: string;
  is_verified: boolean;
  is_active: boolean;
  created_at: string; // ISO 8601 datetime
  updated_at?: string;
  supabase_uid?: string;
}
```

### Shipment Model
```typescript
interface Shipment {
  id: string; // UUID
  shipment_number: string; // e.g., "SH-2024-001"
  supplier_id: string; // UUID
  buyer_id?: string; // UUID
  
  // Route
  origin_port: string;
  destination_port: string;
  incoterm: "FOB" | "CIF" | "CFR" | "EXW" | "DAP" | "DDP";
  cargo_type: "FCL" | "LCL" | "AIR" | "BREAKBULK";
  container_type: string; // "20GP", "40HC", etc.
  container_qty: number;
  
  // Goods
  goods_description: string;
  hs_code?: string;
  gross_weight_kg: number;
  net_weight_kg: number;
  volume_cbm: number;
  total_packages: number;
  package_type: string; // "Cartons", "Pallets", etc.
  
  // Timeline
  preferred_etd?: string; // ISO 8601 datetime
  preferred_eta?: string;
  actual_etd?: string;
  actual_eta?: string;
  
  // Status
  status: "draft" | "pending_quote" | "quoted" | "booked" | 
          "in_transit" | "arrived" | "delivered" | "cancelled";
  
  // Financial
  declared_value_usd?: number;
  insurance_required: boolean;
  
  // Metadata
  created_at: string;
  updated_at?: string;
  metadata?: Record<string, any>;
  
  // Relationships (populated on request)
  supplier?: User;
  buyer?: User;
  documents?: Document[];
  quotes?: Quote[];
  tracking_events?: TrackingEvent[];
}
```

### Document Model
```typescript
interface Document {
  id: string; // UUID
  shipment_id: string; // UUID
  uploaded_by: string; // UUID
  
  type: "invoice" | "packing_list" | "commercial_invoice" | 
        "certificate_of_origin" | "bill_of_lading" | "house_bl" | 
        "master_bl" | "telex_release" | "other";
  
  file_name: string;
  file_url: string; // Supabase storage URL
  file_size: number; // bytes
  mime_type: string;
  
  // AI Extraction
  extracted_data?: Record<string, any>;
  confidence_score: number; // 0-1
  extraction_method?: string; // "gemini_pro", "ocr", etc.
  needs_review: boolean;
  
  created_at: string;
  metadata?: Record<string, any>;
  
  // Relationships
  shipment?: Shipment;
  uploader?: User;
  extraction_job?: ExtractionJob;
}
```

### Quote Model
```typescript
interface Quote {
  id: string; // UUID
  shipment_id: string; // UUID
  forwarder_id: string; // UUID
  
  // Charges
  freight_amount_usd: number;
  fuel_surcharge: number;
  thc_charges: number; // Terminal Handling Charges
  documentation_charges: number;
  other_charges: number;
  total_amount_usd: number; // Auto-calculated
  
  // Service
  validity_date?: string; // ISO 8601 datetime
  transit_time_days?: number;
  free_days_at_destination: number;
  
  // Routing
  routing?: string; // Port rotation
  vessel_name?: string;
  voyage_number?: string;
  
  // Container
  container_type: string;
  container_quantity: number;
  
  // Status
  status: "pending" | "accepted" | "rejected" | "expired";
  
  // Terms
  remarks?: string;
  terms_and_conditions?: string;
  
  created_at: string;
  updated_at?: string;
  
  // Relationships
  shipment?: Shipment;
  forwarder?: User;
}
```

### TrackingEvent Model
```typescript
interface TrackingEvent {
  id: string; // UUID
  shipment_id: string; // UUID
  created_by?: string; // UUID
  
  status: string; // "booked", "loaded", "departed", "in_transit", etc.
  location: string;
  vessel_name?: string;
  voyage_number?: string;
  container_number?: string;
  
  description: string;
  remarks?: string;
  
  estimated_datetime?: string; // ISO 8601
  actual_datetime?: string;
  
  documents?: string[]; // Array of document URLs
  
  is_milestone: boolean;
  verified: boolean;
  
  timestamp: string; // When event was created
  updated_at?: string;
  
  // Relationships
  shipment?: Shipment;
  creator?: User;
}
```

### ExtractionJob Model
```typescript
interface ExtractionJob {
  id: string; // UUID
  document_id: string; // UUID
  
  status: "pending" | "processing" | "completed" | "failed";
  
  attempts: number;
  error_message?: string;
  
  model_used?: string; // "gemini-1.5-pro", "gemini-1.5-flash"
  processing_time_ms?: number;
  
  created_at: string;
  updated_at?: string;
  
  // Relationships
  document?: Document;
}
```

---

## 🔌 API Endpoints

### Shipments

#### List Shipments
```typescript
GET /api/shipments
Query Parameters:
  - status?: string (filter by status)
  - page?: number (default: 1)
  - limit?: number (default: 20)
  - supplier_id?: string (filter by supplier)
  - buyer_id?: string (filter by buyer)

Response (200 OK):
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "shipment_number": "SH-2024-001",
      "origin_port": "Mumbai (INMUN1)",
      "destination_port": "Los Angeles (USLAX1)",
      "status": "pending_quote",
      "cargo_type": "FCL",
      "container_type": "40HC",
      "preferred_etd": "2024-12-15T00:00:00Z",
      "created_at": "2024-12-01T10:30:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "pages": 3,
  "limit": 20
}
```

#### Create Shipment
```typescript
POST /api/shipments
Headers: { Authorization: "Bearer <token>" }

Request Body:
{
  "origin_port": "Mumbai (INMUN1)",
  "destination_port": "Los Angeles (USLAX1)",
  "incoterm": "FOB",
  "cargo_type": "FCL",
  "container_type": "40HC",
  "container_qty": 1,
  "goods_description": "Electronic Components",
  "hs_code": "8542.31.00",
  "gross_weight_kg": 15000,
  "net_weight_kg": 14500,
  "volume_cbm": 65,
  "total_packages": 500,
  "package_type": "Cartons",
  "preferred_etd": "2024-12-15T00:00:00Z",
  "preferred_eta": "2025-01-05T00:00:00Z",
  "declared_value_usd": 50000,
  "insurance_required": true
}

Response (201 Created):
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "shipment_number": "SH-2024-001",
  "supplier_id": "current-user-id",
  "status": "draft",
  "created_at": "2024-12-13T10:30:00Z",
  // ... all other fields
}
```

#### Get Shipment by ID
```typescript
GET /api/shipments/{shipment_id}
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "shipment_number": "SH-2024-001",
  // ... all shipment fields
  "supplier": {
    "id": "...",
    "name": "John Doe",
    "company_name": "ABC Trading Co."
  },
  "documents": [...],
  "quotes": [...],
  "tracking_events": [...]
}
```

#### Update Shipment
```typescript
PUT /api/shipments/{shipment_id}
Headers: { Authorization: "Bearer <token>" }

Request Body: (partial update)
{
  "status": "pending_quote",
  "preferred_etd": "2024-12-20T00:00:00Z"
}

Response (200 OK):
{
  // Updated shipment object
}
```

#### Delete Shipment
```typescript
DELETE /api/shipments/{shipment_id}
Headers: { Authorization: "Bearer <token>" }

Response (204 No Content)
```

---

### Documents

#### Upload Document
```typescript
POST /api/documents/upload
Headers: { 
  Authorization: "Bearer <token>",
  Content-Type: "multipart/form-data"
}

Request Body (FormData):
  - file: File (PDF, JPG, PNG)
  - shipment_id: string (UUID)
  - type: string (document type)

Response (201 Created):
{
  "document": {
    "id": "doc-uuid",
    "shipment_id": "shipment-uuid",
    "file_name": "invoice_001.pdf",
    "file_url": "https://supabase.co/storage/...",
    "file_size": 2500000,
    "mime_type": "application/pdf",
    "type": "commercial_invoice",
    "confidence_score": 0.98,
    "needs_review": false,
    "created_at": "2024-12-13T10:30:00Z"
  },
  "extracted_data": {
    "invoice_number": "INV-2024-001",
    "invoice_date": "2024-12-01",
    "hs_code": "8542.31.00",
    "total_amount": 50000,
    "currency": "USD",
    "gross_weight_kg": 15000,
    "net_weight_kg": 14500,
    "packages": 500,
    "items": [
      {
        "description": "Electronic Components",
        "quantity": 500,
        "unit_price": 100,
        "total": 50000
      }
    ]
  },
  "confidence_score": 0.98
}
```

#### List Documents
```typescript
GET /api/documents
Query Parameters:
  - shipment_id?: string (filter by shipment)
  - type?: string (filter by document type)

Response (200 OK):
{
  "items": [
    {
      "id": "doc-uuid",
      "shipment_id": "shipment-uuid",
      "file_name": "invoice_001.pdf",
      "type": "commercial_invoice",
      "confidence_score": 0.98,
      "created_at": "2024-12-13T10:30:00Z"
    }
  ]
}
```

#### Get Document by ID
```typescript
GET /api/documents/{document_id}
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "id": "doc-uuid",
  "shipment_id": "shipment-uuid",
  "file_name": "invoice_001.pdf",
  "file_url": "https://...",
  "extracted_data": { ... },
  "confidence_score": 0.98,
  // ... all fields
}
```

#### Trigger Re-extraction
```typescript
POST /api/documents/{document_id}/extract
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "extracted_data": { ... },
  "confidence_score": 0.98,
  "extraction_method": "gemini_pro"
}
```

#### Delete Document
```typescript
DELETE /api/documents/{document_id}
Headers: { Authorization: "Bearer <token>" }

Response (204 No Content)
```

---

### Quotes

#### List Quotes
```typescript
GET /api/quotes
Query Parameters:
  - shipment_id?: string
  - status?: string
  - forwarder_id?: string

Response (200 OK):
{
  "items": [
    {
      "id": "quote-uuid",
      "shipment_id": "shipment-uuid",
      "forwarder_id": "forwarder-uuid",
      "total_amount_usd": 2450,
      "transit_time_days": 18,
      "status": "pending",
      "created_at": "2024-12-13T10:30:00Z",
      "forwarder": {
        "name": "ABC Logistics",
        "company_name": "ABC Logistics Ltd."
      }
    }
  ]
}
```

#### Create Quote (Forwarder)
```typescript
POST /api/quotes
Headers: { Authorization: "Bearer <token>" }

Request Body:
{
  "shipment_id": "shipment-uuid",
  "freight_amount_usd": 2000,
  "fuel_surcharge": 200,
  "thc_charges": 150,
  "documentation_charges": 100,
  "other_charges": 0,
  "transit_time_days": 18,
  "free_days_at_destination": 7,
  "validity_date": "2024-12-31T23:59:59Z",
  "routing": "Mumbai → Singapore → Los Angeles",
  "vessel_name": "MSC MAYA",
  "voyage_number": "MY-2401",
  "container_type": "40HC",
  "container_quantity": 1,
  "remarks": "Direct service, no transshipment delays",
  "terms_and_conditions": "Standard terms apply"
}

Response (201 Created):
{
  "id": "quote-uuid",
  "total_amount_usd": 2450, // Auto-calculated
  "status": "pending",
  // ... all quote fields
}
```

#### Get Quote by ID
```typescript
GET /api/quotes/{quote_id}
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "id": "quote-uuid",
  // ... all quote fields
  "shipment": { ... },
  "forwarder": { ... }
}
```

#### Accept Quote (Supplier)
```typescript
POST /api/quotes/{quote_id}/accept
Headers: { Authorization: "Bearer <token>" }

Response (200 OK):
{
  "id": "quote-uuid",
  "status": "accepted",
  // ... updated quote
  "shipment": {
    "status": "booked" // Shipment status updated
  }
}
```

#### Reject Quote (Supplier)
```typescript
POST /api/quotes/{quote_id}/reject
Headers: { Authorization: "Bearer <token>" }

Request Body (optional):
{
  "reason": "Price too high"
}

Response (200 OK):
{
  "id": "quote-uuid",
  "status": "rejected"
}
```

---

### Tracking

#### List Tracking Events
```typescript
GET /api/tracking
Query Parameters:
  - shipment_id: string (required)

Response (200 OK):
{
  "items": [
    {
      "id": "event-uuid",
      "shipment_id": "shipment-uuid",
      "status": "booked",
      "location": "Mumbai, India",
      "description": "Booking confirmed",
      "actual_datetime": "2024-12-01T10:30:00Z",
      "is_milestone": true,
      "verified": true,
      "timestamp": "2024-12-01T10:30:00Z"
    },
    {
      "id": "event-uuid-2",
      "status": "loaded",
      "location": "JNPT Port, Mumbai",
      "vessel_name": "MSC MAYA",
      "voyage_number": "MY-2401",
      "container_number": "MSCU1234567",
      "description": "Container loaded onto vessel",
      "actual_datetime": "2024-12-05T14:15:00Z",
      "documents": ["https://storage.../loading_report.pdf"],
      "is_milestone": true,
      "timestamp": "2024-12-05T14:15:00Z"
    }
  ]
}
```

#### Add Tracking Event (Forwarder)
```typescript
POST /api/tracking
Headers: { Authorization: "Bearer <token>" }

Request Body:
{
  "shipment_id": "shipment-uuid",
  "status": "in_transit",
  "location": "Singapore Port",
  "description": "Vessel arrived at transshipment port",
  "vessel_name": "MSC MAYA",
  "voyage_number": "MY-2401",
  "container_number": "MSCU1234567",
  "actual_datetime": "2024-12-18T14:30:00Z",
  "estimated_datetime": "2024-12-19T08:00:00Z",
  "is_milestone": true,
  "remarks": "On schedule"
}

Response (201 Created):
{
  "id": "event-uuid",
  "shipment_id": "shipment-uuid",
  "status": "in_transit",
  // ... all event fields
  "timestamp": "2024-12-18T14:30:00Z"
}
```

#### Update Tracking Event
```typescript
PUT /api/tracking/{event_id}
Headers: { Authorization: "Bearer <token>" }

Request Body:
{
  "verified": true,
  "remarks": "Updated remarks"
}

Response (200 OK):
{
  // Updated event
}
```

#### Delete Tracking Event
```typescript
DELETE /api/tracking/{event_id}
Headers: { Authorization: "Bearer <token>" }

Response (204 No Content)
```

---

## ❌ Error Handling

### Error Response Format
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### Common Error Codes

#### 400 Bad Request
```json
{
  "detail": "Validation error",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

#### 401 Unauthorized
```json
{
  "detail": "Invalid or expired token"
}
```

#### 403 Forbidden
```json
{
  "detail": "You don't have permission to access this resource"
}
```

#### 404 Not Found
```json
{
  "detail": "Shipment not found"
}
```

#### 409 Conflict
```json
{
  "detail": "Email already registered"
}
```

#### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error. Please try again later."
}
```

---

## 💻 Code Examples

### React/TypeScript Examples

#### Setup API Client
```typescript
// services/api.ts
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Redirect to login
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

#### Authentication Service
```typescript
// services/auth.service.ts
import { api } from './api';

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  name: string;
  company_name: string;
  role: 'supplier' | 'forwarder' | 'buyer';
  phone?: string;
  gstin?: string;
  country?: string;
}

export const authService = {
  async login(credentials: LoginCredentials) {
    const response = await api.post('/auth/login', credentials);
    const { access_token, user } = response.data;
    localStorage.setItem('access_token', access_token);
    return { token: access_token, user };
  },

  async register(data: RegisterData) {
    const response = await api.post('/auth/register', data);
    const { access_token, user } = response.data;
    localStorage.setItem('access_token', access_token);
    return { token: access_token, user };
  },

  async getCurrentUser() {
    const response = await api.get('/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
    window.location.href = '/login';
  },
};
```

#### Shipment Service
```typescript
// services/shipment.service.ts
import { api } from './api';
import { Shipment } from '../types/shipment.types';

export const shipmentService = {
  async getShipments(params?: {
    status?: string;
    page?: number;
    limit?: number;
  }) {
    const response = await api.get('/shipments', { params });
    return response.data;
  },

  async getShipmentById(id: string) {
    const response = await api.get(`/shipments/${id}`);
    return response.data;
  },

  async createShipment(data: Partial<Shipment>) {
    const response = await api.post('/shipments', data);
    return response.data;
  },

  async updateShipment(id: string, data: Partial<Shipment>) {
    const response = await api.put(`/shipments/${id}`, data);
    return response.data;
  },

  async deleteShipment(id: string) {
    await api.delete(`/shipments/${id}`);
  },
};
```

#### Document Service with File Upload
```typescript
// services/document.service.ts
import { api } from './api';

export const documentService = {
  async uploadDocument(file: File, shipmentId: string, type: string) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('shipment_id', shipmentId);
    formData.append('type', type);

    const response = await api.post('/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  async getDocuments(shipmentId?: string) {
    const response = await api.get('/documents', {
      params: { shipment_id: shipmentId },
    });
    return response.data;
  },

  async getDocumentById(id: string) {
    const response = await api.get(`/documents/${id}`);
    return response.data;
  },

  async triggerExtraction(id: string) {
    const response = await api.post(`/documents/${id}/extract`);
    return response.data;
  },

  async deleteDocument(id: string) {
    await api.delete(`/documents/${id}`);
  },
};
```

#### React Query Hooks
```typescript
// hooks/useShipments.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { shipmentService } from '../services/shipment.service';
import { Shipment } from '../types/shipment.types';

export const useShipments = (params?: any) => {
  return useQuery({
    queryKey: ['shipments', params],
    queryFn: () => shipmentService.getShipments(params),
  });
};

export const useShipment = (id: string) => {
  return useQuery({
    queryKey: ['shipment', id],
    queryFn: () => shipmentService.getShipmentById(id),
    enabled: !!id,
  });
};

export const useCreateShipment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: Partial<Shipment>) => 
      shipmentService.createShipment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['shipments'] });
    },
  });
};

export const useUpdateShipment = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<Shipment> }) =>
      shipmentService.updateShipment(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['shipments'] });
      queryClient.invalidateQueries({ queryKey: ['shipment', variables.id] });
    },
  });
};
```

#### Component Example: Shipment List
```typescript
// components/shipments/ShipmentList.tsx
import React from 'react';
import { useShipments } from '../../hooks/useShipments';
import { ShipmentCard } from './ShipmentCard';
import { LoadingSpinner } from '../ui/LoadingSpinner';
import { ErrorMessage } from '../ui/ErrorMessage';

export const ShipmentList: React.FC = () => {
  const { data, isLoading, error } = useShipments();

  if (isLoading) return <LoadingSpinner />;
  if (error) return <ErrorMessage error={error} />;

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Shipments</h2>
      
      {data?.items.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No shipments yet</p>
        </div>
      ) : (
        <div className="grid gap-4">
          {data?.items.map((shipment) => (
            <ShipmentCard key={shipment.id} shipment={shipment} />
          ))}
        </div>
      )}
    </div>
  );
};
```

#### Component Example: Create Shipment Form
```typescript
// components/shipments/CreateShipmentForm.tsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { useCreateShipment } from '../../hooks/useShipments';
import { toast } from 'react-hot-toast';

const shipmentSchema = z.object({
  origin_port: z.string().min(1, 'Origin port is required'),
  destination_port: z.string().min(1, 'Destination port is required'),
  incoterm: z.enum(['FOB', 'CIF', 'CFR', 'EXW', 'DAP', 'DDP']),
  cargo_type: z.enum(['FCL', 'LCL', 'AIR', 'BREAKBULK']),
  container_type: z.string(),
  container_qty: z.number().min(1),
  goods_description: z.string().min(1),
  gross_weight_kg: z.number().min(0),
  net_weight_kg: z.number().min(0),
  volume_cbm: z.number().min(0),
  total_packages: z.number().min(1),
  package_type: z.string(),
});

type ShipmentFormData = z.infer<typeof shipmentSchema>;

export const CreateShipmentForm: React.FC = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<ShipmentFormData>({
    resolver: zodResolver(shipmentSchema),
  });

  const createShipment = useCreateShipment();

  const onSubmit = async (data: ShipmentFormData) => {
    try {
      await createShipment.mutateAsync(data);
      toast.success('Shipment created successfully!');
    } catch (error) {
      toast.error('Failed to create shipment');
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-1">
            Origin Port
          </label>
          <input
            {...register('origin_port')}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Mumbai (INMUN1)"
          />
          {errors.origin_port && (
            <p className="text-red-500 text-sm mt-1">
              {errors.origin_port.message}
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Destination Port
          </label>
          <input
            {...register('destination_port')}
            className="w-full px-3 py-2 border rounded-md"
            placeholder="Los Angeles (USLAX1)"
          />
          {errors.destination_port && (
            <p className="text-red-500 text-sm mt-1">
              {errors.destination_port.message}
            </p>
          )}
        </div>
      </div>

      {/* More form fields... */}

      <button
        type="submit"
        disabled={createShipment.isPending}
        className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {createShipment.isPending ? 'Creating...' : 'Create Shipment'}
      </button>
    </form>
  );
};
```

---

## 🔒 Security Best Practices

### 1. Token Storage
```typescript
// ✅ Good: Use httpOnly cookies (if possible)
// ✅ Acceptable: localStorage with XSS protection
// ❌ Bad: sessionStorage or global variables

// Store token
localStorage.setItem('access_token', token);

// Retrieve token
const token = localStorage.getItem('access_token');

// Remove token on logout
localStorage.removeItem('access_token');
```

### 2. Request Validation
```typescript
// Always validate user input
const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const result = schema.safeParse(formData);
if (!result.success) {
  // Handle validation errors
}
```

### 3. Error Handling
```typescript
// Don't expose sensitive information in errors
try {
  await api.post('/auth/login', credentials);
} catch (error) {
  if (axios.isAxiosError(error)) {
    const message = error.response?.data?.detail || 'Login failed';
    toast.error(message);
  }
}
```

---

## 📊 Rate Limiting

The API implements rate limiting:
- **100 requests per minute** per IP address
- **1000 requests per hour** per user

Rate limit headers in response:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1702468800
```

---

## 🎯 Summary

This API provides:
- ✅ **Complete CRUD operations** for all entities
- ✅ **JWT-based authentication**
- ✅ **File upload with AI extraction**
- ✅ **Real-time tracking updates**
- ✅ **Quote management workflow**
- ✅ **Comprehensive error handling**
- ✅ **Type-safe TypeScript interfaces**
- ✅ **React Query integration examples**

All endpoints are documented, tested, and ready for frontend integration! 🚀

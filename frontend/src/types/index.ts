 // FAQ types
 export interface FAQ {
    id: string;
    question: string;
    answer: string;
    categoryId?: string;
    documentId?: string;
    created_by: string;
    createdAt: string;
    updatedAt?: string;
    status: 'draft' | 'published' | 'archived';
    version: number;
    expanded: boolean;
  }

  // Document types
  export interface Document {
    id: string;
    filename: string;
    filepath: string;
    fileType: string;
    uploadedBy: string;
    uploadedAt: string;
    processedAt?: string;
    status: string;
  }

// User types
export interface User {
    id: string;
    email: string;
    firstName: string;
    lastName: string;
    roles: string[];
  }
  
 
  

  
  // API response types
  export interface ApiResponse<T> {
    status: 'success' | 'error';
    data?: T;
    message?: string;
  }
  
  // Auth types
  export interface LoginCredentials {
    email: string;
    password: string;
  }
  
  export interface RegisterData extends LoginCredentials {
    firstName: string;
    lastName: string;
  }
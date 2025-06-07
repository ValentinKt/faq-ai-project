import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import { store } from '../store';
import { logout } from '../store/authSlice';
import { FAQ as FAQType } from '../types';

const API_BASE_URL = (import.meta as any).env.VITE_API_BASE_URL || 'http://localhost:5000/api';

class APIService {
    private instance: AxiosInstance;

    constructor() {
        this.instance = axios.create({
            baseURL: API_BASE_URL,
            withCredentials: true,
            timeout: 10000,
        });
        this.setupInterceptors();
    }

    private setupInterceptors() {
        this.instance.interceptors.request.use(
            config => {
                const token = localStorage.getItem('token');
                if (token && config.headers) config.headers.Authorization = `Bearer ${token}`;
                return config;
            },
            error => Promise.reject(error)
        );

        this.instance.interceptors.response.use(
            response => response,
            error => {
                if (error.response?.status === 401) {
                    store.dispatch(logout());
                    window.location.href = '/login';
                }
                return Promise.reject(error);
            }
        );
    }

    async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
        const response = await this.instance.get<T>(url, config);
        return response.data;
    }

    async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
        const response = await this.instance.post<T>(url, data, config);
        return response.data;
    }

    public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
        const response = await this.instance.put<T>(url, data, config);
        return response.data;
    }
}

export const apiService = new APIService();

export const AuthService = {
    login: async (data: { email: string; password: string }) => {
        const response = await apiService.post<{ data: { access_token: string; user: any } }>('/auth/login', data);
        localStorage.setItem('token', response.data.access_token);
        return response.data;
    },
    logout: async () => {
        await apiService.post('/auth/logout');
        localStorage.removeItem('token');
    }
};

// Typed FAQ Service
export const FAQService = {
  getAll: async (searchTerm?: string): Promise<FAQ[]> => {
    const params = searchTerm ? { search: searchTerm } : undefined;
    return apiService.get<FAQ[]>('/faq', { params });
  },
  getById: async (id: string): Promise<FAQ> => {
    return apiService.get<FAQ>(`/faq/${id}`);
  },
  create: async (data: FAQCreateData): Promise<FAQ> => {
    return apiService.post<FAQ>('/faq', data);
  },
  update: async (id: string, data: FAQUpdateData): Promise<FAQ> => {
    return apiService.put<FAQ>(`/faq/${id}`, data);
  },
};

// Type Definitions
interface FAQ {
    id: string;
    question: string;
    answer: string;
    category_id?: string;
    document_id?: string;
    created_at: string;
    updated_at?: string;
    status: 'draft' | 'published' | 'archived';
    version: number;
  }
  
  interface FAQCreateData {
    question: string;
    answer: string;
    category_id?: string;
    document_id?: string;
  }
  
  interface FAQUpdateData extends Partial<FAQCreateData> {}

export const AnalyticsService = {
    logFAQFeedback: async (faqId: string, feedback: { is_helpful: boolean; feedback_text?: string }) => {
        await apiService.post(`/analytics/faq/${faqId}/feedback`, feedback);
    }
};
import { apiService } from './api';
import { Document } from '../types';

export const DocumentService = {
  
    uploadDocument: async (file: File): Promise<Document> => {
            const formData = new FormData();
            formData.append('file', file);
            
            const response = await apiService.post('/documents', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
            });
            return (response as any).data as Document;
    },
  
    getAllDocuments: async (): Promise<Document[]> => {
        const response = await apiService.get('/documents');
        return (response as any).data as Document[];
    }

}
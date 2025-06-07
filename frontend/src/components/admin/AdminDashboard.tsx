import React, { useState, useEffect } from 'react';
import DocumentUpload from './DocumentUpload';
import { apiService } from '../../services/api';
import { Document } from '../../types';
import { formatDateTime } from '../../utils';

const AdminDashboard: React.FC = () => {
    const [documents, setDocuments] = useState<Document[]>([]);
    const [isUploadOpen, setIsUploadOpen] = useState(false);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchDocuments = async () => {
            try {
                const response = await apiService.get<{ data: Document[] }>('/documents');
                setDocuments(response.data);
            } catch (err) {
                setError('Failed to load documents');
            } finally {
                setLoading(false);
            }
        };
        fetchDocuments();
    }, []);

    const handleUpload = async (file: File) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await apiService.post<{ data: Document }>('/documents', formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
        setDocuments([...documents, response.data]);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-gray-800 mb-6">Admin Dashboard</h1>
            <button
                onClick={() => setIsUploadOpen(true)}
                className="mb-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
                Upload Document
            </button>
            {loading && <p className="text-gray-600">Loading documents...</p>}
            {error && <p className="text-red-600">{error}</p>}
            {!loading && !error && (
                <div className="bg-white shadow rounded-lg p-6">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">Documents</h2>
                    <table className="min-w-full divide-y divide-gray-200">
                        <thead className="bg-gray-50">
                            <tr>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Filename</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Type</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Uploaded At</th>
                            </tr>
                        </thead>
                        <tbody className="bg-white divide-y divide-gray-200">
                            {documents.map(doc => (
                                <tr key={doc.id}>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{doc.filename}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.fileType}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{doc.status}</td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{formatDateTime(doc.uploadedAt)}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            )}
            <DocumentUpload isOpen={isUploadOpen} onClose={() => setIsUploadOpen(false)} onUpload={handleUpload} />
        </div>
    );
};

export default AdminDashboard;
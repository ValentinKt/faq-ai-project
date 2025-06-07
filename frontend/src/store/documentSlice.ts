import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { Document } from '../types';
import { DocumentService } from '../services/documents';

interface DocumentState {
  documents: Document[];
  loading: boolean;
  error: string | null;
}

const initialState: DocumentState = {
  documents: [],
  loading: false,
  error: null
};

export const fetchDocuments = createAsyncThunk(
  'documents/fetchAll',
  async () => {
    return await DocumentService.getAllDocuments();
  }
);

export const uploadDocument = createAsyncThunk(
  'documents/upload',
  async (file: File) => {
    return await DocumentService.uploadDocument(file);
  }
);

const documentSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDocuments.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.loading = false;
        state.documents = action.payload;
      })
      .addCase(fetchDocuments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch documents';
      })
      .addCase(uploadDocument.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(uploadDocument.fulfilled, (state, action) => {
        state.loading = false;
        state.documents.push(action.payload);
      })
      .addCase(uploadDocument.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to upload document';
      });
  }
});

export default documentSlice.reducer;
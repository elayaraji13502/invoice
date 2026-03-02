import { apiClient } from './api';

/**
 * Email Ingestion Service
 * 
 * Handles email fetching, OCR processing, and invoice creation.
 * Requires valid API key in X-API-Key header.
 */

export interface IngestionResult {
  success: boolean;
  message: string;
  result: {
    message: string;
    processed: number;
    total: number;
  };
  timestamp: string;
}

export interface IngestionLog {
  id: number;
  emailSubject: string;
  filename: string;
  emailFrom: string;
  status: 'success' | 'failed' | 'skipped';
  driveLink?: string;
  errorMessage?: string;
  createdAt: string;
}

/**
 * Trigger email ingestion process
 * 
 * This will:
 * 1. Connect to Gmail IMAP
 * 2. Fetch unread emails with invoice keywords
 * 3. Extract attachments (PDF/Images)
 * 4. Run OCR using Mindee
 * 5. Upload files to Google Drive
 * 6. Save invoice data to PostgreSQL
 * 7. Move processed emails to "Processed_Invoices" label
 */
export const triggerEmailIngestion = async (): Promise<IngestionResult> => {
  try {
    const response = await apiClient.post('/ingestion/trigger');
    return response.data;
  } catch (error: any) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to trigger email ingestion');
  }
};

/**
 * Get email ingestion logs
 * 
 * Returns the last 100 ingestion attempts with their status
 */
export const getIngestionLogs = async (): Promise<IngestionLog[]> => {
  try {
    const response = await apiClient.get('/ingestion-logs');
    return response.data.data;
  } catch (error: any) {
    if (error.response?.data?.detail) {
      throw new Error(error.response.data.detail);
    }
    throw new Error('Failed to fetch ingestion logs');
  }
};

/**
 * Get ingestion status
 */
export const getIngestionStatus = async () => {
  try {
    const logs = await getIngestionLogs();
    
    const statuses = {
      success: logs.filter(l => l.status === 'success').length,
      failed: logs.filter(l => l.status === 'failed').length,
      skipped: logs.filter(l => l.status === 'skipped').length,
      total: logs.length,
    };
    
    return statuses;
  } catch (error) {
    throw new Error('Failed to get ingestion status');
  }
};

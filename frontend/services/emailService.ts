import { apiClient } from './api';

export interface EmailIngestionResponse {
  success: boolean;
  message: string;
  status?: string;
  result?: any;
}

/**
 * Trigger email ingestion in background
 * Requires API key
 */
export const triggerEmailIngestion = async (): Promise<EmailIngestionResponse> => {
  try {
    const response = await apiClient.post('/ingestion/run');
    return response.data;
  } catch (error: any) {
    throw new Error(
      error.response?.data?.detail || 'Failed to trigger email ingestion'
    );
  }
};

/**
 * Trigger email ingestion synchronously (waits for completion)
 * Requires API key
 */
export const triggerEmailIngestionSync = async (): Promise<EmailIngestionResponse> => {
  try {
    const response = await apiClient.post('/ingestion/run-sync');
    return response.data;
  } catch (error: any) {
    throw new Error(
      error.response?.data?.detail || 'Failed to trigger email ingestion'
    );
  }
};

/**
 * Get email ingestion logs
 */
export const getIngestionLogs = async () => {
  try {
    const response = await apiClient.get('/ingestion-logs');
    return response.data.data || [];
  } catch (error: any) {
    throw new Error(
      error.response?.data?.detail || 'Failed to fetch ingestion logs'
    );
  }
};

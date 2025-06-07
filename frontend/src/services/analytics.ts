import { apiService } from './api';

export const AnalyticsService = {
  logFAQView: async (faqId: string): Promise<void> => {
    try {
      await apiService.post(`/analytics/faq/${faqId}/view`);
    } catch (error) {
      console.error('Failed to log FAQ view:', error);
      throw error;
    }
  },
  logFAQFeedback: async (faqId: string, feedback: { isHelpful: boolean; feedbackText?: string }): Promise<void> => {
    try {
      await apiService.post(`/analytics/faq/${faqId}/feedback`, feedback);
    } catch (error) {
      console.error('Failed to log FAQ feedback:', error);
      throw error;
    }
  },
  getFAQViews: async (faqId: string): Promise<any> => {
    try {
      const response = await apiService.get(`/analytics/faq/${faqId}/views`);
      return (response as any).data;
    } catch (error) {
      console.error('Failed to retrieve FAQ views:', error);
      throw error;
    }
  },
  getFAQFeedback: async (faqId: string): Promise<any> => {
    try {
      const response = await apiService.get(`/analytics/faq/${faqId}/feedback`);
      return (response as any).data;
    } catch (error) {
      console.error('Failed to retrieve FAQ feedback:', error);
      throw error;
    }
  },
};
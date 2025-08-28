import axios, { AxiosInstance, AxiosResponse } from 'axios';
import toast from 'react-hot-toast';
import {
  UserProfile,
  OnboardingResponse,
  Plan,
  WorkoutPlan,
  MealPlan,
  Feedback,
  FeedbackCreate,
  FeedbackSummary,
  FeedbackAnalysis,
  KnowledgeQuery,
  KnowledgeResponse,
  USDASearchResult,
  ExerciseSearchResult,
  WGERSearchResult,
  ApiResponse,
  PaginatedResponse
} from '@/types';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('auth_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for global error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        const message = error.response?.data?.detail || error.message || 'An error occurred';
        toast.error(message);
        return Promise.reject(error);
      }
    );
  }

  // User Profile Methods
  async createUserProfile(profile: Omit<UserProfile, 'id' | 'created_at' | 'updated_at'>): Promise<OnboardingResponse> {
    const response: AxiosResponse<OnboardingResponse> = await this.client.post('/api/users/profile', profile);
    return response.data;
  }

  async getUserProfile(userId: string): Promise<UserProfile> {
    const response: AxiosResponse<UserProfile> = await this.client.get(`/api/users/profile/${userId}`);
    return response.data;
  }

  async updateUserProfile(userId: string, updates: Partial<UserProfile>): Promise<UserProfile> {
    const response: AxiosResponse<UserProfile> = await this.client.put(`/api/users/profile/${userId}`, updates);
    return response.data;
  }

  // Plan Methods
  async getUserPlans(userId: string): Promise<Plan[]> {
    const response: AxiosResponse<Plan[]> = await this.client.get(`/api/plans/user/${userId}`);
    return response.data;
  }

  async getCurrentPlans(userId: string): Promise<{ workout?: Plan; meal?: Plan }> {
    const response: AxiosResponse<{ workout?: Plan; meal?: Plan }> = await this.client.get(`/api/plans/current/${userId}`);
    return response.data;
  }

  async generateWorkoutPlan(userId: string): Promise<Plan> {
    const response: AxiosResponse<Plan> = await this.client.post(`/api/plans/generate/workout/${userId}`);
    return response.data;
  }

  async generateMealPlan(userId: string): Promise<Plan> {
    const response: AxiosResponse<Plan> = await this.client.post(`/api/plans/generate/meal/${userId}`);
    return response.data;
  }

  async updatePlan(planId: string, updates: Partial<Plan>): Promise<Plan> {
    const response: AxiosResponse<Plan> = await this.client.put(`/api/plans/${planId}`, updates);
    return response.data;
  }

  async deactivatePlan(planId: string): Promise<void> {
    await this.client.delete(`/api/plans/${planId}`);
  }

  // Feedback Methods
  async submitFeedback(userId: string, feedback: FeedbackCreate): Promise<Feedback> {
    const response: AxiosResponse<Feedback> = await this.client.post(`/api/feedback/${userId}`, feedback);
    return response.data;
  }

  async getUserFeedback(userId: string): Promise<Feedback[]> {
    const response: AxiosResponse<Feedback[]> = await this.client.get(`/api/feedback/user/${userId}`);
    return response.data;
  }

  async getFeedbackSummary(userId: string): Promise<FeedbackSummary> {
    const response: AxiosResponse<FeedbackSummary> = await this.client.get(`/api/feedback/summary/${userId}`);
    return response.data;
  }

  async getFeedbackAnalysis(userId: string): Promise<FeedbackAnalysis> {
    const response: AxiosResponse<FeedbackAnalysis> = await this.client.get(`/api/feedback/analysis/${userId}`);
    return response.data;
  }

  // Knowledge Search Methods
  async searchKnowledge(query: KnowledgeQuery): Promise<KnowledgeResponse> {
    const response: AxiosResponse<KnowledgeResponse> = await this.client.post('/api/knowledge/search', query);
    return response.data;
  }

  async searchNutrition(query: string, pageSize: number = 10, pageNumber: number = 1): Promise<USDASearchResult> {
    const response: AxiosResponse<USDASearchResult> = await this.client.get('/api/knowledge/nutrition/search', {
      params: { query, page_size: pageSize, page_number: pageNumber }
    });
    return response.data;
  }

  async getFoodDetails(fdcId: number): Promise<any> {
    const response: AxiosResponse<any> = await this.client.get(`/api/knowledge/nutrition/food/${fdcId}`);
    return response.data;
  }

  async searchExercises(query: string, target?: string, equipment?: string): Promise<ExerciseSearchResult> {
    const response: AxiosResponse<ExerciseSearchResult> = await this.client.get('/api/knowledge/exercises/search', {
      params: { query, target, equipment }
    });
    return response.data;
  }

  async searchWGERExercises(query: string, category?: number, muscle?: number): Promise<WGERSearchResult> {
    const response: AxiosResponse<WGERSearchResult> = await this.client.get('/api/knowledge/exercises/wger/search', {
      params: { query, category, muscle }
    });
    return response.data;
  }

  async getWGERCategories(): Promise<any> {
    const response: AxiosResponse<any> = await this.client.get('/api/knowledge/exercises/wger/categories');
    return response.data;
  }

  async getWGERMuscles(): Promise<any> {
    const response: AxiosResponse<any> = await this.client.get('/api/knowledge/exercises/wger/muscles');
    return response.data;
  }

  async getKnowledgeSources(): Promise<any> {
    const response: AxiosResponse<any> = await this.client.get('/api/knowledge/sources');
    return response.data;
  }

  // Utility Methods
  async healthCheck(): Promise<{ status: string; services: string[] }> {
    const response: AxiosResponse<{ status: string; services: string[] }> = await this.client.get('/health');
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new ApiClient();

// Export individual methods for convenience
export const {
  createUserProfile,
  getUserProfile,
  updateUserProfile,
  getUserPlans,
  getCurrentPlans,
  generateWorkoutPlan,
  generateMealPlan,
  updatePlan,
  deactivatePlan,
  submitFeedback,
  getUserFeedback,
  getFeedbackSummary,
  getFeedbackAnalysis,
  searchKnowledge,
  searchNutrition,
  getFoodDetails,
  searchExercises,
  searchWGERExercises,
  getWGERCategories,
  getWGERMuscles,
  getKnowledgeSources,
  healthCheck,
} = apiClient;

// User Profile Types
export interface UserProfile {
  id: string;
  name: string;
  sex: 'male' | 'female' | 'other';
  age: number;
  height_cm: number;
  weight_kg: number;
  goals: string[];
  injuries: string[];
  equipment: string[];
  days_per_week: number;
  created_at: string;
  updated_at: string;
}

export interface OnboardingStep {
  id: number;
  title: string;
  description: string;
  field: keyof UserProfile;
  type: 'text' | 'number' | 'select' | 'multiselect' | 'radio';
  options?: string[];
  required: boolean;
  validation?: (value: any) => string | null;
}

export interface OnboardingResponse {
  user_id: string;
  profile: UserProfile;
}

// Exercise and Workout Types
export interface Exercise {
  name: string;
  sets: number;
  reps: string;
  rir: number;
  notes?: string;
}

export interface WorkoutDay {
  day: number;
  focus: string;
  exercises: Exercise[];
}

export interface WorkoutPlan {
  week: string;
  days: WorkoutDay[];
}

// Nutrition Types
export interface NutritionTargets {
  cal: number;
  protein_g: number;
  carb_g: number;
  fat_g: number;
}

export interface MealItem {
  name: string;
  quantity: string;
  calories: number;
  protein_g: number;
  carb_g: number;
  fat_g: number;
}

export interface DailyMealPlan {
  day: number;
  targets: NutritionTargets;
  meals: {
    name: string;
    items: MealItem[];
  }[];
}

export interface MealPlan {
  week: string;
  daily: DailyMealPlan[];
}

// Plan Types
export interface Plan {
  id: string;
  user_id: string;
  version: number;
  kind: 'workout' | 'meal';
  data: WorkoutPlan | MealPlan;
  active: boolean;
  created_at: string;
}

// Feedback Types
export interface Feedback {
  id: string;
  user_id: string;
  plan_version: number;
  workout_day: number;
  difficulty: number;
  soreness: number;
  pain: boolean;
  enjoyment: number;
  notes?: string;
  created_at: string;
}

export interface FeedbackCreate {
  plan_version: number;
  workout_day: number;
  difficulty: number;
  soreness: number;
  pain: boolean;
  enjoyment: number;
  notes?: string;
}

export interface FeedbackSummary {
  total_workouts: number;
  avg_difficulty: number;
  avg_soreness: number;
  avg_enjoyment: number;
  pain_reports: number;
  recent_feedback: Feedback[];
}

export interface FeedbackAnalysis {
  trends: {
    difficulty_trend: 'increasing' | 'decreasing' | 'stable';
    soreness_trend: 'increasing' | 'decreasing' | 'stable';
    enjoyment_trend: 'increasing' | 'decreasing' | 'stable';
  };
  recommendations: string[];
  adaptations_needed: boolean;
}

// External API Types
export interface USDANutrient {
  id: number;
  number: string;
  name: string;
  amount: number;
  unit: string;
}

export interface USDAFoodItem {
  fdc_id: number;
  description: string;
  brand_owner?: string;
  ingredients?: string;
  serving_size?: number;
  serving_size_unit?: string;
  nutrients: USDANutrient[];
}

export interface USDASearchResult {
  total_hits: number;
  current_page: number;
  total_pages: number;
  page_size: number;
  foods: USDAFoodItem[];
}

export interface ExerciseTarget {
  bodyPart: string;
  equipment: string;
  gifUrl: string;
  id: string;
  name: string;
  target: string;
}

export interface ExerciseSearchResult {
  exercises: ExerciseTarget[];
  total_count: number;
}

export interface WGERExercise {
  id: number;
  uuid: string;
  name: string;
  description: string;
  category: Record<string, any>;
  muscles: Record<string, any>[];
  muscles_secondary: Record<string, any>[];
  equipment: Record<string, any>[];
  variations?: number;
  images: Record<string, any>[];
  comments: Record<string, any>[];
}

export interface WGERSearchResult {
  count: number;
  next?: string;
  previous?: string;
  results: WGERExercise[];
}

export interface SearchResult {
  source: string;
  title: string;
  content: string;
  metadata: Record<string, any>;
  relevance_score?: number;
}

export interface KnowledgeQuery {
  query: string;
  sources?: string[];
  max_results: number;
  include_metadata: boolean;
}

export interface KnowledgeResponse {
  query: string;
  results: SearchResult[];
  total_results: number;
  search_time_ms: number;
  sources_used: string[];
}

// UI Component Types
export interface NavItem {
  label: string;
  href: string;
  icon?: React.ComponentType<{ className?: string }>;
  active?: boolean;
}

export interface StatCard {
  title: string;
  value: string | number;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon?: React.ComponentType<{ className?: string }>;
}

export interface ChartData {
  name: string;
  value: number;
  color?: string;
}

// API Response Types
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

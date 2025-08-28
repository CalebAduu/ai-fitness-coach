'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import { 
  User, 
  Dumbbell, 
  Utensils, 
  TrendingUp, 
  Calendar, 
  Target, 
  BarChart3,
  Plus,
  LogOut,
  Settings,
  Activity,
  Heart,
  Zap,
  Award
} from 'lucide-react';
import { 
  getUserProfile, 
  getCurrentPlans, 
  getFeedbackSummary,
  generateWorkoutPlan,
  generateMealPlan
} from '@/lib/api';
import { UserProfile, Plan, FeedbackSummary } from '@/types';
import { 
  formatDate, 
  formatRelativeDate, 
  getDifficultyColor, 
  getDifficultyLabel,
  getSorenessColor,
  getSorenessLabel,
  getEnjoymentColor,
  getEnjoymentLabel,
  calculateBMI,
  getBMICategory
} from '@/lib/utils';
import toast from 'react-hot-toast';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<UserProfile | null>(null);
  const [plans, setPlans] = useState<{ workout?: Plan; meal?: Plan }>({});
  const [feedback, setFeedback] = useState<FeedbackSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);

  useEffect(() => {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      router.push('/onboarding');
      return;
    }

    loadDashboardData(userId);
  }, [router]);

  const loadDashboardData = async (userId: string) => {
    try {
      const [userData, plansData, feedbackData] = await Promise.all([
        getUserProfile(userId),
        getCurrentPlans(userId),
        getFeedbackSummary(userId)
      ]);

      setUser(userData);
      setPlans(plansData);
      setFeedback(feedbackData);
    } catch (error) {
      console.error('Error loading dashboard data:', error);
      toast.error('Failed to load dashboard data');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGeneratePlan = async (type: 'workout' | 'meal') => {
    if (!user) return;

    setIsGenerating(true);
    try {
      const userId = localStorage.getItem('user_id');
      if (!userId) throw new Error('User ID not found');

      const newPlan = type === 'workout' 
        ? await generateWorkoutPlan(userId)
        : await generateMealPlan(userId);

      // Update plans state
      setPlans(prev => ({
        ...prev,
        [type]: newPlan
      }));

      toast.success(`${type === 'workout' ? 'Workout' : 'Meal'} plan generated successfully!`);
    } catch (error) {
      console.error(`Error generating ${type} plan:`, error);
      toast.error(`Failed to generate ${type} plan`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('user_id');
    router.push('/');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="loading-spinner" />
      </div>
    );
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600 mb-4">User not found</p>
          <button 
            onClick={() => router.push('/onboarding')}
            className="btn-primary"
          >
            Create Profile
          </button>
        </div>
      </div>
    );
  }

  const bmi = calculateBMI(user.weight_kg, user.height_cm);
  const bmiCategory = getBMICategory(bmi);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-4">
              <div className="w-10 h-10 bg-gradient-to-r from-primary-600 to-fitness-600 rounded-lg flex items-center justify-center">
                <Zap className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">AI Fitness Coach</h1>
                <p className="text-sm text-gray-500">Welcome back, {user.name}!</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <button className="btn-secondary flex items-center space-x-2">
                <Settings className="w-4 h-4" />
                <span>Settings</span>
              </button>
              <button 
                onClick={handleLogout}
                className="btn-secondary flex items-center space-x-2"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <User className="w-6 h-6 text-primary-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Weight</p>
                <p className="text-2xl font-bold text-gray-900">{user.weight_kg} kg</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="w-12 h-12 bg-fitness-100 rounded-lg flex items-center justify-center">
                <Target className="w-6 h-6 text-fitness-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">BMI</p>
                <p className="text-2xl font-bold text-gray-900">{bmi.toFixed(1)}</p>
                <p className="text-xs text-gray-500">{bmiCategory}</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <Calendar className="w-6 h-6 text-success-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Workout Days</p>
                <p className="text-2xl font-bold text-gray-900">{user.days_per_week}</p>
                <p className="text-xs text-gray-500">per week</p>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="card"
          >
            <div className="flex items-center">
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <Activity className="w-6 h-6 text-warning-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Total Workouts</p>
                <p className="text-2xl font-bold text-gray-900">{feedback?.total_workouts || 0}</p>
                <p className="text-xs text-gray-500">completed</p>
              </div>
            </div>
          </motion.div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Today's Workout */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              className="card mb-8"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <Dumbbell className="w-5 h-5 text-primary-600" />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">Today's Workout</h2>
                    <p className="text-sm text-gray-500">{formatDate(new Date())}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleGeneratePlan('workout')}
                  disabled={isGenerating}
                  className="btn-primary flex items-center space-x-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>Generate Plan</span>
                </button>
              </div>

              {plans.workout ? (
                <div className="space-y-4">
                  <div className="bg-primary-50 rounded-lg p-4">
                    <h3 className="font-semibold text-primary-900 mb-2">
                      Week {plans.workout.data.week}
                    </h3>
                    <p className="text-primary-700">
                      {plans.workout.data.days.length} workout days planned
                    </p>
                  </div>
                  
                  {plans.workout.data.days.slice(0, 3).map((day, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">Day {day.day}</h4>
                        <span className="text-sm text-gray-500">{day.exercises.length} exercises</span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3">{day.focus}</p>
                      <div className="space-y-2">
                        {day.exercises.slice(0, 3).map((exercise, exIndex) => (
                          <div key={exIndex} className="flex items-center justify-between text-sm">
                            <span className="text-gray-700">{exercise.name}</span>
                            <span className="text-gray-500">
                              {exercise.sets} sets × {exercise.reps}
                            </span>
                          </div>
                        ))}
                        {day.exercises.length > 3 && (
                          <p className="text-xs text-gray-500">
                            +{day.exercises.length - 3} more exercises
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Dumbbell className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No workout plan yet</h3>
                  <p className="text-gray-500 mb-4">
                    Generate your first personalized workout plan to get started
                  </p>
                  <button
                    onClick={() => handleGeneratePlan('workout')}
                    disabled={isGenerating}
                    className="btn-primary"
                  >
                    Generate Workout Plan
                  </button>
                </div>
              )}
            </motion.div>

            {/* Today's Meal Plan */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="card"
            >
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="w-10 h-10 bg-success-100 rounded-lg flex items-center justify-center">
                    <Utensils className="w-5 h-5 text-success-600" />
                  </div>
                  <div>
                    <h2 className="text-xl font-semibold text-gray-900">Today's Meal Plan</h2>
                    <p className="text-sm text-gray-500">{formatDate(new Date())}</p>
                  </div>
                </div>
                <button
                  onClick={() => handleGeneratePlan('meal')}
                  disabled={isGenerating}
                  className="btn-success flex items-center space-x-2"
                >
                  <Plus className="w-4 h-4" />
                  <span>Generate Plan</span>
                </button>
              </div>

              {plans.meal ? (
                <div className="space-y-4">
                  <div className="bg-success-50 rounded-lg p-4">
                    <h3 className="font-semibold text-success-900 mb-2">
                      Week {plans.meal.data.week}
                    </h3>
                    <p className="text-success-700">
                      {plans.meal.data.daily.length} days of meals planned
                    </p>
                  </div>
                  
                  {plans.meal.data.daily.slice(0, 2).map((day, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-medium text-gray-900">Day {day.day}</h4>
                        <span className="text-sm text-gray-500">
                          {day.targets.cal} calories
                        </span>
                      </div>
                      <div className="grid grid-cols-3 gap-4 mb-3">
                        <div className="text-center">
                          <p className="text-xs text-gray-500">Protein</p>
                          <p className="font-medium text-gray-900">{day.targets.protein_g}g</p>
                        </div>
                        <div className="text-center">
                          <p className="text-xs text-gray-500">Carbs</p>
                          <p className="font-medium text-gray-900">{day.targets.carb_g}g</p>
                        </div>
                        <div className="text-center">
                          <p className="text-xs text-gray-500">Fat</p>
                          <p className="font-medium text-gray-900">{day.targets.fat_g}g</p>
                        </div>
                      </div>
                      <div className="space-y-2">
                        {day.meals.slice(0, 3).map((meal, mealIndex) => (
                          <div key={mealIndex} className="flex items-center justify-between text-sm">
                            <span className="text-gray-700">{meal.name}</span>
                            <span className="text-gray-500">{meal.items.length} items</span>
                          </div>
                        ))}
                        {day.meals.length > 3 && (
                          <p className="text-xs text-gray-500">
                            +{day.meals.length - 3} more meals
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <Utensils className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No meal plan yet</h3>
                  <p className="text-gray-500 mb-4">
                    Generate your first personalized meal plan to optimize your nutrition
                  </p>
                  <button
                    onClick={() => handleGeneratePlan('meal')}
                    disabled={isGenerating}
                    className="btn-success"
                  >
                    Generate Meal Plan
                  </button>
                </div>
              )}
            </motion.div>
          </div>

          {/* Sidebar */}
          <div className="space-y-8">
            {/* Progress Overview */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              className="card"
            >
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-warning-100 rounded-lg flex items-center justify-center">
                  <TrendingUp className="w-5 h-5 text-warning-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Progress Overview</h2>
                  <p className="text-sm text-gray-500">Your recent performance</p>
                </div>
              </div>

              {feedback ? (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Avg Difficulty</span>
                    <span className={`font-medium ${getDifficultyColor(feedback.avg_difficulty)}`}>
                      {feedback.avg_difficulty.toFixed(1)}/10
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Avg Soreness</span>
                    <span className={`font-medium ${getSorenessColor(feedback.avg_soreness)}`}>
                      {feedback.avg_soreness.toFixed(1)}/10
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Avg Enjoyment</span>
                    <span className={`font-medium ${getEnjoymentColor(feedback.avg_enjoyment)}`}>
                      {feedback.avg_enjoyment.toFixed(1)}/5
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Pain Reports</span>
                    <span className="font-medium text-gray-900">
                      {feedback.pain_reports}
                    </span>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <BarChart3 className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">No feedback data yet</p>
                </div>
              )}
            </motion.div>

            {/* Quick Actions */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="card"
            >
              <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
              <div className="space-y-3">
                <button className="w-full btn-primary flex items-center space-x-3">
                  <Plus className="w-4 h-4" />
                  <span>Submit Feedback</span>
                </button>
                <button className="w-full btn-secondary flex items-center space-x-3">
                  <BarChart3 className="w-4 h-4" />
                  <span>View Progress</span>
                </button>
                <button className="w-full btn-secondary flex items-center space-x-3">
                  <Target className="w-4 h-4" />
                  <span>Update Goals</span>
                </button>
                <button className="w-full btn-secondary flex items-center space-x-3">
                  <Heart className="w-4 h-4" />
                  <span>Health Check</span>
                </button>
              </div>
            </motion.div>

            {/* Goals Summary */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="card"
            >
              <div className="flex items-center space-x-3 mb-6">
                <div className="w-10 h-10 bg-fitness-100 rounded-lg flex items-center justify-center">
                  <Award className="w-5 h-5 text-fitness-600" />
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">Your Goals</h2>
                  <p className="text-sm text-gray-500">{user.goals.length} goals set</p>
                </div>
              </div>

              <div className="space-y-2">
                {user.goals.map((goal, index) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-fitness-600 rounded-full"></div>
                    <span className="text-sm text-gray-700">{goal}</span>
                  </div>
                ))}
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}

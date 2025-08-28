'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { 
  ArrowLeft, 
  ArrowRight, 
  User, 
  Calendar, 
  Ruler, 
  Weight, 
  Target, 
  AlertTriangle, 
  Dumbbell, 
  CalendarDays,
  CheckCircle
} from 'lucide-react';
import { createUserProfile } from '@/lib/api';
import { UserProfile } from '@/types';
import toast from 'react-hot-toast';

const onboardingSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  age: z.number().min(13, 'Must be at least 13 years old').max(120, 'Invalid age'),
  sex: z.enum(['male', 'female', 'other']),
  height_cm: z.number().min(100, 'Height must be at least 100cm').max(250, 'Height must be less than 250cm'),
  weight_kg: z.number().min(30, 'Weight must be at least 30kg').max(300, 'Weight must be less than 300kg'),
  goals: z.array(z.string()).min(1, 'Please select at least one goal'),
  injuries: z.array(z.string()),
  equipment: z.array(z.string()).min(1, 'Please select at least one equipment type'),
  days_per_week: z.number().min(1, 'Must be at least 1 day').max(7, 'Cannot exceed 7 days'),
});

type OnboardingForm = z.infer<typeof onboardingSchema>;

const steps = [
  {
    id: 1,
    title: 'Basic Information',
    description: 'Tell us about yourself',
    icon: User,
    fields: ['name', 'age', 'sex']
  },
  {
    id: 2,
    title: 'Physical Stats',
    description: 'Your current measurements',
    icon: Ruler,
    fields: ['height_cm', 'weight_kg']
  },
  {
    id: 3,
    title: 'Fitness Goals',
    description: 'What do you want to achieve?',
    icon: Target,
    fields: ['goals']
  },
  {
    id: 4,
    title: 'Health & Safety',
    description: 'Any injuries or limitations?',
    icon: AlertTriangle,
    fields: ['injuries']
  },
  {
    id: 5,
    title: 'Equipment',
    description: 'What equipment do you have access to?',
    icon: Dumbbell,
    fields: ['equipment']
  },
  {
    id: 6,
    title: 'Schedule',
    description: 'How often can you work out?',
    icon: CalendarDays,
    fields: ['days_per_week']
  }
];

const goalOptions = [
  'Lose Weight',
  'Build Muscle',
  'Improve Strength',
  'Increase Endurance',
  'General Fitness',
  'Sports Performance',
  'Rehabilitation',
  'Maintain Current Level'
];

const injuryOptions = [
  'None',
  'Lower Back Pain',
  'Knee Issues',
  'Shoulder Problems',
  'Ankle/Foot Issues',
  'Wrist/Elbow Problems',
  'Hip Issues',
  'Neck Problems',
  'Other'
];

const equipmentOptions = [
  'None (Bodyweight Only)',
  'Dumbbells',
  'Resistance Bands',
  'Pull-up Bar',
  'Bench',
  'Barbell & Plates',
  'Cardio Machine (Treadmill/Bike)',
  'Full Gym Access',
  'Yoga Mat',
  'Foam Roller'
];

export default function OnboardingPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    setValue,
    formState: { errors, isValid }
  } = useForm<OnboardingForm>({
    resolver: zodResolver(onboardingSchema),
    mode: 'onChange'
  });

  const watchedValues = watch();

  const handleNext = () => {
    if (currentStep < steps.length) {
      setCurrentStep(currentStep + 1);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  const onSubmit = async (data: OnboardingForm) => {
    setIsSubmitting(true);
    try {
      const response = await createUserProfile(data);
      localStorage.setItem('user_id', response.user_id);
      toast.success('Profile created successfully!');
      router.push('/dashboard');
    } catch (error) {
      toast.error('Failed to create profile. Please try again.');
      console.error('Error creating profile:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const getStepContent = (step: number) => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                {...register('name')}
                className="input-field"
                placeholder="Enter your full name"
              />
              {errors.name && (
                <p className="text-danger-600 text-sm mt-1">{errors.name.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Age
              </label>
              <input
                type="number"
                {...register('age', { valueAsNumber: true })}
                className="input-field"
                placeholder="Enter your age"
                min="13"
                max="120"
              />
              {errors.age && (
                <p className="text-danger-600 text-sm mt-1">{errors.age.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Sex
              </label>
              <select {...register('sex')} className="input-field">
                <option value="">Select your sex</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
              </select>
              {errors.sex && (
                <p className="text-danger-600 text-sm mt-1">{errors.sex.message}</p>
              )}
            </div>
          </div>
        );

      case 2:
        return (
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Height (cm)
              </label>
              <input
                type="number"
                {...register('height_cm', { valueAsNumber: true })}
                className="input-field"
                placeholder="Enter your height in centimeters"
                min="100"
                max="250"
              />
              {errors.height_cm && (
                <p className="text-danger-600 text-sm mt-1">{errors.height_cm.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Weight (kg)
              </label>
              <input
                type="number"
                {...register('weight_kg', { valueAsNumber: true })}
                className="input-field"
                placeholder="Enter your weight in kilograms"
                min="30"
                max="300"
              />
              {errors.weight_kg && (
                <p className="text-danger-600 text-sm mt-1">{errors.weight_kg.message}</p>
              )}
            </div>
          </div>
        );

      case 3:
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Select your fitness goals (choose all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {goalOptions.map((goal) => (
                <label key={goal} className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    value={goal}
                    {...register('goals')}
                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <span className="text-gray-700">{goal}</span>
                </label>
              ))}
            </div>
            {errors.goals && (
              <p className="text-danger-600 text-sm mt-2">{errors.goals.message}</p>
            )}
          </div>
        );

      case 4:
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              Do you have any injuries or physical limitations? (choose all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {injuryOptions.map((injury) => (
                <label key={injury} className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    value={injury}
                    {...register('injuries')}
                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <span className="text-gray-700">{injury}</span>
                </label>
              ))}
            </div>
          </div>
        );

      case 5:
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              What equipment do you have access to? (choose all that apply)
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {equipmentOptions.map((equipment) => (
                <label key={equipment} className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    value={equipment}
                    {...register('equipment')}
                    className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                  />
                  <span className="text-gray-700">{equipment}</span>
                </label>
              ))}
            </div>
            {errors.equipment && (
              <p className="text-danger-600 text-sm mt-2">{errors.equipment.message}</p>
            )}
          </div>
        );

      case 6:
        return (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-4">
              How many days per week can you work out?
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[1, 2, 3, 4, 5, 6, 7].map((days) => (
                <button
                  key={days}
                  type="button"
                  onClick={() => setValue('days_per_week', days)}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    watchedValues.days_per_week === days
                      ? 'border-primary-600 bg-primary-50 text-primary-700'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="text-2xl font-bold">{days}</div>
                  <div className="text-sm text-gray-600">
                    {days === 1 ? 'day' : 'days'}
                  </div>
                </button>
              ))}
            </div>
            {errors.days_per_week && (
              <p className="text-danger-600 text-sm mt-2">{errors.days_per_week.message}</p>
            )}
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
            Let's Get Started
          </h1>
          <p className="text-gray-600">
            Tell us about yourself so we can create your personalized fitness plan
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">
              Step {currentStep} of {steps.length}
            </span>
            <span className="text-sm text-gray-500">
              {Math.round((currentStep / steps.length) * 100)}% Complete
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <motion.div
              className="bg-gradient-to-r from-primary-600 to-fitness-600 h-2 rounded-full"
              initial={{ width: 0 }}
              animate={{ width: `${(currentStep / steps.length) * 100}%` }}
              transition={{ duration: 0.3 }}
            />
          </div>
        </div>

        {/* Step Indicator */}
        <div className="flex items-center justify-between mb-8">
          {steps.map((step, index) => (
            <div key={step.id} className="flex items-center">
              <div
                className={`w-10 h-10 rounded-full flex items-center justify-center border-2 transition-colors ${
                  currentStep >= step.id
                    ? 'bg-primary-600 border-primary-600 text-white'
                    : 'bg-white border-gray-300 text-gray-500'
                }`}
              >
                {currentStep > step.id ? (
                  <CheckCircle className="w-5 h-5" />
                ) : (
                  <step.icon className="w-5 h-5" />
                )}
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`w-16 h-0.5 mx-2 ${
                    currentStep > step.id ? 'bg-primary-600' : 'bg-gray-300'
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-8">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
            className="card"
          >
            <div className="mb-6">
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                {steps[currentStep - 1].title}
              </h2>
              <p className="text-gray-600">
                {steps[currentStep - 1].description}
              </p>
            </div>

            {getStepContent(currentStep)}
          </motion.div>

          {/* Navigation */}
          <div className="flex justify-between">
            <button
              type="button"
              onClick={handlePrevious}
              disabled={currentStep === 1}
              className="btn-secondary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <ArrowLeft className="w-4 h-4" />
              <span>Previous</span>
            </button>

            {currentStep < steps.length ? (
              <button
                type="button"
                onClick={handleNext}
                className="btn-primary flex items-center space-x-2"
              >
                <span>Next</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            ) : (
              <button
                type="submit"
                disabled={!isValid || isSubmitting}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <>
                    <div className="loading-spinner" />
                    <span>Creating Profile...</span>
                  </>
                ) : (
                  <>
                    <span>Create Profile</span>
                    <CheckCircle className="w-4 h-4" />
                  </>
                )}
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}

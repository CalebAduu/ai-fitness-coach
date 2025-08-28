import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, formatDistanceToNow, formatRelative } from 'date-fns';

// Tailwind class merging utility
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Date formatting utilities
export function formatDate(date: string | Date, formatStr: string = 'MMM dd, yyyy'): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return format(dateObj, formatStr);
}

export function formatRelativeDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return formatDistanceToNow(dateObj, { addSuffix: true });
}

export function formatTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? new Date(date) : date;
  return format(dateObj, 'HH:mm');
}

// Number formatting
export function formatNumber(num: number, decimals: number = 0): string {
  return num.toLocaleString('en-US', {
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals,
  });
}

export function formatPercentage(num: number, decimals: number = 1): string {
  return `${(num * 100).toFixed(decimals)}%`;
}

// Weight and height conversions
export function kgToLbs(kg: number): number {
  return kg * 2.20462;
}

export function lbsToKg(lbs: number): number {
  return lbs / 2.20462;
}

export function cmToInches(cm: number): number {
  return cm / 2.54;
}

export function inchesToCm(inches: number): number {
  return inches * 2.54;
}

// Fitness-specific utilities
export function getDifficultyColor(difficulty: number): string {
  if (difficulty <= 3) return 'text-success-600';
  if (difficulty <= 6) return 'text-warning-600';
  return 'text-danger-600';
}

export function getDifficultyLabel(difficulty: number): string {
  if (difficulty <= 2) return 'Very Easy';
  if (difficulty <= 4) return 'Easy';
  if (difficulty <= 6) return 'Moderate';
  if (difficulty <= 8) return 'Hard';
  return 'Very Hard';
}

export function getSorenessColor(soreness: number): string {
  if (soreness <= 2) return 'text-success-600';
  if (soreness <= 5) return 'text-warning-600';
  return 'text-danger-600';
}

export function getSorenessLabel(soreness: number): string {
  if (soreness === 0) return 'No Soreness';
  if (soreness <= 2) return 'Mild';
  if (soreness <= 5) return 'Moderate';
  if (soreness <= 8) return 'Significant';
  return 'Severe';
}

export function getEnjoymentColor(enjoyment: number): string {
  if (enjoyment >= 4) return 'text-success-600';
  if (enjoyment >= 3) return 'text-warning-600';
  return 'text-danger-600';
}

export function getEnjoymentLabel(enjoyment: number): string {
  if (enjoyment === 1) return 'Hated it';
  if (enjoyment === 2) return 'Disliked it';
  if (enjoyment === 3) return 'Neutral';
  if (enjoyment === 4) return 'Liked it';
  return 'Loved it';
}

// Nutrition calculations
export function calculateCalories(protein: number, carbs: number, fat: number): number {
  return protein * 4 + carbs * 4 + fat * 9;
}

export function formatMacros(protein: number, carbs: number, fat: number): string {
  return `${protein}g protein, ${carbs}g carbs, ${fat}g fat`;
}

export function calculateBMI(weightKg: number, heightCm: number): number {
  const heightM = heightCm / 100;
  return weightKg / (heightM * heightM);
}

export function getBMICategory(bmi: number): string {
  if (bmi < 18.5) return 'Underweight';
  if (bmi < 25) return 'Normal weight';
  if (bmi < 30) return 'Overweight';
  return 'Obese';
}

// Array utilities
export function chunk<T>(array: T[], size: number): T[][] {
  const chunks: T[][] = [];
  for (let i = 0; i < array.length; i += size) {
    chunks.push(array.slice(i, i + size));
  }
  return chunks;
}

export function unique<T>(array: T[]): T[] {
  return [...new Set(array)];
}

export function sortBy<T>(array: T[], key: keyof T, direction: 'asc' | 'desc' = 'asc'): T[] {
  return [...array].sort((a, b) => {
    const aVal = a[key];
    const bVal = b[key];
    
    if (aVal < bVal) return direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return direction === 'asc' ? 1 : -1;
    return 0;
  });
}

// String utilities
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
}

export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + '...';
}

export function slugify(str: string): string {
  return str
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

// Validation utilities
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function isValidAge(age: number): boolean {
  return age >= 13 && age <= 120;
}

export function isValidHeight(height: number): boolean {
  return height >= 100 && height <= 250; // 100cm to 250cm
}

export function isValidWeight(weight: number): boolean {
  return weight >= 30 && weight <= 300; // 30kg to 300kg
}

// Local storage utilities
export function getFromStorage<T>(key: string, defaultValue: T): T {
  if (typeof window === 'undefined') return defaultValue;
  
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : defaultValue;
  } catch {
    return defaultValue;
  }
}

export function setToStorage<T>(key: string, value: T): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(key, JSON.stringify(value));
  } catch (error) {
    console.error('Error saving to localStorage:', error);
  }
}

export function removeFromStorage(key: string): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.removeItem(key);
  } catch (error) {
    console.error('Error removing from localStorage:', error);
  }
}

// Debounce and throttle utilities
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean;
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args);
      inThrottle = true;
      setTimeout(() => (inThrottle = false), limit);
    }
  };
}

// Week utilities
export function getCurrentWeek(): string {
  const now = new Date();
  const year = now.getFullYear();
  const week = Math.ceil((now.getTime() - new Date(year, 0, 1).getTime()) / (7 * 24 * 60 * 60 * 1000));
  return `${year}-W${week.toString().padStart(2, '0')}`;
}

export function getNextWeek(): string {
  const now = new Date();
  now.setDate(now.getDate() + 7);
  const year = now.getFullYear();
  const week = Math.ceil((now.getTime() - new Date(year, 0, 1).getTime()) / (7 * 24 * 60 * 60 * 1000));
  return `${year}-W${week.toString().padStart(2, '0')}`;
}

// Color utilities
export function getColorForValue(value: number, min: number, max: number): string {
  const percentage = (value - min) / (max - min);
  
  if (percentage <= 0.33) return 'text-success-600';
  if (percentage <= 0.66) return 'text-warning-600';
  return 'text-danger-600';
}

export function getBackgroundColorForValue(value: number, min: number, max: number): string {
  const percentage = (value - min) / (max - min);
  
  if (percentage <= 0.33) return 'bg-success-50';
  if (percentage <= 0.66) return 'bg-warning-50';
  return 'bg-danger-50';
}

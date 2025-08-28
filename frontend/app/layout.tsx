import type { Metadata } from 'next'
import { Inter, Poppins } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
})

const poppins = Poppins({ 
  subsets: ['latin'],
  weight: ['400', '500', '600', '700', '800'],
  variable: '--font-poppins',
})

export const metadata: Metadata = {
  title: 'AI Fitness Coach - Personalized Workout & Meal Plans',
  description: 'Get personalized workout and meal plans powered by AI. Track your progress, get feedback, and achieve your fitness goals with our intelligent coaching system.',
  keywords: 'fitness, workout, meal plan, AI coach, personal training, nutrition, exercise',
  authors: [{ name: 'AI Fitness Coach Team' }],
  creator: 'AI Fitness Coach',
  publisher: 'AI Fitness Coach',
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  metadataBase: new URL('https://ai-fitness-coach.vercel.app'),
  openGraph: {
    title: 'AI Fitness Coach - Personalized Workout & Meal Plans',
    description: 'Get personalized workout and meal plans powered by AI. Track your progress, get feedback, and achieve your fitness goals.',
    url: 'https://ai-fitness-coach.vercel.app',
    siteName: 'AI Fitness Coach',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'AI Fitness Coach',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'AI Fitness Coach - Personalized Workout & Meal Plans',
    description: 'Get personalized workout and meal plans powered by AI. Track your progress, get feedback, and achieve your fitness goals.',
    images: ['/og-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className={`${inter.variable} ${poppins.variable}`}>
      <body className={`${inter.className} antialiased`}>
        {children}
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
            success: {
              duration: 3000,
              iconTheme: {
                primary: '#22c55e',
                secondary: '#fff',
              },
            },
            error: {
              duration: 5000,
              iconTheme: {
                primary: '#ef4444',
                secondary: '#fff',
              },
            },
          }}
        />
      </body>
    </html>
  )
}

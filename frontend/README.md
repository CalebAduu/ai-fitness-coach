# AI Fitness Coach Frontend

A beautiful, modern Next.js frontend for the AI Fitness Coach application. Built with TypeScript, Tailwind CSS, and Framer Motion for a premium user experience.

## 🚀 Features

### Core Functionality
- **Landing Page**: Stunning hero section with features showcase and testimonials
- **Conversational Onboarding**: Step-by-step profile creation with smooth animations
- **Dashboard**: Comprehensive overview with workout plans, meal plans, and progress tracking
- **Responsive Design**: Mobile-first approach with beautiful UI on all devices
- **Real-time Updates**: Live data synchronization with the backend API

### UI/UX Features
- **Modern Design**: Clean, professional interface with gradient accents
- **Smooth Animations**: Framer Motion powered transitions and micro-interactions
- **Dark/Light Mode Ready**: Built with theming support
- **Accessibility**: WCAG compliant with proper ARIA labels and keyboard navigation
- **Performance Optimized**: Next.js 14 with App Router for optimal performance

### Technical Features
- **TypeScript**: Full type safety across the application
- **Tailwind CSS**: Utility-first styling with custom design system
- **API Integration**: Comprehensive API client with error handling
- **Form Validation**: Client-side validation with real-time feedback
- **State Management**: React hooks for efficient state management

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Animations**: Framer Motion
- **Icons**: Lucide React
- **Forms**: React Hook Form + Zod
- **Charts**: Recharts
- **HTTP Client**: Axios
- **Notifications**: React Hot Toast
- **Date Handling**: date-fns

## 📦 Installation

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Backend API running (see backend README)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-fitness-coach/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Environment Configuration**
   Create a `.env.local` file in the frontend directory:
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 🚀 Deployment to Vercel

### Automatic Deployment (Recommended)

1. **Connect to Vercel**
   - Push your code to GitHub/GitLab/Bitbucket
   - Go to [vercel.com](https://vercel.com) and sign up/login
   - Click "New Project" and import your repository

2. **Configure Environment Variables**
   In your Vercel project settings, add:
   ```env
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

3. **Deploy**
   - Vercel will automatically detect Next.js and deploy
   - Your app will be live at `https://your-project.vercel.app`

### Manual Deployment

1. **Build the application**
   ```bash
   npm run build
   ```

2. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

3. **Deploy**
   ```bash
   vercel
   ```

4. **Follow the prompts**
   - Link to existing project or create new
   - Set environment variables
   - Deploy

## 📁 Project Structure

```
frontend/
├── app/                    # Next.js App Router pages
│   ├── dashboard/         # Dashboard page
│   ├── onboarding/       # Onboarding flow
│   ├── globals.css       # Global styles
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Landing page
├── components/           # Reusable components
├── lib/                  # Utility functions
│   ├── api.ts           # API client
│   └── utils.ts         # Helper functions
├── types/               # TypeScript type definitions
├── public/              # Static assets
├── tailwind.config.js   # Tailwind configuration
├── next.config.js       # Next.js configuration
└── package.json         # Dependencies
```

## 🎨 Design System

### Colors
- **Primary**: Blue gradient (`#0ea5e9` to `#0284c7`)
- **Fitness**: Purple gradient (`#d946ef` to `#c026d3`)
- **Success**: Green (`#22c55e`)
- **Warning**: Orange (`#f59e0b`)
- **Danger**: Red (`#ef4444`)

### Typography
- **Primary Font**: Inter (system fallback)
- **Display Font**: Poppins (for headings)

### Components
- **Cards**: Rounded corners with subtle shadows
- **Buttons**: Gradient backgrounds with hover effects
- **Forms**: Clean inputs with focus states
- **Navigation**: Sticky header with backdrop blur

## 🔧 Configuration

### Tailwind CSS
The project uses a custom Tailwind configuration with:
- Extended color palette
- Custom animations
- Responsive breakpoints
- Component classes

### Next.js
- App Router enabled
- Image optimization
- API route handling
- Environment variables

### API Integration
The frontend communicates with the backend through:
- RESTful API endpoints
- Type-safe API client
- Error handling and retries
- Request/response interceptors

## 📱 Responsive Design

The application is fully responsive with breakpoints:
- **Mobile**: < 640px
- **Tablet**: 640px - 1024px
- **Desktop**: > 1024px

## 🧪 Development

### Available Scripts
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
```

### Code Quality
- **ESLint**: Code linting with Next.js rules
- **TypeScript**: Strict type checking
- **Prettier**: Code formatting (recommended)

### Testing
```bash
# Add testing dependencies
npm install --save-dev jest @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

## 🚀 Performance Optimization

### Built-in Optimizations
- **Next.js Image Component**: Automatic image optimization
- **Code Splitting**: Automatic route-based code splitting
- **Static Generation**: Pre-rendered pages where possible
- **Bundle Analysis**: Built-in bundle analyzer

### Best Practices
- **Lazy Loading**: Components loaded on demand
- **Memoization**: React.memo for expensive components
- **Debouncing**: API calls debounced to prevent spam
- **Caching**: Local storage for user preferences

## 🔧 Troubleshooting

### Common Issues

1. **API Connection Errors**
   - Verify `NEXT_PUBLIC_API_URL` is correct
   - Check backend is running
   - Ensure CORS is configured

2. **Build Errors**
   - Clear `.next` folder: `rm -rf .next`
   - Reinstall dependencies: `npm install`
   - Check TypeScript errors: `npm run type-check`

3. **Styling Issues**
   - Verify Tailwind CSS is properly configured
   - Check for conflicting CSS
   - Ensure PostCSS is working

### Debug Mode
Enable debug logging:
```bash
DEBUG=* npm run dev
```

## 📈 Analytics & Monitoring

### Recommended Tools
- **Vercel Analytics**: Built-in performance monitoring
- **Google Analytics**: User behavior tracking
- **Sentry**: Error tracking and monitoring

### Implementation
```bash
# Add analytics
npm install @vercel/analytics
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow TypeScript best practices
- Use functional components with hooks
- Maintain consistent naming conventions
- Add proper JSDoc comments

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting section

## 🔄 Updates

To update dependencies:
```bash
npm update
npm audit fix
```

---

**Built with ❤️ using Next.js, TypeScript, and Tailwind CSS**

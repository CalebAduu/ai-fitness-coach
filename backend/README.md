# AI Fitness Coach Backend

Enhanced FastAPI backend with comprehensive AI-powered fitness coaching, including external API integrations for nutrition and exercise data.

## Features

### Core Functionality
- **User Profile Management**: Create, update, and manage user profiles with detailed fitness information
- **Conversational Onboarding**: AI-guided onboarding process to collect user preferences and goals
- **Personalized Plan Generation**: AI-powered workout and meal plan creation using multiple data sources
- **Feedback Collection & Analysis**: Comprehensive feedback system with AI analysis
- **Adaptive Planning**: Intelligent plan adaptation based on user feedback and progress

### Enhanced RAG System
- **Internal Knowledge Base**: LlamaIndex-powered RAG with fitness documentation
- **External API Integrations**: Real-time data from multiple free APIs
- **Comprehensive Knowledge Search**: Multi-source knowledge retrieval and synthesis

### External API Integrations

#### Nutrition Data
- **USDA Food Database**: Comprehensive nutrition information including:
  - Detailed food descriptions and ingredients
  - Macronutrient breakdown (protein, carbs, fat)
  - Vitamin and mineral content
  - Serving size information
  - Brand-specific data

#### Exercise Data
- **ExerciseDB**: Exercise database with:
  - Exercise names and descriptions
  - Target muscle groups
  - Equipment requirements
  - Animated GIF demonstrations
  - Body part categorization

- **WGER Exercise Database**: Open-source exercise database with:
  - Detailed exercise descriptions
  - Primary and secondary muscle targeting
  - Equipment requirements and variations
  - User comments and ratings
  - Exercise images and categories

## API Endpoints

### User Management
- `POST /api/users/` - Create user profile
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/{user_id}` - Update user profile
- `DELETE /api/users/{user_id}` - Delete user profile
- `POST /api/users/{user_id}/onboarding` - Complete onboarding

### Plan Management
- `POST /api/plans/generate` - Generate workout/meal plans
- `GET /api/plans/{user_id}` - Get user's active plans
- `PUT /api/plans/{plan_id}` - Update plan
- `POST /api/plans/adapt` - Adapt plans based on feedback

### Feedback System
- `POST /api/feedback/` - Submit workout feedback
- `GET /api/feedback/{user_id}` - Get user feedback
- `GET /api/feedback/{user_id}/summary` - Get feedback summary
- `POST /api/feedback/analyze` - Analyze feedback with AI

### Knowledge Search (NEW)
- `POST /api/knowledge/search` - Comprehensive knowledge search across all sources
- `GET /api/knowledge/nutrition/search` - Search USDA nutrition database
- `GET /api/knowledge/nutrition/food/{fdc_id}` - Get detailed food information
- `GET /api/knowledge/exercises/search` - Search ExerciseDB
- `GET /api/knowledge/exercises/wger/search` - Search WGER exercise database
- `GET /api/knowledge/exercises/wger/categories` - Get exercise categories
- `GET /api/knowledge/exercises/wger/muscles` - Get muscle groups
- `GET /api/knowledge/sources` - Get available data sources

## Environment Variables

```env
# Core Configuration
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_KEY=your_supabase_service_key

# External API Keys (All Free)
USDA_API_KEY=your_usda_api_key
EXERCISE_DB_API_KEY=your_exercisedb_api_key
WGER_API_KEY=your_wger_api_key

# API Configuration
API_CACHE_TTL=3600
API_RATE_LIMIT=100
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000
```

## Getting Free API Keys

### USDA Food Database
1. Visit [USDA API Portal](https://fdc.nal.usda.gov/api-key-signup.html)
2. Register for a free account
3. Get your API key (1000 requests/day free)

### ExerciseDB
1. Visit [RapidAPI ExerciseDB](https://rapidapi.com/justin-WFnsXH_t6/api/exercisedb/)
2. Sign up for free RapidAPI account
3. Subscribe to ExerciseDB (100 requests/hour free)

### WGER Exercise Database
1. Visit [WGER API](https://wger.de/en/software/api)
2. Register for a free account
3. Get your API token (unlimited requests)

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Database Setup

Run the SQL schema in `db/schemas.sql` in your Supabase project to create the required tables and indexes.

## Knowledge Base Structure

The internal knowledge base is built from markdown files in `docs/`:
- `exercises.md` - Exercise descriptions, technique cues, progressions
- `nutrition.md` - Nutrition guidelines, macro recommendations
- `progressions.md` - Exercise progression frameworks

## Architecture

### Services
- **AIService**: OpenAI integration and plan generation
- **ExternalAPIService**: External API integrations with caching and rate limiting
- **PlanService**: Business logic for plan management
- **UserService**: User profile and onboarding management

### Models
- **User Models**: Profile management and onboarding
- **Plan Models**: Workout and meal plan structures
- **Feedback Models**: Feedback collection and analysis
- **External API Models**: Data structures for external API responses

### Features
- **Caching**: TTLCache for external API responses
- **Rate Limiting**: Throttling for API calls
- **Error Handling**: Comprehensive error handling and fallbacks
- **Validation**: Pydantic models for data validation
- **Logging**: Structured logging throughout the application

## Usage Examples

### Search for Nutrition Information
```python
# Search USDA database
response = await client.get("/api/knowledge/nutrition/search?query=chicken breast")
```

### Search for Exercises
```python
# Search ExerciseDB
response = await client.get("/api/knowledge/exercises/search?query=push up")
```

### Comprehensive Knowledge Search
```python
# Search across all sources
response = await client.post("/api/knowledge/search", json={
    "query": "protein sources for muscle building",
    "sources": ["internal", "usda"],
    "include_nutrition": True,
    "include_exercises": False
})
```

## Development

### Adding New External APIs
1. Add API configuration to `config.py`
2. Create models in `models/external_apis.py`
3. Implement methods in `services/external_api_service.py`
4. Add endpoints in `api/knowledge.py`
5. Update documentation

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## Deployment

The backend can be deployed to:
- **Railway**: Easy deployment with automatic scaling
- **Render**: Free tier available with automatic deployments
- **Heroku**: Traditional deployment option
- **AWS/GCP**: For production workloads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

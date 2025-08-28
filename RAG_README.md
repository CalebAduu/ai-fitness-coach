# RAG Knowledge Base Integration

## Overview

The AI Fitness Coach now includes a **RAG (Retrieval-Augmented Generation)** knowledge base layer that enhances the AI service with local fitness knowledge while maintaining all external API integrations.

## Features

### 🧠 **RAG Knowledge Base**
- **Local knowledge storage** - No external dependencies like llama-index
- **Automatic document chunking** - Splits content by headers and paragraphs
- **Keyword-based search** - Simple but effective relevance scoring
- **Context retrieval** - Gets relevant knowledge for AI prompts
- **Default fitness content** - Pre-loaded with training principles, nutrition basics, and safety guidelines

### 🔄 **Enhanced AI Capabilities**
- **Workout Plan Generation** - Now includes training principles and safety guidelines
- **Meal Plan Generation** - Enhanced with nutrition fundamentals and meal timing
- **Feedback Analysis** - Better analysis using recovery and training principles
- **Plan Adaptation** - Improved adaptations with injury prevention strategies

### 📚 **Knowledge Management**
- **Add custom documents** - Upload your own fitness knowledge
- **Search functionality** - Find relevant information quickly
- **Statistics tracking** - Monitor knowledge base size and sources
- **Health monitoring** - Check RAG service status

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Service    │    │   RAG Service   │    │ External APIs   │
│                 │    │                 │    │                 │
│ • OpenAI GPT-4  │◄──►│ • Local Search  │    │ • USDA Database │
│ • Plan Gen      │    │ • Context Ret.  │    │ • ExerciseDB    │
│ • Feedback      │    │ • Document Mgmt │    │ • WGER          │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## API Endpoints

### RAG Knowledge Base Management

#### `GET /api/rag/stats`
Get knowledge base statistics
```json
{
  "success": true,
  "statistics": {
    "total_documents": 12,
    "sources": ["fitness_principles.md", "nutrition_basics.md"],
    "types": [".md", ".txt"],
    "total_content_length": 15420
  }
}
```

#### `POST /api/rag/search`
Search the knowledge base
```json
{
  "query": "progressive overload training",
  "top_k": 5
}
```

#### `POST /api/rag/context`
Get context for AI prompts
```json
{
  "query": "nutrition protein requirements",
  "max_length": 2000
}
```

#### `POST /api/rag/add-document`
Add new knowledge document
```json
{
  "content": "# Advanced Training\n\n## Periodization...",
  "source": "advanced_training.md",
  "doc_type": "md"
}
```

#### `GET /api/rag/health`
Health check for RAG service
```json
{
  "status": "healthy",
  "documents_loaded": 12,
  "sources_available": 4
}
```

## Default Knowledge Content

The RAG service automatically creates these knowledge files:

### 📖 **fitness_principles.md**
- Progressive Overload principles
- Specificity in training
- Recovery importance
- Consistency guidelines

### 🥗 **nutrition_basics.md**
- Macronutrient guidelines
- Meal timing recommendations
- Hydration principles
- Protein, carbs, and fat requirements

### 🏋️ **exercise_technique.md**
- General exercise principles
- Common mistakes to avoid
- Progression guidelines
- Form and safety tips

### 🛡️ **injury_prevention.md**
- Warm-up protocols
- Proper form guidelines
- Recovery strategies
- Warning signs to watch for

## Usage Examples

### Python Integration

```python
from app.services.ai_service import AIService

# Initialize AI service with RAG
ai_service = AIService()

# Search RAG knowledge
results = ai_service.search_rag_knowledge("injury prevention", top_k=3)

# Get context for AI prompts
context = ai_service.get_rag_context("progressive overload", max_length=1000)

# Add custom knowledge
doc_id = ai_service.add_rag_document(
    content="# Custom Training Method\n\nAdvanced techniques...",
    source="custom_method.md"
)

# Get statistics
stats = ai_service.get_rag_statistics()
```

### Enhanced Plan Generation

The AI service now automatically includes RAG knowledge in:

1. **Workout Plans** - Training principles and safety guidelines
2. **Meal Plans** - Nutrition fundamentals and timing
3. **Feedback Analysis** - Recovery and adaptation principles
4. **Plan Adaptation** - Injury prevention and modification strategies

## File Structure

```
backend/
├── app/
│   ├── services/
│   │   ├── ai_service.py      # Enhanced with RAG integration
│   │   ├── rag_service.py     # RAG knowledge base service
│   │   └── external_api_service.py
│   ├── api/
│   │   └── rag.py            # RAG management endpoints
│   └── knowledge_base/       # Auto-created knowledge storage
│       ├── fitness_principles.md
│       ├── nutrition_basics.md
│       ├── exercise_technique.md
│       └── injury_prevention.md
```

## Benefits

### ✅ **No External Dependencies**
- No llama-index installation issues
- No complex dependency conflicts
- Simple, lightweight implementation

### ✅ **Enhanced AI Responses**
- More accurate and relevant fitness advice
- Better safety considerations
- Improved plan quality

### ✅ **Extensible Knowledge**
- Easy to add custom content
- Maintainable knowledge base
- Version-controlled fitness knowledge

### ✅ **Performance**
- Fast local search
- No external API calls for knowledge
- Reduced latency

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

3. **Check RAG health**:
   ```bash
   curl http://localhost:8000/api/rag/health
   ```

4. **Add custom knowledge**:
   ```bash
   curl -X POST http://localhost:8000/api/rag/add-document \
     -H "Content-Type: application/json" \
     -d '{"content": "# My Method\n\nCustom training...", "source": "my_method.md"}'
   ```

The RAG integration enhances your AI Fitness Coach with reliable, local knowledge while maintaining all the benefits of external APIs for exercise and nutrition data.

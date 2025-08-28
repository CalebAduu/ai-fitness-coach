import os
import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import hashlib
from datetime import datetime

logger = logging.getLogger(__name__)

class RAGService:
    """Simple RAG service using local knowledge base without llama-index dependencies"""
    
    def __init__(self, knowledge_base_path: str = None):
        self.knowledge_base_path = knowledge_base_path or os.path.join(
            os.path.dirname(__file__), "..", "knowledge_base"
        )
        self.knowledge_base = {}
        self.embeddings_cache = {}
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load knowledge base from local files"""
        try:
            knowledge_dir = Path(self.knowledge_base_path)
            if not knowledge_dir.exists():
                logger.info(f"Creating knowledge base directory: {self.knowledge_base_path}")
                knowledge_dir.mkdir(parents=True, exist_ok=True)
                self._create_default_knowledge()
                return
            
            # Load all markdown and text files
            for file_path in knowledge_dir.rglob("*.md"):
                self._load_file(file_path)
            
            for file_path in knowledge_dir.rglob("*.txt"):
                self._load_file(file_path)
                
            logger.info(f"Loaded {len(self.knowledge_base)} knowledge documents")
            
        except Exception as e:
            logger.error(f"Failed to load knowledge base: {e}")
    
    def _load_file(self, file_path: Path):
        """Load a single file into the knowledge base"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple chunking by sections (headers)
            chunks = self._chunk_content(content, file_path.name)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"{file_path.stem}_{i}"
                self.knowledge_base[doc_id] = {
                    "content": chunk,
                    "source": file_path.name,
                    "type": file_path.suffix,
                    "created_at": datetime.now().isoformat()
                }
                
        except Exception as e:
            logger.error(f"Failed to load file {file_path}: {e}")
    
    def _chunk_content(self, content: str, filename: str) -> List[str]:
        """Split content into chunks based on headers"""
        lines = content.split('\n')
        chunks = []
        current_chunk = []
        
        for line in lines:
            # Check if line is a header (starts with #)
            if line.strip().startswith('#'):
                # Save current chunk if it has content
                if current_chunk:
                    chunks.append('\n'.join(current_chunk).strip())
                    current_chunk = []
            
            current_chunk.append(line)
        
        # Add the last chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk).strip())
        
        # If no headers found, split by paragraphs
        if len(chunks) <= 1:
            chunks = [p.strip() for p in content.split('\n\n') if p.strip()]
        
        return chunks
    
    def _create_default_knowledge(self):
        """Create default knowledge base files"""
        default_files = {
            "fitness_principles.md": """
# Fitness Training Principles

## Progressive Overload
Progressive overload is the gradual increase of stress placed upon the body during exercise training. This can be achieved by:
- Increasing weight/resistance
- Increasing repetitions
- Increasing sets
- Decreasing rest periods
- Improving exercise form

## Specificity
Training should be specific to the desired outcome:
- Strength training for strength gains
- Endurance training for cardiovascular fitness
- Skill training for sport-specific movements

## Recovery
Adequate recovery is essential for progress:
- Rest days between training sessions
- Proper nutrition and hydration
- Quality sleep (7-9 hours)
- Stress management

## Consistency
Regular training is more important than perfect training:
- Aim for 3-5 sessions per week
- Focus on sustainable habits
- Track progress over time
""",
            "nutrition_basics.md": """
# Nutrition Fundamentals

## Macronutrients

### Protein
- Essential for muscle building and repair
- Recommended: 1.6-2.2g per kg body weight
- Sources: lean meats, fish, eggs, dairy, legumes

### Carbohydrates
- Primary energy source for exercise
- Recommended: 3-7g per kg body weight
- Sources: whole grains, fruits, vegetables, potatoes

### Fats
- Essential for hormone production and absorption
- Recommended: 20-35% of total calories
- Sources: nuts, seeds, avocados, olive oil

## Meal Timing
- Pre-workout: 2-3 hours before exercise
- Post-workout: Within 30 minutes after exercise
- Regular meals: Every 3-4 hours

## Hydration
- Drink water throughout the day
- Additional fluids during exercise
- Monitor urine color (pale yellow is ideal)
""",
            "exercise_technique.md": """
# Exercise Technique Guidelines

## General Principles
- Maintain proper form throughout movement
- Control the weight, don't let it control you
- Breathe consistently
- Keep core engaged for stability

## Common Mistakes to Avoid
- Rushing through movements
- Using momentum instead of muscle
- Not maintaining neutral spine
- Locking out joints

## Progression Guidelines
- Master bodyweight movements first
- Add resistance gradually
- Focus on quality over quantity
- Listen to your body for signs of overtraining
""",
            "injury_prevention.md": """
# Injury Prevention Strategies

## Warm-up
- 5-10 minutes of light cardio
- Dynamic stretching
- Movement preparation exercises
- Gradual intensity increase

## Proper Form
- Learn correct technique before adding weight
- Use mirrors or video for feedback
- Consider working with a trainer initially
- Don't sacrifice form for heavier weights

## Recovery
- Adequate rest between sessions
- Proper nutrition and hydration
- Sleep quality and quantity
- Stress management

## Warning Signs
- Sharp pain during exercise
- Persistent soreness beyond 48 hours
- Decreased range of motion
- Swelling or inflammation
"""
        }
        
        knowledge_dir = Path(self.knowledge_base_path)
        for filename, content in default_files.items():
            file_path = knowledge_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        logger.info("Created default knowledge base files")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search knowledge base using simple keyword matching"""
        query_lower = query.lower()
        query_words = set(query_lower.split())
        
        results = []
        
        for doc_id, doc in self.knowledge_base.items():
            content_lower = doc["content"].lower()
            content_words = set(content_lower.split())
            
            # Simple relevance scoring based on word overlap
            overlap = len(query_words.intersection(content_words))
            if overlap > 0:
                relevance_score = overlap / len(query_words)
                
                # Boost score for title matches
                if any(word in doc["source"].lower() for word in query_words):
                    relevance_score += 0.5
                
                results.append({
                    "doc_id": doc_id,
                    "content": doc["content"],
                    "source": doc["source"],
                    "relevance_score": relevance_score
                })
        
        # Sort by relevance score and return top_k results
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return results[:top_k]
    
    def get_context(self, query: str, max_length: int = 2000) -> str:
        """Get relevant context from knowledge base for a query"""
        results = self.search(query, top_k=3)
        
        if not results:
            return "No relevant knowledge found."
        
        context_parts = []
        current_length = 0
        
        for result in results:
            content = result["content"]
            if current_length + len(content) <= max_length:
                context_parts.append(f"From {result['source']}:\n{content}")
                current_length += len(content)
            else:
                # Truncate if needed
                remaining_length = max_length - current_length
                if remaining_length > 100:  # Only add if we have meaningful space
                    truncated_content = content[:remaining_length] + "..."
                    context_parts.append(f"From {result['source']}:\n{truncated_content}")
                break
        
        return "\n\n".join(context_parts)
    
    def add_document(self, content: str, source: str, doc_type: str = "md") -> str:
        """Add a new document to the knowledge base"""
        try:
            # Generate unique ID
            doc_id = hashlib.md5(f"{source}_{datetime.now().isoformat()}".encode()).hexdigest()[:8]
            
            # Chunk the content
            chunks = self._chunk_content(content, source)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{doc_id}_{i}"
                self.knowledge_base[chunk_id] = {
                    "content": chunk,
                    "source": source,
                    "type": doc_type,
                    "created_at": datetime.now().isoformat()
                }
            
            logger.info(f"Added document {source} with {len(chunks)} chunks")
            return doc_id
            
        except Exception as e:
            logger.error(f"Failed to add document: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge base statistics"""
        return {
            "total_documents": len(self.knowledge_base),
            "sources": list(set(doc["source"] for doc in self.knowledge_base.values())),
            "types": list(set(doc["type"] for doc in self.knowledge_base.values())),
            "total_content_length": sum(len(doc["content"]) for doc in self.knowledge_base.values())
        }

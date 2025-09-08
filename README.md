# FeelBot - Emotion-Aware Chatbot

## Overview

FeelBot is an intelligent chatbot application built with Streamlit that provides emotion-aware conversations. The system can detect and analyze emotions from user text input, then generate contextually appropriate responses based on the detected emotional state. The application combines natural language processing for emotion detection with sentiment analysis to create a more empathetic and human-like conversational experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **User Interface**: Chat-based interface with real-time message display
- **Session Management**: Streamlit's session state for maintaining conversation history and user context
- **Visual Feedback**: Emotion indicators using emojis and color-coded sentiment displays

### Backend Architecture
- **Modular Design**: Separated into distinct components for emotion detection and response generation
- **Caching Strategy**: Uses Streamlit's `@st.cache_resource` decorator for model loading optimization
- **Real-time Processing**: Processes user input through emotion detection pipeline before generating responses

### Emotion Detection Engine
- **Primary Library**: NLTK (Natural Language Toolkit) for text processing and sentiment analysis
- **Sentiment Analysis**: TextBlob and NLTK's VADER sentiment analyzer for emotional scoring
- **Keyword Matching**: Rule-based emotion detection using predefined emotion keyword dictionaries
- **Supported Emotions**: Joy, anger, fear, sadness, surprise, disgust, and neutral states
- **Text Preprocessing**: Stopword filtering and text normalization

### Response Generation System
- **Template-Based Responses**: Categorized response templates for different emotional states
- **Response Types**: Acknowledgment, validation, encouragement, and calming responses
- **Contextual Adaptation**: Response selection based on detected emotion and sentiment polarity
- **Personalization**: Dynamic response generation with timestamp and emotional context

### Data Flow
1. User input captured through Streamlit interface
2. Text processed through emotion detection pipeline
3. Emotion and sentiment scores calculated
4. Appropriate response template selected based on emotional context
5. Response generated and displayed with emotional indicators
6. Conversation history maintained in session state

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the user interface
- **NLTK**: Natural language processing toolkit for text analysis and sentiment detection
- **TextBlob**: Simplified text processing library for sentiment analysis

### NLTK Data Packages
- **punkt**: Sentence tokenization
- **stopwords**: Common word filtering
- **vader_lexicon**: Sentiment intensity analysis
- **wordnet**: Word meaning analysis

### Python Standard Library
- **datetime**: Timestamp generation for messages
- **time**: Time-related functionality
- **re**: Regular expression processing for text pattern matching
- **random**: Response template randomization
- **collections**: Data structure utilities for emotion keyword management
- **os**: Operating system interface utilities

The application is designed to run as a self-contained Streamlit application with no external API dependencies, making it suitable for local deployment and testing environments.

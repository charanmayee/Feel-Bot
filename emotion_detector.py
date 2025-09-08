import nltk
import re
from textblob import TextBlob
from collections import defaultdict
import os

class EmotionDetector:
    def __init__(self):
        """Initialize the emotion detector with necessary NLTK data"""
        try:
            # Download required NLTK data
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('vader_lexicon', quiet=True)
            nltk.download('wordnet', quiet=True)
            
            from nltk.corpus import stopwords
            from nltk.sentiment import SentimentIntensityAnalyzer
            
            self.stop_words = set(stopwords.words('english'))
            self.sia = SentimentIntensityAnalyzer()
            
        except Exception as e:
            print(f"Warning: NLTK setup failed: {e}")
            self.stop_words = set()
            self.sia = None
        
        # Define emotion keywords and patterns
        self.emotion_keywords = {
            'joy': [
                'happy', 'joyful', 'excited', 'thrilled', 'elated', 'cheerful', 
                'delighted', 'pleased', 'glad', 'wonderful', 'amazing', 'fantastic',
                'great', 'excellent', 'awesome', 'brilliant', 'superb', 'marvelous',
                'celebrate', 'celebration', 'party', 'fun', 'laugh', 'smile',
                'love', 'adore', 'enjoy', 'bliss', 'ecstatic', 'euphoric'
            ],
            'anger': [
                'angry', 'mad', 'furious', 'rage', 'irritated', 'annoyed',
                'frustrated', 'outraged', 'livid', 'irate', 'pissed', 'hate',
                'disgusted', 'infuriated', 'aggravated', 'hostile', 'bitter',
                'resentful', 'indignant', 'wrathful', 'incensed', 'enraged',
                'damn', 'fuck', 'shit', 'hell', 'stupid', 'idiot', 'moron'
            ],
            'fear': [
                'afraid', 'scared', 'terrified', 'frightened', 'anxious', 'worried',
                'nervous', 'panic', 'dread', 'horror', 'terror', 'phobia',
                'intimidated', 'alarmed', 'concerned', 'uneasy', 'apprehensive',
                'fearful', 'paranoid', 'insecure', 'threatened', 'vulnerable',
                'helpless', 'overwhelmed', 'stress', 'stressed', 'tension'
            ],
            'sadness': [
                'sad', 'depressed', 'unhappy', 'miserable', 'melancholy', 'gloomy',
                'sorrowful', 'mournful', 'grief', 'despair', 'hopeless', 'lonely',
                'isolated', 'abandoned', 'rejected', 'hurt', 'pain', 'suffering',
                'cry', 'crying', 'tears', 'weep', 'sob', 'devastated',
                'heartbroken', 'disappointed', 'discouraged', 'defeated'
            ],
            'surprise': [
                'surprised', 'shocked', 'amazed', 'astonished', 'stunned', 'bewildered',
                'confused', 'puzzled', 'perplexed', 'baffled', 'startled',
                'unexpected', 'sudden', 'wow', 'omg', 'unbelievable', 'incredible',
                'remarkable', 'extraordinary', 'mind-blowing', 'jaw-dropping'
            ],
            'disgust': [
                'disgusted', 'revolted', 'repulsed', 'nauseated', 'sick', 'gross',
                'nasty', 'horrible', 'terrible', 'awful', 'dreadful', 'appalling',
                'repugnant', 'loathsome', 'vile', 'foul', 'offensive', 'distasteful',
                'yuck', 'ew', 'ugh', 'revolting', 'abhorrent', 'detestable'
            ]
        }
        
        # Compile regex patterns for faster matching
        self.emotion_patterns = {}
        for emotion, keywords in self.emotion_keywords.items():
            pattern = r'\b(' + '|'.join(keywords) + r')\b'
            self.emotion_patterns[emotion] = re.compile(pattern, re.IGNORECASE)
    
    def preprocess_text(self, text):
        """Preprocess text for emotion analysis"""
        # Convert to lowercase and remove extra whitespace
        text = re.sub(r'\s+', ' ', text.lower().strip())
        
        # Remove URLs, mentions, and hashtags (social media preprocessing)
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        text = re.sub(r'@\w+', '', text)
        text = re.sub(r'#\w+', '', text)
        
        # Remove excessive punctuation but keep emotional punctuation
        text = re.sub(r'[^\w\s!?.,;:\'"()-]', '', text)
        
        return text
    
    def calculate_emotion_scores(self, text):
        """Calculate emotion scores based on keyword matching"""
        processed_text = self.preprocess_text(text)
        emotion_scores = defaultdict(float)
        total_matches = 0
        
        # Count emotion keyword matches
        for emotion, pattern in self.emotion_patterns.items():
            matches = pattern.findall(processed_text)
            if matches:
                # Weight by frequency and adjust for text length
                score = len(matches) / max(1, len(processed_text.split()) * 0.1)
                emotion_scores[emotion] = score
                total_matches += len(matches)
        
        # Normalize scores
        if total_matches > 0:
            for emotion in emotion_scores:
                emotion_scores[emotion] = emotion_scores[emotion] / total_matches
        
        # Add contextual boosters
        emotion_scores = self.apply_contextual_boosters(processed_text, emotion_scores)
        
        return dict(emotion_scores)
    
    def apply_contextual_boosters(self, text, emotion_scores):
        """Apply contextual rules to boost certain emotions"""
        # Exclamation marks boost intensity
        exclamation_count = text.count('!')
        if exclamation_count > 0:
            boost_factor = min(1.5, 1 + exclamation_count * 0.2)
            for emotion in ['joy', 'anger', 'surprise']:
                if emotion in emotion_scores:
                    emotion_scores[emotion] *= boost_factor
        
        # Question marks can indicate confusion/surprise
        question_count = text.count('?')
        if question_count > 0:
            emotion_scores['surprise'] = emotion_scores.get('surprise', 0) + question_count * 0.1
        
        # All caps words boost anger/excitement
        caps_words = re.findall(r'\b[A-Z]{2,}\b', text.upper())
        if caps_words:
            boost_factor = min(1.3, 1 + len(caps_words) * 0.1)
            for emotion in ['anger', 'joy', 'surprise']:
                if emotion in emotion_scores:
                    emotion_scores[emotion] *= boost_factor
        
        # Repeated letters indicate strong emotion
        repeated_letters = re.findall(r'(.)\1{2,}', text)
        if repeated_letters:
            boost_factor = 1.2
            for emotion in emotion_scores:
                emotion_scores[emotion] *= boost_factor
        
        return emotion_scores
    
    def get_sentiment_analysis(self, text):
        """Get sentiment analysis using TextBlob and NLTK's VADER"""
        # TextBlob sentiment
        try:
            blob = TextBlob(text)
            textblob_polarity = blob.sentiment.polarity
        except Exception as e:
            textblob_polarity = 0.0
        
        # VADER sentiment (if available)
        vader_sentiment = None
        if self.sia:
            try:
                vader_scores = self.sia.polarity_scores(text)
                vader_sentiment = vader_scores['compound']
            except:
                pass
        
        # Combine or use TextBlob as fallback
        if vader_sentiment is not None:
            # Average the two approaches
            combined_score = (textblob_polarity + vader_sentiment) / 2
        else:
            combined_score = textblob_polarity
        
        # Classify sentiment
        if combined_score >= 0.1:
            sentiment = 'positive'
        elif combined_score <= -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'sentiment': sentiment,
            'polarity_score': combined_score,
            'textblob_score': textblob_polarity,
            'vader_score': vader_sentiment
        }
    
    def determine_primary_emotion(self, emotion_scores, sentiment_data):
        """Determine the primary emotion from scores and sentiment"""
        if not emotion_scores:
            # Fallback to sentiment-based emotion
            sentiment = sentiment_data['sentiment']
            if sentiment == 'positive':
                return 'joy'
            elif sentiment == 'negative':
                return 'sadness'
            else:
                return 'neutral'
        
        # Find the emotion with the highest score
        primary_emotion = max(emotion_scores, key=emotion_scores.get)
        
        # Apply minimum threshold
        if emotion_scores[primary_emotion] < 0.1:
            # If no strong emotion detected, use sentiment
            sentiment = sentiment_data['sentiment']
            if sentiment == 'positive':
                return 'joy'
            elif sentiment == 'negative':
                return 'sadness'
            else:
                return 'neutral'
        
        return primary_emotion
    
    def analyze_text(self, text):
        """Main method to analyze text for emotions and sentiment"""
        if not text or not text.strip():
            return {
                'primary_emotion': 'neutral',
                'emotion_scores': {},
                'sentiment': 'neutral',
                'sentiment_data': {'sentiment': 'neutral', 'polarity_score': 0.0},
                'confidence': 0.0
            }
        
        try:
            # Get emotion scores
            emotion_scores = self.calculate_emotion_scores(text)
            
            # Get sentiment analysis
            sentiment_data = self.get_sentiment_analysis(text)
            
            # Determine primary emotion
            primary_emotion = self.determine_primary_emotion(emotion_scores, sentiment_data)
            
            # Calculate confidence score
            if emotion_scores:
                max_score = max(emotion_scores.values())
                confidence = min(0.95, max_score)
            else:
                confidence = abs(sentiment_data['polarity_score']) * 0.7
            
            return {
                'primary_emotion': primary_emotion,
                'emotion_scores': emotion_scores,
                'sentiment': sentiment_data['sentiment'],
                'sentiment_data': sentiment_data,
                'confidence': confidence
            }
            
        except Exception as e:
            # Return neutral analysis on error
            return {
                'primary_emotion': 'neutral',
                'emotion_scores': {},
                'sentiment': 'neutral',
                'sentiment_data': {'sentiment': 'neutral', 'polarity_score': 0.0},
                'confidence': 0.0,
                'error': str(e)
            }

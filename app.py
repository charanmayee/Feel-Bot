import streamlit as st
import time
from datetime import datetime
from emotion_detector import EmotionDetector
from response_generator import ResponseGenerator

# Initialize the emotion detector and response generator
@st.cache_resource
def load_models():
    """Load and cache the emotion detection models"""
    emotion_detector = EmotionDetector()
    response_generator = ResponseGenerator()
    return emotion_detector, response_generator

def initialize_session_state():
    """Initialize session state variables"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add welcome message from FeelBot
        welcome_msg = {
            'role': 'assistant',
            'content': "Hello! I'm FeelBot, your emotion-aware chatbot companion. I can understand not just what you're saying, but how you're feeling too. Feel free to share anything on your mind! 😊",
            'emotion': 'neutral',
            'sentiment': 'neutral',
            'timestamp': datetime.now().strftime("%H:%M")
        }
        st.session_state.messages.append(welcome_msg)
    
    if 'emotion_detector' not in st.session_state:
        st.session_state.emotion_detector, st.session_state.response_generator = load_models()

def get_emotion_emoji(emotion):
    """Get emoji representation for emotions"""
    emotion_emojis = {
        'joy': '😊',
        'anger': '😠',
        'fear': '😨',
        'sadness': '😢',
        'surprise': '😲',
        'disgust': '🤢',
        'neutral': '😐',
        'positive': '🙂',
        'negative': '😔'
    }
    return emotion_emojis.get(emotion, '😐')

def get_sentiment_color(sentiment):
    """Get color for sentiment indicators"""
    colors = {
        'positive': '#4CAF50',
        'negative': '#F44336',
        'neutral': '#9E9E9E'
    }
    return colors.get(sentiment, '#9E9E9E')

def display_message(message, is_user=False):
    """Display a chat message with emotion indicators"""
    with st.container():
        if is_user:
            # User message (right aligned)
            col1, col2 = st.columns([1, 4])
            with col2:
                st.markdown(f"""
                <div style="
                    background-color: #DCF8C6;
                    padding: 10px 15px;
                    border-radius: 18px;
                    margin: 5px 0;
                    margin-left: auto;
                    max-width: 80%;
                    text-align: left;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                ">
                    <strong>You:</strong> {message['content']}
                    <br><small style="color: #666; font-size: 0.8em;">
                        {get_emotion_emoji(message.get('emotion', 'neutral'))} {message.get('emotion', 'neutral').title()} • 
                        <span style="color: {get_sentiment_color(message.get('sentiment', 'neutral'))}">
                            {message.get('sentiment', 'neutral').title()}
                        </span> • {message.get('timestamp', '')}
                    </small>
                </div>
                """, unsafe_allow_html=True)
        else:
            # FeelBot message (left aligned)
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"""
                <div style="
                    background-color: #F1F1F1;
                    padding: 10px 15px;
                    border-radius: 18px;
                    margin: 5px 0;
                    max-width: 80%;
                    text-align: left;
                    box-shadow: 0 1px 2px rgba(0,0,0,0.1);
                ">
                    <strong>🤖 FeelBot:</strong> {message['content']}
                    <br><small style="color: #666; font-size: 0.8em;">
                        {message.get('timestamp', '')}
                    </small>
                </div>
                """, unsafe_allow_html=True)

def main():
    # Page configuration
    st.set_page_config(
        page_title="FeelBot - Emotion-Aware Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Initialize session state
    initialize_session_state()
    
    # Main title and description
    st.title("🤖 FeelBot - Your Emotion-Aware Companion")
    st.markdown("*An advanced chatbot that understands both your words and emotions*")
    
    # Create two columns for layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            # Display all messages
            for message in st.session_state.messages:
                display_message(message, is_user=(message['role'] == 'user'))
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            # Get current timestamp
            current_time = datetime.now().strftime("%H:%M")
            
            # Analyze user's emotion and sentiment
            try:
                emotion_data = st.session_state.emotion_detector.analyze_text(prompt)
                
                # Add user message to chat history
                user_message = {
                    'role': 'user',
                    'content': prompt,
                    'emotion': emotion_data['primary_emotion'],
                    'sentiment': emotion_data['sentiment'],
                    'timestamp': current_time
                }
                st.session_state.messages.append(user_message)
                
                # Generate appropriate response based on emotion
                bot_response = st.session_state.response_generator.generate_response(
                    user_input=prompt,
                    emotion=emotion_data['primary_emotion'],
                    sentiment=emotion_data['sentiment'],
                    emotion_scores=emotion_data['emotion_scores']
                )
                
                # Add bot response to chat history
                bot_message = {
                    'role': 'assistant',
                    'content': bot_response,
                    'timestamp': current_time
                }
                st.session_state.messages.append(bot_message)
                
            except Exception as e:
                # Handle emotion analysis errors gracefully
                st.error(f"Error analyzing emotions: {str(e)}")
                
                # Add user message without emotion data
                user_message = {
                    'role': 'user',
                    'content': prompt,
                    'emotion': 'neutral',
                    'sentiment': 'neutral',
                    'timestamp': current_time
                }
                st.session_state.messages.append(user_message)
                
                # Generate neutral response
                bot_response = "I'm having trouble understanding your emotions right now, but I'm here to help! Could you tell me more about how you're feeling?"
                
                bot_message = {
                    'role': 'assistant',
                    'content': bot_response,
                    'timestamp': current_time
                }
                st.session_state.messages.append(bot_message)
            
            # Rerun to update the chat
            st.rerun()
    
    with col2:
        # Sidebar with statistics and controls
        st.subheader("📊 Emotion Analytics")
        
        if len(st.session_state.messages) > 1:  # Exclude welcome message
            # Analyze conversation emotions
            user_messages = [msg for msg in st.session_state.messages if msg['role'] == 'user']
            
            if user_messages:
                # Count emotions
                emotion_counts = {}
                sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
                
                for msg in user_messages:
                    emotion = msg.get('emotion', 'neutral')
                    sentiment = msg.get('sentiment', 'neutral')
                    
                    emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
                    sentiment_counts[sentiment] += 1
                
                # Display emotion distribution
                st.write("**Detected Emotions:**")
                for emotion, count in emotion_counts.items():
                    percentage = (count / len(user_messages)) * 100
                    st.write(f"{get_emotion_emoji(emotion)} {emotion.title()}: {percentage:.1f}%")
                
                st.write("**Sentiment Distribution:**")
                for sentiment, count in sentiment_counts.items():
                    percentage = (count / len(user_messages)) * 100
                    color = get_sentiment_color(sentiment)
                    st.markdown(f'<span style="color: {color}">● {sentiment.title()}: {percentage:.1f}%</span>', unsafe_allow_html=True)
        else:
            st.write("Start chatting to see emotion analytics!")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", help="Clear all messages and start fresh"):
            st.session_state.messages = []
            # Re-add welcome message
            welcome_msg = {
                'role': 'assistant',
                'content': "Hello! I'm FeelBot, your emotion-aware chatbot companion. I can understand not just what you're saying, but how you're feeling too. Feel free to share anything on your mind! 😊",
                'emotion': 'neutral',
                'sentiment': 'neutral',
                'timestamp': datetime.now().strftime("%H:%M")
            }
            st.session_state.messages.append(welcome_msg)
            st.rerun()
        
        # About section
        with st.expander("ℹ️ About FeelBot"):
            st.write("""
            **FeelBot** is an advanced emotion-aware chatbot that:
            
            - 🎭 Detects 6 core emotions: joy, anger, fear, sadness, surprise, disgust
            - 💭 Analyzes sentiment: positive, negative, neutral  
            - 🎯 Provides contextually appropriate responses
            - 📈 Tracks emotional patterns in conversations
            - 🤝 Responds with empathy and understanding
            
            Built with TextBlob and NLTK for accurate emotion detection.
            """)

if __name__ == "__main__":
    main()

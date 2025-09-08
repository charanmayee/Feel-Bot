import random
import re
from datetime import datetime

class ResponseGenerator:
    def __init__(self):
        """Initialize the response generator with emotion-specific templates"""
        
        # Response templates for different emotions
        self.emotion_responses = {
            'joy': {
                'acknowledgment': [
                    "I can feel your happiness radiating through your words! 😊",
                    "Your joy is absolutely contagious! That's wonderful! ✨",
                    "I love seeing you so happy and excited! 🌟",
                    "Your positive energy is amazing! Keep that smile going! 😄",
                    "That's fantastic! Your enthusiasm really brightens my day! 🌈"
                ],
                'encouragement': [
                    "This is such great news! Tell me more about what's making you so happy!",
                    "I'm so glad things are going well for you! What's the best part?",
                    "Your happiness is inspiring! How can we keep this positive momentum going?",
                    "Wonderful! Moments like these are what life is all about!",
                    "I'm thrilled for you! What are you most looking forward to next?"
                ],
                'celebration': [
                    "Let's celebrate this moment together! 🎉",
                    "You deserve all this happiness! Enjoy every second of it! 🎊",
                    "This calls for a virtual high-five! ✋",
                    "I'm doing a happy dance over here! 💃",
                    "Time to party! Your joy is the best kind of energy! 🎈"
                ]
            },
            'anger': {
                'acknowledgment': [
                    "I can sense you're really frustrated right now, and that's completely understandable.",
                    "Your anger is valid - it sounds like you're dealing with something really challenging.",
                    "I hear you, and I can tell this situation is really getting to you.",
                    "It's clear you're upset, and you have every right to feel that way.",
                    "I understand you're angry - sometimes things just push us to our limit."
                ],
                'validation': [
                    "It's okay to feel angry when things aren't fair or going right.",
                    "Your feelings are completely justified - anyone would be upset in your situation.",
                    "Anger can actually show us what we care deeply about.",
                    "It's natural to feel this way when you're facing such challenges.",
                    "You're not wrong to feel angry - this sounds really difficult."
                ],
                'calming': [
                    "Take a deep breath with me. Let's work through this together.",
                    "What would help you feel a bit calmer right now?",
                    "Sometimes talking through our anger can help us find a path forward.",
                    "I'm here to listen without judgment. What's weighing on you most?",
                    "Let's focus on what's within your control. What small step could help?"
                ]
            },
            'fear': {
                'reassurance': [
                    "I can tell you're feeling scared or anxious, and I want you to know you're not alone.",
                    "Fear can be overwhelming, but you're stronger than you realize.",
                    "It's brave of you to share these feelings with me. You're safe here.",
                    "I'm here with you through this. We can face this worry together.",
                    "Your fear is understandable - many people would feel the same way."
                ],
                'support': [
                    "What would help you feel a little safer or more secure right now?",
                    "Sometimes naming our fears helps reduce their power over us.",
                    "You've overcome challenges before - what helped you then?",
                    "Let's break this down into smaller, more manageable pieces.",
                    "I believe in your ability to handle whatever you're facing."
                ],
                'grounding': [
                    "Let's focus on the present moment. What are three things you can see around you?",
                    "Take a moment to feel your feet on the ground. You're here, you're safe.",
                    "Breathe with me - in for 4, hold for 4, out for 4.",
                    "What's one small thing that always makes you feel a bit better?",
                    "Remember, this feeling will pass. You don't have to carry it forever."
                ]
            },
            'sadness': {
                'empathy': [
                    "I can feel the sadness in your words, and I'm so sorry you're going through this.",
                    "It sounds like you're carrying a heavy heart right now. I'm here for you.",
                    "Your sadness is valid and important. Thank you for sharing it with me.",
                    "I wish I could give you a comforting hug right now. Please know I care.",
                    "It takes courage to express sadness. I'm honored you trust me with these feelings."
                ],
                'comfort': [
                    "It's okay to feel sad - it shows how much you care and how deeply you feel.",
                    "Sadness is a natural response to loss and disappointment. Be gentle with yourself.",
                    "You don't have to be strong all the time. It's okay to let yourself feel this.",
                    "Even in sadness, you're not alone. I'm here to sit with you in this feeling.",
                    "This pain you're feeling is real, and it matters. Your feelings matter."
                ],
                'hope': [
                    "While I can't take away your pain, I believe brighter days are ahead for you.",
                    "You have so much strength, even when you don't feel it. This won't last forever.",
                    "Small steps count. What's one tiny thing that might bring a moment of peace?",
                    "Your heart is capable of healing, even if it doesn't feel that way now.",
                    "You matter more than you know, especially on days when it's hard to believe."
                ]
            },
            'surprise': {
                'excitement': [
                    "Wow, that sounds unexpected! I'm curious to hear more!",
                    "What a surprise! Life certainly has interesting ways of keeping us on our toes!",
                    "That's amazing! I love when life throws us pleasant surprises!",
                    "How exciting! Unexpected moments can be the most memorable ones!",
                    "That caught me off guard too! What was your first reaction?"
                ],
                'curiosity': [
                    "I'm so intrigued! Tell me everything - how did that happen?",
                    "What an interesting turn of events! How are you processing all of this?",
                    "That's fascinating! What surprised you the most about the whole situation?",
                    "I'm on the edge of my seat! What happened next?",
                    "That's incredible! How did you handle such an unexpected moment?"
                ]
            },
            'disgust': {
                'understanding': [
                    "I can tell something really bothered or disgusted you - that must have been unpleasant.",
                    "It sounds like you encountered something that really didn't sit well with you.",
                    "That sounds genuinely awful - I completely understand your reaction.",
                    "I can hear the disgust in your words, and I don't blame you one bit.",
                    "Some things are just genuinely hard to stomach - your reaction is totally normal."
                ],
                'support': [
                    "I'm sorry you had to experience something so off-putting.",
                    "It's okay to feel disgusted when something violates your values or comfort.",
                    "You have every right to feel repulsed by things that go against your standards.",
                    "Sometimes we encounter things that just feel wrong - trust your instincts.",
                    "That sounds really unpleasant. How can we help you feel better about it?"
                ]
            },
            'neutral': {
                'engagement': [
                    "I'm here and ready to chat! What's on your mind today?",
                    "Thank you for sharing that with me. I'm listening!",
                    "That's interesting. Tell me more about what you're thinking.",
                    "I appreciate you taking the time to talk with me. How can I help?",
                    "I'm glad you're here! What would you like to explore together?"
                ],
                'curiosity': [
                    "What brings you here today? I'm curious to learn more about you!",
                    "That's a thoughtful perspective. What's been on your mind lately?",
                    "I'd love to hear more about what matters to you right now.",
                    "Thanks for sharing! What else would you like to talk about?",
                    "I'm interested in your thoughts. What's something you've been pondering?"
                ]
            }
        }
        
        # Transition phrases to make responses flow naturally
        self.transitions = [
            "By the way,", "Also,", "I'm curious,", "Tell me,", 
            "What do you think about", "I wonder", "Speaking of which,"
        ]
        
        # Follow-up questions based on emotions
        self.follow_up_questions = {
            'joy': [
                "What's been the highlight of your day?",
                "Who else have you shared this good news with?",
                "What are you most grateful for right now?",
                "How long have you been feeling this happy?",
                "What do you think contributed most to this positive feeling?"
            ],
            'anger': [
                "What do you think would help resolve this situation?",
                "Have you been able to talk to anyone else about this?",
                "What's the most frustrating part of all this?",
                "Is this something new or has it been building up?",
                "What would need to change for you to feel better about this?"
            ],
            'fear': [
                "What's the worst part about this worry for you?",
                "Have you felt this way before? What helped then?",
                "Is there someone who makes you feel safer when you're scared?",
                "What would you tell a friend who was feeling the same way?",
                "What's one small step you could take to feel a bit more in control?"
            ],
            'sadness': [
                "How long have you been feeling this way?",
                "Is there anything that usually helps when you're sad?",
                "Do you feel comfortable talking about what's making you sad?",
                "What's something small that might bring you a moment of comfort?",
                "Have you been able to take care of yourself during this difficult time?"
            ],
            'surprise': [
                "How did you react when this first happened?",
                "Is this a good surprise or a challenging one?",
                "What do you think will happen next?",
                "How has this changed your perspective on things?",
                "What's the most surprising part of all this?"
            ],
            'disgust': [
                "What made this particularly hard to deal with?",
                "Is this something you encounter often?",
                "How do you usually handle situations like this?",
                "What would help you feel better after experiencing something so unpleasant?",
                "Is there a way to avoid similar situations in the future?"
            ],
            'neutral': [
                "What's something interesting that happened to you recently?",
                "How has your day been going so far?",
                "Is there anything particular you'd like to talk about?",
                "What's been occupying your thoughts lately?",
                "What would make today feel like a good day for you?"
            ]
        }
    
    def generate_response(self, user_input, emotion, sentiment, emotion_scores):
        """Generate an appropriate response based on detected emotion and sentiment"""
        try:
            # Get response templates for the detected emotion
            emotion_templates = self.emotion_responses.get(emotion, self.emotion_responses['neutral'])
            
            # Select response components based on emotion intensity and type
            response_parts = []
            
            # Start with acknowledgment/empathy
            if emotion in ['anger', 'fear', 'sadness', 'disgust']:
                # Negative emotions need validation and support
                if 'acknowledgment' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['acknowledgment']))
                elif 'empathy' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['empathy']))
                elif 'reassurance' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['reassurance']))
                elif 'understanding' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['understanding']))
            
            elif emotion in ['joy', 'surprise']:
                # Positive emotions get celebration and excitement
                if 'acknowledgment' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['acknowledgment']))
                elif 'excitement' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['excitement']))
            
            else:
                # Neutral emotions get engaging responses
                if 'engagement' in emotion_templates:
                    response_parts.append(random.choice(emotion_templates['engagement']))
            
            # Add supportive/encouraging content
            if emotion == 'anger' and 'calming' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['calming']))
            elif emotion == 'fear' and 'support' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['support']))
            elif emotion == 'sadness' and 'comfort' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['comfort']))
            elif emotion == 'joy' and 'encouragement' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['encouragement']))
            elif emotion == 'surprise' and 'curiosity' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['curiosity']))
            elif emotion == 'disgust' and 'support' in emotion_templates:
                response_parts.append(random.choice(emotion_templates['support']))
            
            # Add follow-up question
            follow_ups = self.follow_up_questions.get(emotion, self.follow_up_questions['neutral'])
            follow_up = random.choice(follow_ups)
            response_parts.append(follow_up)
            
            # Combine response parts
            if len(response_parts) == 1:
                full_response = response_parts[0]
            elif len(response_parts) == 2:
                full_response = f"{response_parts[0]} {response_parts[1]}"
            else:
                # Add transition for longer responses
                transition = random.choice(self.transitions)
                full_response = f"{response_parts[0]} {transition} {' '.join(response_parts[1:])}"
            
            # Add personalization based on emotion intensity
            if emotion_scores and max(emotion_scores.values()) > 0.7:
                # High intensity emotion - more emphatic response
                full_response = self.add_intensity_markers(full_response, emotion)
            
            return full_response
            
        except Exception as e:
            # Fallback response
            return f"I can sense you're feeling {emotion}, and I want you to know I'm here to listen and support you. What's on your mind?"
    
    def add_intensity_markers(self, response, emotion):
        """Add intensity markers for strong emotions"""
        if emotion == 'joy':
            # Add more enthusiasm
            if not response.endswith(('!', '?')):
                response += '!'
            return response
        
        elif emotion in ['anger', 'fear', 'sadness']:
            # Add more empathy markers
            empathy_additions = [
                "I really hear you on this.",
                "This sounds genuinely difficult.",
                "I can only imagine how tough this must be.",
                "Your feelings make complete sense."
            ]
            addition = random.choice(empathy_additions)
            return f"{response} {addition}"
        
        elif emotion == 'surprise':
            # Add more excitement/curiosity
            if '!' not in response:
                response = response.replace('.', '!')
            return response
        
        return response
    
    def personalize_response(self, response, user_input):
        """Add personalization based on user's specific input"""
        # Extract key topics or concerns from user input
        user_lower = user_input.lower()
        
        # Add contextual understanding
        if any(word in user_lower for word in ['work', 'job', 'boss', 'colleague']):
            response += " Work situations can be especially challenging to navigate."
        
        elif any(word in user_lower for word in ['family', 'parent', 'mom', 'dad', 'sister', 'brother']):
            response += " Family relationships can bring up such complex emotions."
        
        elif any(word in user_lower for word in ['relationship', 'partner', 'boyfriend', 'girlfriend', 'spouse']):
            response += " Relationships require so much emotional energy and care."
        
        elif any(word in user_lower for word in ['school', 'study', 'exam', 'test', 'grade']):
            response += " Academic pressure can really weigh on us."
        
        elif any(word in user_lower for word in ['health', 'sick', 'doctor', 'hospital']):
            response += " Health concerns can be so worrying and overwhelming."
        
        return response

from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatBot:
    def __init__(self):
        try:
            logger.info("Loading BlenderBot model and tokenizer...")
            self.tokenizer = BlenderbotTokenizer.from_pretrained("facebook/blenderbot-400M-distill")
            self.model = BlenderbotForConditionalGeneration.from_pretrained("facebook/blenderbot-400M-distill")
            self.image_context = None  # Store image context
            self.conversation_history = []  # Store conversation history
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise

    def set_image_context(self, label, confidence):
        """Set the current image context for the chatbot."""
        self.image_context = {
            'label': label,
            'confidence': confidence
        }

    def respond(self, user_input):
        try:
            if not user_input or not user_input.strip():
                return "Please provide a valid input."
            
            # Add image context to the input if available
            if self.image_context:
                # Emphasize the image context in the input
                user_input = (
                    f"The image shows a {self.image_context['label']} with {self.image_context['confidence']}% confidence. "
                    f"Please focus on the image when answering questions about it. {user_input}"
                )
                self.image_context = None  # Reset image context after using it
            
            # Add user input to conversation history
            self.conversation_history.append(f"User: {user_input}")
            
            # Generate response
            inputs = self.tokenizer([user_input], return_tensors="pt")
            reply_ids = self.model.generate(**inputs)
            response = self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]
            
            # Add bot response to conversation history
            self.conversation_history.append(f"Bot: {response}")
            
            # Ensure response is not empty
            if not response.strip():
                return "I'm not sure how to respond to that. Can you rephrase?"
            
            return response
        
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "Sorry, I'm having trouble responding right now."
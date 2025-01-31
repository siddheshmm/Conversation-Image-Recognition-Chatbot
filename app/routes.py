from flask import render_template, request, jsonify
import os

def configure_routes(app):
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/upload', methods=['POST'])
    def upload_image():
        if 'file' not in request.files:
            return jsonify(error="No file uploaded"), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify(error="Empty filename"), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        label, confidence = app.image_recognizer.predict(filepath)
        
        # Set image context in chatbot
        app.chatbot.set_image_context(label, confidence)
        
        return jsonify({
            'image_url': filepath,
            'prediction': label,
            'confidence': confidence
        })

    @app.route('/chat', methods=['POST'])
    def handle_chat():
        try:
            user_message = request.json.get('message')
            if not user_message or not user_message.strip():
                return jsonify({'error': 'Empty message'}), 400
            
            response = app.chatbot.respond(user_message.strip())
            return jsonify({'response': response})
        
        except Exception as e:
            print(f"Chat error: {str(e)}")
            return jsonify({'error': 'Failed to generate response'}), 500
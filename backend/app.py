from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def init_db():
    try:
        logger.info("Initializing database...")
        conn = sqlite3.connect('college_faq.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS faqs
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    category TEXT NOT NULL)''')
        
        # Insert some sample FAQs
        sample_faqs = [
            # Admissions Related
            ("What are the admission requirements?", "For undergraduate programs, you need:\n- Minimum 60% in 12th grade\n- Valid entrance exam score (JEE/SAT)\n- English proficiency test scores (IELTS/TOEFL)\n- Letter of recommendation\n- Statement of purpose", "Admissions"),
            ("When is the application deadline?", "The application deadlines are:\n- Early Decision: November 15\n- Regular Decision: January 15\n- Transfer Students: March 1", "Admissions"),
            ("How can I apply for admission?", "You can apply through:\n1. Online application portal at college-website.com/apply\n2. Common Application\n3. Submit required documents and pay application fee ($50)\n4. Track your application status online", "Admissions"),
            
            # Courses and Academics
            ("What courses do you offer?", "We offer various undergraduate programs including:\n- Computer Science and Engineering\n- Electrical Engineering\n- Mechanical Engineering\n- Civil Engineering\n- Business Administration\n- Psychology\n- Liberal Arts", "Courses"),
            ("What is the duration of courses?", "Course durations:\n- Bachelor's Programs: 4 years\n- Master's Programs: 2 years\n- PhD Programs: 3-5 years", "Courses"),
            ("Are there any specialization options?", "Yes, we offer specializations in:\n- AI and Machine Learning\n- Data Science\n- Robotics\n- Digital Marketing\n- Finance\n- Environmental Engineering", "Courses"),
            
            # Fees and Financial Aid
            ("What is the fee structure?", "Annual fees for 2025-26:\n- Tuition: $35,000\n- Housing: $12,000\n- Meal Plan: $5,000\n- Books and Supplies: $2,000\n- Total: $54,000", "Fees"),
            ("Is financial aid available?", "Yes, we offer various financial aid options:\n- Merit-based scholarships\n- Need-based grants\n- Work-study programs\n- Student loans\n- Athletic scholarships", "Fees"),
            ("How can I apply for scholarships?", "To apply for scholarships:\n1. Submit FAFSA form\n2. Complete scholarship application\n3. Provide required documents\n4. Meet application deadlines\n5. Maintain required GPA", "Fees"),
            
            # Campus Life
            ("What accommodation options are available?", "We offer:\n- On-campus dormitories\n- Shared apartments\n- Single rooms\n- Family housing\nAll accommodations include Wi-Fi, laundry facilities, and 24/7 security.", "Campus"),
            ("What facilities are available on campus?", "Our campus features:\n- Modern libraries\n- Research laboratories\n- Sports complex\n- Student center\n- Health center\n- Cafeterias\n- 24/7 study spaces", "Campus"),
            ("Are there any sports facilities?", "Yes, we have:\n- Olympic-size swimming pool\n- Indoor sports complex\n- Football field\n- Basketball courts\n- Tennis courts\n- Fitness center", "Campus"),
            
            # Career Services
            ("What career services do you provide?", "Our career services include:\n- Resume writing workshops\n- Mock interviews\n- Job fairs\n- Industry connections\n- Internship placements\n- Career counseling", "Career"),
            ("Do you offer placement assistance?", "Yes, we have a dedicated placement cell that:\n- Arranges campus interviews\n- Provides company-specific training\n- Helps with interview preparation\n- Maintains industry connections\n- Tracks placement statistics", "Career"),
            
            # Contact Information
            ("How can I contact the college?", "You can reach us through:\n- Email: info@college.edu\n- Phone: (555) 123-4567\n- Address: 123 College Street, City, State 12345\n- Website: www.college.edu\n- Social Media: @CollegeName", "Contact")
        ]
        
        c.executemany('INSERT OR IGNORE INTO faqs (question, answer, category) VALUES (?, ?, ?)', sample_faqs)
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully!")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise

def get_response(query):
    try:
        conn = sqlite3.connect('college_faq.db')
        c = conn.cursor()
        
        # Simple keyword matching
        c.execute('''SELECT answer FROM faqs 
                    WHERE LOWER(question) LIKE ? 
                    OR LOWER(answer) LIKE ?''', 
                    ('%' + query.lower() + '%', '%' + query.lower() + '%'))
        
        result = c.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return "I'm sorry, I don't have information about that. Please contact the college administration for more details."
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        return "I apologize, but I'm having trouble accessing the database right now."

@app.route('/')
def home():
    try:
        logger.info("Serving home page...")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error serving home page: {e}")
        return "Error loading the chat interface", 500

@app.route('/ask', methods=['POST'])
def ask():
    try:
        user_message = request.json['message']
        logger.info(f"Received question: {user_message}")
        response = get_response(user_message)
        logger.info(f"Sending response for question")
        return jsonify({'response': response})
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        return jsonify({'response': 'Sorry, there was an error processing your request.'}), 500

if __name__ == '__main__':
    try:
        init_db()
        logger.info("Starting Flask server on port 8081...")
        # Add host='0.0.0.0' to make it accessible from other devices
        app.run(host='0.0.0.0', port=8081, debug=False)
    except Exception as e:
        logger.error(f"Error starting the application: {e}")
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")

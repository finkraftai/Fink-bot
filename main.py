# from flask import Flask, request, jsonify
# import mysql.connector
# from mysql.connector import Error as MySQLError, errorcode
# import json
# from fuzzywuzzy import fuzz
# import openai

# # MySQL connection configuration
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'kaviyam@1410',
#     'database': 'STUDENT1',
#     'raise_on_warnings': True
# }

# # Initialize Flask application
# app = Flask(__name__)

# # Load Finkraft data from JSON file
# with open('finkraft_data.json', 'r') as file:
#     finkraft_data = json.load(file)

# # Initialize OpenAI client
# client = openai.AzureOpenAI(
#     azure_endpoint="https://finkdataopenai.openai.azure.com/",
#     api_key='d57b4f240c6f4c12bb8d316469e45f69',
#     api_version="2024-02-15-preview"
# )

# def extract_information(data, query, threshold=80):
#     """
#     Recursively extract relevant information from nested data based on the user's query
#     with fuzzy matching.
#     """
#     # Normalize the query
#     query = query.lower()
    
#     # Define a list to hold matching values
#     extracted_values = []
    
#     if isinstance(data, dict):
#         for key, value in data.items():
#             if fuzz.partial_ratio(query, key.lower()) >= threshold:
#                 if isinstance(value, (dict, list)):
#                     nested_values = extract_information(value, query, threshold)
#                     extracted_values.extend(nested_values)
#                 else:
#                     extracted_values.append(str(value))
#             elif isinstance(value, (dict, list)):
#                 nested_values = extract_information(value, query, threshold)
#                 extracted_values.extend(nested_values)
#     elif isinstance(data, list):
#         for item in data:
#             nested_values = extract_information(item, query, threshold)
#             extracted_values.extend(nested_values)
    
#     return extracted_values

# def is_related_to_finkraft(query):
#     """
#     Check if the query is related to FinKraft AI using fuzzy matching.
#     Adjust the threshold as needed for accuracy.
#     """
#     keywords = ["finkraft", "fink", "fink ai", "finkraft ai"]
#     query = query.lower()
    
#     for keyword in keywords:
#         if fuzz.partial_ratio(query, keyword) >= 90:  # Adjust threshold as needed
#             return True
#     return False

# def query(user_input, cursor, conn, email_id):
#     try:
#         # Check if the query is related to FinKraft AI
#         if not is_related_to_finkraft(user_input):
#             return "I'm a chatbot providing information about FinKraft AI. Please ask about FinKraft AI."

#         # Extract relevant information from finkraft_data
#         info = extract_information(finkraft_data, user_input)

#         if info:
#             # Format the extracted information
#             bot_response = "\n".join(info)
#         else:
#             # Call OpenAI API using appropriate method if info not found in JSON
#             completion = client.chat.completions.create(
#                 model="gpt-35-turbo",
#                 messages=[
#                     {"role": "system", "content": "I'm a chatbot providing information about FinKraft AI. Here is the FinKraft AI data."},
#                     {"role": "user", "content": user_input}
#                 ],
#                 temperature=0.7,
#                 max_tokens=150,
#                 top_p=1.0,
#                 frequency_penalty=0,
#                 presence_penalty=0,
#                 stop=None
#             )
#             bot_response = completion.choices[0].message.content

#         # Update conversation in the MySQL database
#         update_row(cursor, conn, email_id, user_input, bot_response)
#         return bot_response

#     except MySQLError as err:
#         print(f"MySQL error: {err}")
#         return None

# def create_table(cursor):
#     table_schema = (
#         "CREATE TABLE IF NOT EXISTS CHATGPT ("
#         "  email_id VARCHAR(255) PRIMARY KEY,"
#         "  user_input TEXT NOT NULL,"
#         "  bot_response TEXT NOT NULL"
#         ")"
#     )
#     try:
#         cursor.execute(table_schema)
#     except MySQLError as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("CHATGPT table already exists.")
#         else:
#             print(err.msg)

# def update_row(cursor, conn, email_id, user_input, bot_response):
#     update_query = (
#         "UPDATE CHATGPT "
#         "SET user_input = CONCAT(user_input, %s), "
#         "    bot_response = CONCAT(bot_response, %s) "
#         "WHERE email_id = %s"
#     )
#     cursor.execute(update_query, (f'\nUser: {user_input}', f'\nBot: {bot_response}', email_id))
#     conn.commit()

# @app.route('/chat', methods=['POST'])
# def chat():
#     try:
#         data = request.get_json()
#         user_input = data['message']
#         email_id = 'dummy@example.com'  # Replace with actual email retrieval logic

#         # Connect to MySQL
#         conn = mysql.connector.connect(**mysql_config)
#         cursor = conn.cursor()

#         # Ensure table exists
#         create_table(cursor)

#         # Query and get bot response
#         bot_response = query(user_input, cursor, conn, email_id)

#         # Close connection
#         cursor.close()
#         conn.close()

#         return jsonify({'response': bot_response})

#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == "__main__":
#     app.run(debug=True)




# from flask import Flask, request, jsonify
# import openai
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Your API key and endpoint
# client = openai.AzureOpenAI(
#     azure_endpoint="https://finkdataopenai.openai.azure.com/",
#     api_key='d57b4f240c6f4c12bb8d316469e45f69',
#     api_version="2024-02-15-preview"
# )

# def query(user_input):
#     completion = client.chat.completions.create(
#         model="gpt-35-turbo",
#         messages=[
#             {"role": "system", "content": "I'm a chat bot"},
#             {"role": "user", "content": user_input}
#         ],
#         temperature=0.7,
#         max_tokens=150,
#         top_p=1.0,
#         frequency_penalty=0,
#         presence_penalty=0,
#         stop=None
#     )
#     bot_response = completion.choices[0].message.content
#     return bot_response

# @app.route('/chat', methods=['POST'])
# def chat():
#     user_input = request.json.get('message')
#     response = query(user_input)
#     return jsonify({'response': response})

# if __name__ == "__main__":
#     app.run(debug=True)






# from flask import Flask, request, jsonify
# from mysql.connector import errorcode
# from flask_cors import CORS
# import mysql.connector
# import openai
# import json
# app = Flask(__name__)
# CORS(app)
# # MySQL connection configuration
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'kaviyam@1410',
#     'database': 'STUDENT1',
#     'raise_on_warnings': True
# }
# # Initialize OpenAI client
# client = openai.AzureOpenAI(
#     azure_endpoint="https://finkdataopenai.openai.azure.com/",
#     api_key='d57b4f240c6f4c12bb8d316469e45f69',
#     api_version="2024-02-15-preview"
# )
# # Load FinKraft data from JSON file
# with open('finkraft_data.json', 'r') as file:
#     finkraft_data = json.load(file)
# def extract_information(query):
#     query = query.lower()
#     extracted_info = {}
#     for key, value in finkraft_data.items():
#         if key.lower() in query:
#             extracted_info[key] = value
#     if extracted_info:
#         response = ""
#         for key, value in extracted_info.items():
#             response += f"{key}:\n{value}\n\n"
#         return response.strip()
#     else:
#         return None
# def create_table(cursor):
#     table_schema = (
#         "CREATE TABLE IF NOT EXISTS CHATGPT ("
#         "  id INT AUTO_INCREMENT PRIMARY KEY,"
#         "  email_id VARCHAR(255),"
#         "  user_input TEXT NOT NULL,"
#         "  bot_response TEXT NOT NULL"
#         ")"
#     )
#     try:
#         cursor.execute(table_schema)
#     except mysql.connector.Error as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("CHATGPT table already exists.")
#         else:
#             print(err.msg)
# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_input = data.get('message')
#     email_id = data.get('email')  # Assuming email is passed in the request
#     conn = None
#     cursor = None
#     try:
#         conn = mysql.connector.connect(**mysql_config)
#         cursor = conn.cursor()
#         # Drop the existing table (if exists) and create a new one with the correct schema
#         cursor.execute("DROP TABLE IF EXISTS CHATGPT")
#         create_table(cursor)
#         info = extract_information(user_input)
#         if info:
#             bot_response = info
#         else:
#             completion = client.chat.completions.create(
#                 model="gpt-35-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are Fink, a chatbot for FinKraft AI. Provide detailed and user-friendly information to the users."},
#                     {"role": "user", "content": user_input}
#                 ],
#                 temperature=0.7,
#                 max_tokens=150,
#                 top_p=1.0,
#                 frequency_penalty=0,
#                 presence_penalty=0,
#                 stop=None
#             )
#             bot_response = completion.choices[0].message.content
#         insert_query = "INSERT INTO CHATGPT (email_id, user_input, bot_response) VALUES (%s, %s, %s)"
#         insert_data = (email_id, user_input, bot_response)
#         print(insert_data)
#         cursor.execute(insert_query, insert_data)
#         conn.commit()
#         return jsonify({'response': bot_response})
#     except mysql.connector.Error as err:
#         print(f"MySQL error: {err}")
#         return jsonify({'response': 'Database error.'}), 500
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()
# if __name__ == '__main__':
#     app.run(debug=True)




#my fixed code below

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import mysql.connector
# from mysql.connector import Error as MySQLError, errorcode
# import openai
# import json

# app = Flask(__name__)
# CORS(app)

# # MySQL connection configuration
# mysql_config = {
#     'host': 'localhost',
#     'user': 'root',
#     'password': 'kaviyam@1410',
#     'database': 'STUDENT1',
#     'raise_on_warnings': True
# }

# # Initialize OpenAI client
# client = openai.AzureOpenAI(
#     azure_endpoint="https://finkdataopenai.openai.azure.com/",
#     api_key='d57b4f240c6f4c12bb8d316469e45f69',
#     api_version="2024-02-15-preview"
# )

# # Load FinKraft data from JSON file
# with open('finkraft_data.json', 'r') as file:
#     finkraft_data = json.load(file)

# def extract_information(query):
#     query = query.lower()
#     extracted_info = {}
#     for key, value in finkraft_data.items():
#         if key.lower() in query:
#             extracted_info[key] = value
#     if extracted_info:
#         response = ""
#         for key, value in extracted_info.items():
#             response += f"{key}:\n{value}\n\n"
#         return response.strip()
#     else:
#         return None

# def create_table(cursor):
#     table_schema = (
#         "CREATE TABLE IF NOT EXISTS CHATGPT ("
#         "  id INT AUTO_INCREMENT PRIMARY KEY,"
#         "  email_id VARCHAR(255),"
#         "  user_input TEXT NOT NULL,"
#         "  bot_response TEXT NOT NULL"
#         ")"
#     )
#     try:
#         cursor.execute(table_schema)
#     except MySQLError as err:
#         if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
#             print("CHATGPT table already exists.")
#         else:
#             print(err.msg)

# @app.route('/chat', methods=['POST'])
# def chat():
#     data = request.json
#     user_input = data.get('message')
#     email_id = data.get('email')  # Assuming email is passed in the request
#     conn = None
#     cursor = None
#     try:
#         conn = mysql.connector.connect(**mysql_config)
#         cursor = conn.cursor()
        
#         # Create table if not exists
#         create_table(cursor)
        
#         # Extract information from local data or OpenAI if not found
#         info = extract_information(user_input)
#         if info:
#             bot_response = info
#         else:
#             completion = client.chat.completions.create(
#                 model="gpt-35-turbo",
#                 messages=[
#                     {"role": "system", "content": "You are Fink, a chatbot for FinKraft AI. Provide detailed and user-friendly information to the users."},
#                     {"role": "user", "content": user_input}
#                 ],
#                 temperature=0.7,
#                 max_tokens=150,
#                 top_p=1.0,
#                 frequency_penalty=0,
#                 presence_penalty=0,
#                 stop=None
#             )
#             bot_response = completion.choices[0].message.content
        
#         # Insert conversation into the database
#         insert_query = "INSERT INTO CHATGPT (email_id, user_input, bot_response) VALUES (%s, %s, %s)"
#         insert_data = (email_id, user_input, bot_response)
#         cursor.execute(insert_query, insert_data)
#         conn.commit()
        
#         return jsonify({'response': bot_response})
    
#     except MySQLError as err:
#         print(f"MySQL error: {err}")
#         return jsonify({'response': 'Database error.'}), 500
    
#     finally:
#         if cursor:
#             cursor.close()
#         if conn:
#             conn.close()

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error as MySQLError, errorcode
import openai
import json

app = Flask(__name__)
CORS(app)

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'kaviyam@1410',
    'database': 'STUDENT1',
    'raise_on_warnings': True
}

# Initialize OpenAI client
client = openai.AzureOpenAI(
    azure_endpoint="https://finkdataopenai.openai.azure.com/",
    api_key='d57b4f240c6f4c12bb8d316469e45f69',
    api_version="2024-02-15-preview"
)

# Load FinKraft data from JSON file
with open('finkraft_data.json', 'r') as file:
    finkraft_data = json.load(file)

def extract_information(query):
    query = query.lower()
    extracted_info = {}
    for key, value in finkraft_data.items():
        if key.lower() in query:
            extracted_info[key] = value
    if extracted_info:
        response = ""
        for key, value in extracted_info.items():
            response += f"{key}:\n{value}\n\n"
        return response.strip()
    else:
        return None

def create_table(cursor):
    table_schema = (
        "CREATE TABLE IF NOT EXISTS CHATGPT ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  email_id VARCHAR(255) NOT NULL,"
        "  user_input TEXT NOT NULL,"
        "  bot_response TEXT NOT NULL,"
        "  context TEXT"
        ")"
    )
    try:
        cursor.execute(table_schema)
    except MySQLError as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("CHATGPT table already exists.")
        else:
            print(err.msg)

def get_context(cursor, email_id):
    cursor.execute("SELECT context FROM CHATGPT WHERE email_id = %s ORDER BY id DESC LIMIT 1", (email_id,))
    result = cursor.fetchone()
    return result[0] if result else ""

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    email_id = data.get('email')
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        
        # Create table if not exists
        create_table(cursor)
        
        # Get context for the user
        context = get_context(cursor, email_id)
        context += f"\nUser: {user_input}\n"
        
        # Extract information from local data or OpenAI if not found
        info = extract_information(user_input)
        if info:
            bot_response = info
        else:
            completion = client.chat.completions.create(
                model="gpt-35-turbo",
                messages=[
                    {"role": "system", "content": "You are Fink, a chatbot for FinKraft AI. Provide detailed and user-friendly information to the users."},
                    {"role": "user", "content": context}
                ],
                temperature=0.7,
                max_tokens=150,
                top_p=1.0,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None
            )
            bot_response = completion.choices[0].message.content
        
        # Update context
        context += f"Bot: {bot_response}\n"
        
        # Insert conversation into the database
        insert_query = "INSERT INTO CHATGPT (email_id, user_input, bot_response, context) VALUES (%s, %s, %s, %s)"
        insert_data = (email_id, user_input, bot_response, context)
        cursor.execute(insert_query, insert_data)
        conn.commit()
        
        return jsonify({'response': bot_response})
    
    except MySQLError as err:
        print(f"MySQL error: {err}")
        return jsonify({'response': 'Database error.'}), 500
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True)

import sqlite3
import uuid
from datetime import datetime

class Context(dict):
    """
    Context is a Singleton DotDict that allows access to its attributes
    using dot notation. Being a singleton, it ensures that only one instance of this
    class is created throughout the lifetime of the program.
    Example Usage:
        my_context = Context()
        my_context.some_key = 'some_value'  # Set an item
        # Access the same instance elsewhere
        another_reference = Context()
        print(another_reference.some_key)  # Outputs 'some_value'
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __getattr__(self, item):
        return self.get(item)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, item):
        del self[item]


class ChatMessages:
  def __init__(self, db_filename="chatroom.db", thread_id=None):
       # Create a SQLite database connection and cursor
      self.db_filename = db_filename
      self.db_connection = sqlite3.connect(self.db_filename)
      self.db_cursor = self.db_connection.cursor()
      self.thread_id = thread_id or self.new_thread_id()
      self.init_db()

  def init_db(self):
      # Create a SQLite database and Messages table if it doesn't exist
      conn = sqlite3.connect(self.db_filename)
      cursor = conn.cursor()
      cursor.execute('''
          CREATE TABLE IF NOT EXISTS Messages (
              message_id INTEGER PRIMARY KEY AUTOINCREMENT,
              thread_id TEXT,
              timestamp DATETIME,
              sender TEXT,
              content TEXT,
              agent_name TEXT,
              participants TEXT,
              agents TEXT
          )
      ''')
      conn.commit()
      conn.close()

  def new_thread_id(self):
      thread_id = str(uuid.uuid4())
      return thread_id

  def add_new_message(self, msg_dict):
      self.insert_message(msg_dict['sender'], msg_dict['content'], msg_dict['agent_name'],
                          msg_dict['participants'], msg_dict['agents'], thread_id=msg_dict['thread_id'])

  def insert_message(self, sender, content, agent_name, participants, agents, thread_id=None):
      # Insert a message into the database
      thread_id = thread_id or self.thread_id
      timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      print(thread_id, timestamp, sender, content, agent_name, participants, agents)
      conn = sqlite3.connect(self.db_filename)
      cursor = conn.cursor()
      cursor.execute('''
          INSERT INTO Messages (thread_id, timestamp, sender, content, agent_name, participants, agents)
          VALUES (?, ?, ?, ?, ?, ?, ?)
      ''', (thread_id, timestamp, sender, content, agent_name, str(participants), str(agents)))
      conn.commit()
      conn.close()

  def get_last_n_messages(self, n=5, thread_id=None):
      # Retrieve the last n messages from the database
      conn = sqlite3.connect(self.db_filename)
      cursor = conn.cursor()
      if thread_id:
          cursor.execute('''
              SELECT * FROM Messages
               WHERE thread_id = ?
              ORDER BY message_id DESC
              LIMIT ?
          ''', (thread_id,n,))            
      else:
          cursor.execute('''
              SELECT * FROM Messages
              ORDER BY message_id DESC
              LIMIT ?
          ''', (n,))
      messages = cursor.fetchall()
      conn.close()
      return messages
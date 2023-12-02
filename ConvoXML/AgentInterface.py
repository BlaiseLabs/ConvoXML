import subprocess
import xml.etree.ElementTree as ET
import uuid
import sqlite3
from bs4 import BeautifulSoup
from .Context import Context


class Node:
  element = "node"
  def __init__(self, name=None, **params):
      self.name = name or 'unnamed_node'
      # Set predefined attributes and any additional attributes from params
      for key, value in params.items():
          setattr(self, key, value)
      # Set defaults for predefined attributes if not in params
      self.context = params.get('context', Context())
      self.parent = params.get('parent', None)
      self.children = []


  @classmethod
  def from_node(cls, action_node):
    raise NotImplementedError

  def add_child(self, child):
      self.children.append(child)

  def add_properties_from_element(self):
      raise NotImplementedError

  def execute(self):
      raise NotImplementedError

class AgentInterface(Node):
  def __init__(self, **params):
      super().__init__(**params)

      # Set predefined attributes and any additional attributes from params
      for key, value in params.items():
          setattr(self, key, value)

      # Set defaults for non-provided attributes
      self.thread_id = params.get('thread_id', str(uuid.uuid4())[:8])
      self.input_table = params.get('input_table', 'Messages').split(',')
      self.output_table = params.get('output_table', 'Messages')
      self.rows = params.get('rows', 10)
      self.db_path = params.get('db_path', 'messages.db')
      #self.connection = sqlite3.connect(self.db_path)
      self.response_tag = params.get('response_tag', None)
      self.prompt = params.get('prompt','You are a helpful assistant.')

      self.setup()

  def setup(self):
    pass

  def parse_response(self, response):
      # Check if a response tag was specified and if it exists in the response
      if self.response_tag and f"<{self.response_tag}>" in response:
          try:
              # Parse the XML response to extract the content inside the specified tag
              root = ET.fromstring(response)
              tag_content = root.find(self.response_tag).text
              return tag_content

          except Exception as e:
              # Handle any potential parsing errors
              print(f"Error parsing XML response: {e}")
      return response

  def get_inputs(self):
        # handle multiple inputs if passed
        inputs = []
        connection = sqlite3.connect(self.db_path)
        for idx, table in enumerate(self.input_table):
            try:
                # handle rows if they were specified for each table
                rows = self.rows if not isinstance(self.rows, list) else self.rows[idx]
                cursor = connection.cursor()
                cursor.execute(f"SELECT * FROM {table} WHERE thread_id = ? ORDER BY timestamp DESC LIMIT ?",
                               (self.thread_id, self.rows))
                message = cursor.fetchall()[0][3]
                inputs.append(message)
            except:
                print("failed to extract input")
        connection.close()
        return inputs

  def output_messsage(self, message):
      # Store the parsed content in the database
      connection = sqlite3.connect(self.db_path)
      cursor = connection.cursor()
      cursor.execute(f"INSERT INTO {self.output_table} (thread_id, sender, content) VALUES (?, ?, ?)",
                     (self.thread_id, self.role, message))
      connection.commit()
      connection.close()

  def send_message(self, messages=None):
      raise NotImplementedError(f"{self.__class__.__name__} does not implement the send_message method")


  def execute(self):
      return self.send_message()



class AgentTerminalInterface(AgentInterface):

    def parse_response(self, response):
        soup = BeautifulSoup(response, 'html.parser')

        # Find and execute Python code sections
        python_elements = soup.find_all('python')
        for python_element in python_elements:
            python_code = python_element.get_text()
            try:
                python_output = subprocess.check_output(['python', '-c', python_code], universal_newlines=True)
                python_element.replace_with(f'<python>{python_output}</python>')
            except subprocess.CalledProcessError as e:
                python_element.replace_with(f'<python>Error: {e.stderr}</python>')

        # Find and execute terminal command sections
        terminal_elements = soup.find_all('terminal')
        for terminal_element in terminal_elements:
            terminal_command = terminal_element.get_text()
            try:
                terminal_output = subprocess.check_output(terminal_command, shell=True, universal_newlines=True)
                terminal_element.replace_with(f'<terminal>{terminal_output}</terminal>')
            except subprocess.CalledProcessError as e:
                terminal_element.replace_with(f'<terminal>Error: {e.stderr}</terminal>')

        return str(soup)


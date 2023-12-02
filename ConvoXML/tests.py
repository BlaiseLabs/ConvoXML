from .ConvoXML import ConvoXML

import sqlite3
import unittest
import os



class TestConvoXML(unittest.TestCase):
    # Re-adjusting the test suite for the corrected parser
    def setUp(self):
        # Sample XML string
        with open('./ConvoXml/examples/test_xml.xml', 'r') as f:
            xml_string = f.read()
        
        self.db_connection = sqlite3.connect('tests.db')
        self.parser = ConvoXML(xml_string)
        self.parser.setup_database()
    
    def test_initialization(self):
        self.assertIsNotNone(self.parser)
    
    def test_parse_roles(self):
        agents = self.parser.agents
        expected_roles = ["Moderator", "Participant1", "Participant2", "Participant3"]
        self.assertEqual(len(agents), len(expected_roles))
        for role in expected_roles:
            self.assertIn(role, [agent.role for agent in agents])
    
    def test_parse_queue(self):
        queue = self.parser.queue
        self.assertTrue(len(queue) > 0)
        queue_roles = []
        for item in queue:
            
            if isinstance(item, list):
                queue_roles.extend([agent.role for agent in item])
            elif item:
                queue_roles.append(item.role)
                print(item.__dict__)
        self.assertIn("Moderator", queue_roles)
        self.assertIn("Participant1", queue_roles)
        self.assertIn("Participant2", queue_roles)
        self.assertIn("Participant3", queue_roles)

    def test_run_method(self):
      self.parser.run()
      cursor = self.parser.db_connection.cursor()
      cursor.execute("SELECT * FROM Messages")
      messages = cursor.fetchall()
      print(messages)
      self.assertTrue(len(messages) > 0)
    
    def tearDown(self):
        self.db_connection.close()
        os.remove('tests.db')



if __name__ == '__main__':
    # Re-running the test suite with the adjusted test case
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestConvoXML)
    unittest.TextTestRunner().run(test_suite)


# ConvoXML: XML based Language for Modeling Conversations

## Introduction
ConvoXML is a Python-based framework that offers an intuitive and easy-to-use language for modeling conversations using XML. It is ideal for developers and researchers in conversational AI, allowing for structured definition and interaction with various conversational agents, including integrations with AI models like OpenAI and Google's generative AI.


## Core Concepts and Functionalities
- **XML-Based Modeling**: Easily define conversation structures and agent roles using XML.
- **Agent Flexibility**: Create various types of agents, including custom ones, to suit different models of conversation.
- **AI Integration**: Seamlessly integrate with popular AI models like OpenAI and Google's generative AI for advanced conversational capabilities.
- **Conversation Flow Control**: Manage conversation paths, loops, and conditions effectively.
- **Scalability and Extensibility**: Easily scale and extend conversations and agent functionalities.

## Installation
```bash
git clone [repository-url]
cd ConvoXML
pip install -r requirements.txt  # if a requirements file exists
```

## Usage
```python
from ConvoXML import ConvoXML

with open('./your_convo_file.xml', 'r') as file:
    xml_string = file.read()

parser = ConvoXML(xml_string)
parser.run()
```

## Examples

### Basic Conversation Model
In this basic example, we define a simple conversation flow between two roles: a user and a bot.

```
User                 Bot
|                   |
|---(1) sayHello--->|
|<-(2) replyHello---|
|                   |
|<-(3) askQuestion--|
|---(4) answer----->|
|                   |
```

```xml
<InteractionModel>
  <Roles>
    <Role name="User"/>
    <Role name="Bot" class="TestAgent"/>
  </Roles>

  <ConvoLoop>
    <User action="sayHello">
      <Bot response="replyHello"/>
    </User>
    <Bot action="askQuestion">
      <User response="answerQuestion"/>
    </Bot>
  </ConvoLoop>
</InteractionModel>

```

### Complex Scenario with AI Integration
In this more advanced example, the conversation involves a Moderator and several AI-integrated agents. The Moderator directs the conversation flow among AI agents, each capable of sophisticated responses.

```
Moderator       AI_Agent1       AI_Agent2       AI_Agent3
|               |               |               |
|---(1) select----------------->|               |
|               |<-(2) engageAI1|               |
|               |               |               |
|---(1) select--------------------------------->|
|               |               |<-(2) engageAI2|
|               |               |               |
|---(1) select----------------->|               |
|               |               |               |
|               |<-(2) engageAI3----------------|
```

```xml
<InteractionModel>
  <Roles>
    <Role name="Moderator" class="TestModerator"/>
    <Role name="AI_Agent1" class="OpenAIAgent"/>
    <Role name="AI_Agent2" class="PalmAgent"/>
    <Role name="AI_Agent3" class="CustomAIAgent"/>
  </Roles>

  <ConvoLoop>
    <Moderator action="selectAgent">
      <Case action="engageAI1" trigger="selectAgent" case="A" role="AI_Agent1"/>
      <Case action="engageAI2" trigger="selectAgent" case="B" role="AI_Agent2"/>
      <Case action="engageAI3" trigger="selectAgent" case="C" role="AI_Agent3"/>
    </Moderator>

    <AI_Agent1 action="provideResponse"/>
    <AI_Agent2 action="generateIdea"/>
    <AI_Agent3 action="solveProblem"/>
  </ConvoLoop>
</InteractionModel>

```

## Understanding XML Syntax in ConvoXML
The XML syntax in ConvoXML is intuitive:
- `<Role>`: Defines a participant in the conversation.
- `<ConvoLoop>`: Sets up the structure for conversation loops and decision-making.
- `Attributes and Tags`: Represent property and class values for each role instance and allows for detailed control over the conversation flow and agent behavior.

## Advantages of ConvoXML
- **Ease of Use**: Simple, XML-based conversation definition.
- **Versatility**: Suitable for various conversational AI applications.
- **Customizability**: Easy to create and integrate custom agents.
- **Advanced AI Integration**: Supports leading AI technologies.


## Installation
```bash
git clone [repository-url]
cd ConvoXML
pip install -r requirements.txt  # if a requirements file exists
```

## Usage
1. Define your conversational agents and interactions in a ConvoXML file (see `examples` directory).
2. Use the `ConvoXML` to parse the XML and create agents.
3. Run the conversation loop to simulate interactions.

```python
from ConvoXML import ConvoXML

with open('./examples/your_convo_file.xml', 'r') as file:
    xml_string = file.read()

parser = ConvoXML(xml_string)
parser.run()
```

## Sequence Diagram Representation
Below is an ASCII representation of the `test_xml2.xml` conversation model:

```
Moderator       Participant4       Participant5       Participant6
    |                 |                   |                  |
    |---(1) decideNext-------------------->|                  |
    |                 |<--(2) acknowledge--|                  |
    |                 |                   |                  |
    |---(1) decideNext--------------------------------------->|
    |                 |                   |<--(2) acknowledge|
    |                 |                   |                  |
    |---(1) decideNext-------------------->|                  |
    |                 |                   |                  |
    |                 |<--(2) acknowledge--------------------|
```

## Creating Your Own Agent Subclass
Creating a custom agent subclass involves extending the `AgentInterface` class. Here's a simplified example of how you can create your own agent, similar to the `OpenAIAgent`.

```python
from .AgentInterface import AgentInterface

class MyCustomAgent(AgentInterface):
    def __init__(self, **params):
        super().__init__(**params)
        # Initialize your agent with additional parameters

    def send_message(self, message):
        # Implement how your agent sends a message
        pass

    def execute(self):
        # Define the main behavior of your agent
        pass
```

In this example, `MyCustomAgent` is a new agent type. You can customize the `send_message` and `execute` methods based on your agent's specific behavior.

## Features
- **XML-Based Conversation Modeling**
- **Multiple Agent Types**
- **Extensible Framework**
- **Testing and Examples**

## Running Tests
```bash
python -m unittest tests.py
```

## Contribution
Contributions are welcome!

## MIT License
Copyright (c) 2023 Blaiselabs

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Acknowledgments
- BeautifulSoup


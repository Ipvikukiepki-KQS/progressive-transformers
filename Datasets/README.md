## Multiwoz data analysis
source: https://www.repository.cam.ac.uk/handle/1810/280608
The annotated MultiWOZ dataset has obtained from the following Github Profile of Convlab by Microsoft Research and Tsinghua University Team (https://github.com/ConvLab/ConvLab/tree/master/data/multiwoz/annotation).

## Description
Dialogue - each utterance of the user and the system
Conversation - The Whole interactions between the user and the system until the desired end goal (end greetings by the user and the system) 

The Dataset consists of human-human conversations. It consists of dialogues of each conversation involving multiple domain or single domain dialogues. The dataset has been collected using Wizard-of-Oz Experiments. Though it might have grammatical imperfections, it has context rich data along with the database for API for handling the user specifications. Though the dataset has intent and dialogue for end greetings, it doesn't have the specific dialogues for greetings at the beginning. This has to added while customizing the dataset for the specification corresponding to the chosen conversational AI Framework data format. For this Implementation, three domain specific corpus (Progressive domains) data has to be extracted and customized according to the required json format.

The dataset has to be categorized into Natural Language Understanding (NLU) Corpus, Dialogue Management (DM) Corpus, and Natural Language Generation (NLG) corpus data separately. The utterances of the user belongs to NLU corpus, and the utterances given by the system belongs to NLG corpus. The intent of the user in the uttered dialogue along with its enitities and values pairs in corresponding to the response of the system's intent along with its entities and value pairs form the stories for each whole conversation.

### Domain
1) Hotel
2) Restaurant
3) Attraction
4) Taxi
5) Police
6) Hospital

Each domain consists of corresponding API-Database to satisfy the User requirements along with several attributes.

### API Database Attributes
1) Hotel - Address, Area, Internet, Parking, Location, Name, Phone, Postcode, price of the bed for single, double, family, Pricerange of the room, Stars, Takesbookings, and Type

2) Restaurant - Address, Area, Food, Introduction, Location, Name, Phone, Postcode, Pricerange, Type


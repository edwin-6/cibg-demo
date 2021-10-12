import spacy

nlp = spacy.load('training/model-best')
print(nlp.pipeline)

doc = nlp('Helaas zit 1234AB niet in de trainingsdata. 1234 AB wel. Niet de echte hoor, die is 8172 BW te Vaassen. Agent 007 kennen we, agent 1007 is minder bekend.')
print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

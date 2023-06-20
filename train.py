import spacy
import os
import random
import json


class Model:
    rootPath = "./models"

    # This function converts the JSON data sent from the frontend into Spacy readable format in the backend
    @staticmethod
    def parseData(rawData):
        try:
            result = []
            for row in rawData:
                entities = []
                text = row["text"]
                annotations = row["annotations"]
                for entity in annotations:
                    entities.append(
                        (entity["startIndex"], entity["endIndex"], entity["tag"]))
                result.append((text, {"entities": entities}))
            return result
        except Exception as e:
            raise Exception("Parsing error: " + str(e))

    # This function converts the stored JSON training data into Spacy readable format
    def __jsonToTuples(self, jsonData):
        result = []
        for row in jsonData:
            text = row[0]
            entitiesObject = row[1]
            entities = entitiesObject["entities"]
            convertEntitiesToTuples = list(
                map(lambda x: (x[0], x[1], x[2]), entities))
            result.append((text, {"entities": convertEntitiesToTuples}))
        return result

    # This function loads the model saved locally, for re-training or testing purposes
    # Also loads the training data
    def __loadModel(self, modelName, isNewModel):
        path = self.rootPath + "/" + modelName
        if isNewModel:
            if os.path.exists(path):
                raise Exception("Model already exists!")
            nlp = spacy.blank("en")
            ner = nlp.add_pipe("ner")  # ran only for new models
            return nlp, []
        try:
            nlp_loaded = spacy.load(path)
            f = open(path + "/data.json", "r")
            lines = json.load(f)
            return nlp_loaded, self.__jsonToTuples(lines)
        except Exception as e:
            raise Exception(
                "Error loading model, model missing or does not exist yet: " + str(e))

    # This function saves the model locally, for production, re-training or testing purposes
    def __saveModel(self, modelName, nlp, data):
        output_dir = self.rootPath + "/" + modelName
        nlp.to_disk(output_dir)
        # save training data, important for retraining
        json_object = json.dumps(data, indent=4)
        with open(output_dir + "/data.json", "w") as outfile:
            outfile.write(json_object)
        outfile.close()

    # Driver function for training. This functions handles the training of the model
    def train(self, modelName, data, isNewModel):
        try:
            nlp, savedData = self.__loadModel(modelName, isNewModel)
            TRAIN_DATA = data + savedData
            nlp.begin_training()
            # 10 iters optimal for training, ensures model doesnt generalize based on order of examples
            for itn in range(10):
                random.shuffle(TRAIN_DATA)
                losses = {}
                for text, annotations in TRAIN_DATA:
                    doc = nlp.make_doc(text)
                    example = spacy.training.Example.from_dict(
                        doc, annotations)
                    nlp.update([example], losses=losses)
                # print("Iteration:", itn, "Losses:", losses)
            # save the model
            self.__saveModel(modelName, nlp, TRAIN_DATA)
            print("Saved model:", modelName)
            return {"status": 200}
        except Exception as e:
            return {"status": 400, "error": "Training error: " + str(e)}

    # Driver function for testing. The function handles the testing of the model
    def test(self, modelName, testArray):
        try:
            nlp, savedData = self.__loadModel(modelName, False)
            allResults = []
            for testString in testArray:
                doc = nlp(testString)
                results = []
                for ent in doc.ents:
                    # print(ent.start_char, ent.end_char)
                    results.append({"text": ent.text, "tag": ent.label_,
                                   "start_index": ent.start_char, "end_index": ent.end_char})
                allResults.append(results)
            return {"status": 200, "data": allResults}
        except Exception as e:
            return {"status": 400, "error": "Testing error: " + str(e)}

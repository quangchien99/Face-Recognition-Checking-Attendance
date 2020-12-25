

from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
import argparse
import pickle

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--embeddings", default="output/embeddings.pickle",
	help="path to serialized db of facial embeddings")
ap.add_argument("-r", "--model", default="output/model.pickle",
	help="path to output model trained to recognize faces")
ap.add_argument("-l", "--label", default="output/label.pickle",
	help="path to output label encoder")

args = vars(ap.parse_args())


# load the face embeddings
print("[INFO] loading face embeddings...")
data = pickle.loads(open(args["embeddings"], "rb").read())

# encode the labels
print("[INFO] encoding labels...")
label = LabelEncoder()
labels = label.fit_transform(data["names"])

# train the model used to accept the 128-d embeddings of the face and
# then produce the actual face recognition
print("[INFO] training model...")

#C =1 để phân chia chính xác - để có 1 maximum margin tốt và phân chia chính xác clasìication , 1.0 là default của thằng này và nó phù hợp với model của tôi.
#kernel: khai báo chiều - linear -> 2 chiều
recognizer = SVC(C=1.0, kernel="linear", probability=True)
recognizer.fit(data["embeddings"], labels)


# write the actual face recognition model to disk
f = open(args["model"], "wb")
f.write(pickle.dumps(recognizer))
f.close()

# write the label encoder to disk
f = open(args["label"], "wb")
f.write(pickle.dumps(label))
f.close()
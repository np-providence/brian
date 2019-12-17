import face_recognition
import numpy as np
from .features import getAllFeatures
from .eventowner import getEventOwnerById
def get_features():
  testing_features = [-0.12152737,  0.06416188,  0.01735289, -0.06186358, -0.06014183,
       -0.06157691, -0.03397509, -0.11230542,  0.14670537, -0.09582033,
        0.21820967, -0.08050989, -0.26305115, -0.05811048, -0.07776095,
        0.15903744, -0.11117086, -0.14190663, -0.06596021,  0.04264126,
        0.15111473, -0.01253414, -0.03915079,  0.05385059, -0.06261817,
       -0.26534283, -0.12787063, -0.03931737, -0.00605257, -0.06070725,
       -0.02723841, -0.01593168, -0.20295212, -0.10068697,  0.04701954,
        0.10396921,  0.01464966, -0.08453935,  0.19308101,  0.00322937,
       -0.247761  ,  0.0366584 ,  0.04393771,  0.23064551,  0.14146064,
        0.06717199,  0.00697681, -0.17266221,  0.10049669, -0.13412723,
        0.03903287,  0.16617188,  0.13101931,  0.05863789, -0.00613026,
       -0.16582705,  0.07376889,  0.14604639, -0.16925612,  0.00644561,
        0.11445857, -0.07145656,  0.00838053, -0.06996691,  0.24674779,
        0.03882862, -0.14145803, -0.20042637,  0.16558349, -0.12015072,
       -0.08712359,  0.06209444, -0.1855783 , -0.17255479, -0.31349301,
        0.06579113,  0.43867895,  0.10712178, -0.20610562,  0.08997003,
       -0.07626635,  0.01932675,  0.10333417,  0.15700167, -0.0145964 ,
        0.05553341, -0.09248675, -0.03086844,  0.22723573, -0.02898866,
       -0.061731  ,  0.16254987, -0.00281901,  0.05462154,  0.04636962,
       -0.01197787, -0.06292164,  0.00250852, -0.13027748, -0.03081456,
        0.02209044, -0.03342281,  0.00384188,  0.14880785, -0.12370354,
        0.09270674, -0.0098871 ,  0.00447296, -0.038004  ,  0.02025894,
       -0.11093871, -0.05178867,  0.10958652, -0.22560714,  0.23860151,
        0.13893592,  0.10088944,  0.07121279,  0.16053338,  0.11866304,
        0.02936053,  0.04304205, -0.20527382, -0.05371002,  0.11654183,
        0.00175785,  0.18246639,  0.00376287]
  
  known_facial_features= [
	np.asarray(testing_features),
    ]
  return [known_facial_features]

def compare_features(incoming_features):
    known_features = getAllFeatures()
    incoming_features = np.asarray(incoming_features['features'])
    is_match = None
    res = None
    for feat in known_features:
        lol = feat
        feat = feat['feat']
        matches = face_recognition.compare_faces(feat, incoming_features)
        if matches[0] == True:
            id = lol['eventowner_id']
            res = getEventOwnerById(id)

    return res
#def compare_features(incoming_features):
#    known_features = get_features()
#    incoming_features = incoming_features['features']
#    is_match = None
#    for face_feature in incoming_features:
#        face_feature = np.asarray(face_feature)
#        matches = face_recognition.compare_faces(known_features[0], face_feature)
#        is_match = matches[0]
#
#    if is_match:
#        return "match"
#    else:
#        return "did not match"

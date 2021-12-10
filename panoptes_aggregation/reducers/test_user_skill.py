'''
Subject Gold Standard Reducer for difficulty calculation
---------------------------------------------------------
This module provides functions to reduce the gold standard task extracts
to determine a `difficulty' score per subject (defined as the fraction
of succesful classification by all users for that subject)

See also: tess_gold_standard_reducer
'''
from .reducer_wrapper import reducer_wrapper
import numpy as np
from sklearn.metrics import confusion_matrix
import sys

@reducer_wrapper(relevant_reduction=True)
def test_user_skill_reducer(extracts, relevant_reduction=[], binary=False):
    confusion_simple, confusion_subject = get_confusion_matrix(extracts, relevant_reduction, binary)

    print(confusion_simple, file=sys.stderr)
    print(confusion_subject, file=sys.stderr)

    per_class_skill = (confusion_subject.diagonal())/(np.sum(confusion_subject, axis=0) + 1.e-16)

    print(per_class_skill, file=sys.stderr)

    sys.stderr.flush()

    return {'skill': per_class_skill[0]}


def get_confusion_matrix(extracts, relevant_reduction, binary):
    if binary:
        # binary always defaults to 2x2 where the second column
        # (gold standard = False) is NaN
        confusion_simple = np.zeros((2, 2))
        confusion_subject = np.zeros((2, 2))

        successes = []
        difficulties = []

        # create an array of success/failure. multiple cases
        # per subject are treated independently, and the final
        # array is a flattened version of all success/failure checks
        for extracti, reductioni in zip(extracts, relevant_reduction):
            successes.extend(extracti['feedback']['success'])

            # input difficulty is inverted... we want higher difficulty
            # values for subjects which were classified incorrectly
            difficultyi = 1. - np.array(reductioni['data']['difficulty'])


            difficulties.extend( list(difficultyi))
        successes = np.asarray(successes)
        difficulties = np.asarray(difficulties)

        # find the easiest subject in the set and set all fully successful 
        # subjects to this "easy" score. limit the easy score to 0.05 so that 
        # we don't have a runaway growth of easy weights
        difficulty_min = np.min([np.min(difficulties[difficulties>0], initial=0), 0.05])

        # limit the difficulty to a mininum of 0.05 so that 
        # easy subjects still have some weight
        difficulties[difficulties==0] = difficulty_min

        print(difficulties, file=sys.stderr)
        print(successes, file=sys.stderr)

        true_mask = successes==True
        false_mask = successes==False

        # create the confusion matrix from the list of success/failures
        confusion_simple[0,0] = np.sum(true_mask)
        confusion_simple[1,0] = np.sum(false_mask)
        confusion_simple[:,1] = np.nan

        # the true score is the sum of difficulties of the correct classifications
        # so hard subjects give you a boost in score and the difficult subjects 
        # give you a small increase
        confusion_subject[0,0] = np.sum(difficulties[true_mask])

        # do the opposite for failure scores: easy subject failures should be
        # penalized more strongly compared to difficulty failures
        confusion_subject[1,0] = np.sum(1. - difficulties[false_mask])
        confusion_subject[:,1] = np.nan
    else:
        #feedback_data = [extracti['feedback'] for extracti in extracts if 'feedback' in extracti.keys()]
        user_classifications = []

        # first we need a list of labels 
        # obtain a list of labels from user classifications
        for extracti in extracts:
            user_classifications += [key for key in extracti if isinstance(extracti[key], int)]

        user_classifications = user_classifications

        # get the same from the feedback data
        true_values = [extracti['feedback']['true_answer'] for extracti in extracts]

        # get a full list of classes as the union of the two sets of labels
        classes = np.unique([*np.unique(user_classifications), *np.unique(true_values)])

        nclasses = len(classes)

        subject_difficulty = 1 - np.asarray([reductioni['data']['difficulty'][0] for reductioni in relevant_reduction])

        # find the easiest subject in the set and set all fully successful 
        # subjects to this "easy" score. limit the easy score to 0.05 so that 
        # we don't have a runaway growth of easy weights
        difficulty_min = np.min([np.min(subject_difficulty[subject_difficulty>0]), 0.05])

        # limit the difficulty to a mininum of 0.05 so that 
        # easy subjects still have some weight
        subject_difficulty[subject_difficulty==0] = difficulty_min

        mask = (np.asarray(true_values).flatten()=='4')&(np.asarray(user_classifications)=='4')
        print(np.asarray(true_values).flatten(), user_classifications, mask, len(mask), len(subject_difficulty), file=sys.stderr)
        print(subject_difficulty[mask], np.sum(subject_difficulty[mask]), file=sys.stderr)

        confusion_simple = confusion_matrix(user_classifications, true_values)
        confusion_subject = confusion_matrix(user_classifications, true_values, sample_weight=subject_difficulty)

    return (confusion_simple, confusion_subject)

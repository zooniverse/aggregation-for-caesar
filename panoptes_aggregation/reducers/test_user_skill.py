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
from ..feedback_strategies import FEEDBACK_STRATEGIES
from sklearn.metrics import confusion_matrix
import sys
import ast

print2 = lambda x: print(*x, file=sys.stderr, flush=True)

@reducer_wrapper(relevant_reduction=True)
def test_user_skill_reducer(extracts, relevant_reduction=[], binary=False, null_class='NONE'):
    if isinstance(binary, str):
        binary = ast.literal_eval(binary)
    if binary:
        classes = ['True', 'False']
        confusion_simple, confusion_subject = get_confusion_matrix(extracts, relevant_reduction, binary, None)
    else:
        confusion_simple, confusion_subject, classes = \
            get_confusion_matrix(extracts, relevant_reduction, binary, null_class)

    #print(confusion_simple, file=sys.stderr)
    #print(confusion_subject, file=sys.stderr)

    # get both the weighted and non-weighted skill
    weight_per_class_skill = (confusion_subject.diagonal()) / (np.sum(confusion_subject, axis=0) + 1.e-16)
    per_class_skill = (confusion_simple.diagonal()) / (np.sum(confusion_simple, axis=0) + 1.e-16)

    #print(per_class_skill, file=sys.stderr)

    # print2(("class skill: ", per_class_skill))

    #sys.stderr.flush()

    return {'skill': per_class_skill, 'weighted_skill': weight_per_class_skill, 'classes': classes, 'confusion_simple': confusion_simple}


def get_confusion_matrix(extracts, relevant_reduction, binary, null_class):
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

            difficulties.extend(list(difficultyi))
        successes = np.asarray(successes)
        difficulties = np.asarray(difficulties)

        # find the easiest subject in the set and set all fully successful
        # subjects to this "easy" score. limit the easy score to 0.05 so that
        # we don't have a runaway growth of easy weights
        difficulty_min = np.max([np.min(difficulties[difficulties > 0], initial=0), 0.05])

        # limit the difficulty to a mininum of 0.05 so that
        # easy subjects still have some weight
        difficulties[difficulties == 0] = difficulty_min

        #print(f" Difficulty min: {difficulty_min}", file=sys.stderr)
        #print(f"Difficulties: {difficulties}", file=sys.stderr)
        #print(f"Success: {successes}", file=sys.stderr)

        true_mask = successes == 1
        false_mask = successes == 0

        # create the confusion matrix from the list of success/failures
        confusion_simple[0, 0] = np.sum(true_mask)
        confusion_simple[1, 0] = np.sum(false_mask)
        confusion_simple[:, 1] = np.nan


        # the true score is the sum of difficulties of the correct classifications
        # so hard subjects give you a boost in score and the easy subjects
        # give you a small increase
        confusion_subject[0, 0] = np.sum(difficulties[true_mask])

        # do the opposite for failure scores: easy subject failures should be
        # penalized more strongly compared to difficulty failures
        neg_difficulty = 1. - difficulties[false_mask]
        neg_difficulty[neg_difficulty==0] = difficulty_min
        confusion_subject[1, 0] = np.sum(neg_difficulty)
        confusion_subject[:, 1] = np.nan
        
        #print(confusion_subject, file=sys.stderr)
        #sys.stderr.flush()
        return (confusion_simple, confusion_subject)
    else:
        user_classifications = []
        classes = []
        strategy = extracts[0]['feedback']['strategy']

        true_key = 'true_'+FEEDBACK_STRATEGIES[strategy][0]

        true_values = []

        # first we need a list of labels
        # obtain a list of labels from user classifications
        if strategy in ['singleAnswerQuestion']:
            for extracti in extracts:
                user_classifications += [key for key in extracti if isinstance(extracti[key], int)]
                # get the same from the feedback data
                true_values.extend(extracti['feedback'][true_key])

            classes = user_classifications
        elif strategy in ['surveySimple']:
            # for survey simple, the idea is the same
            # except that the keys have a value of 1 when the 
            # user selects that class
            for j, extracti in enumerate(extracts):
                user_classifications += [key for key in extracti.keys() if isinstance(extracti[key], int)&(extracti[key]==1)]
                classes              += [key for key in extracti.keys() if isinstance(extracti[key], int)]
                true_values.extend(extracti['feedback'][true_key])
                #print2(("classes: ", j, [key for key in extracti.keys() if isinstance(extracti[key], int)&(extracti[key]==1)]))

        #print2(("Extracts: ", extracts))

        #print2(("# extracts: ", len(extracts)))

        # get a full list of classes as the union of the two sets of labels
        #print2(("Classes: ", np.unique(classes)))
        #print2(("True_values: ", true_values))
        classes = np.sort(np.unique([*np.unique(classes), *np.unique(true_values)]))
        classes = classes.tolist()
        classes.append(null_class)

        #print2(("Merged Classes: ", classes))


        #print2(("Classifications: ", user_classifications))

        difficulties = []
        for reductioni in relevant_reduction:
            difficulties.append( np.mean(reductioni['data']['difficulty']) )

        subject_difficulty = 1 - np.asarray(difficulties)

        # find the easiest subject in the set and set all fully successful
        # subjects to this "easy" score. limit the easy score to 0.05 so that
        # we don't have a runaway growth of easy weights
        difficulty_min = np.max([np.min(subject_difficulty[subject_difficulty > 0], initial=0), 0.05])

        # limit the difficulty to a mininum of 0.05 so that
        # easy subjects still have some weight
        subject_difficulty[subject_difficulty == 0] = difficulty_min

        true_counts = []
        class_counts = []
        subject_difficulties = []

        #print2(("# of difficulties", len(relevant_reduction)))
        #print2(("# of extracts", len(extracts)))

        # we will loop through all the extracts and create a list 
        # of user classified label and a corresponding gold standard
        # label. then, the confusion matrix is just determined using
        # the element-wise comparison between the two lists
        for j, extract in enumerate(extracts):

            # find a list of user classified labels in this extract
            user_class_i  = [key for key in extract.keys() if isinstance(extract[key], int)&(extract[key]==1)]

            # get a full list of classifications
            classi = np.sort(np.unique([*np.unique(extract['feedback'][true_key]),
                                        *np.unique(user_class_i)]))
            classi = classi.tolist()

            # create a temporary list of classes that will
            # incorporate both the user selected classes
            # and the tru classes
            true_count_i = [null_class]*len(classi)
            #print2(("Classi: ", extract['feedback'][true_key]))

            # loop through the true classes and populate the corresponding
            # indices in the list
            for value in extract['feedback'][true_key]:
                true_count_i[classi.index(value)] = value

            # do the same for the user classifications
            class_count_i = [null_class]*len(classi)
            #print2((j, "user classi: ", user_class_i))
            for value in user_class_i:
                class_count_i[classi.index(value)] = value
            
            # add both lists to the master list of 
            # classifications and true classes
            true_counts.extend(true_count_i)
            class_counts.extend(class_count_i)

            # also add the subject difficulties for each extract. subject
            # difficulty per class is not trivial to do, so we will average
            # the subject difficulty across all the classes in this subject.
            # easy subjects should get small bump for correct classifications
            # while difficult subjects will get a huge bump for success
            # do the opposite for failure scores: easy subject failures should be
            # penalized more strongly compared to difficulty failures
            subject_difficulty_i = [subject_difficulty[j]]*len(classi)
            for class_ind in range(len(classi)):
                if true_count_i[class_ind] != class_count_i[class_ind]:
                    subject_difficulty_i[class_ind] = np.max([1. - subject_difficulty_i[class_ind], 0.05])

            subject_difficulties.extend(subject_difficulty_i)

        
        #mask = (np.array(class_counts)!='NONE')&(np.array(true_counts)!='NONE')
        #class_counts = np.asarray(class_counts)[mask]
        #true_counts  = np.asarray(true_counts)[mask]
        #print("Mask = ", mask, file=sys.stderr)
        #print2(("Class counts: ", class_counts))
        #print2(("True counts: ", subject_difficulties))

        # get the simple confusion matrix without the subject difficulty
        confusion_simple  = confusion_matrix(class_counts, true_counts, labels=classes)

        # get the more complicated confusion matrix accounting for subject difficulty
        confusion_subject = confusion_matrix(class_counts, true_counts, sample_weight=subject_difficulties,
                                             labels=classes)

        #print2(("Confusion: ", confusion_simple[classes.index('HIPPOPOTAMUS'),:]))
        #confusion_subject = confusion_matrix(user_classifications, true_values, sample_weight=subject_difficulty, labels=classes)

        #confusion_simple  = confusion_matrix(user_classifications, true_values, labels=classes)
        #confusion_subject = confusion_matrix(user_classifications, true_values, sample_weight=subject_difficulty, labels=classes)

        #print2(("Confusion_simple: ", confusion_simple))
        #print2(("Len conf simple: ", len(confusion_simple)))

        return (confusion_simple, confusion_subject, classes)

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

# smallest possible value for difficulty so that
# subjects have a non-negligible effect on user skill
# in extreme cases
DIFFICULTY_FLOOR = 0.05


@reducer_wrapper(relevant_reduction=True)
def user_skill_reducer(extracts, relevant_reduction=[], mode='binary', null_class='NONE',
                       skill_threshold=0.7, count_threshold=10, strategy='mean', focus_classes=None):
    '''
        Parameters
        ----------
        extracts : list
            List of extracts
        relevant_reduction : list
            List of subject difficulty values attached as `relevant_reduction` on Caesar
        mode : str
            The type of confusion matrix to return. Possible options are:
              - binary: (True/False) mode
              - one-to-one: k-class mode where individual classifications are compared against corresponding gold standard values
              - many-to-many mode: k-class mode where several volunteer classifications are compared against several gold standard values.
                In this case, incorrect classifications are compared against a `null_class` and therefore, the function returns a pseudo-confusion matrix.
        null_class : str
            Value for the NULL class for k-class method [default: 'NONE']
        skill_threshold : float
            Threshold for user skill to toggle the `level_up` flag [default: 0.7]
        count_threshold : int
            Threshold for the number of classifications done by the volunteer to get an accurate
            measurement of skill [default: 10]
        strategy : str
            Strategy to use to calculate the leveling up toggle:
             - `mean` : use the mean skill (excluding the NULL class) compared to the skill threshold
             - `all` : check every class against the threshold skill (all classes must be greater than the threshold)

        Returns
        -------
        data : dict
            A dictionary with the following keys:
                - classes : list
                    a list of classes (in the case of binary, this is [True, False])
                - confusion_simple : list
                    a confusion matrix using the raw counts (without subject difficulty weighting)
                - weighted_skill : dict
                    the subject difficulty weighted user skill per class
                - skill : dict
                    the simple (non-subject difficulty weighted) user skill per class
                - count : dict
                    the count of classifications per class
                - mean_skill : float
                    the average skill excluding the NULL class
                - level_up : bool
                    flag to show whether the user should be leveled up using the input thresholds
    '''
    extracts = [extracti for extracti in extracts if 'feedback' in extracti.keys()]
    relevant_reduction = [redi for redi in relevant_reduction if 'difficulty' in redi['data'].keys()]

    assert len(extracts) == len(relevant_reduction), f"mismatch in length of extract ({len(extracts)}) and subject difficulty ({len(relevant_reduction)}) arrays!"

    # confusion_simple, confusion_subject = get_confusion_matrix(extracts, relevant_reduction, mode, None)
    confusion_simple, confusion_subject, classes = get_confusion_matrix(extracts, relevant_reduction, mode, null_class)

    # get both the weighted and non-weighted skill
    weight_per_class_skill = (confusion_subject.diagonal()) / (np.sum(confusion_subject, axis=1) + 1.e-16)
    weight_per_class_skill = weight_per_class_skill.tolist()
    per_class_skill = (confusion_simple.diagonal()) / (np.sum(confusion_simple, axis=1) + 1.e-16)
    per_class_skill = per_class_skill.tolist()

    weighted_per_class_skill_dict = {key: value for key, value in zip(classes, weight_per_class_skill)}
    per_class_skill_dict = {key: value for key, value in zip(classes, per_class_skill)}
    per_class_count = {key: value for key, value in zip(classes, np.sum(confusion_simple, axis=1).tolist())}

    # remove the null class from the skill array to calculate the mean skill
    if mode == 'binary':
        null_class = 'False'
    else:
        null_class = null_class

    # compute either on user-specified classes or perform mean skill calculation on all detected classes
    if focus_classes is None:
        null_removed_classes = [classi for classi in classes if classi != null_class]
        null_removed_counts = [ci for classi, ci in per_class_count.items() if classi != null_class]
        mean_skill = np.sum([weighted_per_class_skill_dict[key] for key in null_removed_classes]) / (len(null_removed_classes) + 1.e-16)
    else:
        null_removed_classes = [classi for classi in focus_classes if classi != null_class]
        null_removed_counts = [ci for classi, ci in per_class_count.items() if classi in null_removed_classes]
        mean_skill = np.sum([weighted_per_class_skill_dict[key] for key in null_removed_classes]) / (len(null_removed_classes) + 1.e-16)

    # check the leveling up value
    if strategy == 'mean':
        level_up = (mean_skill >= skill_threshold) & all([c >= count_threshold for c in null_removed_counts])
    elif strategy == 'all':
        level_up = all([weighted_per_class_skill_dict[s] >= skill_threshold for s in null_removed_classes]) & all([c >= count_threshold for c in null_removed_counts])

    return {'classes': classes,
            'confusion_simple': confusion_simple.tolist(),
            'weighted_skill': weighted_per_class_skill_dict,
            'skill': per_class_skill_dict,
            'count': per_class_count,
            'mean_skill': float(mean_skill),
            'level_up': bool(level_up)
            }


def get_confusion_matrix(extracts, relevant_reduction, mode, null_class):
    '''
        Returns two confusion matrices (both unweighted and weighted by subject difficulty),
        and the list of classes (for a k-class run). Note: confusion matrix for the k-class
        version is a pseudo-confusion matrix since there can be multiple true classes and multiple
        chosen classes per classification. This will require a many-to-many comparison which is
        inherently impossible. Therefore, we compare all incorrectly chosen classes with the "null"
        class instead.

        Parameters
        ----------
        extracts : list
            List of extracts for a given user
        relevant_reduction : dict
            Dictionary containing the `subject_difficulty` array that gives
            the difficulty of the all the subjects seen by the user
        mode : str
            The type of confusion matrix to return. Possible options are:
              - binary: (True/False) mode
              - one-to-one: k-class mode where individual classifications are compared against corresponding gold standard values
              - many-to-many mode: k-class mode where several volunteer classifications are compared against several gold standard values.
                In this case, incorrect classifications are compared against a `null_class` and therefore, the function returns a pseudo-confusion matrix.
        null_class : string
            The value of the null/non-existant class for the many-to-many k-class mode

        Returns
        -------
        confusion_simple : list
            Simple confusion matrix without subject difficulty weighting
        confusion_subject : list
            Confusion matrix with subject difficulty weighting
        classes : list
            List of unique classes corresponding to indices of the confusion matrix.
            Only returned for k-class mode
    '''
    if mode == 'binary':
        class_counts, subject_difficulties = get_user_skill_binary(extracts, relevant_reduction)
        true_counts = ['True'] * len(class_counts)
        classes = ['True', 'False']
    else:
        strategy = extracts[0]['feedback']['strategy']

        user_classifications = []
        classes = []

        true_key = 'true_' + FEEDBACK_STRATEGIES[strategy][0]

        true_values = []

        # first we need a list of labels
        # obtain a list of labels from user classifications
        for extracti in extracts:
            user_classifications += [key for key in extracti.keys() if isinstance(extracti[key], int) & (extracti[key] == 1)]

            # convert all answers to lower case to be consistent across both lists
            classes += [key.lower() for key in extracti.keys() if isinstance(extracti[key], int)]
            true_values.extend(list(map(lambda e: e.lower(), extracti['feedback'][true_key])))

        # get a full list of classes as the union of the two sets of labels
        classes = np.sort(np.unique([*np.unique(classes), *np.unique(true_values)]))
        classes = classes.tolist()

        difficulties = []
        for reductioni in relevant_reduction:
            difficulties.append(np.mean(reductioni['data']['difficulty']))

        subject_difficulty = 1 - np.asarray(difficulties)

        # we will loop through all the extracts and create a list
        # of user classified label and a corresponding gold standard
        # label. then, the confusion matrix is just determined using
        # the element-wise comparison between the two lists
        if mode == 'one-to-one':
            true_counts, class_counts, subject_difficulties = get_one_to_one(extracts, subject_difficulty, true_key)
        elif mode == 'many-to-many':
            true_counts, class_counts, subject_difficulties = get_multi_class(extracts, subject_difficulty, true_key, null_class)
            classes.append(null_class)
        else:
            raise ValueError(f"Mode must be 'binary', 'one-to-one' or 'many-to-many' not '{mode}'")

    # limit the difficulty to a mininum of 0.05 so that
    # easy subjects still have some weight
    subject_difficulties = np.clip(subject_difficulties, DIFFICULTY_FLOOR, 1)

    # get the simple confusion matrix without the subject difficulty
    confusion_simple = confusion_matrix(true_counts, class_counts, labels=classes)

    # get the more complicated confusion matrix accounting for subject difficulty
    confusion_subject = confusion_matrix(true_counts, class_counts, sample_weight=subject_difficulties,
                                         labels=classes)

    return (confusion_simple, confusion_subject, classes)


def get_user_skill_binary(extracts, relevant_reduction):
    '''
        Get the confusion matrix for a binary (True/False) case.
        This function is used to create a 2x2 confusion matrix where the second column (gold standard = False) is NaN.

        Inputs
        ------
        extracts : list
            List of extracts for a given user
        relevant_reduction : dict
            Dictionary containing the `subject_difficulty` array that gives
            the difficulty of the all the subjects seen by the user
        Returns
        -------
        class_counts : list
            List containing successful or incorrect classifications
        weights : list
            Corresponding weight for each classification based on the subject difficulty score
    '''
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

    true_mask = successes == 1
    false_mask = successes == 0

    weights = np.zeros_like(difficulties)

    weights[true_mask] = difficulties[true_mask]
    weights[false_mask] = 1 - difficulties[false_mask]

    class_counts = [str(s == 1) for s in successes]

    return class_counts, weights


def get_multi_class(extracts, subject_difficulty, true_key, null_class):
    '''
        Get the confusion matrix for a k-class many-to-many comparison.
        This function is used to create a (k + 1) x (k + 1) confusion matrix for
        `k` real classes and one additional `null_class`. In this case, it is not
        possible to get an accurate confusion between classes since many classes are
        compared simultaneously. Therefore, incorrect classifications are instead
        compared with the `null_class`.

        Inputs
        ------
        extracts : list
            List of extracts for a given user
        relevant_reduction : dict
            Dictionary containing the `subject_difficulty` array that gives
            the difficulty of the all the subjects seen by the user
        true_key : str
            Dictionary key to get the true choice from the extracts
        null_class : str
            Class name for the null class to be used for incorrect classifications
        Returns
        -------
        true_counts : list
            List containing the gold standard classes per classification
        class_counts : list
            List containing volunteer labels per classifications.
        weights : list
            Corresponding weight for each classification based on the subject difficulty score
    '''
    true_counts = []
    class_counts = []
    subject_difficulties = []

    for j, extract in enumerate(extracts):
        # find a list of user classified labels in this extract
        user_class_i = [key.lower() for key in extract.keys() if isinstance(extract[key], int) & (extract[key] == 1)]
        true_keys = [key.lower() for key in extract['feedback'][true_key]]

        # get a full list of classifications
        classi = np.sort(np.unique([*np.unique(true_keys),
                                    *np.unique(user_class_i)]))
        classi = classi.tolist()

        # create a temporary list of classes that will
        # incorporate both the user selected classes
        # and the tru classes
        true_count_i = [null_class] * len(classi)

        # loop through the true classes and populate the corresponding
        # indices in the list
        for value in true_keys:
            true_count_i[classi.index(value)] = value

        # do the same for the user classifications
        class_count_i = [null_class] * len(classi)

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
        subject_difficulty_i = [subject_difficulty[j]] * len(classi)
        for class_ind in range(len(classi)):
            if true_count_i[class_ind] != class_count_i[class_ind]:
                subject_difficulty_i[class_ind] = 1. - subject_difficulty[j]

        subject_difficulties.extend(subject_difficulty_i)

    return true_counts, class_counts, subject_difficulties


def get_one_to_one(extracts, subject_difficulty, true_key):
    '''
        Get the confusion matrix for a k-class one-to-one comparison.
        This function is used to create a k x k confusion matrix for
        `k` real classes.

        Inputs
        ------
        extracts : list
            List of extracts for a given user
        relevant_reduction : dict
            Dictionary containing the `subject_difficulty` array that gives
            the difficulty of the all the subjects seen by the user
        true_key : str
            Dictionary key to get the true choice from the extracts
        Returns
        -------
        true_counts : list
            List containing the gold standard classes per classification
        class_counts : list
            List containing volunteer labels per classifications.
        weights : list
            Corresponding weight for each classification based on the subject difficulty score
    '''
    true_counts = []
    class_counts = []
    subject_difficulties = []

    for j, extract in enumerate(extracts):
        # find a list of user classified labels in this extract
        # here, we know that there is only one classification class and true class
        user_class_i = [key.lower() for key in extract.keys() if isinstance(extract[key], int) & (extract[key] == 1)]
        true_keys = [key.lower() for key in extract['feedback'][true_key]]

        # also add the subject difficulties for each extract. subject
        # difficulty per class is not trivial to do, so we will average
        # the subject difficulty across all the classes in this subject.
        # easy subjects should get small bump for correct classifications
        # while difficult subjects will get a huge bump for success
        # do the opposite for failure scores: easy subject failures should be
        # penalized more strongly compared to difficulty failures
        if user_class_i == true_keys:
            subject_difficulties.append(subject_difficulty[j])
        else:
            subject_difficulties.append(1 - subject_difficulty[j])

        true_counts.extend(true_keys)
        class_counts.extend(user_class_i)

    return true_counts, class_counts, subject_difficulties

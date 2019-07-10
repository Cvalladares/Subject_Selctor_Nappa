# ****************************************************************#
# Requirements Section:                                           #
#                                                                 #
# The variables declared in this section represent the set of all #
# requirements in order to run nappa                              #
# ****************************************************************#

inclusion_criteria = {
    # Must contain either OkHttp or Retrofit as a client
    'http_client': {'com.squareup.okhttp3',
                    'com.squareup.retrofit2'},
    # Must compile to any sdk between 22 and 27
    # 'compileSdkVersion': {
    #                       'compileSdkVersion 26',
    #                       'compileSdkVersion 27',
    #                       # 'compileSdkVersion 22',
                          # 'compileSdkVersion 23',
                          # 'compileSdkVersion 24',
                          # 'compileSdkVersion 25',
                          # }
}
exclusion_criteria = {
    # may not use a minimum sdk lower than 22
    # 'minSdkVersion': {'minSdkVersion 14',
    #                   'minSdkVersion 15',
    #                   'minSdkVersion 16',
    #                   'minSdkVersion 17',
    #                   'minSdkVersion 18',
    #                   'minSdkVersion 19',
    #                   'minSdkVersion 20',
    #                   'minSdkVersion 21'},
    # May not use a target sdk version of sdk 28
    # 'targetSdkVersion': {'targetSdkVersion 28'
    #                      },
    #'androidx': {'androidx'},
    # Must not use kotline as the programming language
    'kotlin': {'kotlin', 'Kotlin'}

}


def contains_criteria(criterion, build_file_contents):
    for individual_criteria in criterion:
        # if the dependency is found in the build file,  then the project is a good candidate
        if individual_criteria in build_file_contents:
            return True

    # If the build file did not contain any of the dependencies
    return False


# ******************* TESTING FOR INCLUSION CRITERIA *******************************
def passes_all_inclusion_criteria(build_file_contents):
    for criteria, inclusion_criteria_candidates in inclusion_criteria.items():
        # For each category, assume that the project PASSES until a specific dependency category FAILS to be met
        if not contains_criteria(inclusion_criteria_candidates, build_file_contents):
            # print("Failed Inclusion Criteria: {0}".format(criteria))
            return False

    # If all inclusion criteria are met save this candidate
    return True


# ******************* TESTING FOR EXCLUSION CRITERIA *******************************

def contains_no_exclusion_criteria(build_file_contents):
    for criteria, exclusion_criteria_candidates in exclusion_criteria.items():
        # For each category, assume that the project PASSES until a specific exclusion dependency is found in the
        #   Build file
        if contains_criteria(exclusion_criteria_candidates, build_file_contents):
            # print("Contains Exclusion Criteria: {0}\t".format(criteria))
            return False

    # If all exclusion criteria are avoided, save this candidate
    return True

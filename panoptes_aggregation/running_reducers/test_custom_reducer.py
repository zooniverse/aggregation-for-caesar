from ..reducers.reducer_wrapper import reducer_wrapper
# DEFAULTS = {'id':{'default': None, 'type': str} }
@reducer_wrapper(defaults_data=None,user_id=True,relevant_reduction=True)
def test_custom_reducer(data_list,user_id,relevant_reduction):
    # result = {}
    for each_list,each_id,k in zip(data_list,user_id,relevant_reduction):
        each_list['user_id'] = each_id
        each_list['relevant_reduction'] = k
    #     if each_list['extractor_key'] == 'gold_standard':
    #         result['%s'%each_list['classification_id']] = each_list['data']
    # print(user_id)
    return data_list
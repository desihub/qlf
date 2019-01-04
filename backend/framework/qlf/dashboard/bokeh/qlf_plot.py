def sort_obj(gen_info):
    """ Hover info of objects type in fibers (wedge) plots.
            input: gen_info= mergedqa['GENERAL_INFO']
            returns: list(500)
    """
    obj_type = ['']*500
    for key in ['LRG', 'ELG', 'QSO', 'STAR', 'SKY']:
        if gen_info.get(key+'_FIBERID', None):
            for i in gen_info[key+'_FIBERID']:
                obj_type[i] = key
        else:
            pass
    return obj_type


import interface as bbox
cimport interface as bbox
import numpy as np



cdef int get_action_by_state_fast(float* state):	
    cdef int n_actions = 4
    cdef float best_val = -1e9
    cdef float val
    for act in range(n_actions):
        val = calc_reg_for_action(act, state)
        if val > best_val:
            best_val = val
            action_to_do = act
    return action_to_do

cdef float* reg_coefs

from cymem.cymem cimport Pool
cdef Pool mem = Pool() 
reg_coefs = <float*>mem.alloc(150, sizeof(float))

cdef int n_features, n_actions


def load_regression_coefs(filename):
        f = open(filename, "r")        
        for i in range (148):
            reg_coefs[i] = float(f.readline())  
        f.close()
        


cdef float c_dot(int action, float *state):
    cdef:
        float ans = 0
        int j = 0
        int i = action * 37
    while(i < (action + 1) * 37 - 1):
        ans = ans + reg_coefs[i] * state[j]
        j = j + 1
        i = i + 1
    ans = ans + reg_coefs[i]
    return ans

cdef float calc_reg_for_action(int action, float *state):     
        return c_dot(action, state)

 
def prepare_bbox():
    global n_features, n_actions
 
    if bbox.is_level_loaded():
        bbox.reset_level()
    else:
        bbox.load_level("../levels/train_level.data", verbose=1)
        n_features = bbox.get_num_of_features()
        n_actions = bbox.get_num_of_actions()
 
 
def run_bbox():
    cdef:
        float* state
        int action, has_next = 1
    prepare_bbox()
    load_regression_coefs("reg_coefs2.txt")
    while has_next:
        state = bbox.c_get_state()
        action = get_action_by_state_fast(state)
        has_next = bbox.c_do_action(action)
 
    bbox.finish(verbose=1)

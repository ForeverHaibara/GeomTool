import GeomTool
import Explainer

def get_value(vl, vnl):
    outlst = []
    for obj_num in range(len(vl)):
        if vnl[obj_num] == 0:
            outlst.append(vl[obj_num].freec)
        if vnl[obj_num] == 1:
            outlst.append(vl[obj_num].freec[0])
        if vnl[obj_num] == 2:
            outlst.append(vl[obj_num].freec[1])
    return outlst

def calc_value(instr, inlst, vl, vnl):
    for obj_num in range(len(vl)):
        if vnl[obj_num] == 0:
            vl[obj_num].freec = inlst[obj_num]
        if vnl[obj_num] == 1:
            vl[obj_num].freec = (inlst[obj_num], inlst[obj_num + 1])
    vl[obj_num].tree.calc_all()
    return Explainer.calculate(instr, vl[obj_num].tree.obj_list)

def update_value(inlst, vl, vnl):
    for obj_num in range(len(vl)):
        if vnl[obj_num] == 0:
            vl[obj_num].freec = inlst[obj_num]
        if vnl[obj_num] == 1:
            vl[obj_num].freec = (inlst[obj_num], inlst[obj_num + 1])
    vl[obj_num].tree.calc_all()

DELTA = 3e-5
FIRST_STEP = 1e-4
TIMES = 100

STEP = FIRST_STEP

def descent(in_str, in_tree):
    instr = in_str
    variable_list = []
    variable_num_list = []
    for obj in in_tree.get_movable():
        if obj.method.name == "free_pt":
            variable_list += [obj, obj]
            variable_num_list += [1, 2]
        else:
            variable_list += [obj]
            variable_num_list += [0]
    value_list = get_value(variable_list, variable_num_list)

    last_grad_list = []
    last_value_list = []
    for timer in range(TIMES):
        
        if timer > 0:
            last_grad_list = grad_list.copy()

        grad_list = []
        for obj_num in range(len(value_list)):
            value_list0 = value_list.copy()
            value_list0[obj_num] -= DELTA * 2
            fmm = calc_value(instr, value_list0, variable_list, variable_num_list)

            value_list0 = value_list.copy()
            value_list0[obj_num] -= DELTA
            fm = calc_value(instr, value_list0, variable_list, variable_num_list)

            value_list0 = value_list.copy()
            value_list0[obj_num] += DELTA
            fp = calc_value(instr, value_list0, variable_list, variable_num_list)

            value_list0 = value_list.copy()
            value_list0[obj_num] += DELTA * 2
            fpp = calc_value(instr, value_list0, variable_list, variable_num_list)

            der = ((fmm - fpp) - (fm - fp)*8) / (12 * DELTA)
            grad_list.append(der)
            update_value(value_list, variable_list, variable_num_list)
        
        # print(timer, grad_list)

        if timer == 0:
            STEP = FIRST_STEP
        else:
            delta_value_list = []
            for obj_num in range(len(value_list)):
                delta_value_list.append(value_list[obj_num] - last_value_list[obj_num])
            delta_grad_list = []
            for obj_num in range(len(grad_list)):
                delta_grad_list.append(grad_list[obj_num] - last_grad_list[obj_num])
            A = sum(delta_value_list[_] * delta_grad_list[_] for _ in range(len(value_list)))
            if A == 0:
                return timer
            B = sum(delta_grad_list[_] * delta_grad_list[_] for _ in range(len(grad_list)))
            STEP = abs(A / B)
            # print(timer, delta_grad_list, grad_list, last_grad_list, delta_value_list, value_list, last_value_list, A, B, STEP)

        last_value_list = value_list.copy()

        for obj_num in range(len(value_list)):
            value_list[obj_num] -= STEP * grad_list[obj_num]
        update_value(value_list, variable_list, variable_num_list)

    return TIMES

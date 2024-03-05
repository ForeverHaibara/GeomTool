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

def cyclic_det(x1, y1, x2, y2, x3, y3):
    # Determine whether the four points (0, 0), (xi, yi) are cyclic
    return x2**2 * (x3 * y1 - x1 * y3) + x2 * (-x3**2 * y1 + y3 * (x1**2 + y1**2 - y1 * y3)) + y2 * (-x1**2 * x3 + x3 * y1 * (-y1 + y2) + x1 * (x3**2 - y2 * y3 + y3**2))

def calc_datum(descent_datum, in_geom_list):
    # Calculate the descent datum. -- To minimize what? 
    outsum = 0
    for data in descent_datum:
        if data[0] == "eq":
            if data[1].type == "Point":
                outsum += (data[1].c[0] - data[2].c[0]) **2 + (data[1].c[1] - data[2].c[1]) **2
            if data[1].type == "Circle":
                outsum += (data[1].c[0] - data[2].c[0]) **2 + (data[1].c[1] - data[2].c[1]) **2 + (data[1].c[2] - data[2].c[2]) **2
            if data[1].type == "Line":
                outsum += (data[1].c[0] * data[2].c[1] - data[2].c[0] * data[1].c[1]) **2 + (data[1].c[1] * data[2].c[2] - data[2].c[1] * data[1].c[2]) **2 + (data[1].c[2] * data[2].c[0] - data[2].c[2] * data[1].c[0]) **2
            continue

        if data[0] == "eqdist":
            if data[1].type == "Line":
                d1 = (data[1].c[0] * data[2].c[0] + data[1].c[1] * data[2].c[1] + data[1].c[2])**2 / (data[1].c[0] ** 2 + data[1].c[1] ** 2)
            elif data[2].type == "Line":
                d1 = (data[2].c[0] * data[1].c[0] + data[2].c[1] * data[1].c[1] + data[2].c[2])**2 / (data[2].c[0] ** 2 + data[2].c[1] ** 2)
            else:
                d1 = (data[1].c[0] - data[2].c[0]) **2 + (data[1].c[1] - data[2].c[1]) **2
            if data[3].type == "Line":
                d2 = (data[3].c[0] * data[4].c[0] + data[3].c[1] * data[4].c[1] + data[3].c[2])**2 / (data[3].c[0] ** 2 + data[3].c[1] ** 2)
            elif data[4].type == "Line":
                d2 = (data[4].c[0] * data[3].c[0] + data[4].c[1] * data[3].c[1] + data[4].c[2])**2 / (data[4].c[0] ** 2 + data[4].c[1] ** 2)
            else:
                d2 = (data[3].c[0] - data[4].c[0]) **2 + (data[3].c[1] - data[4].c[1]) **2
            outsum += (d1 - d2) **2
            continue

        if data[0] == "col":
            outsum += (data[1].c[0] * data[2].c[1] + data[2].c[0] * data[3].c[1] + data[3].c[0] * data[1].c[1] - data[1].c[1] * data[2].c[0] - data[2].c[1] * data[3].c[0] - data[3].c[1] * data[1].c[0]) ** 2
            continue

        if data[0] == "cyc":
            outsum += (cyclic_det(data[2].c[0]-data[1].c[0], data[2].c[1]-data[1].c[1], data[3].c[0]-data[1].c[0], data[3].c[1]-data[1].c[1], data[4].c[0]-data[1].c[0], data[4].c[1]-data[1].c[1])) ** 2
            continue
        
        if data[0] == "para":
            outsum += ((data[1].c[1] - data[2].c[1]) * (data[3].c[0] - data[4].c[0]) - (data[3].c[1] - data[4].c[1]) * (data[1].c[0] - data[2].c[0])) ** 2
            continue
        
        if data[0] == "perp":
            outsum += ((data[1].c[1] - data[2].c[1]) * (data[3].c[1] - data[4].c[1]) + (data[3].c[0] - data[4].c[0]) * (data[1].c[0] - data[2].c[0])) ** 2
            continue

        if data[0] == "online":
            outsum += (data[1].c[0] * data[2].c[0] + data[1].c[1] * data[2].c[1] + data[2].c[2]) ** 2
            continue
        
        if data[0] == "oncirc":
            outsum += ((data[1].c[0] - data[2].c[0])**2 + (data[1].c[1] - data[2].c[1])**2 - data[2].c[2]**2) ** 2
            continue

        if data[0] == "eqangle":
            dx1 = x[2].c[0] - x[1].c[0]
            dy1 = x[2].c[1] - x[1].c[1]
            dx2 = x[4].c[0] - x[3].c[0]
            dy2 = x[4].c[1] - x[3].c[1]
            dx3 = x[6].c[0] - x[5].c[0]
            dy3 = x[6].c[1] - x[5].c[1]
            dx4 = x[8].c[0] - x[7].c[0]
            dy4 = x[8].c[1] - x[7].c[1]
            outsum += ((dy1 * dx2 - dy2 * dx1) * (dy3 * dy4 + dx3 * dx4) - (dy3 * dx4 - dy4 * dx3) * (dy1 * dy2 + dx1 * dx2)) ** 2
            continue

        if data[0] == "Formula":
            outsum += Explainer.calculate(data[1], in_geom_list) ** 2
    return outsum

def update_and_calc_value(datum, inlst, vl, vnl):
    for obj_num in range(len(vl)):
        if vnl[obj_num] == 0:
            vl[obj_num].freec = inlst[obj_num]
        if vnl[obj_num] == 1:
            vl[obj_num].freec = (inlst[obj_num], inlst[obj_num + 1])
    vl[0].tree.calc_all()
    return calc_datum(datum, vl[0].tree.obj_list)

def update_value(inlst, vl, vnl):
    for obj_num in range(len(vl)):
        if vnl[obj_num] == 0:
            vl[obj_num].freec = inlst[obj_num]
        if vnl[obj_num] == 1:
            vl[obj_num].freec = (inlst[obj_num], inlst[obj_num + 1])
    vl[0].tree.calc_all()

DERIVATIVE_DELTA = 3e-5
FIRST_STEP = 1e-6
BIGTIMES = 3
TIMES = 70

STEP = FIRST_STEP

def descent(in_datum, in_tree):
    datum = in_datum
    # Create a list of objects with free variables 
    # Variable_num_list: 0 if degree_of_freedom == 1; 1, 2 the freec tuple when degree_of_freedom == 2
    variable_list = []
    variable_num_list = []
    for obj in in_tree.get_movable():
        if obj.method.name == "free_pt":
            variable_list += [obj, obj]
            variable_num_list += [1, 2]
        else:
            variable_list += [obj]
            variable_num_list += [0]
    for bigtimer in range(BIGTIMES):
        
        # The list of values of the free variables
        value_list = get_value(variable_list, variable_num_list)
        last_grad_list = []
        last_value_list = []
        for timer in range(TIMES):
            
            if timer > 0:
                last_grad_list = grad_list.copy()

            grad_list = []
            for obj_num in range(len(value_list)):
                # Calculate the partial derivatives using values at 4 points
                value_list_shifted = value_list.copy()
                value_list_shifted[obj_num] -= DERIVATIVE_DELTA * 2
                fmm = update_and_calc_value(datum, value_list_shifted, variable_list, variable_num_list)

                value_list_shifted = value_list.copy()
                value_list_shifted[obj_num] -= DERIVATIVE_DELTA
                fm = update_and_calc_value(datum, value_list_shifted, variable_list, variable_num_list)

                value_list_shifted = value_list.copy()
                value_list_shifted[obj_num] += DERIVATIVE_DELTA
                fp = update_and_calc_value(datum, value_list_shifted, variable_list, variable_num_list)

                value_list_shifted = value_list.copy()
                value_list_shifted[obj_num] += DERIVATIVE_DELTA * 2
                fpp = update_and_calc_value(datum, value_list_shifted, variable_list, variable_num_list)

                der = ((fmm - fpp) - (fm - fp)*8) / (12 * DERIVATIVE_DELTA)
                grad_list.append(der)
                update_value(value_list, variable_list, variable_num_list)

            if timer == 0:
                STEP = FIRST_STEP
            else:
                # The Barzilar-Borwein Step
                delta_value_list = []
                for obj_num in range(len(value_list)):
                    delta_value_list.append(value_list[obj_num] - last_value_list[obj_num])
                delta_grad_list = []
                for obj_num in range(len(grad_list)):
                    delta_grad_list.append(grad_list[obj_num] - last_grad_list[obj_num])
                A = sum(delta_value_list[_] * delta_grad_list[_] for _ in range(len(value_list)))
                if A == 0:
                    return timer + bigtimer * TIMES
                B = sum(delta_grad_list[_] * delta_grad_list[_] for _ in range(len(grad_list)))
                STEP = abs(A / B)

            # Update values of free variables
            last_value_list = value_list.copy()
            for obj_num in range(len(value_list)):
                value_list[obj_num] -= STEP * grad_list[obj_num]
            update_value(value_list, variable_list, variable_num_list)

    return BIGTIMES * TIMES

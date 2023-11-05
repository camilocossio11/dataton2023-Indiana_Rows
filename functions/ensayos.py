def assign_breaks(start_day_schedule: list, lunch_schedule: list, demand: np.array, schedule: np.array, TC: bool, sat: bool):
    if TC == True and sat == False:
        final_slot = 34
    elif TC == True and sat == True:
        final_slot = 20
        lunch_schedule = [final_slot]*4 #la hora final si no tienen almuerzos
    elif TC == False:
        final_slot = 16
        lunch_schedule = [final_slot]*4 #la hora final si no tienen almuerzos

    for i in range(len(start_day_schedule)):
        breaks = []
        aux = lunch_schedule[i]-start_day_schedule[i]
        # Find the slots that cannot change due to the condition that employees must
        # work minimum 1 hour (4 slots) at the beginning, at the end of the day,
        # before and after lunch.
        if TC == True and sat == False:
            unavailable = set(
                list(range(0, 4)) +  # Beginning of the day
                list(range(aux-4, aux+10)) +  # Before, during and after lunch
                list(range(final_slot-4, final_slot))  # End of the day
            )
        else:
            unavailable = set(
                list(range(0, 4)) +  # Beginning of the day
                list(range(final_slot-4, final_slot))  # End of the day
            )
        # Find the candidate stripes to be active pause at the beginning of the day and
        # exclude those that cannot change
        beginning_day = set(list(range(4, 9))) - unavailable
        # Find the candidate stripes to be active pause before the lunch and exclude
        # those that cannot change
        if aux - 9 >= 0:
            before_lunch = set(list(range(aux-9, aux-4))) - unavailable
        else:
            before_lunch = set(list(range(0, aux-4))) - unavailable
        # Find the candidate stripes to be active pause after the lunch and exclude
        # those that cannot change
        if aux + 15 <= 34:
            after_lunch = set(list(range(aux+10, aux+15))) - unavailable
        else:
            after_lunch = set(list(range(aux+10, 34))) - unavailable
        # Find the candidate stripes to be active pause at the end of the day and
        # exclude those that cannot change
        ending_day = set(list(range(25, 30))) - unavailable
        # Evaluate if there are common elements in beginning_day and before_lunch
        if beginning_day & before_lunch:
            brk = assign_break_intersection(
                beginning_day, before_lunch, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif beginning_day.union(before_lunch):
            switch = set(
                list(range(0, lunch_schedule[i]-start_day_schedule[i])))
            brk = assign_break_no_intersection(beginning_day,
                                               before_lunch,
                                               demand,
                                               unavailable,
                                               switch,
                                               start_day_schedule[i])
            brk = list(map(lambda x: x + start_day_schedule[i], brk))
            breaks = breaks + brk
        # Evaluate if there are common elements in after_lunch and ending_day
        if after_lunch & ending_day:
            brk = assign_break_intersection(
                after_lunch, ending_day, demand, start_day_schedule[i])
            breaks = breaks + [brk]
        elif after_lunch.union(ending_day):
            switch = set(
                list(range(lunch_schedule[i]-start_day_schedule[i]+6, 34)))
            brk = assign_break_no_intersection(after_lunch,
                                               ending_day,
                                               demand,
                                               unavailable,
                                               switch,
                                               start_day_schedule[i])
            brk = list(map(lambda x: x + start_day_schedule[i], brk))
            breaks = breaks + brk
        schedule[i, breaks] = 2
        demand[breaks] = demand[breaks] + 1
    return [schedule, demand]
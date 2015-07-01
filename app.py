import random

def resolve_round(g):
    wolves = wolf_count(g)
    villagers = vill_count(g)
    if wolves >= villagers:
        results['w_win'] += 1
        return True
    elif wolves <= 0:
        results['v_win'] += 1
        return True
    elif wolves == 0 and villagers == 0:
        print('wtf')
        return True
    else:
        # game not over yet
        return False


def wolf_count(g):
    return g.values().count('w')

def vill_count(g):
    plain = g.values().count('v')
    bodyguard = g.values().count('b')
    return plain + bodyguard

def get_villager_ids(g):
    """ returns ids of all pro town """
    v_list = []
    for id in g.keys():
        if g[id] == 'v':
            v_list.append(id)
        elif g[id] == 'b':
            v_list.append(id)
    return v_list

def all_ids(g):
    return g.keys()

def remove_id(id_list, id):
    id_list.pop(id_list.index(id))
    return id_list

def is_wolf(g, id):
    if g[id] == 'w':
        return True
    else:
        return False

def is_guard(g, id):
    if g[id] == 'b':
        return True
    else:
        return False

def guard_pick(g):
    """ pick someone randomly not himself """
    guard_id = game_state['guard_id']
    guard_pick = random_pick(
                    remove_id(all_ids(g), guard_id))
    return guard_pick

def is_guard_alive(g):
    guard_id = game_state.get('guard_id', False)
    if guard_id:
        if g.get(guard_id) == 'b':
            return True
        else:
            return False
    else:
        return False


def random_pick(id_list):
    # here to add custom logic for scum quotients etc.
    return random.choice(id_list)

def get_wolf_ids(g):
    w_list = []
    for id in g.keys():
        if g[id] == 'v':
            w_list.append(id)
    return w_list

def day_round(g):
    # day
    # kill one random player
    d = random_pick(g.keys())
    # if guard is alive
    g = kill_player(g, d)

    return g

def kill_player(g, player_id):
    # remove player_id from g
    del g[player_id]
    return g

def night_round(g):
    """
    w pick random
    seer pick randomly
    bodyguard pick randomly
    """
    d = random_pick(get_villager_ids(g))

    # if guard is alive
    if is_guard_alive(g):
        # he picks a dude
        g_pick = guard_pick(g)
    else:
        g_pick = 'guard is dead'
    if g_pick != d:
        g = kill_player(g, d)
    else:
        pass
    return g

def new_game_setup(config):
    # quick setup
    players = {}
    curr_index = config['num_v']
    for i in range(curr_index): #up to num villagers
        players[i] = 'v'

    for j in range(curr_index, curr_index + config['num_w']):
        players[j] = 'w'

    curr_index += config['num_w']

    if config.get('num_b') > 0:
        players[curr_index] = 'b'
        game_state['guard_id'] = curr_index
    return players

def run_sim(config, n_trials):
    for i in range(n_trials):

        config['game_over'] = False # reset game
        players = new_game_setup(config)
        while True:
            # day
            players = day_round(players)
            config['game_over'] = resolve_round(players)
            if config['game_over']: break
            # night
            players = night_round(players)
            config['game_over'] = resolve_round(players)
            if config['game_over']: break

    return

def reset_results():
    return {'v_win': 0, 'w_win': 0}

def reset_state():
    return {}


no_b_config = {
        'game_over': False,
        'num_w': 4,
        'num_v': 16,
        'num_b': 0
}



w_b_config = {
        'game_over': False,
        'num_w': 4,
        'num_v': 15,
        'num_b': 1 #bodyguard
}

# sim 1
results = reset_results()
game_state = reset_state()
run_sim(no_b_config, 10000)
no_b_results = results

# sim 2
results = reset_results()
game_state = reset_state()
run_sim(w_b_config, 10000)
w_b_results = results

print('no bodyguard', no_b_results)
print('w. bodyguard', w_b_results)

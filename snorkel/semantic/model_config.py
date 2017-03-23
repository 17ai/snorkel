configuration = {
    # General
    'parallelism': 1,
    'max_docs': 1500,
    'splits': [0,1],
    'verbose': True,
    'seed': 0,


    # Supervision
    # source
    'source': 'py',
    'include': ['correct', 'passing'],
    # settings
    'model_dep': False,
    'majority_vote': False,
    # filters
    'beam_width': 10,
    'top_k': None,
    'remove_twins': False,
    'remove_useless': False,
    # restrictions
    'max_lfs': None,
    'max_train': None,
    'threshold': 1.0/3.0,
    # display
    'display_correlation': False,
    'display_marginals': False,
    # real-world conditions
    'include_closer_lfs': False,
    'remove_paren': True,
    # testing
    'traditional': False, # e.g, 1000
    'empirical_from_train': False,


    # Classification,
    'model': 'logreg',
    'n_search': 10,
    'n_epochs': 50,
    'rebalance': True,
    'b': 0.5,
    'lr': [1e-5, 1e-2],
    'l1_penalty': [1e-6, 1e-2],
    'l2_penalty': [1e-6, 1e-2],
    'print_freq': 5,
}
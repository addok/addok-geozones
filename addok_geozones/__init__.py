def preconfigure(config):
    # Default configuration values.
    config.GEOZONES_LEVELS = ['fr:region', 'fr:departement', 'fr:commune']
    config.GEOZONES_MAX_IMPORTANCE = {
        'fr:region': 11898502,
        'fr:departement': 2830000,
        'fr:commune': 2249975
    }

from shapely.geometry import shape

from addok.config import config
from addok.core import Result
from addok.helpers import yielder


@yielder
def prepare_document(doc):
    level = doc.get('level')
    if level not in config.GEOZONES_LEVELS:
        return
    doc.update(doc.get('keys'))  # Flat doc.
    max_importance = config.GEOZONES_MAX_IMPORTANCE.get(level)
    if max_importance:
        doc['importance'] = (doc.get('population', 0) / max_importance)
    if 'geom' not in doc:  # Geohisto adds old towns without shapes.
        return
    geom = shape(doc['geom'])
    doc['bounds'] = str(list(geom.bounds))
    center = geom.centroid
    doc['lat'] = center.y
    doc['lon'] = center.x
    del doc['geom']
    del doc['keys']
    return doc


def follow_successor(helper, result):
    if result.successors:
        id = result.successors
        try:
            successor = Result.from_id(id)
        except ValueError:
            # https://github.com/addok/addok-geozones/issues/1
            print('Unable to find successor {0.successors} from id '
                  '{0._id}'.format(result))
            return
        # Sometimes name does not change (merge).
        if successor.name != result.name:
            result.labels = ['{} (anciennement {})'.format(
                             successor.name, result.name)]
            result._cache = {}
            result._doc = successor._doc


def make_labels(helper, result):
    if not result.labels:
        result.labels = result._rawattr(config.NAME_FIELD)[:]
        postal = getattr(result, 'postal', None)
        if postal:
            result.labels.append(postal)
        code = getattr(result, 'code', None)
        if code:
            result.labels.append(code)

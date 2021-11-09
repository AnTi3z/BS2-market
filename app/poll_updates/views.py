from app.argparser import get_datetime_arg

from app.poll_updates import bp
from app.poll_updates.services import get_update, update_wait
from app.ident.decorators import ident_token_required


@bp.route('/api/updates')
@ident_token_required
def handle_updates():
    from_datetime = get_datetime_arg()

    result = None
    # try to get new records from db
    if from_datetime:
        result = get_update(from_datetime)

    # if no new data in db then wait for new data
    if not result:
        # db.close()
        result = update_wait()

    return result or ""

import falcon
from falcon_cors import CORS
import meter

# https://github.com/lwcolton/falcon-cors
cors = CORS(allow_all_origins=True,
            allow_credentials_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)
api = falcon.API(middleware=[cors.middleware])

api.add_route('/meters',
              meter.MeterCollection())
api.add_route('/meters/{id_}',
              meter.MeterItem())

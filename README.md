# booking-api

## Installation & Usage

### Create client package

```bash
mkdir booking_api_client
cd booking_api_client
~/bin/openapitools/openapi-generator-cli generate -i /media/sf_private/api/booking.json -g python --package-name booking_api_client
```
Open with Pycharm and open Python terminal

```bash
pip install build 
python -m build
```

The result is a whl file under dists. This can be installed the normal pip-way:
```sh
pip install /home/datalab/Documenten/dev/openapi-generator/dist/booking_api_client-1.0.0-py3-none-any.whl
```

Then import the package:
```python
import booking_api_client
```

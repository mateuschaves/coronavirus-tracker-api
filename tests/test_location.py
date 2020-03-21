import pytest
from unittest import mock
from app import location, coordinates, timeline

def mocked_timeline(*args, **kwargs):
    class TestTimeline:
        def __init__(self, latest):
            self.latest = latest
            
    return TestTimeline(args[0])

@pytest.mark.parametrize("test_id, country, country_code, province, latitude, longitude, \
                          confirmed_latest, deaths_latest, recovered_latest",
                         [(0, "Thailand", "TH", "", 15, 100, 1000, 1111, 22222),
                          (1, "Deutschland", "DE", "", 15, 100, 1000, 1111, 22222),
                          (2, "Cruise Ship", "XX", "", 15, 100, 1000, 1111, 22222)])
@mock.patch('app.timeline.Timeline', side_effect=mocked_timeline)
def test_location_class(mocked_timeline, test_id, country, country_code, province, latitude,
                        longitude, confirmed_latest, deaths_latest, recovered_latest):

    # id, country, province, coordinates, confirmed, deaths, recovered
    coords = coordinates.Coordinates(latitude=latitude, longitude=longitude)

    # Timelines
    confirmed = timeline.Timeline(confirmed_latest)
    deaths = timeline.Timeline(deaths_latest)
    recovered = timeline.Timeline(recovered_latest)

    # Location.
    location_obj = location.TimelinedLocation(test_id, country, province, coords, {
        'confirmed': confirmed, 
        'deaths'   : deaths,
        'recovered': recovered,
    })

    assert location_obj.country_code == country_code

    #validate serialize
    check_dict = {
        'id': test_id,
        'country': country,
        'country_code': country_code,
        'province': province,
        'coordinates': {
            'latitude': latitude,
            'longitude': longitude
        },
        'latest': {
            'confirmed': confirmed_latest,
            'deaths': deaths_latest,
            'recovered': recovered_latest
        }
    }

    assert location_obj.serialize() == check_dict
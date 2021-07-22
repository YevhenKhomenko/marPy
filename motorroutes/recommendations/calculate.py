from navigation.models import Points
from .serializers import PointViewSerializer
import math


class GetNearest():
    def __init__(self):
        self.TO_KM = 111.2
        self.CIRCLE = 57.3

    def get_distance(self, point):
        # distance formula: SQRT( POW(111.2 * (latitude - [startlat]), 2) +  POW(111.2 * ([startlng] - longitude) * COS(latitude / 57.3), 2)) AS distance
        all_attractions = Points.objects.filter(attractions=True)
        d = {}
        for row in all_attractions:
            distance = math.sqrt(pow(self.TO_KM * (getattr(row, 'latitude') - getattr(point[0], 'latitude')), 2) + pow(
                self.TO_KM * (getattr(point[0], 'longitude') - getattr(row, 'longitude')) * math.cos(
                    getattr(row, 'latitude')) / self.CIRCLE, 2))
            d[getattr(row, 'id')] = {'distance': distance}
        sorted_d = sorted(d.items(), key=lambda k_v: k_v[1]['distance'])
        list_id = {k: v for k, v in sorted_d[0:5]}
        return list_id

    def get_nearest_points(self, point):
        list_id = self.get_distance(point)
        result = {}
        for k, v in list_id.items():
            point_q = Points.objects.get(id=k)
            point_q_detail_data = PointViewSerializer(point_q, context={"distance": {k: v.get("distance")}}).data
            result[k] = point_q_detail_data
        return result

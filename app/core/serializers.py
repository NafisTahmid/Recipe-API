from rest_framework import serializers

class GeoSerializer(serializers.Serializer):
    lat = serializers.CharField()
    lng = serializers.CharField()


class AddressSerializer(serializers.Serializer):
    street = serializers.CharField()
    suite = serializers.CharField()
    city = serializers.CharField()
    zipcode = serializers.CharField()
    geo = GeoSerializer()

class CompanySerializer(serializers.Serializer):
    name = serializers.CharField()
    catchPhrase = serializers.CharField()
    bs = serializers.CharField()

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    address = AddressSerializer()
    phone = serializers.CharField()
    website = serializers.CharField()
    company = CompanySerializer()


class AudioStreamSerializer(serializers.Serializer):
    accessPoint = serializers.CharField()
    isActivated = serializers.BooleanField()

class VideoStreamSerializer(serializers.Serializer):
    accessPoint = serializers.CharField()

# class CameraSerializer(serializers.Serializer):
#     camera_url = serializers.SerializerMethodField()
#     camera_access = serializers.CharField()
#     comment = serializers.CharField()
#     displayId = serializers.CharField()
#     displayName = serializers.CharField()
#     enabled = serializers.BooleanField()
#     ip_address = serializers.CharField(source='ipAddress')
#     panomorph = serializers.BooleanField()
#     latitude = serializers.CharField()
#     longitude = serializers.CharField()
#     model = serializers.CharField()
#     is_activated = serializers.BooleanField(source='isActivated')
#     camera_id = serializers.CharField(source='displayId')
#     location = serializers.CharField(source='displayName')
#     azimuth = serializers.CharField()
#     vendor= serializers.CharField()

#     def get_camera_url(self, obj):
#         vendor_sid = 'root'
#         vendor_key = 'Accelx123456'
#         base_url = '192.168.1.13:8000'
#         access_point = obj.get('videoStreams', [{}])[0].get('accessPoint', '')
#         return f"http://{vendor_sid}:{vendor_key}@{base_url}/live/media/snapshot/{access_point}"

class CameraSerializer(serializers.Serializer):
    accessPoint = serializers.CharField()
    archives = serializers.ListField(child=serializers.CharField(), default=list)
    audioStreams = serializers.CharField()
    azimuth = serializers.CharField()
    camera_access = serializers.CharField()
    comment = serializers.CharField()
    detectors = serializers.ListField(child=serializers.CharField(), default=list)
    displayId = serializers.CharField()
    displayName = serializers.CharField()
    enabled = serializers.BooleanField()
    groups = serializers.ListField(child=serializers.CharField(), default=list)
    ipAddress = serializers.CharField()
    isActivated = serializers.BooleanField()
    latitude = serializers.BooleanField()
    longitude = serializers.CharField()
    model = serializers.CharField()
    offlineDetectors = serializers.CharField()
    panomorph = serializers.BooleanField()
    ptzs = serializers.ListField(child=serializers.CharField(), default=list)
    rays = serializers.ListField(child=serializers.CharField(), default=list)
    textSources = serializers.ListField(child=serializers.CharField(), default=list)
    vendor = serializers.CharField()
    videoStreams = serializers.CharField()
from rest_framework import generics
from rest_framework.views import APIView

from .models import Image
from .serializers import ImageSerializer

from django.http import JsonResponse

class ImageList(generics.ListAPIView):
    queryset = Image.objects.raw("SELECT * FROM Image")
    serializer_class = ImageSerializer




class MisLabelledImages(APIView):

    # GET /image/mislabelled/?count=num
    # {
    #     images: Array<{
    #         url:string
    #         image_id: string
    #     }>
    # }
    def get(self, request, format=None):
        from django.db import connection, transaction

        count = int(request.GET.get("count")) if request.GET.get("count") and int(request.GET.get("count")) < 100 else 25


        row_ordering = ["url", "img_id"]

        cursor = connection.cursor()

        cursor.execute("SELECT small_url, img_id FROM image WHERE img_id IN \
        (SELECT DISTINCT img_id FROM Classification as c, Label as l \
            WHERE confidence < 0.5 \
            AND pre_classified = %s \
            AND c.label_id = l.label_id LIMIT %s)", (True, count))
        mislabelled_images = cursor.fetchall()

        cursor.execute("SELECT small_url, img_id FROM image WHERE img_id IN \
        (SELECT DISTINCT img_id FROM Classification as c, Label as l \
            WHERE confidence < 0.5 \
            AND pre_classified = %s \
            AND c.label_id = l.label_id LIMIT %s)", (False, count))

        mislabelled_images.extend(cursor.fetchall())
        parsed_mislabelled_images = []

        for image in mislabelled_images:
            img_obj = {}
            for i, val in enumerate(image):
                img_obj[row_ordering[i]] = val
            parsed_mislabelled_images.append(img_obj)

        return JsonResponse(parsed_mislabelled_images, safe=False)
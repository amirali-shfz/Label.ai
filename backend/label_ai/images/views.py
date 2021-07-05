from rest_framework import generics
from rest_framework.views import APIView

from .models import Image
from .serializers import ImageSerializer

from django.http import JsonResponse, Http404

class ImageListView(generics.ListAPIView):

    # GET /label/all
    # Resp:
    # {
    #   labels: Array<{
    #       label_id:string,
    #       name: string
    #   }>
    # }
    queryset = Image.objects.raw("SELECT * FROM Image")
    serializer_class = ImageSerializer

class ImagesByLabelView(APIView):

    # GET /image/?label_id=""
    # Resp:
    # {
    #   images: Array<{
    #       url: string,
    #       image_id: string,
    #   }>
    # }
    def get(set, request, format=None):
        from django.db import connection, transaction
        
        if not request.GET.get("label_id"): raise Http404() 
        label_id = request.GET.get("label_id")
        row_ordering = ["url", "img_id" ]
        
        sql_statement = "SELECT i.original_url, i.img_id FROM classificationview as c, image as i, label as l \
            WHERE i.img_id = c.img_id AND c.label_id = l.label_id \
                AND c.pre_classified = True \
                AND l.label_id = %s \
                AND c.confidence >= %s LIMIT %s"

        cursor = connection.cursor()
        cursor.execute(sql_statement, [label_id, 0, 50]) # TODO: in prod change to [label_id, 0.8, 50]
        label_related_imgs = cursor.fetchall()

        parsed_images = []

        for image in label_related_imgs:
            img_obj = {}
            for i, val in enumerate(image):
                img_obj[row_ordering[i]] = val
            parsed_images.append(img_obj)

        return JsonResponse(parsed_images, safe=False)

class MisLabelledImagesView(APIView):

    # GET /image/mislabelled/?count=num
    # {
    #     images: Array<{
    #         url:string
    #         image_id: string
    #         labels: Array<{ label_id: string, name: string  }>       
    #     }>
    # }
    def get(self, request, format=None):
        from django.db import connection, transaction

        count = int(request.GET.get("count")) if request.GET.get("count") and int(request.GET.get("count")) < 500 else 500
        row_ordering = {
            "original_url": 0, 
            "name": 1, 
            "img_id": 2, 
            "label_id": 3
        }

        cursor = connection.cursor()
        cursor.execute("SELECT original_url, name, img_id, label_id \
        FROM MisClassification NATURAL JOIN Image NATURAL JOIN Label \
        WHERE pre_classified LIMIT %s", [count])
        ml_images = cursor.fetchall()

        parsed_ml_images = []
        parsed_image_map = {}

        for image in ml_images:
            url = image[row_ordering["original_url"]]
            img_id = image[row_ordering["img_id"]]
            label_id = image[row_ordering["label_id"]]
            name = image[row_ordering["name"]]
             
            if img_id not in parsed_image_map: 
                parsed_image_map[img_id] = len(parsed_ml_images)
                parsed_ml_images.append({
                    "img_id": img_id,
                    "url": url,
                    "labels": []
                })

            parsed_ml_images[parsed_image_map[img_id]]["labels"].append({
                "label_id": label_id,
                "name": name
            })        

        return JsonResponse(parsed_ml_images, safe=False)


class UnderClassifiedImagesViews(APIView):

    # GET /image/underclassified/?count=num
    # {
    #     images: Array<{
    #         url:string
    #         image_id: string
    #         labels: Array<{ label_id: string, name: string  }>       
    #     }>
    # }
    def get(self, request, format=None):
        from django.db import connection, transaction

        count = int(request.GET.get("count")) if request.GET.get("count") and int(request.GET.get("count")) < 500 else 500
        row_ordering = {
            "original_url": 0, 
            "name": 1, 
            "img_id": 2, 
            "label_id": 3
        }

        cursor = connection.cursor()
        cursor.execute("SELECT original_url, name, img_id, label_id \
        FROM ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label \
        WHERE NOT pre_classified LIMIT %s", [count])
        uc_images = cursor.fetchall()

        parsed_uc_images = []
        parsed_image_map = {}
        
        for image in uc_images:
            url = image[row_ordering["original_url"]]
            img_id = image[row_ordering["img_id"]]
            label_id = image[row_ordering["label_id"]]
            name = image[row_ordering["name"]]
             
            if img_id not in parsed_image_map: 
                parsed_image_map[img_id] = len(parsed_uc_images)
                parsed_uc_images.append({
                    "img_id": img_id,
                    "url": url,
                    "labels": []
                })

            parsed_uc_images[parsed_image_map[img_id]]["labels"].append({
                "label_id": label_id,
                "name": name
            })        

        return JsonResponse(parsed_uc_images, safe=False)


class ImageClassificationPrompt(APIView):
    def get(self, request, format=None):
        from django.db import connection, transaction
        cursor = connection.cursor()
        query = 'SELECT small_url, original_url, name, class_id\
                 FROM (UnConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label)\
                 as a WHERE NOT EXISTS (SELECT * FROM Submission\
                 WHERE member_id = %s AND class_id = a.class_id) ORDER BY RANDOM() LIMIT %s;'
        cursor.execute(query,(1,1))
        image_classification_prompt = cursor.fetchall()
        return JsonResponse(image_classification_prompt[0], safe=False)

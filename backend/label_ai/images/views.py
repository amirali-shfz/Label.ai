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

    # GET /image/confirmed/?label_id=""
    # Resp:
    # {
    #   images: Array<{
    #       url: string,
    #       image_id: string,
    #       total_votes: int,
    #       confidence: float,
    #   }>
    # }
    def get(set, request, format=None):
        from django.db import connection, transaction
        
        if not request.GET.get("label_id"): raise Http404() 
        label_id = request.GET.get("label_id")
        row_ordering = ["url", "img_id", "total_votes", "confidence"]
        
        sql_statement = "SELECT i.original_url, i.img_id, c.total_votes, c.confidence FROM classificationview as c, image as i, label as l \
            WHERE i.img_id = c.img_id AND c.label_id = l.label_id \
                AND c.pre_classified = True \
                AND l.label_id = %s \
                AND c.confidence >= %s LIMIT %s;"

        cursor = connection.cursor()
        cursor.execute(sql_statement, [label_id, 0, 50]) # TODO: parameterize limit
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
# GET /images/prompt?count=num?user_id=num
# {
# prompt:
#   Array<{
#       url: string,
#       image_id: string,
#       labels: Array<{
#           label_id: string,
#           label_name: string,
#           class_id: int
#       }>
#   }>
# }
    def get(self, request, format=None):
        from django.db import connection
        count = int(request.GET.get("count")) if request.GET.get("count") else 100
        user_id = int(request.GET.get("user_id"))

        cursor = connection.cursor()
        query = 'SELECT original_url, img_id, class_id, label_id, name\
                 FROM (UnConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label)\
                 as a WHERE NOT EXISTS (SELECT * FROM Submission\
                 WHERE member_id = %s AND class_id = a.class_id) ORDER BY RANDOM() LIMIT %s;'
        cursor.execute(query,(user_id, count))

        image_classification_prompt = cursor.fetchall()
        images = {}
        for url, img_id, class_id, label_id, label_name in image_classification_prompt:
            images.setdefault(img_id, {"url": url, "labels": []})
            images[img_id]["labels"].append({
                "label_id": label_id,
                "label_name": label_name,
                "class_id": class_id
            })

        prompt = []
        for img_id, val in images.items():
            prompt.append({"url": val["url"], "image_id": img_id, "labels": val["labels"]})

        parsed_out = {"prompt": prompt}
        
        return JsonResponse(parsed_out)

# GET /image/<endpoint>/?<label_id="">,count=""
# Resp:
# {
#   images: Array<{
#       class_id: string,
#       url: string,
#       img_id: string,
#       total_votes: int,
#       confidence: float,
#       label: string,
#   }>
# }
def get_images_label_count(query, request, format=None):
        from django.db import connection
        
        query = "SELECT class_id, original_url, img_id, total_votes-10 as total_votes, confidence, name as label_name " + query

        count = int(request.GET.get("count")) if request.GET.get("count") else 100
        label_id = request.GET.get("label_id")
        count = [count]
        label_id = [label_id] if label_id else []
        print(label_id+count)

        row_ordering = ["class_id", "url", "img_id", "total_votes", "confidence", "label"]

        cursor = connection.cursor()
        cursor.execute(query, label_id+count)
        label_related_imgs = cursor.fetchall()

        parsed_images = []

        for image in label_related_imgs:
            img_obj = {}
            for i, val in enumerate(image):
                
                img_obj[row_ordering[i]] = val
            parsed_images.append(img_obj)
        print(parsed_images)
        return JsonResponse(parsed_images, safe=False)



class MisclassifiedImagesView(APIView):
    def get(self, request, format=None):
        query = "FROM Misclassification NATURAL JOIN Image NATURAL JOIN Label \
                LIMIT %s;"
        return get_images_label_count(query, request)

class ConfirmedClassificationsByLabelView(APIView):
    def get(self, request, format=None):
        query = "FROM ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label \
                WHERE pre_classified AND label_id=%s \
                LIMIT %s;"
        return get_images_label_count(query, request)


class ConfirmedClassificationImagesView(APIView):
    def get(self, request, format=None):
        query = "FROM ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label \
                WHERE pre_classified \
                LIMIT %s;"
        return get_images_label_count(query, request)

class NewClassificationsImagesView(APIView):
    def get(self, request, format=None):
        query = "FROM ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label \
                WHERE NOT pre_classified \
                LIMIT %s;"
        return get_images_label_count(query, request)

class LeastVotesClassificationImagesView(APIView):
    def get(self, request, format=None):
        query = "FROM ClassificationView NATURAL JOIN Image NATURAL JOIN Label \
                WHERE AND label_id = %s \
                ORDER BY total_votes asc \
                LIMIT %s;"
        return get_images_label_count(query, request)
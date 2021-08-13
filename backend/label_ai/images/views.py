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
def get_images_label_count(query_FROM, query_WHERE, query_OTHER, request, format=None):
        from django.db import connection
        
        count = int(request.GET.get("count")) if request.GET.get("count") else 100
        label_id = request.GET.get("label_id")
        
        if label_id:
            if query_WHERE:
                query_WHERE += f" AND label_id='{label_id}'"
            else:
                query_WHERE = f"label_id='{label_id}'"

        query_SELECT = "SELECT class_id, original_url, img_id, total_votes-10 as total_votes, confidence, name as label_name"

        if not query_OTHER:
            query_OTHER = ""

        query = query_SELECT + " FROM "+ query_FROM
        if query_WHERE:
            query += " WHERE " + query_WHERE
        query += query_OTHER + f" LIMIT 10"
        
        print(query)
        row_ordering = ["class_id", "url", "img_id", "total_votes", "confidence", "label"]

        cursor = connection.cursor()
        cursor.execute(query)
        label_related_imgs = cursor.fetchall()

        parsed_images = []

        for image in label_related_imgs:
            img_obj = {}
            for i, val in enumerate(image):
                
                img_obj[row_ordering[i]] = val
            parsed_images.append(img_obj)
        print(parsed_images)
        return JsonResponse(parsed_images, safe=False)

# /all/?count=""
class All_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "ClassificationView NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = None
        query_OTHER = None 
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER,  request, format)

# /confirmed/?count=""
class Confirmed_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = "pre_classified"
        query_OTHER = None
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER,  request, format)

# /misclassified/?count=""
class Misclassified_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "Misclassification NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = None
        query_OTHER = None
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER,  request, format)

# /discovered/?count=""
class DiscoveredClassification_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "ConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = "NOT pre_classified"
        query_OTHER = None
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER,  request, format)

# /controversial/?count=""
class Controversial_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "UnconfirmedClassification NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = "total_votes > 100 AND confidence < 0.7"
        query_OTHER = None
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER,  request, format)

# /leastvotes/?count=""
class LeastVotes_Endpoint(APIView):
    def get(self, request, format=None):
        query_FROM = "ClassificationView NATURAL JOIN Image NATURAL JOIN Label"
        query_WHERE = None
        query_OTHER = "ORDER BY total_votes asc"
        return get_images_label_count(query_FROM, query_WHERE, query_OTHER, request, format)

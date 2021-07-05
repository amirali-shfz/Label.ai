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
        row_ordering = ["original_url", "small_url", "img_id" ]
        
        sql_statement = "SELECT original_url, small_url, img_id \
            FROM ConfirmedClassification NATURAL JOIN Image \
            WHERE l.label_id = %s LIMIT %s;"

        cursor = connection.cursor()
        cursor.execute(sql_statement, [label_id, 50]) # TODO: parameterize limit
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
    #     }>
    # }
    def get(self, request, format=None):
        from django.db import connection, transaction

        count = int(request.GET.get("count")) if request.GET.get("count") and int(request.GET.get("count")) < 100 else 25
        row_ordering = ["url", "img_id"]

        cursor = connection.cursor()

        cursor.execute("SELECT small_url, img_id FROM image WHERE img_id IN \
        (SELECT DISTINCT img_id FROM ClassificationView as c, Label as l \
            WHERE confidence < %s \
            AND pre_classified = %s \
            AND c.label_id = l.label_id LIMIT %s)", (0.5, True, count))
        mislabelled_images = cursor.fetchall()

        cursor.execute("SELECT small_url, img_id FROM image WHERE img_id IN \
        (SELECT DISTINCT img_id FROM ClassificationView as c, Label as l \
            WHERE confidence < %s \
            AND pre_classified = %s \
            AND c.label_id = l.label_id LIMIT %s)", (0.5, False, count))

        mislabelled_images.extend(cursor.fetchall())
        parsed_mislabelled_images = []

        for image in mislabelled_images:
            img_obj = {}
            for i, val in enumerate(image):
                img_obj[row_ordering[i]] = val
            parsed_mislabelled_images.append(img_obj)

        return JsonResponse(parsed_mislabelled_images, safe=False)

class ImageClassificationPrompt(APIView):
    # GET /images/prompt?count=num,user_id=""
	# return {prompt:[{url, image_id, labels:[{label_id, label_name, class_id}]}]}
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
            images[img_id]["labels"].append({"label_id": label_id, "label_name": label_name, "class_id": class_id})

        prompt = []
        for img_id, val in images.items():
            prompt.append({"url": val["url"], "image_id": img_id, "labels": val["labels"]})

        parsed_out = {"prompt": prompt}
        
        return JsonResponse(parsed_out)


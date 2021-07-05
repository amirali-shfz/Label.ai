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
    # GET /image/prompt
    # {
    #     images: Array<{
    #           original_url: string,
    #           name: string,
    #           class_id: int
    #     }>
    # }
    def get(self, request, format=None):
        '''
        GET /image/prompt?count=num?user_id=num
        {
        prompt:
        Array<
        url: string,
        image_id: string,
        label_name: string>
        >
        }
        '''
        from django.db import connection, transaction
        cursor = connection.cursor()
        query = 'SELECT original_url, name, class_id\
                 FROM (UnConfirmedClassification NATURAL JOIN Image NATURAL JOIN Label)\
                 as a WHERE NOT EXISTS (SELECT * FROM Submission\
                 WHERE member_id = %s AND class_id = a.class_id) ORDER BY RANDOM() LIMIT %s;'
        cursor.execute(query,(1,1))
        image_classification_prompt = cursor.fetchall()
        image_classification_prompt=image_classification_prompt[0]
        image_classification_prompt = {
            'original_url':image_classification_prompt[0],
            'label_name_string':image_classification_prompt[1],
            'classification_id':image_classification_prompt[2]
        }
        return JsonResponse(image_classification_prompt)

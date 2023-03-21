from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import FileSystemStorage
from AudioToText.helper import *
import uuid
from django.http import HttpResponse, FileResponse


class AudioToTextAPIView(APIView):
    def get(self, request):
        return Response(
            {"data": "", "msg": "Rendered successfully"},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        try:
            filename = ""
            extracted_text = ""
            print(request.FILES)
            print(request.data)
            if request.FILES is not None:
                request_file = request.FILES["file"]

                folder_name = (
                    str(uuid.uuid4()) + "_" + str(request_file.name).split(".")[0]
                )
                print(folder_name)
                # create a new instance of FileSystemStorage
                fs = FileSystemStorage()
                file = fs.save(folder_name + "/" + request_file.name, request_file)
                # the fileurl variable now contains the url to the file. This can be used to serve the file when needed.
                fileurl = fs.url(file)
                print(fileurl)
                extracted_text = extract_txt_frm_audio(
                    filename=str(request_file.name), foldername=str(folder_name)
                )

                ##after everything is done delete that whole folder
                # clear_directory_with_startswith()
            else:
                return Response(
                    {"data": "", "msg": "File not found."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"data": "", "msg": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # file_path = os.path.join(folder_name, "file.txt")
        # if os.path.exists(file_path):
        #     with open(file_path, "rb") as fh:
        #         response = HttpResponse(fh.read(), content_type="text/plain")
        #         response[
        #             "Content-Disposition"
        #         ] = 'attachment; filename="Audio2Text.txt"'
        #         print("Correct")
        #         print(response)
        #         return response

        return Response(
            {"data": extracted_text, "msg": "Converted successfully"},
            status=status.HTTP_200_OK,
        )

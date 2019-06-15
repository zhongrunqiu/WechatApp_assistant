import os
from django.http import Http404,HttpRequest,HttpResponse,FileResponse,JsonResponse
from backend import settings
import utils.response
from django.views import View
import hashlib

def image(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imagefile = os.path.join(settings.IMAGES_DIR,md5 + '.jpg')
        if not os.path.exists(imagefile):
            return Http404()
        else:
            # data = open(imagefile,'rb').read()
            # return HttpResponse(content=data,content_type='image/jpg')
            return FileResponse(open(imagefile,'rb'),content_type='image/jpg')

class ImageListView(View,utils.response.CommonResponseMixin):
    def get(self,request):
        image_files = os.listdir(settings.IMAGES_DIR)
        response_data = []
        for image_file in image_files:
            response_data.append(
                {
                    'name':image_file,
                    'md5':image_file[:-4]
                }
            )
        response_data = self.wrap_json_response(data=response_data)
        return JsonResponse(data=response_data,safe=False)

class ImageView(View,utils.response.CommonResponseMixin):
    def get(self,request):
        if request.method == 'GET':
            md5 = request.GET.get('md5')
            img_file = os.path.join(settings.IMAGES_DIR,md5 + '.jpg')
            if not os.path.exists(img_file):
                return Http404()
            else:
                return FileResponse(open(img_file,'rb'),content_type='image/jpg')
    def post(self,request):
        files = request.FILES
        response = []
        for key,value in files.items():
            content = value.read()
            md5 = hashlib.md5(content).hexdigest()
            path = os.path.join(settings.IMAGES_DIR,md5 + '.jpg')
            with open(path,'wb') as f:
                f.write(content)
                f.close()
            response.append({
                'name':key,
                'md5':md5
            })
        message = 'post method success'
        response = self.wrap_json_response(data=response,message=message)
        return JsonResponse(response,safe=False)
    def put(self,request):
        message = 'put method success'
        response = self.wrap_json_response(message=message)
        return JsonResponse(response,safe=False)
    def delete(self,request):
        md5 = request.GET.get('md5')
        img_name = md5 + '.jpg'
        img_file = os.path.join(settings.IMAGES_DIR,img_name)
        if os.path.exists(img_file):
            os.remove(img_file)
            message = 'remove success'
        else:
            message = 'File(%s) not found' % img_name
        response = self.wrap_json_response(message=message)
        return JsonResponse(response,safe=False)

def image_text(request):
    if request.method == 'GET':
        md5 = request.GET.get('md5')
        imagefile = os.path.join(settings.IMAGES_DIR,md5 + '.jpg')
        if not os.path.exists(imagefile):
            return utils.response.wrap_json_response(utils.response.ReturnCode.RESOURCES_NOT_EXISTS)
        else:
            response_data = {}
            response_data['name'] = md5 + '.jpg'
            response_data['url'] = '/service/image?md5=%s' % md5
            response = utils.response.wrap_json_response(data=response_data)
            return JsonResponse(response,safe=False)
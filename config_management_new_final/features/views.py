from django.views.generic import View
from .models import Feature
from django.http.response import JsonResponse
import json
from domain_feature_mapping.models import DomainFeatureMapping

# Create your views here.
class FeatureView(View):

    def get(self, request, f_id): #get a feature name using its id

        if Feature.objects.filter(id=f_id).exists(): #raising error if feature with provided id doesn't exist
            feature_object = Feature.objects.get(id=f_id) 
        else:
            return JsonResponse({'error_message':'The requested feature does not exist'})

        map_object = DomainFeatureMapping.objects.filter(feature=f_id).all()
        domain_id_list = []
        for obj in (list(map_object)):
            domain_info={}
            domain_info['name']=obj.domain.name
            domain_info['id']=obj.domain.id
            domain_id_list.append(domain_info)

        feature_info = feature_object.get_info()
        feature_info['domain_id_list'] = domain_id_list
                
        args = {'feature_info':feature_info} 

        return JsonResponse(args) #returning feature's name and id


    def delete(self, request, f_id):
        
        if Feature.objects.filter(id=f_id).exists(): #raising error if feature with provided id doesn't exist
            feature_object = Feature.objects.get(id=f_id) #fetching the object to be deleted if it exists
            feature_info = feature_object.get_info() #after delete operation, feature_id becomes null
        else:
            return JsonResponse({'error_message': 'The requested feature does not exist'}) 

        feature_object.delete()
        args = {'feature_info':feature_info}

        return JsonResponse(args) #returning deleted feature's name and id

    def put(self, request, f_id):

        if Feature.objects.filter(id=f_id).exists():
            feature_object = Feature.objects.get(id=f_id)
        else:
            return JsonResponse({'error_message':'The requested feature does not exist'})

        try: #raising error if body cannot be parsed 
            json_data = json.loads(str(request.body, encoding='utf-8'))
        except:
            return JsonResponse({'error_message':'posted body cannot be parsed, post in json format'})

        try: #raising error if domain name is not under 'name' key
            feature_id = (json_data['feature_id'])
        except:
            return JsonResponse({'error_message':'Kindly post the feature id under \'feature_id\' key'})

        try:
            feature_name = (json_data['feature_name'])
        except:
            return JsonResponse({'error_message':'Kindly post the feature name list under \'feature_name\' key'})

        try:
            Feature.objects.filter(id=f_id).update(name=feature_name)
        except:
            return JsonResponse({'error_message':('Feature ' + str(feature_name.lower()) + ' already exists')})

        feature_object = Feature.objects.get(id=f_id)

        feature_info = feature_object.get_info()

        args = {'feature_info':feature_info}
        return JsonResponse(args)

class FeatureGetPost(View):

    def get(self, request): #fetch list of all the features

        features = Feature.objects.all() #fetch all feature objects
        features_info = []

        for feature in features:
            feature_all_info = feature.get_info()
            features_info.append(feature_all_info) #storing name and id of all features in a list

        args = {'features_info':features_info}
        return JsonResponse(args) #returning list containing feature's ids and names


    def post(self, request):
        
        try: #raising error if body cannot be parsed 
            json_data = json.loads(str(request.body, encoding='utf-8'))
        except:
            return JsonResponse({'error_message':'posted body cannot be parsed, post in json format'})

        try: #raising error if feature name is not under 'name' key
            feature_name = (json_data['feature_name'])
        except:
            return JsonResponse({'error_message':'Kindly post the feature name under \'feature_name\' key'})

        #checking if feature with provided name already exists
        if Feature.objects.filter(name=(feature_name.lower())).exists(): 
            return JsonResponse({'error_message':('feature ' + str(feature_name.lower()) + ' already exists')})

        feature_object = Feature.objects.create(name=(feature_name.lower())) 
        #creating a new feature object if it doesn't exist

        args = {'feature_info':feature_object.get_info()}
        return JsonResponse(args) #returning added feature's name and id
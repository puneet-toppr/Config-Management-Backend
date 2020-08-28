from django.views.generic import View
from .models import Domain
from django.http.response import JsonResponse
import json, validators
from domain_feature_mapping.models import DomainFeatureMapping
from features.models import Feature

# Create your views here.
class DomainView(View):

    def get(self, request, d_id): #get a domain name using its id

        if Domain.objects.filter(id=d_id).exists(): #raising error if domain with provided id doesn't exist
            domain_object = Domain.objects.get(id=d_id)
        else:
            return JsonResponse({'error_message':'The requested domain does not exist'})
                
        map_object = DomainFeatureMapping.objects.filter(domain=domain_object).all()
        feature_id_list = []
        for obj in (list(map_object)):
            feature_info={}
            feature_info['name']=obj.feature.name
            feature_info['id']=obj.feature.id
            feature_id_list.append(feature_info)

        domain_info = domain_object.get_info()
        domain_info['feature_id_list'] = feature_id_list
                
        args = {'domain_info':domain_info} 

        return JsonResponse(args) #returning domain's name and id


    def delete(self, request, d_id):
        
        if Domain.objects.filter(id=d_id).exists(): #raising error if domain with provided id doesn't exist
            domain_object = Domain.objects.get(id=d_id) #fetching the object to be deleted if it exists
            domain_info = domain_object.get_info() #after delete operation, domain_id becomes null
        else:
            return JsonResponse({'error_message': 'The requested domain does not exist'}) 

        domain_object.delete()
        args = {'domain_info':domain_info}

        return JsonResponse(args) #returning deleted domain's name and id

    def put(self, request, d_id):

        if Domain.objects.filter(id=d_id).exists():
            domain_object = Domain.objects.get(id=d_id)
        else:
            return JsonResponse({'error_message':'The requested domain does not exist'})

        try: #raising error if body cannot be parsed 
            json_data = json.loads(str(request.body, encoding='utf-8'))
        except:
            return JsonResponse({'error_message':'posted body cannot be parsed, post in json format'})

        try: #raising error if domain name is not under 'name' key
            domain_id = (json_data['domain_id'])
        except:
            return JsonResponse({'error_message':'Kindly post the domain id under \'domain_id\' key'})

        try:
            feature_id_list = (json_data['feature_id_list'])
        except:
            return JsonResponse({'error_message':'Kindly post the feature id list under \'feature_id_list\' key'})

        try:
            domain_name = (json_data['domain_name'])
        except:
            return JsonResponse({'error_message':'Kindly post the domain name list under \'domain_name\' key'})

        if len(feature_id_list)>0:
            for feature_id in feature_id_list:
                if type(feature_id) != str and type(feature_id) != int:
                    return JsonResponse({'error_message':'post feature ids in integer/string format'})

                try:
                    feature_id_list = list(map(lambda a:int(a), feature_id_list))
                except:
                    return JsonResponse({'error_message':'post feature ids in integer/string format'})

                try:#doubt on reducing database calls
                    feature_object = Feature.objects.get(id = int(feature_id))
                except:
                    return JsonResponse({'error_message':'feature with this id does not exist'})
            
        if not validators.domain(domain_name):
            return JsonResponse({'error_message':'Domain name is invalid, kindly enter a valid domain name'})

        try:
            Domain.objects.filter(id=d_id).update(name=domain_name)
        except:
            return JsonResponse({'error_message':('domain ' + str(domain_name.lower()) + ' already exists')})

        domain_object = Domain.objects.get(id=d_id)

        DomainFeatureMapping.objects.filter(domain=domain_object).all().delete()
        
        if len(feature_id_list)>0:
            for feature_id in feature_id_list:
                feature_object = Feature.objects.get(id = int(feature_id))
                DomainFeatureMapping.objects.create(domain = domain_object, feature = feature_object)

        domain_info = domain_object.get_info()
        domain_info['feature_id_list'] = feature_id_list

        args = {'domain_info':domain_info}
        return JsonResponse(args)

class DomainGetPost(View):

    def get(self, request): #fetch list of all the domains

        domains = Domain.objects.all() #fetch all domain objects
        domains_info = []

        for domain in domains:
            domain_all_info = domain.get_info()
            domains_info.append(domain_all_info) #storing name and id of all domains in a list

        args = {'domains_info':domains_info}
        return JsonResponse(args) #returning list containing domain's ids and names


    def post(self, request):
        
        try: #raising error if body cannot be parsed 
            json_data = json.loads(str(request.body, encoding='utf-8'))
        except:
            return JsonResponse({'error_message':'posted body cannot be parsed, post in json format'})

        try: #raising error if domain name is not under 'name' key
            domain_name = (json_data['domain_name'])
        except:
            return JsonResponse({'error_message':'Kindly post the domain name under \'domain_name\' key'})

        try:
            feature_id_list = (json_data['feature_id_list'])
        except:
            return JsonResponse({'error_message':'Kindly post the feature id list under \'feature_id_list\' key'})

        if not validators.domain(domain_name):
            return JsonResponse({'error_message':'Domain name is invalid, kindly enter a valid domain name'})

        #checking if domain with provided name already exists
        if Domain.objects.filter(name=(domain_name.lower())).exists(): 
            return JsonResponse({'error_message':('domain ' + str(domain_name.lower()) + ' already exists')})

        domain_object = Domain.objects.create(name=(domain_name.lower())) 
        #creating a new domain object if it doesn't exist

        if len(feature_id_list)>0:
            for obj in feature_id_list:
                
                if type(obj)!=str and type(obj)!=int:
                    domain_object.delete()#if feature id is not in string, delete created domain object -> operation failed
                    return JsonResponse({'error_message':'post feature ids in integer/string format'})
                try:
                    feature_object = Feature.objects.get(id = int(obj))
                except:
                    domain_object.delete() #if feature id does not exist, delete created domain object -> operation failed
                    return JsonResponse({'error_message':'feature with this id does not exist'})

                DomainFeatureMapping.objects.create(domain = domain_object, feature = feature_object)

        args = {'domain_info':domain_object.get_info()}
        return JsonResponse(args) #returning added domain's name and id